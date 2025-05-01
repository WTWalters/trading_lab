# dashboard/management/commands/export_ohlcv.py

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings # Potentially useful for settings
import os # For path manipulation

# Import your model
try:
    from dashboard.models import OHLCVData
except ImportError:
    # Handle the case where models might not be ready or app not configured
    # This might occur during initial setup phases or if run outside manage.py
    OHLCVData = None

class Command(BaseCommand):
    """
    Django management command to export OHLCV data for a specific ticker to a CSV file.

    Example Usage:
        python manage.py export_ohlcv --ticker AAPL --output /path/to/aapl_data.csv
    """
    help = 'Exports OHLCV data for a specified ticker to a CSV file.'

    def add_arguments(self, parser):
        """
        Define command-line arguments.
        """
        parser.add_argument(
            '--ticker',
            type=str,
            required=True,
            help='The stock ticker symbol to export data for (e.g., AAPL).'
        )
        parser.add_argument(
            '--output',
            type=str,
            required=True,
            help='The full path to the output CSV file.'
        )

    def handle(self, *args, **options):
        """
        The main logic of the command.
        """
        if OHLCVData is None:
             raise CommandError("OHLCVData model could not be imported. Ensure the 'dashboard' app is configured correctly.")

        ticker = options['ticker'].upper() # Standardize ticker to uppercase
        output_path = options['output']

        self.stdout.write(f"Starting export for ticker: {ticker}")

        # --- Query the Database ---
        try:
            # Fetch relevant fields, ordered by timestamp
            # Using .values() is more memory-efficient than fetching full model instances
            data_qs = OHLCVData.objects.filter(ticker=ticker).order_by('timestamp').values(
                'timestamp', 'open', 'high', 'low', 'close', 'volume'
            )

            if not data_qs.exists():
                raise CommandError(f"No OHLCV data found for ticker '{ticker}' in the database.")

            self.stdout.write(f"Found {data_qs.count()} records for {ticker}.")

            # --- Convert to DataFrame ---
            # Pandas can directly read a queryset using .values()
            df = pd.DataFrame.from_records(data_qs)

            # Optional: Format timestamp if needed (e.g., remove timezone for CSV)
            # df['timestamp'] = df['timestamp'].dt.tz_localize(None) # Example: Make naive
            # df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S') # Example: Format as string

        except Exception as e:
            # Catch potential database errors during query
            raise CommandError(f"Error querying database for ticker '{ticker}': {e}")

        # --- Write to CSV ---
        try:
            # Ensure the output directory exists (optional, depends on desired behavior)
            output_dir = os.path.dirname(output_path)
            if output_dir: # Check if output_dir is not empty (i.e., not just filename)
                 os.makedirs(output_dir, exist_ok=True)

            # Write the DataFrame to CSV
            # index=False prevents pandas from writing the DataFrame index as a column
            df.to_csv(output_path, index=False)

            self.stdout.write(self.style.SUCCESS(f"Successfully exported data for {ticker} to: {output_path}"))

        except IOError as e:
            # Catch file system errors (e.g., permission denied)
            raise CommandError(f"Error writing to output file '{output_path}': {e}")
        except Exception as e:
            # Catch other potential errors (e.g., pandas errors)
            raise CommandError(f"An unexpected error occurred during CSV export: {e}")
