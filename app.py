# Import necessary libraries
import finnhub
import json
import numpy as np
import csv
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from db_app import Correction, Session

# Load the pre-trained sentiment analysis model
model = load_model('positive_negative_model.h5') 

# Load the same tokenizer used for preprocessing text data / tokenizer will convert words to integers based on a frequency rank
with open('new_tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)

# Setup Finnhub API client to fetch company news
with open("config.json", "r") as file:
    config = json.load(file)
finnhub_client = finnhub.Client(api_key=config["FINNHUB_API_KEY"])

# Initialise Flask application
app = Flask(__name__)

# Define route for home page
@app.route('/')
def home():
    # Render the home page template on request
    return render_template('index.html')

# Define route for analysing news sentiment
@app.route('/analysis', methods=['POST'])
def analysis():
        # Retrieve user input from web form submission
        ticker = request.form['ticker']
        from_date = request.form['from_date']
        to_date = request.form['to_date']

        # Check if ticker field is empty / error handling 
        if not ticker.strip():
        # Return an error message and a link to go back
            return render_template('no_data.html', message="Please enter a ticker symbol.")

        # Check if date field is empty / error handling 
        if not from_date.strip() or not to_date.strip():
        # Return an error message and a link to go back
            return render_template('no_data.html', message="Please enter a date range.")


        # Fetch news data for the given company ticker and date range
        news_data = finnhub_client.company_news(ticker, _from=from_date, to=to_date)
        print(f"Number of articles returned: {len(news_data)}")
        
        # Return error message if no news data is found
        if not news_data:
            return render_template('no_data.html', message="No news data available for the selected ticker and date range.")

        # Extract headline and URL information from news data
        headlines_data = [{"headline": news['headline'], "url": news['url']} for news in news_data]
        
        # Preprocess news data for prediction
        processed_data = preprocess_news_data(news_data)

        # Use the model to predict sentiments of the news headlines
        predictions = model.predict(processed_data)
        
        interpreted_results = [interpret_prediction(pred) for pred in predictions]

        # Combine headlines, sentiments, scores, and URLs for rendering in the template
        results_data = [
            {"headline": data["headline"], "url": data["url"], 
             "sentiment": interpreted[0], "score": interpreted[1]} 
            for data, interpreted in zip(headlines_data, interpreted_results)
        ]

        # Calculate overall sentiment and score for all headlines
        overall_score = sum([results[1] for results in interpreted_results]) / len(interpreted_results)
        overall_sentiment = "Positive" if overall_score > 0.5 else "Negative"

        # # Sort results by score
        # sorted_results = sorted(results_data, key=lambda x: x['score'], reverse=True)

        return render_template('result.html', 
                            ticker=ticker,
                            results=results_data,
                            overall_sentiment=overall_sentiment, 
                            overall_score=overall_score,
                            news_data=news_data)

@app.route('/market_news', methods=['GET', 'POST'])
def market_news():
    if request.method == 'POST':
        category = request.form.get('category')

        # print(f"The category is: {category}") - debug

        # Fetch market news using Finnhub API
        try:
            news_data = finnhub_client.general_news(category=category)
            
        except Exception as e:
            news_data = []
            print("Error fetching news:", e)

        # Check if news_data is not empty
        if not news_data:
            return render_template('no_data.html', message="No market news data available for the selected category.")

        # Extract headline, source and URL information from news data
        market_data = [{"headline": news['headline'], "source": news['source'], "url": news['url']} for news in news_data]

        # Preprocess news data for prediction
        processed_market_data = preprocess_news_data(market_data)

        # Use the model to predict sentiments of the market_news headlines
        market_predictions = model.predict(processed_market_data)
        interpreted_results = [interpret_prediction(pred) for pred in market_predictions]

        # Combine headlines, sentiments, scores, source, and URLs for rendering in the template
        market_results_data = [
            {"headline": data["headline"], "url": data["url"], "source": data['source'],
             "sentiment": result[0], "score": result[1]}
            for data, result in zip(market_data, interpreted_results)
        ]

        return render_template('market_news.html', results=market_results_data, category=category.capitalize())

    # GET request: Show the form
    else:
        # Render the index.html template for the GET request
        return render_template('index.html')

                               
# Function to preprocess retrieved API news headlines for the model
def preprocess_news_data(news_data):
    # Extract headlines from the news data
    headlines = [news['headline'] for news in news_data]
    
    # Define non-alphanumeric characters to be removed
    non_alphanum = [',','.','/','"',':',';','!','@','#','$','%',"'","*","(",")","&","--"]
    
    # Process each headline
    processed_headlines = []
    for headline in headlines:
        # Remove non-alphanumeric characters
        for char in non_alphanum:
            headline = headline.replace(char, "")
        
        # Replace certain strings
        headline = headline.replace(" s ", " ")
        headline = headline.replace(" '", "'")
        headline = headline.replace("  ", " ")
        headline = headline.replace("   ", " ")
        
        # Convert to lower case
        headline = headline.lower()
        
        # Append the processed headline to the list
        processed_headlines.append(headline)
    
    # Convert processed headlines to sequences of integers using the tokenizer
    sequences = tokenizer.texts_to_sequences(processed_headlines)
    
    # Pad sequences to ensure uniform input size for the model
    padded = pad_sequences(sequences, maxlen=60, padding='post', truncating='post')
    return padded

# Function to interpret the model's prediction
def interpret_prediction(prediction):
    # Extract the score from the prediction array
    score = prediction[0]
    # Determine sentiment as 'Positive' or 'Negative' based on the score
    sentiment = "Positive" if score > 0.5 else "Negative"
    return sentiment, score


@app.route('/report', methods=['POST'])
def report():
    try:
        data = request.get_json()
        headline = data['headline']
        reported_sentiment = data['sentiment']

        if reported_sentiment == "Positive":
            correct_sentiment = "Negative"
        else:
            correct_sentiment = "Positive"

        session = Session()  # Create a new session for each request
        correction = Correction(sentence=headline, correct_sentiment=correct_sentiment)
        session.add(correction)
        session.commit()
        return jsonify({"message": "Correction successfully added to Database"})
    finally:
        session.close()

        

# Run the Flask application when the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)