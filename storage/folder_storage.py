from .abstract_storage import AbstractStorage
import os
import pandas as pd

class FolderStorage(AbstractStorage):
    def __init__(self, base_path="data"):
        self.base_path = base_path

    def check_data_exists(self, symbol):
        # Implementation for checking if data exists in the file system
        file_path = os.path.join(self.base_path, f'{symbol}.csv')
        return os.path.exists(file_path)

    def save_data(self, symbol, data, category, source):
        # Implementation for saving data to the file system
        os.makedirs(self.base_path, exist_ok=True)
        file_path = os.path.join(self.base_path, f'{symbol}.csv')
        data.to_csv(file_path, index=False)

    def load_data(self, symbol):
        # Implementation for loading data from the file system
        file_path = os.path.join(self.base_path, f'{symbol}.csv')
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return None

    def get_latest_date(self, symbol):
        data = self.load_data(symbol)
        if data is not None:
            return data['date'].max()
        else:
            return None
