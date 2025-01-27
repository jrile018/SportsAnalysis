
**The System**

System structure
- 1. data pipeline
    - information from the book; trades
    - quantitative game and player data relavent to sport association
    - qualitative news sentiment data
- 2. runs models
    Models folder
    |_ example_news_sentament_model.py
    |_ example_arbitrage_model.py
- 3. finds buy-sell signals
    - normalized data to translate into execution
- 4. executes trades
    - logs into broker w/ selenium
- 5. PnL data
    - shows results with graphs and helpful multiples

the strategy might be composed of two general trading systems:
- arbitrage; making the market more efficient
- news sentiment; based on highly relavent and ripe data

news sentiment
- classification method 

brainstorming new sentiment:
- what are the possible new items that have high importance
- is there an objective way of determining that
- should players have a preformance rating to determine what news is important and how
- 

brainstorming ai:
- how can we use ai to find buy-sell signals
- is there a way of formatting data in a clean way that the neural network can understand
- is there enough data to train an ai model
- how long would it take to run and would it be competetive
- can we use a general/trained LLM model or might it be better to only use quantitative terms
    - can both be used but for different scenarios; news sentiment & regular buy-sell model




