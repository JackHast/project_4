import finnhub
import pandas as pd
import json

# # location of api key 
# with open("config.json", "r") as file:
#     config = json.load(file)
# api_key = config["FINNHUB_API_KEY"]

# finnhub_client = finnhub.Client(api_key=api_key)

# news_data = finnhub_client.company_news('AAPL', _from="2023-10-28", to="2023-10-29")


# df = pd.DataFrame(news_data)

# csv_filename = "aapl_data.csv"
# df.to_csv(csv_filename, index=False)
# print(f"Data saved to {csv_filename}")

# location of api key 
with open("config.json", "r") as file:
    config = json.load(file)
api_key = config["FINNHUB_API_KEY"]

finnhub_client = finnhub.Client(api_key=api_key)

news_data = finnhub_client.general_news('general', min_id=50)

df = pd.DataFrame(news_data)

csv_filename = "finnhub_data.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")




