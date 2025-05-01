#!/usr/bin/env python
# Simplified test script that only uses yfinance directly

import sys
from datetime import datetime, timedelta

print("Attempting to import yfinance...")
try:
    import yfinance as yf
    print("Successfully imported yfinance")
except ImportError:
    print("Error: yfinance is not installed. Try: pip install yfinance")
    sys.exit(1)

# Test fetching data for a popular stock
ticker = "AAPL"
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

print(f"Fetching data for {ticker} from {start_date} to {end_date}")

try:
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if data is not None and not data.empty:
        print(f"Successfully fetched {len(data)} rows of data")
        print("Sample data:")
        print(data.head(3))
    else:
        print("Failed to fetch data or returned empty dataset")
except Exception as e:
    print(f"Error fetching data: {e}")

print("Test completed")
