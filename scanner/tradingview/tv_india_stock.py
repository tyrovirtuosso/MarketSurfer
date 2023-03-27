# TradingView Indian Stock Scanner
import requests
from pprint import pprint
from time import sleep

# flake8: noqa
class TvIndia:
    """A class to fetch and display indian stock data from TradingView scanner.
    
    Attributes:
        url (str): The URL to send requests to.
        headers (dict): The headers to use for requests.
        payload_1D (dict): The payload to use for 1D data requests.
        payload_4H (dict): The payload to use for 4H data requests.
    """
    def __init__(self):
        self.url = 'https://scanner.tradingview.com/india/scan'
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
