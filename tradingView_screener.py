import requests
import pandas as pd
from pprint import pprint


# flake8: noqa
payload_1D = {
    "filter":[
        {"left":"exchange","operation":"in_range","right":["BINANCE","BYBIT"]},
        {"left":"relative_volume_10d_calc","operation":"in_range","right":[1,7]},
        {"left":"name,description","operation":"match","right":"perp"}
        ],
    "options":{"lang":"en"},"markets":["crypto"],"symbols":{"query":{"types":[]},"tickers":[]},
    "columns":["base_currency_logoid","currency_logoid","name","market_cap_calc","relative_volume_10d_calc","exchange","Recommend.All","Recommend.MA","Recommend.Other","volume","change|60","change|1M","change|1W","change|240","Volatility.W","description","type","subtype","update_mode"],
    "sort":{"sortBy":"relative_volume_10d_calc","sortOrder":"desc"},
    "range":[0,150]
    }

payload_4H = {
    "filter":[
        {"left":"exchange","operation":"in_range","right":["BINANCE","BYBIT"]},
        {"left":"relative_volume_10d_calc|240","operation":"in_range","right":[1,7]},
        {"left":"name,description","operation":"match","right":"perp"}
        ],
    "options":{"lang":"en"},"markets":["crypto"],"symbols":{"query":{"types":[]},"tickers":[]},
    "columns":["base_currency_logoid","currency_logoid","name","market_cap_calc","relative_volume_10d_calc|240","exchange","Recommend.All|240","Recommend.MA|240","Recommend.Other|240","volume|240","change|60","change|1M","change|1W","change|240","Volatility.W","description","type","subtype","update_mode|240"],
    "sort":{"sortBy":"relative_volume_10d_calc|240","sortOrder":"desc"},
    "range":[0,150]}

# Send POST request with headers and params
url = 'https://scanner.tradingview.com/crypto/scan'
# headers = {
#    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#    'Referer': 'https://www.tradingview.com/'
# }

response = requests.post(url, json=payload_4H)
pprint(response.json())



