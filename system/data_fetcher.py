import pandas as pd
import requests
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

class DataFetcher:
    def __init__(self, db_path='mlb_data.db'):
        self.db_path = db_path
        self.api_key = os.getenv("ODDS_API_KEY")

    def fetch_odds(self, sport="baseball_mlb_world_series_winner", fetch_from_api=True):
        """Fetches odds data from the API or database."""
        if fetch_from_api:
            BASE_URL = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
            params = {
                "api_key": self.api_key,
                "regions": "us,uk,eu",
                "markets": "outrights",
                "oddsFormat": "decimal",
                "dateFormat": "iso",
            }
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching odds: {response.status_code} - {response.text}")
                return []

        # If not fetching from API, retrieve data from the database
        conn = sqlite3.connect(self.db_path)
        query = '''
        SELECT * FROM odds
        '''
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data

    def store_odds(self, odds_data):
        """Stores odds data into the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for event in odds_data:
            sport_key = event.get("sport_key")
            commence_time = event.get("commence_time")
            for bookmaker in event.get("bookmakers", []):
                bookmaker_name = bookmaker.get("title")
                for market in bookmaker.get("markets", []):
                    for outcome in market.get("outcomes", []):
                        cursor.execute('''
                        INSERT INTO odds (
                            sport_key, event_id, event_name, bookmaker, market, odds_home, odds_away, odds_draw, region, timestamp
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            sport_key, event.get("id"), outcome.get("name"), bookmaker_name, market.get("key"),
                            outcome.get("price"), None, None, bookmaker.get("region", "unknown"), commence_time
                        ))
        conn.commit()
        conn.close()
