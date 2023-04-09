import requests
import time
import pandas as pd
import datetime
import logging
try:
    from .utils import Utils
except ImportError:
    from utils import Utils
    
utils = Utils()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoinGeckoFetcher:
    CATEGORY = 'crypto'
    SOURCE = 'coingecko'

    def __init__(self, base_url="https://api.coingecko.com/api/v3", storage_handler=None):
        self.base_url = base_url
        self.storage_handler = storage_handler

    def fetch_data(self, symbol):
        data = self.storage_handler.load_data(symbol)

        if data is None:
            start_date = self.earliest_price(symbol)
            raw_data = self.fetch_raw_data(symbol, start_date)
            data = self.process_data(raw_data, symbol)                   
            self.storage_handler.save_data(symbol, data, CoinGeckoFetcher.CATEGORY, CoinGeckoFetcher.SOURCE)
            
        return data

    def fetch_raw_data(self, symbol, start_date):
        data = []
        end_date = self.get_end_date()

        for current_start, current_end in self.date_ranges(start_date, end_date, symbol):
            url = self.construct_request_url(symbol, current_start, current_end)
            data.append(self.make_api_request(url))
        return data

    def process_data(self, raw_data, symbol):
        # Concatenate the data into a single DataFrame        
        df = pd.concat(raw_data)
        
        # Resample the data into intervals, taking the last value for each interval
        df = df.resample('1H').last()
        # Remove last row which is incomplete
        if not df.empty and len(df) != 1:
            df = df.drop(df.index[-1])
        # use linear interpolation to estimate missing values
        df = df.interpolate(method='linear')              
        
        df = self.format_dataframe(df, symbol)
        return df

    def update_data(self, symbol):        
        latest_date = self.storage_handler.get_latest_date(symbol, CoinGeckoFetcher.CATEGORY, CoinGeckoFetcher.SOURCE)
        print(f"Latest Date in Database: {latest_date}")
        if latest_date is not None:
            start_date = pd.to_datetime(latest_date) + datetime.timedelta(hours=1)
            end_date = self.get_end_date()
            print(f"start_date: {start_date}")
            print(f"end_date: {end_date}")
            if start_date < end_date and (end_date - start_date).total_seconds() >= 3600:
                raw_data = self.fetch_raw_data(symbol, start_date)                
                data = self.process_data(raw_data, symbol)                
                self.storage_handler.save_data(symbol, data, CoinGeckoFetcher.CATEGORY, CoinGeckoFetcher.SOURCE)
                all_data = self.storage_handler.load_data(symbol)
                utils.export_to_csv(all_data, f"{symbol}")
                return all_data
            else:
                print(f"No new data to update for {symbol}")
                all_data = self.storage_handler.load_data(symbol)
                utils.export_to_csv(all_data, f"{symbol}")
                return all_data
        else:
            print(f"No data found for {symbol}, fetching all data")
            return self.fetch_data(symbol)
            

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
        except KeyError:
            print(f"There is no {symbol} symbol in Coingecko API name")

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
        
        # Shifting close column values up by 1
        # df[['close', 'open', 'high', 'low']] = df[['close', 'open', 'high', 'low']].shift(-1)
        
        df['category'] = CoinGeckoFetcher.CATEGORY
        df['source'] = CoinGeckoFetcher.SOURCE
        return df

    def handle_http_error(self, err):
        if err.response.status_code == 429:
            logger.info("Rate limit exceeded. Sleeping for 2 seconds.")
            print("Rate limit exceeded. Sleeping for 2 seconds.")
            time.sleep(2)
            utils.vpn_connect()
        elif err.response.status_code == 503:
            logger.info("Service Unavailable. Sleeping for 10 seconds.")
            print("Service Unavailable. Sleeping for 10 seconds.")
            time.sleep(10)
        else:
            raise err

    def handle_connect_timeout(self):
        logger.error('Error: Connection to api.coingecko.com timed out... Sleeping for 10 seconds')
        print('Error: Connection to api.coingecko.com timed out... Sleeping for 10 seconds')
        time.sleep(10)

