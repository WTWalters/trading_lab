"""
Unit tests for the market_data module.
"""

import unittest
from unittest.mock import patch, MagicMock
from core.market_data import (
    get_alpaca_data_client, 
    get_alpaca_trading_client,
    get_latest_quote,
    is_tradable
)

class TestMarketData(unittest.TestCase):
    """Test case for the market_data module functions."""
    
    @patch('core.market_data.StockHistoricalDataClient')
    @patch('core.market_data.ALPACA_API_KEY', 'test-api-key')
    @patch('core.market_data.ALPACA_SECRET_KEY', 'test-secret-key')
    def test_get_alpaca_data_client_success(self, mock_client):
        """Test successful creation of Alpaca data client."""
        # Setup mock
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        
        # Call function
        client = get_alpaca_data_client()
        
        # Assert
        self.assertEqual(client, mock_client_instance)
        mock_client.assert_called_once_with(
            api_key='test-api-key',
            secret_key='test-secret-key'
        )
    
    @patch('core.market_data.StockHistoricalDataClient')
    @patch('core.market_data.ALPACA_API_KEY', 'test-api-key')
    @patch('core.market_data.ALPACA_SECRET_KEY', 'test-secret-key')
    def test_get_alpaca_data_client_exception(self, mock_client):
        """Test handling of exception when creating Alpaca data client."""
        # Setup mock to raise exception
        mock_client.side_effect = Exception("Test error")
        
        # Call function
        client = get_alpaca_data_client()
        
        # Assert
        self.assertIsNone(client)
    
    @patch('core.market_data.TradingClient')
    @patch('core.market_data.ALPACA_API_KEY', 'test-api-key')
    @patch('core.market_data.ALPACA_SECRET_KEY', 'test-secret-key')
    def test_get_alpaca_trading_client_success(self, mock_client):
        """Test successful creation of Alpaca trading client."""
        # Setup mock
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        
        # Call function
        client = get_alpaca_trading_client()
        
        # Assert
        self.assertEqual(client, mock_client_instance)
        mock_client.assert_called_once_with(
            api_key='test-api-key',
            secret_key='test-secret-key',
            paper=True
        )
    
    @patch('core.market_data.get_alpaca_data_client')
    def test_get_latest_quote_success(self, mock_get_client):
        """Test successfully getting latest quote."""
        # Setup mocks
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_quote = MagicMock()
        mock_quote.bid_price = 150.25
        mock_quote.bid_size = 100
        mock_quote.ask_price = 150.50
        mock_quote.ask_size = 200
        mock_quote.timestamp = "2023-05-01T10:30:00Z"
        
        mock_client.get_stock_latest_quote.return_value = {
            'AAPL': mock_quote
        }
        
        # Call function
        result = get_latest_quote('AAPL')
        
        # Assert
        self.assertEqual(result['ticker'], 'AAPL')
        self.assertEqual(result['bid_price'], 150.25)
        self.assertEqual(result['ask_price'], 150.50)
        self.assertEqual(result['status'], 'success')
        
        # Check that the request was called with correct parameters
        request_call_args = mock_client.get_stock_latest_quote.call_args[0][0]
        self.assertEqual(request_call_args.symbol_or_symbols, ['AAPL'])
    
    @patch('core.market_data.get_alpaca_data_client')
    def test_get_latest_quote_ticker_not_found(self, mock_get_client):
        """Test handling of ticker not found in response."""
        # Setup mocks
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Empty response for non-existent ticker
        mock_client.get_stock_latest_quote.return_value = {}
        
        # Call function
        result = get_latest_quote('NONEXISTENT')
        
        # Assert
        self.assertIsNone(result)
    
    @patch('core.market_data.get_alpaca_data_client')
    def test_get_latest_quote_exception(self, mock_get_client):
        """Test handling of exception when getting quote."""
        # Setup mocks
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Simulate an API error
        mock_client.get_stock_latest_quote.side_effect = Exception("API Error")
        
        # Call function
        result = get_latest_quote('AAPL')
        
        # Assert
        self.assertEqual(result['ticker'], 'AAPL')
        self.assertEqual(result['status'], 'error')
        self.assertIn('error_message', result)
    
    @patch('core.market_data.get_alpaca_trading_client')
    def test_is_tradable_success(self, mock_get_client):
        """Test successfully checking if ticker is tradable."""
        # Setup mocks
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Create mock assets
        mock_asset1 = MagicMock()
        mock_asset1.symbol = 'AAPL'
        mock_asset1.tradable = True
        
        mock_asset2 = MagicMock()
        mock_asset2.symbol = 'MSFT'
        mock_asset2.tradable = True
        
        mock_client.get_all_assets.return_value = [mock_asset1, mock_asset2]
        
        # Call function
        result = is_tradable('AAPL')
        
        # Assert
        self.assertTrue(result)
    
    @patch('core.market_data.get_alpaca_trading_client')
    def test_is_tradable_not_found(self, mock_get_client):
        """Test handling of ticker not found in assets."""
        # Setup mocks
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Create mock assets without the requested ticker
        mock_asset = MagicMock()
        mock_asset.symbol = 'MSFT'
        mock_asset.tradable = True
        
        mock_client.get_all_assets.return_value = [mock_asset]
        
        # Call function
        result = is_tradable('AAPL')
        
        # Assert
        self.assertFalse(result)
    
    @patch('core.market_data.get_alpaca_trading_client')
    def test_is_tradable_exception(self, mock_get_client):
        """Test handling of exception when checking tradability."""
        # Setup mocks
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Simulate an API error
        mock_client.get_all_assets.side_effect = Exception("API Error")
        
        # Call function
        result = is_tradable('AAPL')
        
        # Assert
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
