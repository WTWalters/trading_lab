# dashboard/tests/test_backtest_metrics.py
import pytest
from django.urls import reverse
from django.test import Client
from django.utils import timezone
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, ANY
import pytz

from dashboard.models import OHLCVData

@pytest.mark.django_db
class TestBacktestMetricsExtraction:
    """Tests specifically for the metrics extraction logic in the backtest view"""

    def setup_method(self):
        """Set up the test client and other test variables"""
        self.client = Client()
        self.url = reverse('dashboard:backtest_view')
        # Create a dummy ticker for tests that need one
        OHLCVData.objects.create(
            ticker='AAPL', timestamp=timezone.now().replace(tzinfo=pytz.UTC),
            open=1, high=1, low=1, close=1, volume=1
        )

    @patch('dashboard.views.run_backtest')
    @patch('dashboard.views.get_available_date_range')
    @patch('dashboard.views.OHLCVData.objects.values_list')
    def test_metrics_extraction_full_data(self, mock_values_list, mock_get_range, mock_run_backtest):
        """Test that all metrics are correctly extracted when all analyzer data is present"""
        # Mock the available tickers
        mock_values_list.return_value.distinct.return_value = ['AAPL']
        mock_get_range.return_value = (timezone.now() - timedelta(days=365), timezone.now())

        # Create a complete mock backtest result with all analyzers and metrics
        # This simulates what run_backtest would return with complete data
        mock_trade_analyzer = {
            'total': {'closed': 10},
            'won': {'total': 6},
            'pnl': {'net': {'total': 1200.50}},
            'drawdown': {'max': {'drawdown': 0.15}}  # 15% as decimal
        }
        
        mock_sqn_analyzer = {'sqn': 2.35}
        mock_sharpe_analyzer = {'sharperatio': 1.25}
        
        mock_results = {
            'success': True,
            'analyzers': {
                'trade_analyzer': mock_trade_analyzer,
                'sqn': mock_sqn_analyzer,
                'sharpe': mock_sharpe_analyzer
            },
            'start_value': 100000.0,
            'end_value': 101200.50
        }
        mock_run_backtest.return_value = mock_results

        # Create POST data
        post_data = {
            'ticker': 'AAPL',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'initial_cash': '100000',
            'commission': '0.001',
            'lookback': '50'
        }

        # Make POST request with plotly plot mocked
        with patch('dashboard.views.plot', return_value='<div>Mock Chart</div>'):
            response = self.client.post(self.url, post_data)

        # Check response status
        assert response.status_code == 200
        
        # Verify metrics were extracted and calculated correctly
        metrics = response.context['metrics']
        
        # Check portfolio metrics
        assert metrics['initial_capital'] == 100000.0
        assert metrics['final_capital'] == 101200.50
        assert pytest.approx(metrics['total_return']) == 1.2005
        
        # Check trade metrics
        assert metrics['total_trades'] == 10
        assert metrics['winning_trades'] == 6
        assert metrics['win_rate'] == 60.0  # Should be calculated as percentage
        assert metrics['pnl_net'] == 1200.50
        
        # Check risk metrics
        assert metrics['max_drawdown'] == 15.0  # Should be converted to percentage
        assert metrics['sqn'] == 2.35
        assert metrics['sharpe_ratio'] == 1.25

    @patch('dashboard.views.run_backtest')
    @patch('dashboard.views.OHLCVData.objects.values_list')
    def test_metrics_extraction_partial_data(self, mock_values_list, mock_run_backtest):
        """Test metrics extraction with partial or missing analyzer data"""
        mock_values_list.return_value.distinct.return_value = ['AAPL']
        
        # Create a partial mock result with some missing data
        mock_results = {
            'success': True,
            'analyzers': {
                'trade_analyzer': {
                    'total': {'closed': 5},
                    'won': {'total': 2}
                    # pnl and drawdown missing
                },
                'sqn': {}  # empty sqn analyzer, no sqn value
                # sharpe analyzer completely missing
            },
            'start_value': 100000.0,
            'end_value': 99000.0
        }
        mock_run_backtest.return_value = mock_results

        # Create POST data
        post_data = {
            'ticker': 'AAPL',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        }

        # Make POST request with plotly plot mocked
        with patch('dashboard.views.plot', return_value='<div>Mock Chart</div>'):
            response = self.client.post(self.url, post_data)

        # Check response status
        assert response.status_code == 200
        
        # Verify metrics were extracted with proper defaults for missing data
        metrics = response.context['metrics']
        
        # Check portfolio metrics
        assert metrics['initial_capital'] == 100000.0
        assert metrics['final_capital'] == 99000.0
        assert pytest.approx(metrics['total_return']) == -1.0  # should be negative
        
        # Check trade metrics
        assert metrics['total_trades'] == 5
        assert metrics['winning_trades'] == 2
        assert metrics['win_rate'] == 40.0  # Should be calculated as percentage
        assert metrics['pnl_net'] == 0.0  # Default when pnl data is missing
        
        # Check risk metrics
        assert metrics['max_drawdown'] == 0.0  # Default when drawdown is missing
        assert metrics['sqn'] is None  # Should be None when sqn data is missing
        assert metrics['sharpe_ratio'] is None  # Should be None when sharpe is missing

    @patch('dashboard.views.run_backtest')
    @patch('dashboard.views.OHLCVData.objects.values_list')
    def test_metrics_extraction_no_trades(self, mock_values_list, mock_run_backtest):
        """Test metrics extraction when no trades were executed during backtest"""
        mock_values_list.return_value.distinct.return_value = ['AAPL']
        
        # Create a mock result with zero trades
        mock_results = {
            'success': True,
            'analyzers': {
                'trade_analyzer': {
                    'total': {'closed': 0}
                    # No other trade data since no trades
                },
                'sqn': {'sqn': 0.0}  # SQN would be 0 with no trades
            },
            'start_value': 100000.0,
            'end_value': 100000.0  # No change in value
        }
        mock_run_backtest.return_value = mock_results

        # Create POST data
        post_data = {
            'ticker': 'AAPL',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        }

        # Make POST request with plotly plot mocked
        with patch('dashboard.views.plot', return_value='<div>Mock Chart</div>'):
            response = self.client.post(self.url, post_data)

        # Check response status
        assert response.status_code == 200
        
        # Verify metrics were extracted with proper handling for zero trades
        metrics = response.context['metrics']
        
        # Check portfolio metrics
        assert metrics['initial_capital'] == 100000.0
        assert metrics['final_capital'] == 100000.0
        assert metrics['total_return'] == 0.0  # No change
        
        # Check trade metrics
        assert metrics['total_trades'] == 0
        assert metrics['winning_trades'] == 0
        assert metrics['win_rate'] == 0.0  # Should handle division by zero
        
        # Other metrics should have default values
        assert metrics['sqn'] == 0.0  # SQN value from analyzer
