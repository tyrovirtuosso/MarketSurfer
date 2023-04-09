from data_fetcher import CoinGeckoFetcher, AlpacaFetcher
from storage import FolderStorage, SQLiteStorage, HDFSStorage
import configparser
from termcolor import colored


class ConfigHandler:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_storage_handler(self):
        storage_choice = int(self.config.get('Settings', 'storage_choice'))
        if storage_choice == 1:
            return FolderStorage()
        elif storage_choice == 2:
            return SQLiteStorage()
        elif storage_choice == 3:
            return HDFSStorage()
        else:
            raise ValueError("Invalid storage choice")


def create_fetcher(category, storage_handler):
    if category == 'crypto':
        return CoinGeckoFetcher(storage_handler=storage_handler)
    elif category == 'stock':
        return AlpacaFetcher(storage_handler=storage_handler)
    else:
        raise ValueError(f"Unknown category: {category}")


def update_symbols(symbols, storage_handler):
    for category, symbol_list in symbols.items():        
        fetcher = create_fetcher(category, storage_handler)
        for symbol in symbol_list:
            print("\n")
            print(f"Updating {category} {colored(symbol.upper(), 'green', attrs=['bold'])}")
            updated_data = fetcher.update_data(symbol)


def main():
    config_handler = ConfigHandler('config.ini')
    storage_handler = config_handler.get_storage_handler()

    symbols = {
        'crypto': ['matic-network', 'chainlink'],
        'stock': ['ARKK']
    }

    update_symbols(symbols, storage_handler)


if __name__ == "__main__":
    main()
