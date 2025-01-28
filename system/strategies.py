from data_fetcher import DataFetcher
import pandas as pd

class Strategy:
    def __init__(self, risk_target, capital, num_stocks=5):
        self.risk_target = risk_target
        self.capital = capital
        self.num_stocks = num_stocks
        self.data = None

    def fetch_data(self):
        """Fetch and prepare data for the strategy."""
        raise NotImplementedError("Each strategy must implement fetch_data().")

    def run(self):
        """Generate buy-sell signals."""
        raise NotImplementedError("Each strategy must implement run().")

class ExampleStrategy(Strategy):
    def fetch_data(self):
        """Fetch odds data for the strategy."""
        fetcher = DataFetcher()
        raw_data = fetcher.fetch_odds(fetch_from_api=True)

        # Debug: Print raw data length and sample
        print(f"Raw data length: {len(raw_data)}")
        print("Raw data sample:", raw_data[:2])  # Print first two events to inspect structure

        events = []
        for event in raw_data:
            sport_key = event.get("sport_key")
            commence_time = event.get("commence_time")
            for bookmaker in event.get("bookmakers", []):
                bookmaker_name = bookmaker.get("title")
                for market in bookmaker.get("markets", []):
                    for outcome in market.get("outcomes", []):
                        events.append({
                            "event_name": outcome.get("name"),  # Use outcome name as event name
                            "odds_home": outcome.get("price"),
                            "bookmaker": bookmaker_name,
                            "market": market.get("key"),
                            "timestamp": commence_time,
                        })

        # Debug: Check parsed events
        print(f"Parsed events: {len(events)} rows")
        if events:
            print("Sample parsed event:", events[0])

        # Convert to DataFrame
        data = pd.DataFrame(events)
        self.data = data
        return self.data


    def run(self):
        """Generate buy-sell signals based on EV."""
        if self.data is None or self.data.empty:
            raise ValueError("No data available to run the strategy. Ensure fetch_data() was successful.")

        print(f"Data before signal generation: {len(self.data)} rows")
        print(self.data.head())  # Debug first few rows

        # Calculate implied probabilities and expected value
        self.data['implied_prob'] = 1 / self.data['odds_home']
        self.data['expected_value'] = (self.data['implied_prob'] * self.data['odds_home']) - 1

        # Generate buy-sell signals
        self.data['signal'] = self.data['expected_value'].apply(lambda x: 'BUY' if x > 0.05 else 'HOLD')

        print(f"Signals generated: {self.data['signal'].value_counts().to_dict()}")
        return self.data[['event_name', 'odds_home', 'expected_value', 'signal']]
