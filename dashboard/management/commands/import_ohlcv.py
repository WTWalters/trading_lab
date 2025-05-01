# dashboard/management/commands/import_ohlcv.py

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

# Import the saving function from core.data_handler
try:
    from core.data_handler import save_ohlcv_data
except ImportError as e: # pragma: no cover
    # Handle case where core module might not be found
    save_ohlcv_data = None # pragma: no cover

class Command(BaseCommand):
    """
    Django management command to import OHLCV data for a specific ticker from a CSV file.
    ... (docstring remains the same) ...
    """
    help = 'Imports OHLCV data for a specified ticker from a CSV file.'

    def add_arguments(self, parser):
        """ Define command-line arguments. """
        parser.add_argument('--filepath', type=str, required=True, help='...')
        parser.add_argument('--ticker', type=str, required=True, help='...')

    def handle(self, *args, **options):
        """ The main logic of the command. """
        if save_ohlcv_data is None: # pragma: no cover
             # This check might be redundant if the import error is handled,
             # but keep it for robustness if the import logic changes.
             raise CommandError("Could not import 'save_ohlcv_data' function from core.data_handler.")

        filepath = options['filepath']
        ticker = options['ticker'].upper()

        self.stdout.write(f"Starting import for ticker: {ticker} from file: {filepath}")

        if not os.path.exists(filepath):
            raise CommandError(f"Input file not found at: {filepath}")

        try:
            # Attempt to read the CSV
            df = pd.read_csv(filepath, parse_dates=['timestamp'], index_col='timestamp')
            self.stdout.write(f"Successfully read {len(df)} rows from {filepath}.")

        except FileNotFoundError: # pragma: no cover
            # Should be caught by os.path.exists, but include for robustness
            raise CommandError(f"Input file not found at: {filepath}") # pragma: no cover
        except KeyError as e:
             raise CommandError(f"CSV file missing required 'timestamp' column (or failed to parse): {e}")
        except ValueError as e:
            # Covers date parsing errors
            raise CommandError(f"Error parsing timestamp column in CSV file: {e}")
        except Exception as e:
            # Catch other potential pandas read_csv errors
            raise CommandError(f"Error reading CSV file '{filepath}': {e}")

        # --- Validate DataFrame ---
        if df.empty:
            # Test case: test_import_ohlcv_empty_csv
            raise CommandError("CSV file is empty. No data to import.")

        required_cols = {'open', 'high', 'low', 'close', 'volume'}
        actual_cols = {col.lower() for col in df.columns}

        if not required_cols.issubset(actual_cols):
            missing = required_cols - actual_cols
            raise CommandError(f"CSV file is missing required columns: {', '.join(missing)}")

        df.columns = df.columns.str.lower()

        # --- Save Data using core function ---
        self.stdout.write(f"Attempting to save data for {ticker} to database...")
        try:
            save_ohlcv_data(df, ticker)
            self.stdout.write(self.style.SUCCESS(
                f"Import process completed for {ticker}. Processed {len(df)} rows."
            ))
        except Exception as e:
            # This catches errors raised by save_ohlcv_data
            raise CommandError(f"Error saving data to database for ticker '{ticker}': {e}")
