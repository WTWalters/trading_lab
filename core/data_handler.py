import os
import logging
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import yfinance as yf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import Alpha Vantage - make it optional
try:
    from alpha_vantage.timeseries import TimeSeries
    ALPHA_VANTAGE_AVAILABLE = True
except ImportError:
    logger.warning("Alpha Vantage package not installed. Alpha Vantage data source will not be available.")
    ALPHA_VANTAGE_AVAILABLE = False

# Load environment variables
load_dotenv()

def fetch_yfinance_data(ticker, start_date=None, end_date=None):
    """
    Fetch daily OHLCV data for a given ticker using yfinance.
    
    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Optional start date in 'YYYY-MM-DD' format. Defaults to 1 year ago.
        end_date (str): Optional end date in 'YYYY-MM-DD' format. Defaults to today.
        
    Returns:
        pandas.DataFrame: DataFrame with OHLCV data or None if an error occurs.
    """
    try:
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            # Default to 1 year of data
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
        logger.info(f"Fetching yfinance data for {ticker} from {start_date} to {end_date}")
        
        # Download the data
        df = yf.download(ticker, start=start_date, end=end_date)
        
        # Check if the DataFrame is empty
        if df.empty:
            logger.warning(f"No data found for ticker {ticker}")
            return None
            
        # Ensure column names are consistent (lowercase)
        df.columns = df.columns.str.lower()
        
        logger.info(f"Successfully fetched {len(df)} records for {ticker}")
        return df
        
    except Exception as e:
        logger.error(f"Error fetching data from yfinance: {str(e)}")
        return None

def fetch_alpha_vantage_data(ticker):
    """
    Fetch daily OHLCV data for a given ticker using Alpha Vantage API.
    
    Args:
        ticker (str): Stock ticker symbol.
        
    Returns:
        pandas.DataFrame: DataFrame with OHLCV data or None if an error occurs.
    """
    if not ALPHA_VANTAGE_AVAILABLE:
        logger.error("Alpha Vantage package not installed. Cannot fetch data.")
        return None
        
    try:
        # Get API key from environment variables
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not api_key:
            logger.error("ALPHA_VANTAGE_API_KEY not found in .env file")
            return None
            
        logger.info(f"Fetching Alpha Vantage data for {ticker}")
        
        # Initialize Alpha Vantage TimeSeries
        ts = TimeSeries(key=api_key, output_format='pandas')
        
        # Get daily data
        data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
        
        # Rename columns to match our convention (lowercase)
        column_rename = {
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. adjusted close': 'adjusted_close',
            '6. volume': 'volume',
            '7. dividend amount': 'dividend',
            '8. split coefficient': 'split'
        }
        
        df = data.rename(columns=column_rename)
        
        # Check if the DataFrame is empty
        if df.empty:
            logger.warning(f"No data found for ticker {ticker}")
            return None
            
        logger.info(f"Successfully fetched {len(df)} records for {ticker}")
        return df
        
    except Exception as e:
        logger.error(f"Error fetching data from Alpha Vantage: {str(e)}")
        return None

def fetch_stock_data(ticker, source='yfinance', start_date=None, end_date=None):
    """
    Fetch stock data from the specified source.
    
    Args:
        ticker (str): Stock ticker symbol.
        source (str): Data source to use ('yfinance' or 'alpha_vantage'). Defaults to 'yfinance'.
        start_date (str): Optional start date for yfinance (ignored for Alpha Vantage).
        end_date (str): Optional end date for yfinance (ignored for Alpha Vantage).
        
    Returns:
        pandas.DataFrame: DataFrame with OHLCV data or None if an error occurs.
    """
    if source.lower() == 'yfinance':
        return fetch_yfinance_data(ticker, start_date, end_date)
    elif source.lower() == 'alpha_vantage':
        return fetch_alpha_vantage_data(ticker)
    else:
        logger.error(f"Invalid source specified: {source}. Use 'yfinance' or 'alpha_vantage'")
        return None