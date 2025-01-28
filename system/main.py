from database import Database
from strategies import ExampleStrategy
from trading_system import TradingSystem

def main():
    # Initialize the database
    #db = Database()
    #db.initialize()

    # Define risk and capital
    risk_target = 0.30
    capital = 100

    # Initialize trading system with strategies
    trading_system = TradingSystem(
        strategies=[
            # Each strategy fetches its own data
            (1.0, ExampleStrategy(risk_target=risk_target, capital=capital, num_stocks=5)),
        ]
    )

    # Run backtest
    print("Running backtest...")
    results = trading_system.backtest()

    # Display results
    for proportion, result in results:
        print(f"\nStrategy Proportion: {proportion}")
        print(result)

if __name__ == "__main__":
    main()
