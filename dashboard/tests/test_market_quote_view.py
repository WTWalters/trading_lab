#dashboard/tests/test_market_quote_view.py
"""
Tests for the market quote view functionality.
"""

from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch
import json

from dashboard.views import market_quote_view


class MarketQuoteViewTests(TestCase):
    """Test case for the market quote functionality."""

    def setUp(self):
        """Set up test environment."""
        self.factory = RequestFactory()

    @patch('dashboard.views.get_latest_quote')
    @patch('dashboard.views.is_tradable')
    def test_market_quote_view_get(self, mock_is_tradable, mock_get_latest_quote):
        """Test the market quote view with GET request."""
        # Setup mocks
        mock_quote_data = {
            'ticker': 'AAPL',
            'bid_price': 150.25,
            'bid_size': 100,
            'ask_price': 150.50,
            'ask_size': 200,
            'timestamp': '2023-05-01T12:34:56Z',
            'status': 'success'
        }
        mock_get_latest_quote.return_value = mock_quote_data
        mock_is_tradable.return_value = True

        # Create GET request with ticker parameter
        url = f"{reverse('dashboard:market_quote')}?ticker=AAPL"
        response = self.client.get(url)

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/market_quote.html')
        self.assertEqual(response.context['quote_data'], mock_quote_data)
        self.assertTrue(response.context['tradable'])

        # Check that the mocks were called correctly
        mock_get_latest_quote.assert_called_once_with('AAPL')
        mock_is_tradable.assert_called_once_with('AAPL')

    @patch('dashboard.views.get_latest_quote')
    @patch('dashboard.views.is_tradable')
    def test_market_quote_view_ajax(self, mock_is_tradable, mock_get_latest_quote):
        """Test the market quote view with AJAX request."""
        # Setup mocks
        mock_quote_data = {
            'ticker': 'AAPL',
            'bid_price': 150.25,
            'bid_size': 100,
            'ask_price': 150.50,
            'ask_size': 200,
            'timestamp': '2023-05-01T12:34:56Z',
            'status': 'success'
        }
        mock_get_latest_quote.return_value = mock_quote_data
        mock_is_tradable.return_value = True

        # Create AJAX GET request
        url = f"{reverse('dashboard:market_quote')}?ticker=AAPL&refresh=true"
        response = self.client.get(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'  # This makes it an AJAX request
        )

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Parse JSON response
        data = json.loads(response.content)
        self.assertEqual(data['ticker'], mock_quote_data['ticker'])
        self.assertEqual(data['bid_price'], mock_quote_data['bid_price'])
        self.assertEqual(data['status'], mock_quote_data['status'])
        self.assertEqual(data['tradable'], True)

        # Check that the mocks were called correctly
        mock_get_latest_quote.assert_called_once_with('AAPL')
        mock_is_tradable.assert_called_once_with('AAPL')

    @patch('dashboard.views.get_latest_quote')
    def test_market_quote_view_ajax_no_data(self, mock_get_latest_quote):
        """Test the market quote view with AJAX request when no data is found."""
        # Setup mock to return None (no data found)
        mock_get_latest_quote.return_value = None

        # Create AJAX GET request
        url = f"{reverse('dashboard:market_quote')}?ticker=NONEXISTENT&refresh=true"
        response = self.client.get(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Parse JSON response
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertIn('error_message', data)
        self.assertIn('NONEXISTENT', data['error_message'])

        # Check that the mock was called correctly
        mock_get_latest_quote.assert_called_once_with('NONEXISTENT')

    def test_market_quote_view_no_ticker(self):
        """Test the market quote view without a ticker parameter."""
        # Create GET request without ticker
        url = reverse('dashboard:market_quote')
        response = self.client.get(url)

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/market_quote.html')
        self.assertNotIn('quote_data', response.context)
