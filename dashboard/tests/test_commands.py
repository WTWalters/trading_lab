# dashboard/tests/test_commands.py

import pytest
import pandas as pd
from io import StringIO
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import pytz

# Import the model
try:
    from dashboard.models import OHLCVData
    DJANGO_MODELS_AVAILABLE = True
except ImportError:
    DJANGO_MODELS_AVAILABLE = False

# Check if the function exists for conditional skipping (optional)
SAVE_FUNC_AVAILABLE = True # Assume available unless proven otherwise

# Mark all tests in this file to use the database
pytestmark = pytest.mark.django_db

# --- Tests for export_ohlcv ---

def test_export_ohlcv_success(tmp_path):
    """Test successful export of OHLCV data."""
    if not DJANGO_MODELS_AVAILABLE: pytest.skip("Models not available")
    ticker = "EXPTEST"
    ts1 = timezone.now().replace(hour=1, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
    ts2 = ts1 - timezone.timedelta(days=1)
    OHLCVData.objects.create(timestamp=ts1, ticker=ticker, open=100, high=102, low=99, close=101, volume=1000)
    OHLCVData.objects.create(timestamp=ts2, ticker=ticker, open=98, high=100, low=97, close=99, volume=1200)
    OHLCVData.objects.create(timestamp=ts1, ticker="OTHER", open=50, high=51, low=49, close=50, volume=500)
    output_file = tmp_path / "export_test.csv"
    output_file_str = str(output_file)
    call_command('export_ohlcv', ticker=ticker, output=output_file_str)
    assert output_file.is_file()
    df_read = pd.read_csv(output_file_str, parse_dates=['timestamp'])
    assert list(df_read.columns) == ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    assert len(df_read) == 2
    if df_read['timestamp'].dt.tz is None: df_read['timestamp'] = df_read['timestamp'].dt.tz_localize('UTC')
    else: df_read['timestamp'] = df_read['timestamp'].dt.tz_convert('UTC')
    df_read = df_read.sort_values(by='timestamp').reset_index(drop=True)
    assert df_read.loc[0, 'timestamp'].to_pydatetime() == ts2.astimezone(pytz.UTC)
    assert df_read.loc[0, 'close'] == 99.0
    assert df_read.loc[1, 'timestamp'].to_pydatetime() == ts1.astimezone(pytz.UTC)
    assert df_read.loc[1, 'close'] == 101.0

def test_export_ohlcv_ticker_not_found(tmp_path):
    """Test export command when the ticker does not exist."""
    if not DJANGO_MODELS_AVAILABLE: pytest.skip("Models not available")
    ticker = "NOTFOUND"
    output_file_str = str(tmp_path / "notfound_export.csv")
    with pytest.raises(CommandError) as excinfo:
        call_command('export_ohlcv', ticker=ticker, output=output_file_str)
    assert f"No OHLCV data found for ticker '{ticker}'" in str(excinfo.value)

def test_export_ohlcv_invalid_output_path():
    """Test export command with an invalid output path."""
    if not DJANGO_MODELS_AVAILABLE: pytest.skip("Models not available")
    ticker = "EXPTEST"
    OHLCVData.objects.create(timestamp=timezone.now().replace(tzinfo=pytz.UTC), ticker=ticker, open=1, high=1, low=1, close=1, volume=1)
    invalid_output_file = "/proc/non_existent_dir_hopefully/export_fail.csv"
    raised_error = None
    try: call_command('export_ohlcv', ticker=ticker, output=invalid_output_file)
    except CommandError as e: raised_error = e
    except Exception as e: pytest.fail(f"Unexpected exception {type(e).__name__} raised: {e}")
    assert raised_error is not None, "CommandError was not raised"
    assert "Error writing to output file" in str(raised_error)


# --- Tests for import_ohlcv ---

# Custom exception for testing
class MockSaveError(Exception): pass

# --- CORRECTED PATCH TARGET ---
@patch('dashboard.management.commands.import_ohlcv.save_ohlcv_data')
def test_import_ohlcv_success(mock_save_data, tmp_path):
    """Test successful import of OHLCV data."""
    ticker = "IMPTEST"
    csv_content = "timestamp,open,high,low,close,volume\n2024-03-10 00:00:00,150.0,152.5,149.0,151.0,20000\n2024-03-11 00:00:00,151.2,153.0,150.5,152.0,22000"
    input_file = tmp_path / "import_test.csv"
    input_file_str = str(input_file)
    input_file.write_text(csv_content)
    mock_save_data.return_value = 2
    call_command('import_ohlcv', filepath=input_file_str, ticker=ticker)
    mock_save_data.assert_called_once()
    args, kwargs = mock_save_data.call_args
    called_df = args[0]
    called_ticker = args[1]
    assert called_ticker == ticker
    assert isinstance(called_df, pd.DataFrame)
    assert len(called_df) == 2
    assert called_df.loc[pd.Timestamp('2024-03-10 00:00:00'), 'close'] == 151.0
    assert called_df.index.name == 'timestamp'

def test_import_ohlcv_file_not_found():
    """Test import command when the input file does not exist."""
    ticker = "FILENOTFOUND"
    non_existent_file = "/path/to/non_existent_file.csv"
    with pytest.raises(CommandError) as excinfo:
        call_command('import_ohlcv', filepath=non_existent_file, ticker=ticker)
    assert f"Input file not found at: {non_existent_file}" in str(excinfo.value)

def test_import_ohlcv_missing_columns(tmp_path):
    """Test import command when the CSV is missing required columns."""
    ticker = "MISSCOL"
    csv_content = "timestamp,open,high,low,volume\n2024-03-10 00:00:00,150.0,152.5,149.0,20000"
    input_file = tmp_path / "missing_col.csv"
    input_file_str = str(input_file)
    input_file.write_text(csv_content)
    with pytest.raises(CommandError) as excinfo:
        call_command('import_ohlcv', filepath=input_file_str, ticker=ticker)
    assert "CSV file is missing required columns: close" in str(excinfo.value)

# --- CORRECTED PATCH TARGET ---
@patch('dashboard.management.commands.import_ohlcv.save_ohlcv_data')
def test_import_ohlcv_save_error(mock_save_data, tmp_path):
    """Test import command when save_ohlcv_data raises an error."""
    ticker = "SAVEFAIL"
    csv_content = "timestamp,open,high,low,close,volume\n2024-03-10 00:00:00,150.0,152.5,149.0,151.0,20000"
    input_file = tmp_path / "save_fail.csv"
    input_file_str = str(input_file)
    input_file.write_text(csv_content)
    simulated_error_message = "Simulated database save error"
    mock_save_data.side_effect = MockSaveError(simulated_error_message)

    # Expect CommandError because the command should catch the underlying MockSaveError
    # and re-raise it wrapped in CommandError
    with pytest.raises(CommandError) as excinfo:
        call_command('import_ohlcv', filepath=input_file_str, ticker=ticker)

    # Check that the CommandError message includes the original error text
    assert "Error saving data to database" in str(excinfo.value)
    assert simulated_error_message in str(excinfo.value)
    mock_save_data.assert_called_once() # Ensure the mock was still called
