import sqlite3
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def initialize_db():
    # Connect to SQLite database
    conn = sqlite3.connect('mlb_data.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY,
        name TEXT,
        abbreviation TEXT,
        location TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY,
        full_name TEXT,
        team_id INTEGER,
        position TEXT,
        FOREIGN KEY (team_id) REFERENCES teams (team_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        game_id INTEGER PRIMARY KEY,
        date TEXT,
        home_team_id INTEGER,
        away_team_id INTEGER,
        home_score INTEGER,
        away_score INTEGER,
        FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
        FOREIGN KEY (away_team_id) REFERENCES teams (team_id)
    )
    ''')

    # Create odds table
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

    print("Database and tables initialized successfully.")
    conn.commit()
    conn.close()

# Function to fetch data from MLB API or Odds API
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    
REGIONS = "us,uk,eu"

def fetch_odds():
    API_KEY = os.getenv("ODDS_API_KEY")
    BASE_URL = "https://api.the-odds-api.com/v4/sports"
    SPORT = "baseball_mlb_world_series_winner"
    REGIONS = "us,uk,eu"
    MARKETS = "outrights"  # Use outright market
    ODDS_FORMAT = "decimal"
    DATE_FORMAT = "iso"

    url = f"{BASE_URL}/{SPORT}/odds"
    params = {
        "api_key": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT,
        "dateFormat": DATE_FORMAT,
    }

    # Make the request
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    print("Response:", response.json())  # Debugging the response
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching odds: {response.status_code} - {response.text}")
        return None

def insert_outright_odds(odds_data):
    """
    Inserts outright odds into the database, treating each outcome as an event.
    """
    conn = sqlite3.connect('mlb_data.db')
    cursor = conn.cursor()

    for event in odds_data:
        sport_key = event.get("sport_key")
        commence_time = event.get("commence_time")

        for bookmaker in event.get("bookmakers", []):
            bookmaker_name = bookmaker.get("title")
            for market in bookmaker.get("markets", []):
                market_type = market.get("key")
                for outcome in market.get("outcomes", []):
                    # Use outcome name as the event name
                    event_name = outcome.get("name")
                    team_odds = outcome.get("price")

                    # Insert odds into the database
                    cursor.execute('''
                    INSERT INTO odds (
                        sport_key, event_id, event_name, bookmaker, market, odds_home, odds_away, odds_draw, region, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        sport_key, None, event_name, bookmaker_name, market_type,
                        team_odds, None, None, bookmaker.get("region", "unknown"), commence_time
                    ))

    conn.commit()
    print("Outright odds data inserted successfully.")
    conn.close()

odds_data = fetch_odds()
if odds_data is None or len(odds_data) == 0:
    print("No data fetched from the API. Check the API response or parameters.")
else:
    print("Fetched odds data:", odds_data)
    insert_outright_odds(odds_data)
