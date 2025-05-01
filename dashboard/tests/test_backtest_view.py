# dashboard/tests/test_backtest_view.py
import pytest
from django.urls import reverse
from django.test import Client
from django.utils import timezone
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, ANY # Import ANY
import pytz

# Import models and functions for mocking
from dashboard.models import OHLCVData
# Note: We patch run_backtest where it's *used* in the view

@pytest.mark.django_db
class TestBacktestView:
    """Tests for the backtest view"""

    def setup_method(self):
        """Set up the test client and other test variables"""
        self.client = Client()
        self.url = reverse('dashboard:backtest_view')
        # Create a dummy ticker for tests that need one
        OHLCVData.objects.create(
            ticker='AAPL', timestamp=timezone.now().replace(tzinfo=pytz.UTC),
            open=1, high=1, low=1, close=1, volume=1
        )


    @patch('dashboard.views.OHLCVData.objects.values_list')
    def test_get_backtest_view(self, mock_values_list):
        """Test that the backtest view loads correctly"""
        mock_values_list.return_value.distinct.return_value = ['AAPL', 'MSFT', 'GOOG']
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert 'available_tickers' in response.context
        assert 'default_params' in response.context
        assert 'dashboard/backtest_view.html' in [t.name for t in response.templates]
        assert 'metrics' not in response.context

    # Patch run_backtest where it's imported in views.py
    @patch('dashboard.views.run_backtest')
    @patch('dashboard.views.get_available_date_range') # Mock this too if needed
    @patch('dashboard.views.OHLCVData.objects.values_list')
    def test_post_backtest_view_success_and_metrics(self, mock_values_list, mock_get_range, mock_run_backtest):
        """
        Test successful POST request and verify metric extraction.
        """
        # Mock the available tickers
        mock_values_list.return_value.distinct.return_value = ['AAPL', 'MSFT', 'GOOG']
        mock_get_range.return_value = (timezone.now() - timedelta(days=365), timezone.now())

        # --- Detailed Mock Analyzer Results ---
        mock_trade_analyzer_results = MagicMock()
        # Simulate structure for TradeAnalyzer results
        mock_trade_analyzer_results.total.closed = 10 # Total closed trades
        mock_trade_analyzer_results.won.total = 7 # Winning trades
        mock_trade_analyzer_results.pnl.net.total = 1500.75 # Total Net P/L
        mock_trade_analyzer_results.drawdown.max.drawdown = 0.155 # Max Drawdown as decimal

        mock_sqn_analyzer_results = MagicMock()
        mock_sqn_analyzer_results.sqn = 2.1 # System Quality Number

        mock_analyzer_dict = {
            'trade_analyzer': mock_trade_analyzer_results,
            'sqn': mock_sqn_analyzer_results
        }
        # --------------------------------------

        mock_results = {
            'success': True,
            'analyzers': mock_analyzer_dict, # Use detailed mock
            'error': None,
            'start_value': 100000.0,
            'end_value': 101500.75 # Matches Pnl Net Total for simplicity
        }
        mock_run_backtest.return_value = mock_results

        # Create POST data
        start_date_str = (timezone.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        end_date_str = timezone.now().strftime('%Y-%m-%d')
        post_data = {
            'ticker': 'AAPL', 'start_date': start_date_str, 'end_date': end_date_str,
            'initial_cash': '100000', 'commission': '0.001', 'lookback': '50',
            'volume_ma_period': '20', 'volume_mult': '1.5', 'atr_period': '14',
            'initial_stop_atr_mult': '2.0', 'trail_stop_atr_mult': '3.0'
        }

        # Make POST request (mock plotly plot)
        with patch('dashboard.views.plot', return_value='<div>Mock Chart</div>') as mock_plotly_plot:
            response = self.client.post(self.url, post_data)

        # --- Assertions ---
        assert response.status_code == 200
        assert 'backtest_params' in response.context
        assert 'metrics' in response.context # Check metrics dict exists
        assert 'equity_chart_div' in response.context # Check chart exists

        # --- Verify specific metric values in context ---
        metrics = response.context['metrics']
        assert metrics['total_trades'] == 10
        assert metrics['winning_trades'] == 7
        assert metrics['win_rate'] == pytest.approx(70.0) # 7 / 10 * 100
        assert metrics['pnl_net'] == pytest.approx(1500.75)
        assert metrics['max_drawdown'] == pytest.approx(15.5) # Converted to percentage
        assert metrics['sqn'] == pytest.approx(2.1)
        assert metrics['initial_capital'] == pytest.approx(100000.0)
        assert metrics['final_capital'] == pytest.approx(101500.75)
        assert metrics['total_return'] == pytest.approx(1.50075) # (101500.75 - 100000) / 100000 * 100
        # --------------------------------------------------

        # Check run_backtest call
        mock_run_backtest.assert_called_once()
        args, kwargs = mock_run_backtest.call_args
        # First argument should be the ticker
        assert args[0] == 'AAPL'
        # Check for initial_cash in kwargs
        assert kwargs['initial_cash'] == 100000.0

    @patch('dashboard.views.run_backtest')
    @patch('dashboard.views.OHLCVData.objects.values_list')
    def test_post_backtest_view_run_fail(self, mock_values_list, mock_run_backtest):
        """Test that the backtest view handles errors from run_backtest"""
        mock_values_list.return_value.distinct.return_value = ['AAPL']
        error_msg = 'Simulated backtest failure'
        mock_run_backtest.return_value = {'success': False, 'error': error_msg}
        start_date_str = (timezone.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        end_date_str = timezone.now().strftime('%Y-%m-%d')
        post_data = {'ticker': 'AAPL', 'start_date': start_date_str, 'end_date': end_date_str}
        response = self.client.post(self.url, post_data)
        assert response.status_code == 200
        assert 'error_message' in response.context
        assert response.context['error_message'] == error_msg
        assert 'metrics' not in response.context
        
    @patch('dashboard.views.run_backtest')
    @patch('dashboard.views.OHLCVData.objects.values_list')
    def test_missing_metrics_handled_gracefully(self, mock_values_list, mock_run_backtest):
        """Test that the view handles missing metrics gracefully"""
        mock_values_list.return_value.distinct.return_value = ['AAPL']
        
        # Create a successful result but with empty/missing analyzer data
        mock_results = {
            'success': True,
            'analyzers': {}, # Empty analyzer dict
            'start_value': 100000.0,
            'end_value': 100000.0
        }
        mock_run_backtest.return_value = mock_results
        
        post_data = {
            'ticker': 'AAPL',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        }
        
        with patch('dashboard.views.plot', return_value='<div>Mock Chart</div>'):
            response = self.client.post(self.url, post_data)
        
        # Check that metrics exist with default values
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
