import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from datetime import datetime

from core.data_handler import (
    fetch_yfinance_data,
    fetch_alpha_vantage_data,
    fetch_stock_data,
    ALPHA_VANTAGE_AVAILABLE
)

class TestDataHandler(unittest.TestCase):
    
    def setUp(self):
        # Sample OHLCV data for testing
        self.sample_data = pd.DataFrame({
            'open': [100.0, 102.0, 104.0],
            'high': [105.0, 107.0, 108.0],
            'low': [98.0, 100.0, 101.0],
            'close': [103.0, 105.0, 106.0],
            'volume': [1000000, 1200000, 900000]
        }, index=pd.date_range(start='2023-01-01', periods=3))
        
        # Alpha Vantage returns data with different column names
        self.alpha_vantage_data = pd.DataFrame({
            '1. open': [100.0, 102.0, 104.0],
            '2. high': [105.0, 107.0, 108.0],
            '3. low': [98.0, 100.0, 101.0],
            '4. close': [103.0, 105.0, 106.0],
            '5. adjusted close': [103.0, 105.0, 106.0],
            '6. volume': [1000000, 1200000, 900000],
            '7. dividend amount': [0.0, 0.0, 0.0],
            '8. split coefficient': [1.0, 1.0, 1.0]
        }, index=pd.date_range(start='2023-01-01', periods=3, freq='D'))
    
    @patch('yfinance.download')
    def test_fetch_yfinance_data_success(self, mock_download):
        # Configure the mock to return sample data
        mock_download.return_value = self.sample_data
        
        # Call the function
        result = fetch_yfinance_data('AAPL', '2023-01-01', '2023-01-03')
        
        # Assert the mock was called correctly
        mock_download.assert_called_once_with('AAPL', start='2023-01-01', end='2023-01-03')
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertTrue('open' in result.columns)
        self.assertTrue('close' in result.columns)
        self.assertTrue('volume' in result.columns)
    
    @patch('yfinance.download')
    def test_fetch_yfinance_data_empty(self, mock_download):
        # Configure the mock to return empty DataFrame
        mock_download.return_value = pd.DataFrame()
        
        # Call the function
        result = fetch_yfinance_data('INVALID')
        
        # Verify result
        self.assertIsNone(result)
    
    @patch('yfinance.download')
    def test_fetch_yfinance_data_exception(self, mock_download):
        # Configure the mock to raise an exception
        mock_download.side_effect = Exception("API error")
        
        # Call the function
        result = fetch_yfinance_data('AAPL')
        
        # Verify result
        self.assertIsNone(result)

    # Only run Alpha Vantage tests if the package is available  
    @unittest.skipIf(not ALPHA_VANTAGE_AVAILABLE, "Alpha Vantage package not installed")
    @patch('core.data_handler.TimeSeries')
    def test_fetch_alpha_vantage_data_success(self, mock_timeseries):
        # Configure the mock
        mock_ts_instance = MagicMock()
        mock_ts_instance.get_daily_adjusted.return_value = (self.alpha_vantage_data, {})
        mock_timeseries.return_value = mock_ts_instance
        
        # Set environment variable for testing
        os.environ['ALPHA_VANTAGE_API_KEY'] = 'test_key'
        
        # Call the function
        result = fetch_alpha_vantage_data('AAPL')
        
        # Verify mock called correctly
        mock_timeseries.assert_called_once_with(key='test_key', output_format='pandas')
        mock_ts_instance.get_daily_adjusted.assert_called_once_with(symbol='AAPL', outputsize='full')
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertTrue('open' in result.columns)
        self.assertTrue('close' in result.columns)
        self.assertTrue('volume' in result.columns)
    
    @unittest.skipIf(not ALPHA_VANTAGE_AVAILABLE, "Alpha Vantage package not installed")
    @patch('core.data_handler.TimeSeries')
    def test_fetch_alpha_vantage_data_no_api_key(self, mock_timeseries):
        # Remove environment variable
        if 'ALPHA_VANTAGE_API_KEY' in os.environ:
            del os.environ['ALPHA_VANTAGE_API_KEY']
        
        # Call the function
        result = fetch_alpha_vantage_data('AAPL')
        
        # Verify mock not called
        mock_timeseries.assert_not_called()
        
        # Verify result
        self.assertIsNone(result)
    
    @unittest.skipIf(not ALPHA_VANTAGE_AVAILABLE, "Alpha Vantage package not installed")
    @patch('core.data_handler.TimeSeries')
    def test_fetch_alpha_vantage_data_exception(self, mock_timeseries):
        # Configure the mock to raise an exception
        mock_timeseries.side_effect = Exception("API error")
        
        # Set environment variable for testing
        os.environ['ALPHA_VANTAGE_API_KEY'] = 'test_key'
        
        # Call the function
        result = fetch_alpha_vantage_data('AAPL')
        
        # Verify result
        self.assertIsNone(result)
    
    @patch('core.data_handler.fetch_yfinance_data')
    @patch('core.data_handler.fetch_alpha_vantage_data')
    def test_fetch_stock_data_yfinance(self, mock_alpha, mock_yfinance):
        # Configure mocks
        mock_yfinance.return_value = self.sample_data
        
        # Call function with yfinance source
        result = fetch_stock_data('AAPL', source='yfinance', start_date='2023-01-01', end_date='2023-01-03')
        
        # Verify correct function called
        mock_yfinance.assert_called_once_with('AAPL', '2023-01-01', '2023-01-03')
        mock_alpha.assert_not_called()
        
        # Verify result
        self.assertIs(result, self.sample_data)
    
    @patch('core.data_handler.fetch_yfinance_data')
    @patch('core.data_handler.fetch_alpha_vantage_data')
    def test_fetch_stock_data_alpha_vantage(self, mock_alpha, mock_yfinance):
        # Configure mocks
        mock_alpha.return_value = self.alpha_vantage_data
        
        # Call function with alpha_vantage source
        result = fetch_stock_data('AAPL', source='alpha_vantage')
        
        # Verify correct function called
        mock_alpha.assert_called_once_with('AAPL')
        mock_yfinance.assert_not_called()
        
        # Verify result
        self.assertIs(result, self.alpha_vantage_data)
    
    @patch('core.data_handler.fetch_yfinance_data')
    @patch('core.data_handler.fetch_alpha_vantage_data')
    def test_fetch_stock_data_invalid_source(self, mock_alpha, mock_yfinance):
        # Call function with invalid source
        result = fetch_stock_data('AAPL', source='invalid')
        
        # Verify no fetching function called
        mock_yfinance.assert_not_called()
        mock_alpha.assert_not_called()
        
        # Verify result
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()