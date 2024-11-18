def get_instrument_token(stock_names, exchange='BSE'):

  # Load the instruments.csv file
  instruments_df = pd.read_csv('/content/RL_in_Stock_Market/instruments.csv')

  # Filter for NSE and BSE instruments
  nse_bse_instruments = instruments_df[
      instruments_df['exchange'].apply(lambda x: x in ['NSE', 'BSE'])
  ]

  if isinstance(stock_names, str):
    stock_names = [stock_names]

  tokens = []
  for name in stock_names:
    try:
      token = nse_bse_instruments[
          (nse_bse_instruments['tradingsymbol'] == name) &
          (nse_bse_instruments['exchange'] == exchange)
      ]['instrument_token'].values[0]
      tokens.append(token)
    except IndexError:
      print(f"Instrument token not found for {name} on {exchange}")
  return tokens


def get_historical_data(stocks,last_n_days = 1,interval = "minute"):

  # Get the instrument tokens for the stocks
  tokens = get_instrument_token(stocks)

  # Get the historical data
  historical_data = {}
  for i in range(len(stocks)):
    try:

      if last_n_days == 'max':
        from_datetime = datetime.datetime.now() - datetime.timedelta(days=100)     # From last & days
        to_datetime = datetime.datetime.now()
      else:
        from_datetime = datetime.datetime.now() - datetime.timedelta(days=last_n_days)     # From last & days
        to_datetime = datetime.datetime.now()

      print(tokens[i],from_datetime, to_datetime,interval)
      data = kite.historical_data(tokens[i],from_datetime, to_datetime,interval)
      historical_data[stocks[i]] = pd.DataFrame(data)
    except Exception as e:
      print(f"Error fetching data for {stocks[i]}: {e}")

  # Print the historical data
  return historical_data


def get_max_historical_data(stocks, interval="minute",exchange='BSE',show_flg = True):
  """
  Fetches historical data for a given list of stocks at a specified interval.

  Args:
      stocks (list): A list of stock names (strings) to fetch data for.
      interval (str, optional): The desired data interval, e.g., "minute", "5minute", "day".
                                Defaults to "minute".

  Returns:
      pd.DataFrame: A DataFrame containing historical data for the specified stocks.
  """

  if type(stocks) == list:
    for i in range(len(stocks)):

      tokens = get_instrument_token(stocks,exchange)

      if not tokens:
        print(f"No instrument tokens found for {stocks}.")
        return pd.DataFrame()

      data = pd.DataFrame()
      temp_date = datetime.datetime.now()

      while True:
          from_datetime = temp_date - datetime.timedelta(days=50)
          to_datetime = temp_date

          try:
              temp_data = kite.historical_data(tokens[i], from_datetime, to_datetime, interval)
              temp_date = from_datetime
              if show_flg:
                print(f"Extracted data for {stocks[i]} from: {from_datetime} to: {to_datetime}")

              # Saving the data
              if not len(temp_data):
                  if not data.empty:
                      if not os.path.exists(f"/content/{interval}_{exchange}_history_data"):
                        os.makedirs(f"/content/{interval}_{exchange}_history_data")

                      path = os.path.join(f"/content/{interval}_{exchange}_history_data",stocks[0] + f"_max_{interval}_history.csv")
                      data.to_csv(path)
                  break

              data = pd.concat([data, pd.DataFrame(temp_data)], ignore_index=True)
          except Exception as e:
              print(f"Error fetching data: {e}")
              break

      return data