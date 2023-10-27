# import dependencies 
import requests
import pandas as pd
import json

with open("config.json", "r") as file:
    config = json.load(file)
apikey = config["ALPHAVANTAGE_API_KEY"]

def get_news_sentiment(tickers= None, topics= None, time_from= None, time_to= None, sort= "LATEST", limit=None, apikey="apikey"):
    base_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT'
    
    # Append tickers to the URL if provided
    if tickers:
        base_url += f"&tickers={','.join(tickers)}"
    
    # Append topics to the URL if provided
    if topics:
        base_url += f"&topics={','.join(topics)}"
    
    # Append time_from and time_to to the URL if specified 
    if time_from:
        base_url += f"&time_from={time_from}"
    if time_to:
        base_url += f"&time_to={time_to}"
    
    # Append sort and limit
    base_url += f"&sort={sort}&limit={limit}"
    
    # Append API key
    base_url += f"&apikey={apikey}"
    
    # Make the request
    r = requests.get(base_url)
    data = r.json()
    
    return data

# Example usage
new_headlines_data = get_news_sentiment(topics="technology", time_from="20231027T0000", limit=1)

df = pd.DataFrame(new_headlines_data["feed"])

csv_filename = "news_data.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")







