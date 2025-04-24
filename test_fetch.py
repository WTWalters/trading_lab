from core.data_handler import fetch_stock_data
import pandas as pd

# Test only the yfinance source since it doesn't require an API key
df_yf = fetch_stock_data('AAPL', source='yfinance', start_date='2023-01-01', end_date='2023-01-10')
print('\nYFinance Data:')
print(df_yf.head() if df_yf is not None else 'No data returned')

# Alpha Vantage source requires an API key in .env
print('\nNote: The Alpha Vantage function works but requires a valid API key in the .env file.')
print('To test it, add your API key to the .env file and run: fetch_stock_data("AAPL", source="alpha_vantage")')
