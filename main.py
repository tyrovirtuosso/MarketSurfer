from data_fetcher import (CoinGeckoFetcher,AlpacaFetcher)


def main():
    # Instantiate the fetcher classes
    coingecko_fetcher = CoinGeckoFetcher()
    df = coingecko_fetcher.fetch_data('ethereum')

    # Choose the best data source and fetch data
    # For example, you can fetch BTC/USDT data from CCXT

    # Validate the data and present it to the user
    # ...


if __name__ == "__main__":
    main()
