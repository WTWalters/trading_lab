#dashboard/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import pandas as pd
import json
from dashboard.models import OHLCVData
from unittest.mock import patch, MagicMock

class ChartViewTests(TestCase):
    """Test cases for the chart_view function"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.ticker = 'AAPL'

        # Create test OHLCV data
        now = timezone.now()
        for i in range(60):  # Create 60 days of data
            OHLCVData.objects.create(
                ticker=self.ticker,
                timestamp=now - timedelta(days=i),
                open=Decimal('150.00') + i,
                high=Decimal('155.00') + i,
                low=Decimal('145.00') + i,
                close=Decimal('152.00') + i,
                volume=1000000 + i * 10000
            )

    @patch('dashboard.views.plot')
    def test_chart_view_with_ticker(self, mock_plot):
        """Test chart_view with a valid ticker"""
        # Mock the plotly plot function to return a div
        mock_plot.return_value = '<div id="test-plot"></div>'

        # Make the request
        url = reverse('dashboard:chart_view', args=[self.ticker])
        response = self.client.get(url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/chart_view.html')
        self.assertEqual(response.context['ticker'], self.ticker)
        self.assertIn('chart_div', response.context)
        self.assertEqual(response.context['chart_div'], '<div id="test-plot"></div>')
        self.assertIn('chart_indices', response.context)

        # Verify chart_indices contains the expected trace indices
        chart_indices = json.loads(response.context['chart_indices'])
        self.assertIn('sma10Index', chart_indices)
        self.assertIn('sma20Index', chart_indices)
        self.assertIn('sma50Index', chart_indices)
        self.assertIn('ema10Index', chart_indices)
        self.assertIn('ema20Index', chart_indices)
        self.assertIn('ema50Index', chart_indices)
        self.assertIn('volumeIndex', chart_indices)

    @patch('dashboard.views.plot')
    def test_chart_view_with_date_range(self, mock_plot):
        """Test chart_view with specific date range"""
        # Mock the plotly plot function to return a div
        mock_plot.return_value = '<div id="test-plot"></div>'

        # Setup dates
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        # Make the request
        url = reverse('dashboard:chart_view', args=[self.ticker])
        response = self.client.get(
            url,
            {'start_date': start_date.strftime('%Y-%m-%d'),
             'end_date': end_date.strftime('%Y-%m-%d')}
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ticker'], self.ticker)
        # Compare date strings (response.context now contains strings instead of datetime objects)
        self.assertEqual(response.context['start_date'],
                        start_date.strftime('%Y-%m-%d'))
        self.assertEqual(response.context['end_date'],
                        end_date.strftime('%Y-%m-%d'))
        self.assertIn('chart_div', response.context)

    def test_chart_view_with_no_data(self):
        """Test chart_view with a ticker that has no data"""
        url = reverse('dashboard:chart_view', args=['NONEXISTENT'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ticker'], 'NONEXISTENT')
        self.assertIn('error_message', response.context)
        self.assertNotIn('chart_div', response.context)

    def test_chart_view_no_ticker_provided(self):
        """Test chart_view with no ticker provided"""
        url = reverse('dashboard:chart_view_default')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ticker'], '')
        self.assertNotIn('chart_div', response.context)

    @patch('dashboard.views.OHLCVData.objects.filter')
    def test_chart_view_handles_exceptions(self, mock_filter):
        """Test chart_view handles exceptions"""
        # Set up the mock to raise an exception
        mock_filter.side_effect = Exception("Test exception")

        url = reverse('dashboard:chart_view', args=[self.ticker])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ticker'], self.ticker)
        self.assertIn('error_message', response.context)
        self.assertIn('Test exception', response.context['error_message'])
        self.assertNotIn('chart_div', response.context)
