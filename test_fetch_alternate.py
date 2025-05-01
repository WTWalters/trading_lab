from core.data_handler import fetch_stock_data
import pandas as pd
import time
import random

# Function to try different tickers and date ranges
def try_fetch_with_ticker(ticker, year, month, day):
    """Try to fetch data for a specific ticker and date."""
    start_date = f"{year}-{month:02d}-{day:02d}"
    end_date = f"{year}-{month:02d}-{day+5:02d}"  # just 5 days of data
    
    print(f"Trying {ticker} from {start_date} to {end_date}...")
    
    return fetch_stock_data(ticker, source='yfinance', 
                           start_date=start_date, 
                           end_date=end_date)

# List of tickers and years to try
tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META']
years = [2021, 2020, 2019, 2018]

print("Testing yfinance with various tickers and date ranges...")

# Try different combinations until we get data
for ticker in tickers:
    for year in years:
        # Random month and day to avoid patterns that might trigger rate limits
        month = random.randint(1, 12)
        day = random.randint(1, 20)
        
        df = try_fetch_with_ticker(ticker, year, month, day)
        
        if df is not None and not df.empty:
            print("\nSuccessfully fetched data!")
            print(f"\nYFinance Data for {ticker}:")
            print(df.head())
            break
            
        # Add a significant delay before trying again
        time.sleep(5)
    
    if df is not None and not df.empty:
        break

if df is None or df.empty:
    print("\nFailed to fetch data from yfinance after multiple attempts.")
    print("The API might be experiencing issues or has strict rate limits.")

# Test Alpha Vantage if installed
try:
    from alpha_vantage.timeseries import TimeSeries
    print("\nAlpha Vantage package is installed.")
    
    # Check if the API key exists in the environment
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if alpha_key:
        print("Found Alpha Vantage API key. Testing Alpha Vantage data source...")
        # Add delay to avoid hitting rate limits
        time.sleep(2)
        
        df_av = fetch_stock_data('AAPL', source='alpha_vantage')
        print('\nAlpha Vantage Data:')
        if df_av is not None and not df_av.empty:
            print(df_av.head())
        else:
            print('No data returned from Alpha Vantage. Check your API key.')
    else:
        print('No Alpha Vantage API key found in .env file. Skipping Alpha Vantage test.')
        
except ImportError:
    print("\nAlpha Vantage package is not installed in this environment.")
    print("Install it with: pip install alpha-vantage")
