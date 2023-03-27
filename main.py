from scanner import (TvUS, TvCrypto, TvIndia)

# flake8: noqa
def main():
    # Instantiate the scanner classes
    crypto_scanner = TvCrypto()
    india_scanner = TvIndia()
    us_scanner = TvUS()
    data = crypto_scanner.fetch_data()

    # Validate the data and present it to the user
    # ...


if __name__ == "__main__":
    main()