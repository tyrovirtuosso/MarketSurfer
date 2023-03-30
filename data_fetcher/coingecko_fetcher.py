import requests
import time
import pandas as pd
import datetime
from .utils import vpn_connect, export_to_csv

class CoinGeckoFetcher:
    CATEGORY = 'crypto'
    SOURCE = 'coingecko'

    def __init__(self, base_url="https://api.coingecko.com/api/v3"):
        self.base_url = base_url

    def fetch_data(self, symbol):
        start_date = self.earliest_price(symbol)
        raw_data = self.fetch_raw_data(symbol, start_date)
        processed_data = self.process_data(raw_data, symbol)
        export_to_csv(processed_data, 'sample')
        return processed_data

    def fetch_raw_data(self, symbol, start_date):
        data = []
        end_date = self.get_end_date()

        for current_start, current_end in self.date_ranges(start_date, end_date, symbol):
            url = self.construct_request_url(symbol, current_start, current_end)
            data.append(self.make_api_request(url))

        return data

    def process_data(self, raw_data, symbol):
        df = pd.concat(raw_data)
        if not df.empty:
            df = df.drop(df.index[-1])
        df = df.resample('1H').last().interpolate(method='linear')
        df = self.format_dataframe(df, symbol)

        return df

    def construct_request_url(self, symbol, start_date, end_date):
        return f"{self.base_url}/coins/{symbol}/market_chart/range?vs_currency=usd&from={int(start_date.timestamp())}&to={int(end_date.timestamp())}?cache-bust={str(time.time())}"

    def make_api_request(self, url):
        while True:
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                return self.extract_data_from_response(data)
            except requests.exceptions.HTTPError as err:
                self.handle_http_error(err)
            except requests.exceptions.ConnectTimeout:
                self.handle_connect_timeout()

    def earliest_price(self, symbol):
        try:
            url = f"https://coins.llama.fi/prices/first/coingecko:{symbol}"
            response = requests.get(url)
            timestamp = response.json()['coins'][f"coingecko:{symbol}"]['timestamp']
            return pd.to_datetime(timestamp, unit='s')
        except requests.exceptions.ConnectTimeout:
            self.handle_connect_timeout()

    def get_end_date(self):
        return pd.to_datetime(pd.Timestamp.utcnow()).replace(tzinfo=None)

    def date_ranges(self, start_date, end_date, symbol):
        days = (end_date - start_date).days
        num_requests = days // 90 + 1

        for i in range(num_requests):
            current_start = start_date + datetime.timedelta(days=i * 90)
            current_end = min(start_date + datetime.timedelta(days=(i + 1) * 90), end_date)
            print(f"{symbol}:{i+1}/{num_requests}")
            print(current_start)
            print(current_end) 
            yield current_start, current_end

    def extract_data_from_response(self, data):
        timestamps = pd.to_datetime([x[0] for x in data["prices"]], unit="ms")
        prices = [x[1] for x in data["prices"]]
        total_volumes = [x[1] for x in data["total_volumes"]]
        return pd.DataFrame({"close": prices, "open": prices, "high": prices, "low": prices, "volume": total_volumes}, index=timestamps)

    def format_dataframe(self, df, symbol):
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
        df['symbol'] = symbol
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'date'}, inplace=True)
        df[['close', 'open', 'high', 'low']] = df[['close', 'open', 'high', 'low']].shift(-1)
        df = df.drop(df.index[-1])
        df['category'] = CoinGeckoFetcher.CATEGORY
        df['source'] = CoinGeckoFetcher.SOURCE
        return df

    def handle_http_error(self, err):
        if err.response.status_code == 429:
            print("Rate limit exceeded. Sleeping for 2 seconds.")
            time.sleep(2)
            vpn_connect()
        elif err.response.status_code == 503:
            print("Service Unavailable. Sleeping for 10 seconds.")
            time.sleep(10)
        else:
            raise err

    def handle_connect_timeout(self):
        print('Error: Connection to api.coingecko.com timed out... Sleeping for 10 seconds')
        time.sleep(10)

