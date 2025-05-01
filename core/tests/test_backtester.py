"""
Tests for the backtester module
"""
import pytest
import pandas as pd
import numpy as np
import backtrader as bt
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock

from core.backtester import get_data_feed, run_backtest, get_available_date_range
from core.strategies import ClassicBreakoutStrategy

@pytest.fixture
def mock_ohlcv_data():
    """Create mock OHLCV data for testing"""
    # Create a list of dates
    base_date = datetime(2023, 1, 1, tzinfo=datetime.now().tzinfo)
    dates = [base_date + timedelta(days=i) for i in range(100)]
    
    # Create mock data records
    records = []
    for i, date in enumerate(dates):
        price = 100 + i * 0.1  # Simple price trend
        records.append({
            'timestamp': date,
            'open': float(price),
            'high': float(price * 1.01),
            'low': float(price * 0.99),
            'close': float(price * 1.005),
            'volume': 1000 + i * 10
        })
    
    # Create DataFrame
    df = pd.DataFrame(records)
    df.set_index('timestamp', inplace=True)
    
    return df

@pytest.mark.django_db
class TestBacktester:
    """Test suite for the backtester module"""
    
    @patch('core.backtester.OHLCVData.objects.filter')
    def test_get_data_feed(self, mock_filter):
        """Test that get_data_feed correctly queries and processes database data"""
        # Setup mock queryset
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.exists.return_value = True
        
        # Create mock OHLCVData objects
        mock_records = []
        base_date = datetime(2023, 1, 1, tzinfo=datetime.now().tzinfo)
        
        for i in range(10):
            mock_record = MagicMock()
            mock_record.timestamp = base_date + timedelta(days=i)
            mock_record.open = Decimal(str(100 + i))
            mock_record.high = Decimal(str(105 + i))
            mock_record.low = Decimal(str(95 + i))
            mock_record.close = Decimal(str(102 + i))
            mock_record.volume = 1000 + i * 100
            mock_records.append(mock_record)
        
        # Set the mock queryset to return our mock records
        mock_query.__iter__.return_value = mock_records
        mock_filter.return_value = mock_query
        
        # Call the function
        ticker = 'AAPL'
        start_date = base_date
        end_date = base_date + timedelta(days=10)
        
        # Mock the pandas DataFrame and bt.feeds.PandasData
        with patch('pandas.DataFrame') as mock_df, \
             patch('backtrader.feeds.PandasData') as mock_bt_data:
            
            # Configure mock DataFrame
            mock_df_instance = MagicMock()
            mock_df_instance.columns = MagicMock()
            mock_df_instance.columns.str.lower.return_value = mock_df_instance.columns
            mock_df_instance.set_index.return_value = mock_df_instance
            mock_df.return_value = mock_df_instance
            
            # Configure mock PandasData
            mock_bt_data_instance = MagicMock()
            mock_bt_data.return_value = mock_bt_data_instance
            
            result = get_data_feed(ticker, start_date, end_date)
        
        # Assertions
        assert result is not None
        mock_filter.assert_called_once_with(ticker=ticker)
        mock_query.filter.assert_any_call(timestamp__gte=start_date)
        mock_query.filter.assert_any_call(timestamp__lte=end_date)
        mock_query.order_by.assert_called_once_with('timestamp')
        mock_df.assert_called_once()
        mock_bt_data.assert_called_once()
    
    @patch('core.backtester.OHLCVData.objects.filter')
    def test_get_data_feed_no_data(self, mock_filter):
        """Test that get_data_feed handles case with no data"""
        # Setup mock queryset
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.exists.return_value = False
        
        mock_filter.return_value = mock_query
        
        # Call the function
        result = get_data_feed('NONEXISTENT')
        
        # Assertions
        assert result is None
    
    @patch('core.backtester.OHLCVData.objects.filter')
    def test_get_available_date_range(self, mock_filter):
        """Test that get_available_date_range correctly returns min and max dates"""
        # Setup mock aggregate result
        mock_query = MagicMock()
        
        min_date = datetime(2023, 1, 1, tzinfo=datetime.now().tzinfo)
        max_date = datetime(2023, 12, 31, tzinfo=datetime.now().tzinfo)
        
        mock_query.aggregate.return_value = {
            'min_date': min_date,
            'max_date': max_date
        }
        
        mock_filter.return_value = mock_query
        
        # Call the function
        ticker = 'AAPL'
        result_min, result_max = get_available_date_range(ticker)
        
        # Assertions
        assert result_min == min_date
        assert result_max == max_date
        
        # Verify filter call
        mock_filter.assert_called_once_with(ticker=ticker)
    
    @patch('core.backtester.get_data_feed')
    def test_run_backtest(self, mock_get_data_feed):
        """Test that run_backtest correctly orchestrates a backtest"""
        # Create a mock data feed
        mock_data_feed = MagicMock()
        mock_get_data_feed.return_value = mock_data_feed
        
        # Mock cerebro and its methods
        with patch('backtrader.Cerebro') as mock_cerebro_class:
            # Setup mock Cerebro instance
            mock_cerebro = MagicMock()
            mock_cerebro_class.return_value = mock_cerebro
            
            # Setup mock broker
            mock_broker = MagicMock()
            mock_cerebro.broker = mock_broker
            
            # First call should return initial value
            # Second call should return final value
            mock_broker.getvalue.side_effect = [100000.0, 100500.0]
            
            # Setup mock strategy instance with analyzers
            mock_strategy = MagicMock()
            mock_strategy.analyzers = MagicMock()
            
            # Mock analyzer results
            mock_trade_analyzer = MagicMock()
            mock_trade_analyzer.get_analysis.return_value = {'pnl': {'net': {'total': 500.0}}}
            
            mock_sqn_analyzer = MagicMock()
            mock_sqn_analyzer.get_analysis.return_value = {'sqn': 1.5}
            
            mock_drawdown_analyzer = MagicMock()
            mock_drawdown_analyzer.get_analysis.return_value = {'max': {'drawdown': 0.05}}
            
            mock_sharpe_analyzer = MagicMock()
            mock_sharpe_analyzer.get_analysis.return_value = {'sharperatio': 1.2}
            
            # Attach analyzers to strategy
            mock_strategy.analyzers.trade_analyzer = mock_trade_analyzer
            mock_strategy.analyzers.sqn = mock_sqn_analyzer
            mock_strategy.analyzers.drawdown = mock_drawdown_analyzer
            mock_strategy.analyzers.sharpe = mock_sharpe_analyzer
            
            # Mock cerebro.run() to return list with our mock strategy
            mock_cerebro.run.return_value = [mock_strategy]
            
            # Call the function
            ticker = 'AAPL'
            start_date = datetime(2023, 1, 1)
            end_date = datetime(2023, 4, 10)
            
            result = run_backtest(
                ticker, 
                start_date, 
                end_date,
                strategy_class=ClassicBreakoutStrategy,
                initial_cash=100000.0,
                commission=0.001
            )
        
        # Assertions
        assert result['success'] is True
        assert 'analyzers' in result
        assert 'trade_analyzer' in result['analyzers']
        assert 'sqn' in result['analyzers']
        assert 'drawdown' in result['analyzers']
        assert 'sharpe' in result['analyzers']
        assert result['start_value'] == 100000.0
        assert result['end_value'] == 100500.0
        
        # Verify data feed and cerebro configuration
        mock_get_data_feed.assert_called_once_with(ticker, start_date, end_date)
        mock_cerebro.adddata.assert_called_once_with(mock_data_feed)
        mock_cerebro.addstrategy.assert_called_once()
        mock_broker.setcash.assert_called_once_with(100000.0)
        mock_broker.setcommission.assert_called_once_with(commission=0.001)
        mock_cerebro.addanalyzer.call_count >= 4  # At least 4 analyzers added
        mock_cerebro.run.assert_called_once()
    
    @patch('core.backtester.get_data_feed')
    def test_run_backtest_no_data(self, mock_get_data_feed):
        """Test that run_backtest handles case with no data"""
        # Setup mock data feed (None indicates no data)
        mock_get_data_feed.return_value = None
        
        # Call the function
        result = run_backtest('NONEXISTENT')
        
        # Assertions
        assert result['success'] is False
        assert 'error' in result
        assert result['analyzers'] is None
