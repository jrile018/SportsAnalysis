import sqlite3
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

# Fetch NBA player stats
def fetch_nba_data(season="2023-24"):
    print("Fetching NBA player statistics...")
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
    df = stats.get_data_frames()[0]  # Convert API response to DataFrame
    return df

# Store data in SQLite
def store_data_in_sqlite(df, db_name="nba_stats.db"):
    print("Storing data in SQLite database...")
    conn = sqlite3.connect(db_name)
    df.to_sql("player_stats", conn, if_exists="replace", index=False)
    conn.close()
    print("Data successfully stored.")

# Read the first 100 players from SQLite
def read_first_100_players(db_name="nba_stats.db"):
    print("Reading first 100 players from SQLite database...")
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM player_stats LIMIT 200"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Main function
if __name__ == "__main__":
    # Step 1: Fetch data
    player_stats_df = fetch_nba_data()

    # Step 2: Store data in SQLite
    store_data_in_sqlite(player_stats_df)

    # Step 3: Read first 100 players from SQLite and display
    df = read_first_100_players()
    print(df)  # Display first 100 rows
