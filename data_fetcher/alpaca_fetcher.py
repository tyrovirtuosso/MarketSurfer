from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
import pandas_market_calendars as mcal
import datetime
from termcolor import colored
import pytz
import pandas as pd
from dotenv import load_dotenv
import logging
import os

try:
    from .utils import Utils
except ImportError:
    from utils import Utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlpacaFetcher:
    CATEGORY = 'stock'
    SOURCE = 'alpaca'    
    
    def __init__(self, storage_handler=None):
        self.storage_handler = storage_handler
        load_dotenv()
        self.client = StockHistoricalDataClient(api_key=os.environ.get('ALPACA_API_KEY'), secret_key=os.environ.get('ALPACA_SECRET_KEY'))
        self.utils = Utils()

    def fetch_data(self, symbol):
        data = self.storage_handler.load_data(symbol)
        
        if data is None:
            start_date = "2010-01-01 00:00:00" # Alpaca only supports 7yr 1hr data
            end_date = self.get_end_date()
            raw_data = self.fetch_raw_data(symbol, start_date, end_date)
            data = self.process_data(raw_data, symbol)      
            self.utils.export_to_csv(data, f"{symbol}")                                             
            self.storage_handler.save_data(symbol, data, AlpacaFetcher.CATEGORY, AlpacaFetcher.SOURCE)
            
        return data
            
    def fetch_raw_data(self, symbol, start_date, end_date):
        request_params = StockBarsRequest(
                        symbol_or_symbols=[symbol],
                        timeframe=TimeFrame.Hour,
                        start=start_date,
                        end=end_date
                        )  
        if self.is_market_open(start_date, end_date):
            try:
                bars = self.client.get_stock_bars(request_params)
                df = bars.df                                       
                return df
            except KeyError as e:
                print(f"Empty Dataframe for {symbol}")
                return pd.DataFrame()
        else:
            print(f"Market is closed for {symbol}")
            return pd.DataFrame()
    
    def process_data(self, df, symbol):
        df = df.reset_index()   
        df = df.rename(columns={'timestamp': 'date'})
        print(df)
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        df = df.drop(['trade_count', 'vwap', ], axis=1)
        
        df['category'] = AlpacaFetcher.CATEGORY
        df['source'] = AlpacaFetcher.SOURCE
        df['symbol'] = symbol    
        
        return self.interpolate_data(df)
        
    
    def interpolate_data(self, df):
        # Add values to all possible intervals to be uniform with crypto data
        # convert date column to datetime type
        df['date'] = pd.to_datetime(df['date'])        
        
        # define time range
        start_date = df['date'].min()
        end_date = df['date'].max()     
                           
        # set date column as index
        df.set_index('date', inplace=True)
        date_range = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # create new DataFrame with datetime index covering entire time range
        new_df = pd.DataFrame(index=date_range)        
               
        # merge original DataFrame with new DataFrame using outer join
        merged_df = pd.merge(df, new_df, how='outer', left_index=True, right_index=True)
                                
        # interpolate missing values using linear interpolation
        interpolated_df = merged_df.interpolate(method='linear')
        interpolated_df = interpolated_df.ffill()
        interpolated_df.reset_index(inplace=True)
        interpolated_df.rename(columns={'index': 'date'}, inplace=True)
        return interpolated_df

                  
    def update_data(self, symbol):
        latest_date = self.storage_handler.get_latest_date(symbol, AlpacaFetcher.CATEGORY, AlpacaFetcher.SOURCE)
        print(f"Latest Date in Database: {latest_date}")
        
        if latest_date is not None:
            start_date = pd.to_datetime(latest_date) + datetime.timedelta(hours=1)
            end_date = self.get_end_date()
            print(f"start_date: {start_date}")
            print(f"end_date: {end_date}")
            if start_date < end_date and (end_date - start_date).total_seconds() >= 3600:
                raw_data = self.fetch_raw_data(symbol, start_date, end_date)
                all_data = self.handle_update_response(raw_data, symbol)
                return all_data        
            else:
                print(f"No new data to update for {symbol}")
                all_data = self.storage_handler.load_data(symbol)
                self.utils.export_to_csv(all_data, f"{symbol}")
                return all_data             
                
        else:
            print(f"No data found for {symbol}, fetching all data")
            return self.fetch_data(symbol)
        
    def handle_update_response(self, raw_data, symbol):
        if raw_data.empty:
            print(colored(f"No new data is being collected for {symbol} as its a holiday. Holiday data will be interpolated based on next available datapoint", 'blue', attrs=['bold']))                                                               
            all_data = self.storage_handler.load_data(symbol)
            self.utils.export_to_csv(all_data, f"{symbol}")
            return all_data    
        else:
            data = self.process_data(raw_data, symbol)  
            self.storage_handler.save_data(symbol, data, AlpacaFetcher.CATEGORY, AlpacaFetcher.SOURCE)
            all_data = self.storage_handler.load_data(symbol)
            self.utils.export_to_csv(all_data, f"{symbol}")
            return all_data
        
    def get_end_date(self):
        return (pd.to_datetime(pd.Timestamp.utcnow()).replace(tzinfo=None) - datetime.timedelta(minutes=16))
    
    def is_market_open(self, start_date, end_date):
        # get the NASDAQ calendar
        nasdaq = mcal.get_calendar('NASDAQ')
        # Create a date range with hourly frequency
        date_range = pd.date_range(start=start_date, end=end_date, freq='H', tz=pytz.utc)
        # Loop through each hour in the date range
        for date in date_range:
            # Check if the current hour is outside of market hours
            schedule = nasdaq.schedule(start_date=date.date(), end_date=date.date())
            if not schedule.empty: # check if the schedule dataframe is not empty
                market_open_utc = schedule.iloc[0]['market_open'].tz_convert(pytz.utc)
                market_close_utc = schedule.iloc[0]['market_close'].tz_convert(pytz.utc)
                if (date > market_open_utc and date < market_close_utc) and (date not in nasdaq.holidays().holidays):
                    return True
        return False          
