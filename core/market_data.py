#core/market_data.py
"""
Module for interacting with market data APIs.

This module provides functions to fetch live market data from
external APIs such as Alpaca. It's used for observation
purposes only (not trading).
"""

import os
import logging
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass


# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get Alpaca API credentials from environment
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_PAPER_URL = os.getenv('ALPACA_PAPER_URL')

# Check if credentials exist
if not all([ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_PAPER_URL]):
    logger.warning("Alpaca API credentials are not fully configured in .env file")


def get_alpaca_data_client():
    """
    Initialize and return an Alpaca Stock Historical Data client.

    Returns:
        StockHistoricalDataClient: Configured Alpaca data client
        or None if credentials are missing
    """
    if not all([ALPACA_API_KEY, ALPACA_SECRET_KEY]):
        logger.error("Alpaca API credentials missing. Cannot initialize client.")
        return None

    try:
        return StockHistoricalDataClient(
            api_key=ALPACA_API_KEY,
            secret_key=ALPACA_SECRET_KEY
        )
    except Exception as e:
        logger.error(f"Error initializing Alpaca Data client: {str(e)}")
        return None


def get_alpaca_trading_client():
    """
    Initialize and return an Alpaca Trading client (paper trading).

    Returns:
        TradingClient: Configured Alpaca trading client
        or None if credentials are missing
    """
    if not all([ALPACA_API_KEY, ALPACA_SECRET_KEY]):
        logger.error("Alpaca API credentials missing. Cannot initialize client.")
        return None

    try:
        return TradingClient(
            api_key=ALPACA_API_KEY,
            secret_key=ALPACA_SECRET_KEY,
            paper=True  # Use paper trading
        )
    except Exception as e:
        logger.error(f"Error initializing Alpaca Trading client: {str(e)}")
        return None


def get_latest_quote(ticker):
    """
    Get the latest quote data for a specified ticker.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL')

    Returns:
        dict: Quote data including bid, ask, and timestamp information
        or None if an error occurs
    """
    if not ticker:
        logger.error("Ticker symbol is required to get quote data")
        return None

    # Normalize ticker
    ticker = ticker.upper().strip()

    # Get client
    client = get_alpaca_data_client()
    if not client:
        return None

    try:
        # Create request parameters
        request_params = StockLatestQuoteRequest(symbol_or_symbols=[ticker])

        # Get latest quote
        latest_quote = client.get_stock_latest_quote(request_params)

        # Process response
        if ticker not in latest_quote:
            logger.warning(f"No quote data found for ticker {ticker}")
            return None

        quote = latest_quote[ticker]

        # Format the response as a dictionary
        result = {
            'ticker': ticker,
            'bid_price': quote.bid_price,
            'bid_size': quote.bid_size,
            'ask_price': quote.ask_price,
            'ask_size': quote.ask_size,
            'timestamp': quote.timestamp,
            'status': 'success'
        }

        return result

    except Exception as e:
        logger.error(f"Error fetching quote data for {ticker}: {str(e)}")
        return {
            'ticker': ticker,
            'status': 'error',
            'error_message': str(e)
        }


def is_tradable(ticker):
    """
    Check if a ticker symbol is tradable on Alpaca.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL')

    Returns:
        bool: True if the ticker is tradable, False otherwise
    """
    if not ticker:
        return False

    # Normalize ticker
    ticker = ticker.upper().strip()

    # Get client
    client = get_alpaca_trading_client()
    if not client:
        return False

    try:
        # Create request parameters for US stocks
        request_params = GetAssetsRequest(
            asset_class=AssetClass.US_EQUITY,
            status='active'
        )

        # Get assets
        assets = client.get_all_assets(request_params)

        # Check if the ticker is in the list of tradable assets
        for asset in assets:
            if asset.symbol == ticker and asset.tradable:
                return True

        return False

    except Exception as e:
        logger.error(f"Error checking if {ticker} is tradable: {str(e)}")
        return False
