import ccxt


class CCXTFetcher:
    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch_data(self, symbol, timeframe='1h'):
        # Fetch data from CCXT
        print("in fetch data")
        pass
