"""
Backtester module for running trading strategy simulations.

This module provides functionality to:
1. Create data feeds from the PostgreSQL database
2. Configure and run backtests with specified strategies
3. Analyze and return results of backtest runs
"""
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from django.db.models import Min, Max
import backtrader as bt

from dashboard.models import OHLCVData
from core.strategies import ClassicBreakoutStrategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_data_feed(ticker, start_date=None, end_date=None):
    """
    Create a data feed by querying OHLCV data from PostgreSQL.
    
    Parameters:
        ticker (str): Stock ticker symbol
        start_date (datetime): Start date for the data range
        end_date (datetime): End date for the data range
        
    Returns:
        bt.feeds.PandasData: Backtrader data feed
    """
    logger.info(f"Creating data feed for {ticker} from {start_date} to {end_date}")
    
    # Build query for OHLCV data
    query = OHLCVData.objects.filter(ticker=ticker)
    
    # Apply date filters if provided
    if start_date:
        query = query.filter(timestamp__gte=start_date)
    if end_date:
        query = query.filter(timestamp__lte=end_date)
    
    # Order by timestamp
    query = query.order_by('timestamp')
    
    # Check if data exists
    if not query.exists():
        logger.warning(f"No data found for ticker {ticker} in date range")
        return None
    
    # Convert QuerySet to DataFrame
    records = []
    for record in query:
        records.append({
            'timestamp': record.timestamp,
            'open': float(record.open),
            'high': float(record.high),
            'low': float(record.low),
            'close': float(record.close),
            'volume': int(record.volume)
        })
    
    if not records:
        logger.warning(f"No data converted for ticker {ticker}")
        return None
    
    # Create DataFrame with timestamp as index
    df = pd.DataFrame(records)
    df.set_index('timestamp', inplace=True)
    
    # Ensure DataFrame columns match Backtrader naming conventions
    df.columns = df.columns.str.lower()
    
    # Convert DataFrame to Backtrader data feed
    data_feed = bt.feeds.PandasData(
        dataname=df,
        datetime=None,  # Index is already datetime
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1  # Not used
    )
    
    logger.info(f"Created data feed with {len(df)} bars")
    return data_feed


def get_available_date_range(ticker):
    """
    Get the available date range for a ticker in the database.
    
    Parameters:
        ticker (str): Stock ticker symbol
        
    Returns:
        tuple: (min_date, max_date) or (None, None) if no data
    """
    result = OHLCVData.objects.filter(ticker=ticker).aggregate(
        min_date=Min('timestamp'),
        max_date=Max('timestamp')
    )
    
    return result['min_date'], result['max_date']


def run_backtest(ticker, start_date=None, end_date=None,
                 strategy_class=ClassicBreakoutStrategy,
                 strategy_params=None, initial_cash=100000.0, commission=0.001):
    """
    Runs a backtest using the Backtrader engine for the specified ticker,
    date range, and strategy.

    Parameters:
        ticker (str): Stock ticker symbol.
        start_date (datetime): Start date for backtest (timezone aware).
        end_date (datetime): End date for backtest (timezone aware).
        strategy_class: Strategy class to use (default: ClassicBreakoutStrategy).
        strategy_params (dict): Optional parameters for the strategy.
        initial_cash (float): Initial cash amount for the backtest.
        commission (float): Commission rate (e.g., 0.001 for 0.1%).

    Returns:
        dict: A dictionary containing results:
              - 'success': Boolean indicating if the backtest ran.
              - 'analyzers': Dictionary containing results from analyzers (if successful).
              - 'error': Error message string (if failed).
              - 'start_value': Starting portfolio value.
              - 'end_value': Ending portfolio value.
    """
    logger.info(
        f"Initializing Cerebro for backtest: Ticker={ticker}, "
        f"Start={start_date}, End={end_date}, Strategy={strategy_class.__name__}"
    )

    # 1. Initialize Cerebro engine
    cerebro = bt.Cerebro()

    # 2. Add Strategy
    # Pass strategy parameters if provided
    if strategy_params:
        cerebro.addstrategy(strategy_class, **strategy_params)
    else:
        cerebro.addstrategy(strategy_class)

    # 3. Get and Add Data Feed
    data_feed = get_data_feed(ticker, start_date, end_date)
    if data_feed is None:
        error_msg = f"No data feed available for {ticker} in the specified date range."
        logger.error(error_msg)
        return {'success': False, 'error': error_msg, 'analyzers': None, 'start_value': None, 'end_value': None}

    cerebro.adddata(data_feed)

    # 4. Set Initial Cash
    cerebro.broker.setcash(initial_cash)
    start_value = cerebro.broker.getvalue() # Record starting value
    logger.info(f"Initial Portfolio Value: {start_value:.2f}")

    # 5. Set Commission
    cerebro.broker.setcommission(commission=commission)

    # 6. Add Analyzers
    # Standard analyzers for performance evaluation
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    # Additional analyzers
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', timeframe=bt.TimeFrame.Days)

    # 7. Run the Backtest
    try:
        logger.info("Running Cerebro...")
        # The result is a list of strategy instances, one for each data feed (we only have one)
        results = cerebro.run()
        end_value = cerebro.broker.getvalue() # Record ending value
        logger.info(f"Backtest complete. Final Portfolio Value: {end_value:.2f}")

        # 8. Extract and Return Analyzer Results
        # Access analyzers from the first strategy instance in the results list
        strategy_instance = results[0]
        analyzer_results = {}
        if hasattr(strategy_instance.analyzers, 'trade_analyzer'):
            analyzer_results['trade_analyzer'] = strategy_instance.analyzers.trade_analyzer.get_analysis()
        if hasattr(strategy_instance.analyzers, 'sqn'):
             analyzer_results['sqn'] = strategy_instance.analyzers.sqn.get_analysis()
        # Add other analyzers
        if hasattr(strategy_instance.analyzers, 'drawdown'):
            analyzer_results['drawdown'] = strategy_instance.analyzers.drawdown.get_analysis()
        if hasattr(strategy_instance.analyzers, 'sharpe'):
            analyzer_results['sharpe'] = strategy_instance.analyzers.sharpe.get_analysis()

        return {
            'success': True,
            'analyzers': analyzer_results,
            'error': None,
            'start_value': start_value,
            'end_value': end_value
        }

    except Exception as e:
        error_msg = f"An error occurred during Cerebro run: {e}"
        logger.exception(error_msg) # Log exception with traceback
        return {'success': False, 'error': error_msg, 'analyzers': None, 'start_value': start_value, 'end_value': None}
