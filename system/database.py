import sqlite3

class Database:
    def __init__(self, db_path='mlb_data.db'):
        self.db_path = db_path

    def initialize(self):
        """Initializes the database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS odds (
            odds_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport_key TEXT,
            event_id TEXT,
            event_name TEXT,
            bookmaker TEXT,
            market TEXT,
            odds_home REAL,
            odds_away REAL,
            odds_draw REAL,
            region TEXT,
            timestamp TEXT
        )
        ''')

        print("Database initialized successfully.")
        conn.commit()
        conn.close()
