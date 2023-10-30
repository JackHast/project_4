# import dependencies 
import requests
import pandas as pd
import json

# location of api key 
with open("config.json", "r") as file:
    config = json.load(file)
api_key = config["ALPHAVANTAGE_API_KEY"]

# function for retrieving articles from API
def get_new_headlines(tickers=None, topics=None, time_from=None, time_to=None, sort=None, limit=None):
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
    
    # Append sort and limit only if they are provided
    if sort:
        base_url += f"&sort={sort}"
    if limit:
        base_url += f"&limit={limit}"
    
    # Append API key 
    base_url += f"&apikey={api_key}"
    
    # Make the request
    r = requests.get(base_url)
    data = r.json()
    
    print(base_url)
    
    return data

# Fetch some specific data 
new_headlines_data = get_new_headlines(topics="technology", limit=5)

# print(new_headlines_data)

df = pd.DataFrame(new_headlines_data["feed"])

csv_filename = "news_data.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")








