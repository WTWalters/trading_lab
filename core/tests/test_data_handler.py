# core/tests/test_data_handler.py
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from datetime import datetime
from decimal import Decimal
import pytest
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import pytz

# Import functions AND the model path for patching
from core.data_handler import (
    fetch_yfinance_data,
    fetch_alpha_vantage_data,
    fetch_stock_data,
    save_ohlcv_data,
    ALPHA_VANTAGE_AVAILABLE
)
# Check if models can be imported for conditional skipping
try:
    from dashboard.models import OHLCVData
    DJANGO_MODELS_AVAILABLE = True
except ImportError:
    DJANGO_MODELS_AVAILABLE = False


# --- Keep your existing TestDataHandler class for mocking tests ---
class TestDataHandler(unittest.TestCase):
    # ... (all your existing mock tests for fetch functions) ...
    @patch('yfinance.download')
    def test_fetch_yfinance_data_success(self, mock_download):
        # Sample data setup
        self.sample_data = pd.DataFrame({
            'Open': [100.0], 'High': [105.0], 'Low': [98.0], 'Close': [103.0], 'Volume': [1000000], 'Adj Close': [103.0]
        }, index=pd.to_datetime(['2023-01-01']))
        mock_download.return_value = self.sample_data
        result = fetch_yfinance_data('AAPL', '2023-01-01', '2023-01-03')
        mock_download.assert_called_once_with('AAPL', start='2023-01-01', end='2023-01-03', progress=False) # Added progress=False
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertTrue('open' in result.columns) # Check lowercase
    # ... (other mock tests) ...
    pass


# --- Class for database tests ---
@pytest.mark.django_db
class TestDataHandlerDatabase(unittest.TestCase):
    """Tests for data saving logic interacting with the database."""

    def setUp(self):
        pass # pytest-django handles test DB setup/teardown

    def _create_sample_df(self, start_date_str, periods, freq='D', tz_info=pytz.UTC):
        """Helper to create a sample DataFrame."""
        start_date = pd.Timestamp(start_date_str, tz=tz_info)
        dates = pd.date_range(start=start_date, periods=periods, freq=freq)
        data = {
            'open': [100.0 + i for i in range(periods)],
            'high': [105.0 + i for i in range(periods)],
            'low': [98.0 + i for i in range(periods)],
            'close': [103.0 + i for i in range(periods)],
            'volume': [1000000 + (i*10000) for i in range(periods)]
        }
        return pd.DataFrame(data, index=dates)

    def test_save_ohlcv_data_new(self):
        """Test saving new records from a DataFrame."""
        if not DJANGO_MODELS_AVAILABLE: self.skipTest("Models not available")
        ticker = "SAVE_TEST"
        df = self._create_sample_df('2024-01-01', 5)
        initial_count = OHLCVData.objects.filter(ticker=ticker).count()
        self.assertEqual(initial_count, 0)
        save_ohlcv_data(df, ticker)
        final_count = OHLCVData.objects.filter(ticker=ticker).count()
        self.assertEqual(final_count, 5)
        first_ts = df.index[0].to_pydatetime()
        record = OHLCVData.objects.get(ticker=ticker, timestamp=first_ts)
        self.assertEqual(record.open, Decimal("100.0"))

    def test_save_ohlcv_data_duplicates_ignored(self):
        """Test that duplicate records are ignored on save."""
        if not DJANGO_MODELS_AVAILABLE: self.skipTest("Models not available")
        ticker = "DUPE_TEST"
        df1 = self._create_sample_df('2024-02-01', 3)
        save_ohlcv_data(df1, ticker)
        self.assertEqual(OHLCVData.objects.filter(ticker=ticker).count(), 3)
        df2 = self._create_sample_df('2024-02-02', 4)
        save_ohlcv_data(df2, ticker)
        self.assertEqual(OHLCVData.objects.filter(ticker=ticker).count(), 5)
        record_day2 = OHLCVData.objects.get(ticker=ticker, timestamp=pd.Timestamp('2024-02-02', tz='UTC'))
        # Use .iloc[0] if timestamp string doesn't exactly match index after conversion
        self.assertEqual(record_day2.open, Decimal(df1.loc[df1.index[1]]['open'])) # Check open for day 2 of df1 (index 1)

    def test_save_ohlcv_data_nan_values(self):
        """Test that rows with NaN values are skipped."""
        if not DJANGO_MODELS_AVAILABLE: self.skipTest("Models not available")
        ticker = "NAN_TEST"
        df = self._create_sample_df('2024-03-01', 3)
        df.loc[df.index[1], 'open'] = pd.NA
        save_ohlcv_data(df, ticker)
        self.assertEqual(OHLCVData.objects.filter(ticker=ticker).count(), 2)

    def test_save_ohlcv_data_empty_input(self):
        """Test saving with empty or None DataFrame."""
        if not DJANGO_MODELS_AVAILABLE: self.skipTest("Models not available")
        ticker = "EMPTY_TEST"
        empty_df = pd.DataFrame()
        none_df = None
        count_before = OHLCVData.objects.count()
        num_saved_empty = save_ohlcv_data(empty_df, ticker)
        num_saved_none = save_ohlcv_data(none_df, ticker)
        count_after = OHLCVData.objects.count()
        self.assertEqual(num_saved_empty, 0)
        self.assertEqual(num_saved_none, 0)
        self.assertEqual(count_before, count_after)

    # --- Corrected Patch Target ---
    @patch('dashboard.models.OHLCVData.objects.bulk_create')
    def test_save_ohlcv_data_generic_exception(self, mock_bulk_create):
        """Test handling of unexpected exceptions during save."""
        if not DJANGO_MODELS_AVAILABLE: self.skipTest("Models not available")

        ticker = "EXC_TEST"
        df = self._create_sample_df('2024-04-01', 2)
        simulated_error_message = "Simulated DB error"
        mock_bulk_create.side_effect = Exception(simulated_error_message)

        # Assert that calling the function raises the expected exception
        with pytest.raises(Exception, match=simulated_error_message) as excinfo:
             save_ohlcv_data(df, ticker)

        # Check exception type if needed (optional as raises checks type)
        # assert isinstance(excinfo.value, Exception)
        mock_bulk_create.assert_called_once()

    # Test for invalid source in fetch_stock_data
    def test_fetch_stock_data_invalid_source_direct(self):
        """Test fetch_stock_data with an invalid source string."""
        ticker="INVALID_SRC_TEST"
        result = fetch_stock_data(ticker, source='bad_source')
        self.assertIsNone(result)
