# dashboard/tests/test_story8.py
import pytest
from django.urls import reverse
from django.test import Client
from django.utils import timezone
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, ANY
import pytz
import json

from dashboard.models import OHLCVData
from core.strategies import ClassicBreakoutStrategy

@pytest.mark.django_db
class TestStory8Requirements:
    """
    Tests for verifying that the backtest_view meets the requirements of Story 8:
    "Display Backtest Results" - extracting and showing key performance metrics
    """

    def setup_method(self):
        """Set up the test client and other test variables"""
        self.client = Client()
        self.url = reverse('dashboard:backtest_view')
        
        # Create a test ticker
        now = timezone.now()
        for i in range(30):  # 30 days of data
            OHLCVData.objects.create(
                ticker='AAPL',
                timestamp=now - timedelta(days=i),
                open=150.0 + i,
                high=155.0 + i,
                low=145.0 + i,
                close=152.0 + i,
                volume=1000000 + i * 10000
            )

    @patch('dashboard.views.run_backtest')
    def test_all_story8_acceptance_criteria(self, mock_run_backtest):
        """
        Test that all acceptance criteria for Story 8 are met:
        1. View retrieves analysis results from run_backtest
        2. Extracts Total Net P&L from TradeAnalyzer
        3. Calculates Win Rate from TradeAnalyzer
        4. Extracts Maximum Drawdown from TradeAnalyzer
        5. Extracts SQN from SQN analyzer
        6. These metrics are passed to the template context
        7. Template displays metrics in a clear, readable format
        8. Template handles case where results aren't available
        """
        # Set up a complete mock backtest result
        mock_analyzer = {
            'trade_analyzer': {
                'total': {'closed': 15},
                'won': {'total': 9},
                'pnl': {'net': {'total': 2500.75}},
                'drawdown': {'max': {'drawdown': 0.12}}  # 12% drawdown
            },
            'sqn': {'sqn': 1.85}
        }
        
        mock_results = {
            'success': True,
            'analyzers': mock_analyzer,
            'start_value': 100000.0,
            'end_value': 102500.75
        }
        mock_run_backtest.return_value = mock_results

        # Create POST data
        post_data = {
            'ticker': 'AAPL',
            'start_date': (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': timezone.now().strftime('%Y-%m-%d'),
            'initial_cash': '100000',
            'commission': '0.001'
        }

        # Make POST request with plotly plot mocked
        with patch('dashboard.views.plot', return_value='<div>Mock Chart</div>') as mock_plot:
            response = self.client.post(self.url, post_data)

        # Check response
        assert response.status_code == 200
        
        # 1. Verify the view retrieved the analysis results
        mock_run_backtest.assert_called_once()
        assert 'metrics' in response.context
        
        # 2-5. Verify the view correctly extracted all required metrics
        metrics = response.context['metrics']
        assert metrics['pnl_net'] == 2500.75  # Criterion 2: Total P&L
        assert metrics['win_rate'] == 60.0    # Criterion 3: Win Rate (9/15 * 100)
        assert metrics['max_drawdown'] == 12.0  # Criterion 4: Max Drawdown (as percentage)
        assert metrics['sqn'] == 1.85         # Criterion 5: SQN
        
        # 6. Verify that metrics are passed to the template context
        assert 'metrics' in response.context
        assert 'backtest_params' in response.context
        
        # 7. We can't directly check HTML rendering, but we can check that 
        # the template with the metrics table was used
        templates_used = [t.name for t in response.templates]
        assert 'dashboard/backtest_view.html' in templates_used
        
        # 8. Check that template handles case where results aren't available
        # by testing a GET request (no results yet)
        response_get = self.client.get(self.url)
        assert response_get.status_code == 200
        assert 'metrics' not in response_get.context
    
    @patch('dashboard.views.run_backtest')
    def test_handles_error_condition(self, mock_run_backtest):
        """Test that the view correctly handles errors or failed backtests"""
        # Mock a failed backtest
        mock_run_backtest.return_value = {
            'success': False,
            'error': 'No data available for ticker in specified date range',
            'analyzers': None
        }
        
        # Create POST data
        post_data = {
            'ticker': 'NONEXISTENT',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        }
        
        # Make POST request
        response = self.client.post(self.url, post_data)
        
        # Check that error message is displayed and no metrics are in context
        assert response.status_code == 200
        assert 'error_message' in response.context
        assert 'metrics' not in response.context
    
    @patch('dashboard.views.run_backtest')
    def test_handles_empty_analyzers(self, mock_run_backtest):
        """Test that the view gracefully handles missing or empty analyzers"""
        # Mock a successful backtest but with empty analyzers
        mock_run_backtest.return_value = {
            'success': True,
            'analyzers': {},  # Empty analyzers dict
            'start_value': 100000.0,
            'end_value': 100000.0
        }
        
        # Create POST data
        post_data = {
            'ticker': 'AAPL',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        }
        
        # Make POST request with plotly plot mocked
        with patch('dashboard.views.plot', return_value='<div>Mock Chart</div>'):
            response = self.client.post(self.url, post_data)
        
        # Check that metrics have default values and no errors occur
        assert response.status_code == 200
        assert 'metrics' in response.context
        metrics = response.context['metrics']
        
        # All trade-related metrics should have default values
        assert metrics['total_trades'] == 0
        assert metrics['winning_trades'] == 0
        assert metrics['win_rate'] == 0.0
        assert metrics['pnl_net'] == 0.0
        assert metrics['max_drawdown'] == 0.0
        assert metrics['sqn'] is None
