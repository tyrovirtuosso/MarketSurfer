from .abstract_storage import AbstractStorage
import sqlite3
import pandas as pd

class SQLiteStorage(AbstractStorage):
    def __init__(self, db_name="crypto_stock_data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()

        # Create price_data table
        c.execute('''
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                category TEXT NOT NULL,
                source TEXT NOT NULL,
                date DATETIME NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume REAL NOT NULL
            )
        ''')

        # Create metadata table
        c.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                category TEXT NOT NULL,
                source TEXT NOT NULL,
                earliest_date DATETIME NOT NULL,
                available_indicators TEXT,
                UNIQUE(symbol, category, source)
            )
        ''')

        self.conn.commit()

    def check_data_exists(self, symbol):
        c = self.conn.cursor()
        c.execute('SELECT EXISTS(SELECT 1 FROM price_data WHERE symbol=?)', (symbol,))
        return c.fetchone()[0] == 1

    def save_data(self, symbol, data, category, source):
        c = self.conn.cursor()
        data.to_sql('price_data', self.conn, if_exists='append', index=False)
        
        earliest_date = self.get_earliest_date(symbol)
        
        # Check if the symbol exists in the metadata table
        c.execute('SELECT COUNT(*) FROM metadata WHERE symbol=? AND category=? AND source=?', (symbol, category, source))
        exists = c.fetchone()[0] > 0

        if exists:
            # Update the earliest_date for the symbol in the metadata table
            c.execute('''
                UPDATE metadata
                SET earliest_date=?
                WHERE symbol=? AND category=? AND source=?
            ''', (earliest_date, symbol, category, source))
        else:
            # Insert a new row for the symbol in the metadata table
            c.execute('''
                INSERT INTO metadata (symbol, category, source, earliest_date)
                VALUES (?, ?, ?, ?)
            ''', (symbol, category, source, earliest_date))
    
        self.conn.commit()

    def load_data(self, symbol):
        c = self.conn.cursor()
        c.execute('SELECT * FROM price_data WHERE symbol=? ORDER BY symbol, category, date ASC', (symbol,))
        data = c.fetchall()
        if not data:
            return None

        columns = ['id', 'symbol', 'category', 'source', 'date', 'open', 'high', 'low', 'close', 'volume']
        return pd.DataFrame(data, columns=columns)

    def get_latest_date(self, symbol, category, source):
        c = self.conn.cursor()
        c.execute('SELECT MAX(date) FROM price_data WHERE symbol=? AND category=? AND source=?', (symbol, category, source))
        return c.fetchone()[0]
    
    def get_earliest_date(self, symbol):
        data = self.load_data(symbol)
        
        # Get earliest date for the symbol from the data DataFrame
        earliest_date = data['date'].min()
        
        if not isinstance(earliest_date, str):
            # Convert the Timestamp object to a string representation
            earliest_date = earliest_date.strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"earliest_date: {earliest_date}")
        return earliest_date
        
    

    def __del__(self):
        self.conn.close()
