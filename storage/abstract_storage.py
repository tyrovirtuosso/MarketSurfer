'''
By using an abstract class, you can ensure that all storage classes implement the required methods (check_data_exists, save_data, and load_data).
Polymorphism allows you to use a single interface to interact with different storage classes, which makes your code more flexible.
'''
from abc import ABC, abstractmethod

class AbstractStorage(ABC):
    
    @abstractmethod
    def check_data_exists(self, symbol):
        pass

    @abstractmethod
    def save_data(self, symbol, data):
        pass

    @abstractmethod
    def load_data(self, symbol):
        pass
