class TradingSystem:
    def __init__(self, strategies):
        self.strategies = strategies

    def backtest(self):
        """Run all strategies and collect their results."""
        results = []
        for proportion, strategy in self.strategies:
            print(f"Running strategy: {type(strategy).__name__}")

            # Step 1: Fetch data for the strategy
            print("Fetching data for strategy...")
            strategy_data = strategy.fetch_data()
            print(f"Fetched {len(strategy_data)} rows for {type(strategy).__name__}.")

            # Step 2: Execute the strategy
            strategy_results = strategy.run()
            results.append((proportion, strategy_results))
        return results
