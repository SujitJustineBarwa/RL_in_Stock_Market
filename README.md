# RL_in_Stock_Market
This Repo has code that analyzes stock data to form a policy.

To get 'minute' historical data :
    
    historical_data = kite.historical_data(
        instrument_token=5633,
        from_date='2024-09-01',
        to_date='2024-09-06',
        interval='minute'  # Shortest interval
    )
