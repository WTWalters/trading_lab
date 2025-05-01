# dashboard/management/commands/fetch_data.py
from django.core.management.base import BaseCommand, CommandError
from core.data_handler import fetch_stock_data, save_ohlcv_data
from dashboard.models import OHLCVData # Assuming models are available
from datetime import datetime, date, timedelta

class Command(BaseCommand):
    help = 'Fetches historical OHLCV data for a specified ticker from an API and saves it to the database.'

    def add_arguments(self, parser):
        parser.add_argument('ticker', type=str, help='The stock ticker symbol to fetch.')
        parser.add_argument(
            '--source', type=str, default='yfinance', choices=['yfinance', 'alpha_vantage'],
            help='The data source to use (default: yfinance).'
        )
        parser.add_argument(
            '--years', type=int, default=1,
            help='Number of years of data to fetch back from today (default: 1).'
        )
        parser.add_argument('--start', type=str, help='Start date in YYYY-MM-DD format (overrides --years).')
        parser.add_argument('--end', type=str, help='End date in YYYY-MM-DD format (defaults to today).')

    def handle(self, *args, **options):
        ticker = options['ticker'].upper()
        source = options['source']
        years_back = options['years']
        start_str = options['start']
        end_str = options['end']

        # Determine date range
        end_date = datetime.strptime(end_str, '%Y-%m-%d').date() if end_str else date.today()
        if start_str:
            start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        else:
            start_date = end_date - timedelta(days=365 * years_back) # Approx years

        start_date_fmt = start_date.strftime('%Y-%m-%d')
        end_date_fmt = end_date.strftime('%Y-%m-%d')

        self.stdout.write(f"Attempting to fetch data for {ticker} from {source} ({start_date_fmt} to {end_date_fmt})...")

        # Fetch data using the core function
        df = fetch_stock_data(ticker=ticker, source=source, start_date=start_date_fmt, end_date=end_date_fmt)

        if df is not None and not df.empty:
            self.stdout.write(f"Successfully fetched {len(df)} rows.")
            self.stdout.write("Attempting to save data to database...")
            try:
                num_saved = save_ohlcv_data(df, ticker)
                self.stdout.write(self.style.SUCCESS(f"Database save process completed. Potential new records added/ignored: {num_saved}"))
                # Optional: Verify count after saving
                # count = OHLCVData.objects.filter(...).count()
                # self.stdout.write(f"Current DB record count for range: {count}")
            except Exception as e:
                raise CommandError(f"Error saving data to database: {e}")
        else:
            self.stderr.write(self.style.ERROR(f"Failed to fetch data for {ticker} or no data returned."))
