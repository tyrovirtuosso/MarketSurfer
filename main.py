from data_fetcher import CoinGeckoFetcher, AlpacaFetcher
from storage import FolderStorage, SQLiteStorage, HDFSStorage
import configparser
from termcolor import colored


def create_fetcher(category, storage_handler):
    if category == 'crypto':
        return CoinGeckoFetcher(storage_handler=storage_handler)
    elif category == 'stock':
        return AlpacaFetcher(storage_handler=storage_handler)
    else:
        raise ValueError(f"Unknown category: {category}")


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    storage_choice = int(config.get('Settings', 'storage_choice'))
    if storage_choice == 1:
        storage_handler = FolderStorage()
    elif storage_choice == 2:
        storage_handler = SQLiteStorage()
    elif storage_choice == 3:
        storage_handler = HDFSStorage()
    else:
        raise ValueError("Invalid storage choice")

    return storage_handler


def main():
    storage_handler = read_config('config.ini')

    symbols = {
        'crypto': ['bitcoin'],
        'stock': ['AAPL']
    }

    for category, symbol_list in symbols.items():        
        fetcher = create_fetcher(category, storage_handler)
        for symbol in symbol_list:
            print("\n")
            print(f"Updating {category} {colored(symbol.upper(), 'green', attrs=['bold'])}")
            updated_data = fetcher.update_data(symbol) 
            


if __name__ == "__main__":
    main()
