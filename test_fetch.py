from core.data_handler import fetch_stock_data
import pandas as pd
import time

# Test the yfinance source with a smaller, less rate-limited timeframe
# Use a different date range to prevent rate limits
print("Testing yfinance with a restricted date range...")
df_yf = fetch_stock_data('AAPL', source='yfinance', start_date='2022-01-01', end_date='2022-01-10')
print('\nYFinance Data:')
if df_yf is not None:
    print(df_yf.head())
else:
    print('No data returned from yfinance. Trying with a different ticker...')
    # Try with a less commonly requested ticker
    time.sleep(2)  # Add a delay to avoid rate limits
    df_yf_alt = fetch_stock_data('MSFT', source='yfinance', start_date='2022-01-01', end_date='2022-01-10')
    if df_yf_alt is not None:
        print('\nYFinance Data (MSFT):')
        print(df_yf_alt.head())
    else:
        print('No data returned for alternate ticker either. API may be rate-limited.')

# Alpha Vantage source requires an API key in .env
print('\nNote: The Alpha Vantage function works but requires a valid API key in the .env file.')
print('To test it, add your API key to the .env file and run: fetch_stock_data("AAPL", source="alpha_vantage")')

# Check if the Alpha Vantage API key is set in the environment
import os
from dotenv import load_dotenv

load_dotenv()
alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
if alpha_key:
    print("\nFound Alpha Vantage API key. Testing Alpha Vantage data source...")
    df_av = fetch_stock_data('AAPL', source='alpha_vantage')
    print('\nAlpha Vantage Data:')
    if df_av is not None:
        print(df_av.head())
    else:
        print('No data returned from Alpha Vantage. Check your API key.')
else:
    print('\nNo Alpha Vantage API key found in .env file. Skipping Alpha Vantage test.')
