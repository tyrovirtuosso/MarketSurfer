import requests
import json
from datetime import datetime, timedelta

API_KEY = 'GA3AF0C6VV26GCV5'
symbol = 'AAPL'

# set the time interval to 1 hour
interval = '60min'

# create the API request URL
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}'

# send the request and get the response
response = requests.get(url)

# parse the JSON data
data = json.loads(response.text)
print(data)
# get the keys of the time series data
time_series_keys = list(data['Time Series (60min)'].keys())

# find the earliest date by subtracting 1 hour from the first time series key
earliest_date = datetime.strptime(time_series_keys[0], '%Y-%m-%d %H:%M:%S') - timedelta(hours=1)

# print the earliest date
print(f"Earliest available date for {symbol} 1-hour data: {earliest_date}")
