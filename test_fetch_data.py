#!/usr/bin/env python
# Simple test script to verify data fetching

import os
import sys
from datetime import datetime, timedelta

# Add the project directory to path so we can import from core
sys.path.append('.')

# Try to import the data fetching functions
try:
    from core.data_handler import fetch_stock_data
    print("Successfully imported fetch_stock_data function")
except ImportError as e:
    print(f"Error importing data handler: {e}")
    sys.exit(1)

# Test fetching data for a popular stock
ticker = "AAPL"
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

print(f"Fetching data for {ticker} from {start_date} to {end_date}")

# Try with yfinance first as it doesn't require API key
print("\nTesting yfinance data source:")
try:
    yf_data = fetch_stock_data(ticker, source='yfinance', start_date=start_date, end_date=end_date)
    if yf_data is not None and not yf_data.empty:
        print(f"Successfully fetched {len(yf_data)} rows of data from yfinance")
        print("Sample data:")
        print(yf_data.head(3))
    else:
        print("Failed to fetch data from yfinance or returned empty dataset")
except Exception as e:
    print(f"Error fetching from yfinance: {e}")

# Now try with Alpha Vantage if environment variable is set
alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
if alpha_key:
    print("\nTesting Alpha Vantage data source:")
    try:
        av_data = fetch_stock_data(ticker, source='alpha_vantage')
        if av_data is not None and not av_data.empty:
            print(f"Successfully fetched {len(av_data)} rows of data from Alpha Vantage")
            print("Sample data:")
            print(av_data.head(3))
        else:
            print("Failed to fetch data from Alpha Vantage or returned empty dataset")
    except Exception as e:
        print(f"Error fetching from Alpha Vantage: {e}")
else:
    print("\nSkipping Alpha Vantage test as API key is not set in environment")

print("\nData fetching test completed")
