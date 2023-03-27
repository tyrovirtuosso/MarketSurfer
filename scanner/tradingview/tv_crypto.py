# TradingView Crypto Scanner
import requests
from pprint import pprint
from time import sleep


# flake8: noqa
class TvCrypto:
    """A class to fetch and display crypto data from TradingView scanner.
    
    Attributes:
        url (str): The URL to send requests to.
        headers (dict): The headers to use for requests.
        payload_1D (dict): The payload to use for 1D data requests.
        payload_4H (dict): The payload to use for 4H data requests.
    """
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
        
    def __init__(self):
        self.url = 'https://scanner.tradingview.com/crypto/scan'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/111.0.0.0 Safari/537.36'
        referer = 'https://www.tradingview.com/'
        self.headers = dict({'User-Agent': user_agent, 'Referer': referer})
        

    def fetch_data(self):
        try:
            response = requests.post(self.url, json=self.payload_4H, headers=self.headers)
            response.raise_for_status()
            pprint(response.json())
            sleep(5)
            response = requests.post(self.url, json=self.payload_1D, headers=self.headers)
            response.raise_for_status()
            pprint(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")