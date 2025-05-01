# core/data_handler.py
import os
import logging
import pandas as pd
import time
import random
# --- Corrected/Ensured DateTime Import ---
from datetime import datetime, timedelta, timezone as dt_timezone
# -----------------------------------------
from dotenv import load_dotenv
import yfinance as yf
from decimal import Decimal

# --- Django imports ---
# Make sure transaction is imported if using the decorator
from django.db import IntegrityError, transaction
# Use Django's timezone utilities
from django.utils import timezone as django_timezone # Alias to avoid confusion
from django.utils.timezone import make_aware
# Import the model within a try-except block
try:
    from dashboard.models import OHLCVData
    DJANGO_MODELS_AVAILABLE = True
except ImportError:
    # Handle case where Django models aren't available
    # Define logger early if needed here
    logger_setup = logging.getLogger(__name__)
    logger_setup.error("Could not import Django models. Ensure Django environment is set up.")
    OHLCVData = None
    DJANGO_MODELS_AVAILABLE = False
# ---------------------

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Define logger (will use root logger if setup above failed, or scoped logger)
logger = logging.getLogger(__name__)

# Try to import Alpha Vantage - make it optional
try:
    from alpha_vantage.timeseries import TimeSeries
    ALPHA_VANTAGE_AVAILABLE = True
except ImportError:
    logger.warning("Alpha Vantage package not installed. Alpha Vantage data source will not be available.")
    ALPHA_VANTAGE_AVAILABLE = False
    TimeSeries = None # Define as None if not available

# Load environment variables
load_dotenv()

# --- Fetch Functions (Unchanged from your last version) ---

def fetch_yfinance_data(ticker, start_date=None, end_date=None, max_retries=3, retry_delay=2):
    """ Fetch daily OHLCV data for a given ticker using yfinance. """
    if not end_date: end_date = datetime.now().strftime('%Y-%m-%d')
    if not start_date: start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    logger.info(f"Fetching yfinance data for {ticker} from {start_date} to {end_date}")
    for attempt in range(max_retries):
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True) # Explicitly set auto_adjust if needed, or handle Adjustments manually
            if df.empty:
                logger.warning(f"No data found for ticker {ticker} via yfinance")
                return None

            # yfinance with auto_adjust=True might simplify columns, but check anyway
            if isinstance(df.columns, pd.MultiIndex):
                # For a single ticker, the standard names are usually level 0
                logger.info(f"Processing MultiIndex columns for single ticker {ticker}. Using level 0.")
                df.columns = df.columns.get_level_values(0)


            # Ensure required columns are present after potential flattening/auto_adjust
            required_cols_yf = {'open', 'high', 'low', 'close', 'volume'}
            df.columns = df.columns.str.lower().str.replace(' ', '_') # Normalize column names
            if not required_cols_yf.issubset(df.columns):
                 missing = required_cols_yf - set(df.columns)
                 logger.error(f"yfinance data for {ticker} missing required columns after processing: {missing}")
                 return None

            df.index.name = 'timestamp' # Ensure index has a name
            logger.info(f"Successfully fetched {len(df)} records for {ticker} from yfinance")
            return df
        except Exception as e:
            logger.warning(f"yfinance attempt {attempt+1}/{max_retries} failed for {ticker} ({start_date} to {end_date}): {str(e)}")
            if attempt < max_retries - 1:
                sleep_time = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                logger.info(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                logger.error(f"All {max_retries} yfinance attempts failed for {ticker}: {str(e)}")
                return None

def fetch_alpha_vantage_data(ticker):
    """ Fetch daily OHLCV data for a given ticker using Alpha Vantage API. """
    if not ALPHA_VANTAGE_AVAILABLE or TimeSeries is None:
        logger.error("Alpha Vantage package not installed/imported. Cannot fetch data.")
        return None
    try:
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            logger.error("ALPHA_VANTAGE_API_KEY not found in .env file")
            return None
        logger.info(f"Fetching Alpha Vantage data for {ticker}")
        ts = TimeSeries(key=api_key, output_format='pandas')
        # Use get_daily_adjusted for split/dividend adjusted data
        data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')

        # Rename columns based on Alpha Vantage's adjusted output
        column_rename = {
            '1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close',
            '5. adjusted close': 'adjusted_close', # Keep if needed, otherwise remove/ignore
            '6. volume': 'volume', '7. dividend amount': 'dividend',
            '8. split coefficient': 'split'
        }
        df = data.rename(columns=column_rename)
        df.index.name = 'timestamp' # Set index name

        # Ensure required columns are present
        required_cols_av = {'open', 'high', 'low', 'close', 'volume'}
        if not required_cols_av.issubset(df.columns):
            missing = required_cols_av - set(df.columns)
            logger.error(f"Alpha Vantage data for {ticker} missing required columns after rename: {missing}")
            return None # Or handle differently if adjusted_close is primary

        if df.empty:
            logger.warning(f"No data found for ticker {ticker} via Alpha Vantage")
            return None

        logger.info(f"Successfully fetched {len(df)} records for {ticker} from Alpha Vantage")
        return df
    except Exception as e:
        logger.error(f"Error fetching data from Alpha Vantage for {ticker}: {str(e)}")
        return None

def fetch_stock_data(ticker, source='yfinance', start_date=None, end_date=None):
    """ Fetch stock data from the specified source. """
    if source.lower() == 'yfinance':
        return fetch_yfinance_data(ticker, start_date, end_date)
    elif source.lower() == 'alpha_vantage':
        # Alpha Vantage fetch might not use start/end date in the same way, gets full history
        return fetch_alpha_vantage_data(ticker)
    else: # pragma: no cover
        logger.error(f"Invalid source specified: {source}. Use 'yfinance' or 'alpha_vantage'")
        return None

# --- Corrected Save Function ---

@transaction.atomic
def save_ohlcv_data(dataframe: pd.DataFrame, ticker: str):
    """
    Save OHLCV data from a Pandas DataFrame to the OHLCVData model.
    Handles timezone conversion and potential duplicates via ignore_conflicts.
    """
    if not DJANGO_MODELS_AVAILABLE or OHLCVData is None:
        logger.error("OHLCVData model is not available. Cannot save data.")
        return 0 # Return 0 records saved

    if dataframe is None or dataframe.empty:
        logger.warning(f"Received empty or None DataFrame for ticker {ticker}. No data saved.")
        return 0
    if not isinstance(dataframe.index, pd.DatetimeIndex):
        # Convert index to DatetimeIndex if possible (e.g., if it's just date strings)
        try:
            dataframe.index = pd.to_datetime(dataframe.index)
            if not isinstance(dataframe.index, pd.DatetimeIndex):
                 raise ValueError("Index conversion failed.") # Raise if conversion doesn't result in DatetimeIndex
            logger.info(f"Converted index to DatetimeIndex for {ticker}.")
        except Exception as e:
             logger.error(f"DataFrame index for {ticker} is not a DatetimeIndex and could not be converted: {e}")
             return 0

    logger.info(f"Preparing to save {len(dataframe)} data points for ticker {ticker}.")

    # Ensure required columns exist after potential adjustments in fetch functions
    required_cols = {'open', 'high', 'low', 'close', 'volume'}
    dataframe.columns = dataframe.columns.str.lower().str.replace(' ', '_') # Normalize again just in case
    if not required_cols.issubset(dataframe.columns):
        missing_cols = required_cols - set(dataframe.columns)
        logger.error(f"DataFrame for {ticker} missing required columns for saving: {missing_cols}")
        return 0

    ohlcv_instances = []
    # 'timestamp' here is the loop variable representing the index value (a pandas Timestamp)
    for timestamp, row in dataframe.iterrows():

        if pd.isna(timestamp): # Check the index value directly
            logger.warning(f"Skipping row for {ticker} due to invalid timestamp in index.")
            continue

        # --- Refined Timezone Handling ---
        try:
            # Convert pandas Timestamp index value to standard python datetime
            py_dt = timestamp.to_pydatetime()
        except AttributeError: # Handle potential non-Timestamp objects if conversion failed earlier
             logger.warning(f"Skipping row for {ticker} due to invalid index type for timestamp: {timestamp}")
             continue

        # Use Django's timezone utility on the standard python datetime
        # Assume incoming data (like yfinance) represents market time and is naive; make it UTC.
        if django_timezone.is_naive(py_dt):
            # Make the naive datetime UTC aware using datetime.timezone.utc (aliased as dt_timezone.utc)
            aware_timestamp = make_aware(py_dt, timezone=dt_timezone.utc)
        else:
            # If it was somehow already aware, ensure it's converted to UTC
            aware_timestamp = django_timezone.localtime(py_dt, dt_timezone.utc)
        # --- End Refined Timezone Handling ---

        # Check for NaN/None values in critical data columns for the current row
        # Use pandas isna() for checking row data as it handles None/NaN consistently
        if pd.isna(row['open']) or pd.isna(row['high']) or pd.isna(row['low']) or pd.isna(row['close']) or pd.isna(row['volume']):
            logger.warning(f"Skipping row for {ticker} at {aware_timestamp} due to NaN/None values in data.")
            continue

        # Ensure volume is an integer
        try:
            # Handle potential non-numeric volume data before casting
            volume_numeric = pd.to_numeric(row['volume'], errors='coerce')
            if pd.isna(volume_numeric):
                raise ValueError("Volume is NaN")
            volume_int = int(volume_numeric)
        except (ValueError, TypeError):
             logger.warning(f"Skipping row for {ticker} at {aware_timestamp} due to non-integer convertible volume: {row['volume']}")
             continue

        ohlcv_instances.append(
            OHLCVData(
                timestamp=aware_timestamp, # Use the final aware datetime object
                ticker=ticker,
                # Convert to Decimal explicitly if needed, though Django often handles numeric types
                open=Decimal(str(row['open'])), # Convert via string for precision
                high=Decimal(str(row['high'])),
                low=Decimal(str(row['low'])),
                close=Decimal(str(row['close'])),
                volume=volume_int
            )
        )

    if not ohlcv_instances:
        logger.warning(f"No valid instances generated for {ticker}. Nothing to save.")
        return 0

    try:
        # Use bulk_create with ignore_conflicts=True
        # Assumes a unique constraint exists on (ticker, timestamp) in the DB / Timescale hypertable
        created_objects = OHLCVData.objects.bulk_create(ohlcv_instances, ignore_conflicts=True)
        # Note: len(created_objects) might be 0 if ALL were conflicts, or less than len(ohlcv_instances)
        # It reflects objects Django *prepared* for insertion, not necessarily *newly* inserted count with ignore_conflicts.
        num_prepared = len(ohlcv_instances) # How many we tried to insert
        # A more accurate count of *new* records requires querying before/after or specific DB features.
        logger.info(f"Processed bulk insert for {ticker}. Prepared {num_prepared} objects (existing matching ticker/timestamp ignored).")
        # Returning num_prepared might be more informative than len(created_objects) here.
        return num_prepared

    except IntegrityError as e: # Should be less common with ignore_conflicts=True unless other constraints fail
        logger.error(f"Integrity error during bulk save for {ticker}: {e}") # pragma: no cover
        return 0 # pragma: no cover
    except Exception as e:
        logger.error(f"Unexpected error during bulk save for {ticker}: {e}") # pragma: no cover
        raise e # Re-raise unexpected errors # pragma: no cover
