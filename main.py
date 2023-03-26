from data_fetcher import (CCXTFetcher, CoinGeckoFetcher,
                          AlpacaFetcher, YFinanceFetcher)


def main():
    # Instantiate the fetcher classes
    ccxt_fetcher = CCXTFetcher()
    coingecko_fetcher = CoinGeckoFetcher()
    alpaca_fetcher = AlpacaFetcher("your_api_key", "your_api_secret", "https://paper-api.alpaca.markets")
    yfinance_fetcher = YFinanceFetcher()

    # Choose the best data source and fetch data
    # For example, you can fetch BTC/USDT data from CCXT
    data = ccxt_fetcher.fetch_data("BTC/USDT")

    # Validate the data and present it to the user
    # ...


if __name__ == "__main__":
    main()
