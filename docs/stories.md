# Story 1: Initial Project Environment Setup
## Story
**As a** developer
**I want** the foundational project structure, environment, database, and core configurations set up
**so that** I have a stable base to start building the application features according to the defined architecture.

## Status
Draft

## Context
This story covers the essential first steps defined in Story 1.0 of the PRD and Section 4 of the Architecture document. It involves setting up the version control, Python environment using Anaconda, installing and configuring PostgreSQL with TimeScaleDB locally, initializing the Django project and the `dashboard` app, setting up environment variable handling with `.env`, and documenting the process. This ensures the project adheres to the specified architecture (Local Monolith, Python 3.12, Django 5.x, PostgreSQL 16.x, TimeScaleDB) from the beginning.

## Estimation
Story Points: 3

## Acceptance Criteria
1.  - [ ] A Git repository is initialized locally and linked to a remote repository on the user's GitHub.
2.  - [ ] An Anaconda environment named `swing_system` is created with Python `3.12.x`.
3.  - [ ] PostgreSQL `16.x` and the compatible TimeScaleDB extension are installed and running locally.
4.  - [ ] A PostgreSQL database named `swing_system_db` and a user `swing_user` are created with correct privileges, and the TimeScaleDB extension is enabled in the database.
5.  - [ ] A Django `5.0.x` project named `swing_project` is created at the root, and a Django app named `dashboard` is created within it.
6.  - [ ] The `dashboard` app is added to `INSTALLED_APPS` in `swing_project/settings.py`.
7.  - [ ] `python-dotenv`, `psycopg2-binary`, `pandas`, and `numpy` are installed in the Conda environment.
8.  - [ ] A `.env` file exists at the project root containing placeholders for `SECRET_KEY`, `DEBUG`, `DATABASE_URL`, `ALPHA_VANTAGE_API_KEY`, `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `ALPACA_PAPER_URL`, and `GEMINI_API_KEY`.
9.  - [ ] The `.env` file is listed in the `.gitignore` file.
10. - [ ] `swing_project/settings.py` is configured to load variables from `.env` and configure the `DATABASES` setting using the `DATABASE_URL`.
11. - [ ] Initial Django migrations (`manage.py makemigrations` & `manage.py migrate`) run successfully against the configured PostgreSQL database.
12. - [ ] `README.md` contains clear instructions for setting up the environment (Anaconda, PostgreSQL/TimeScaleDB install, DB creation, Python dependencies, running the server).

## Subtasks
1.  - [ ] **Version Control Setup**
    1.  - [ ] Initialize Git repository (`git init`).
    2.  - [ ] Create remote repository on GitHub.
    3.  - [ ] Link local repo to remote and perform initial commit.
    4.  - [ ] Create `.gitignore` file and add necessary entries (`.env`, `__pycache__/`, `*.pyc`, environment dirs, `.DS_Store`, `db.sqlite3`).
2.  - [ ] **Environment Setup (Anaconda)**
    1.  - [ ] Create Conda environment: `conda create --name swing_system python=3.12 -y`.
    2.  - [ ] Activate environment: `conda activate swing_system`.
3.  - [ ] **Database Setup (PostgreSQL & TimeScaleDB)**
    1.  - [ ] Install PostgreSQL `16.x` (e.g., using Homebrew).
    2.  - [ ] Install compatible TimeScaleDB extension (following official docs).
    3.  - [ ] Initialize/Start PostgreSQL service.
    4.  - [ ] Create database: `CREATE DATABASE swing_system_db;`.
    5.  - [ ] Create user: `CREATE USER swing_user WITH PASSWORD 'your_secure_password';`.
    6.  - [ ] Grant privileges: `GRANT ALL PRIVILEGES ON DATABASE swing_system_db TO swing_user;`.
    7.  - [ ] Change owner: `ALTER DATABASE swing_system_db OWNER TO swing_user;`.
    8.  - [ ] Enable TimeScaleDB extension in the database: `CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;`.
4.  - [ ] **Django Project Setup**
    1.  - [ ] Install Django `5.0.x`: `pip install django==5.0.*`.
    2.  - [ ] Create Django project: `django-admin startproject swing_project .`.
    3.  - [ ] Create Django app: `python manage.py startapp dashboard`.
    4.  - [ ] Add `dashboard` to `INSTALLED_APPS` in `swing_project/settings.py`.
5.  - [ ] **Dependency Installation & Configuration**
    1.  - [ ] Install `python-dotenv`: `pip install python-dotenv`.
    2.  - [ ] Install `psycopg2-binary`, `pandas`, `numpy`.
    3.  - [ ] Create `.env` file with specified placeholders.
    4.  - [ ] Modify `swing_project/settings.py` to load `.env` and configure `DATABASES` from `DATABASE_URL`. (Use `dj-database-url` library potentially).
    5.  - [ ] Replace default `SECRET_KEY` in `settings.py` with loading from `.env`.
6.  - [ ] **Initial Migration & Documentation**
    1.  - [ ] Run `python manage.py makemigrations`.
    2.  - [ ] Run `python manage.py migrate`.
    3.  - [ ] Update `README.md` with detailed setup steps based on Architecture Doc Section 4.
    4.  - [ ] Create initial `requirements.txt` (or Conda env file) capturing pinned versions.

## Testing Requirements:**
* Manual verification of setup steps. Unit/Integration tests not applicable for initial setup, but successful migration serves as a basic check. Code coverage requirement (>= 85%) applies to subsequent stories adding code.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 2: Implement Historical Data Fetching
## Story
**As a** developer
**I want** to implement functions to fetch daily OHLCV stock data from both yfinance and Alpha Vantage APIs
**so that** the application can acquire the necessary historical market data for storage, analysis, and backtesting.

## Status
Draft

## Context
This story corresponds to Story 2.1 in the PRD. It involves setting up the `core/data_handler.py` module to interact with external market data APIs (yfinance, Alpha Vantage). Key requirements include installing the necessary libraries, implementing fetching logic for daily OHLCV data, reading API keys securely from the `.env` file, adding basic error handling for API calls, and providing a configuration mechanism to choose the data source. This module is crucial for populating the database with historical data.

## Estimation
Story Points: 2

## Acceptance Criteria
1.  - [ ] The `yfinance` and `alpha-vantage` Python libraries are installed and added to `requirements.txt`.
2.  - [ ] The `core/data_handler.py` module is created.
3.  - [ ] A function exists in `core/data_handler.py` that accepts a stock ticker and date range, and returns a Pandas DataFrame with daily OHLCV data fetched using `yfinance`.
4.  - [ ] A function exists in `core/data_handler.py` that accepts a stock ticker, reads the Alpha Vantage API key from the `.env` file, and returns a Pandas DataFrame with daily OHLCV data fetched using the `alpha-vantage` library.
5.  - [ ] Both fetching functions include basic error handling (e.g., `try...except` blocks for network errors or API errors) and log errors using Python's `logging` module. They should return `None` or raise a custom exception on failure.
6.  - [ ] A mechanism (e.g., a configuration variable or function parameter) exists within `core/data_handler.py` to allow calling code (like a management command or view later) to specify which data source (`yfinance` or `alpha-vantage`) to use.
7.  - [ ] Unit tests exist for the data fetching functions in `core/tests/`, mocking the external API calls, and achieving >= 85% code coverage for the new code in `core/data_handler.py`.

## Subtasks
1.  - [ ] **Install Libraries**
    1.  - [ ] Install `yfinance`: `pip install yfinance`.
    2.  - [ ] Install `alpha-vantage`: `pip install alpha-vantage`.
    3.  - [ ] Update `requirements.txt`.
2.  - [ ] **Create `core/data_handler.py` Module**
    1.  - [ ] Create the file `core/data_handler.py`.
    2.  - [ ] Add basic structure and imports (e.g., `pandas`, `logging`, `os`, `dotenv`, API libraries).
    3.  - [ ] Implement loading of API keys from `.env` using `python-dotenv`.
3.  - [ ] **Implement `yfinance` Fetching Function**
    1.  - [ ] Define function signature (e.g., `Workspace_yfinance_data(ticker, start_date, end_date)`).
    2.  - [ ] Implement call to `yfinance.download()`.
    3.  - [ ] Implement error handling (`try...except`) and logging.
    4.  - [ ] Ensure returned DataFrame has expected columns (Open, High, Low, Close, Volume, adjusted close if needed).
4.  - [ ] **Implement `Alpha Vantage` Fetching Function**
    1.  - [ ] Define function signature (e.g., `Workspace_alpha_vantage_data(ticker)`).
    2.  - [ ] Implement instantiation of Alpha Vantage client using API key from `.env`.
    3.  - [ ] Implement call to get daily adjusted data.
    4.  - [ ] Implement error handling (`try...except`) and logging.
    5.  - [ ] Ensure returned DataFrame is parsed correctly and has expected columns. Handle potential API rate limits gracefully.
5.  - [ ] **Implement Data Source Selection**
    1.  - [ ] Define a higher-level function or modify existing ones to accept a `source` parameter ('yfinance' or 'alpha_vantage').
    2.  - [ ] Alternatively, implement configuration setting (e.g., read from `.env` or a settings file).
6.  - [ ] **Implement Unit Tests**
    1.  - [ ] Create `core/tests/test_data_handler.py`.
    2.  - [ ] Write tests using `pytest` and `unittest.mock` to simulate API responses and errors for both yfinance and Alpha Vantage functions.
    3.  - [ ] Verify correct DataFrame structure or error handling behavior.
    4.  - [ ] Run tests with coverage: `pytest --cov=core`.

## Testing Requirements:**
* Unit tests with mocked API calls are mandatory. Focus on verifying correct data parsing, error handling, and API key usage. >= 85% code coverage required for `core/data_handler.py`.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 3: Integrate with PostgreSQL/TimeScaleDB
## Story
**As a** developer
**I want** to define the database model for OHLCV data and configure it as a TimeScaleDB hypertable, and update the data handler to save fetched data into this table
**so that** historical market data can be persistently stored and efficiently queried using the optimized time-series database.

## Status
Draft

## Context
This story covers Story 2.2 from the PRD and addresses the data storage aspect detailed in the Architecture document (Section 3.3 Data View, ADR-002, ADR-006). It requires defining the `OHLCVData` Django model in `dashboard/models.py`, ensuring it's correctly configured as a TimeScaleDB hypertable (likely requiring a custom migration or a library like `django-timescaledb`), and modifying the `core/data_handler.py` module to insert the Pandas DataFrames fetched in Story 2 into this database table. Performance for bulk inserts should be considered (ADR-006).

## Estimation
Story Points: 3

## Acceptance Criteria
1.  - [ ] A Django model named `OHLCVData` is defined in `dashboard/models.py` with fields: `timestamp` (DateTimeField, primary key with `ticker`), `ticker` (CharField, primary key with `timestamp`), `open` (DecimalField/FloatField), `high` (DecimalField/FloatField), `low` (DecimalField/FloatField), `close` (DecimalField/FloatField), `volume` (BigIntegerField). A composite primary key or unique constraint on `(timestamp, ticker)` is established.
2.  - [ ] Django database settings in `settings.py` correctly point to the PostgreSQL database.
3.  - [ ] A Django migration is created for the `OHLCVData` model.
4.  - [ ] The `OHLCVData` table in PostgreSQL is successfully converted into a TimeScaleDB hypertable partitioned by the `timestamp` column (verified via `psql` or custom migration output). This might involve using `django-timescaledb` or writing raw SQL in a migration file.
5.  - [ ] The `core/data_handler.py` module has a function (e.g., `save_ohlcv_data(df, ticker)`) that takes a Pandas DataFrame (as returned by the fetching functions) and saves its rows to the `OHLCVData` table.
6.  - [ ] The saving mechanism handles potential duplicate entries (e.g., using `update_or_create` or integrity checks) based on the composite key `(timestamp, ticker)`.
7.  - [ ] The saving mechanism is reasonably efficient for inserting multiple rows (considers bulk methods if performance with basic ORM is poor for typical data pulls).
8.  - [ ] Appropriate database indexes (e.g., on `(ticker, timestamp)`) are created via the Django model's `Meta` class or a custom migration.
9.  - [ ] Unit/Integration tests exist in `core/tests/` and/or `dashboard/tests/` verifying that data can be saved to and retrieved from the `OHLCVData` model/table, using a test database. >= 85% code coverage required for the new model and saving logic.

## Subtasks
1.  - [ ] **Define `OHLCVData` Model**
    1.  - [ ] Open `dashboard/models.py`.
    2.  - [ ] Define the `OHLCVData` class inheriting from `models.Model`.
    3.  - [ ] Add fields: `timestamp` (DateTimeField), `ticker` (CharField), `open`, `high`, `low`, `close` (DecimalField preferred, specify `max_digits`, `decimal_places`), `volume` (BigIntegerField).
    4.  - [ ] Define `Meta` class with `unique_together = ('timestamp', 'ticker')` or use `constraints`. Define `ordering`.
    5.  - [ ] Add `__str__` method for representation.
2.  - [ ] **Create Initial Migration**
    1.  - [ ] Run `python manage.py makemigrations dashboard`.
3.  - [ ] **Configure TimeScaleDB Hypertable**
    1.  - [ ] **Option A (django-timescaledb):** Install `django-timescaledb`, add it to `INSTALLED_APPS`, potentially change the model to inherit from `TimescaleModel`, and configure hypertable settings in `Meta`. Run `makemigrations` again.
    2.  - [ ] **Option B (Manual Migration):** Edit the generated migration file. Add a `RunSQL` operation to execute the `create_hypertable` SQL command (`SELECT create_hypertable('dashboard_ohlcvdata', 'timestamp');`) *after* the table creation. Ensure this runs only if the extension is enabled.
    3.  - [ ] Run `python manage.py migrate`.
    4.  - [ ] Verify hypertable creation using `psql`: `\d+ dashboard_ohlcvdata`.
4.  - [ ] **Implement Data Saving Logic in `core/data_handler.py`**
    1.  - [ ] Define a function `save_ohlcv_data(dataframe, ticker)`.
    2.  - [ ] Iterate through the DataFrame rows. For each row, create or update an `OHLCVData` model instance.
    3.  - [ ] Use `YourModel.objects.bulk_create` or `YourModel.objects.bulk_update` or `YourModel.objects.update_or_create` for efficiency and handling duplicates based on the unique constraint `(timestamp, ticker)`. Research performance implications.
    4.  - [ ] Add error handling and logging around the database operations.
5.  - [ ] **Implement Tests**
    1.  - [ ] Create test file(s) (e.g., `dashboard/tests/test_models.py`, `core/tests/test_data_handler_db.py`).
    2.  - [ ] Write tests using `pytest-django`'s test database capabilities.
    3.  - [ ] Test creating `OHLCVData` instances.
    4.  - [ ] Test the `save_ohlcv_data` function: create a sample DataFrame, call the function, assert that the data exists in the test DB and handles duplicates correctly.
    5.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Integration tests using a test PostgreSQL database (managed by `pytest-django`) are mandatory to verify model creation, migration (including hypertable setup if possible via testing hooks), and data saving/retrieval. >= 85% code coverage required.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 4: Implement Basic CSV Import/Export
## Story
**As a** developer
**I want** to create Django management commands for exporting OHLCV data to CSV and importing OHLCV data from CSV
**so that** the user can easily backup, share, or manually load historical data into the system.

## Status
Draft

## Context
This story corresponds to Story 2.3 in the PRD. It focuses on providing utility functions for data interoperability using the common CSV format. This involves creating two custom Django management commands within the `dashboard` app: one to export data from the `OHLCVData` table to a CSV file, and another to import data from a specified CSV file format into the `OHLCVData` table, leveraging the saving logic potentially developed in Story 3.

## Estimation
Story Points: 1

## Acceptance Criteria
1.  - [ ] A Django management command named `export_ohlcv` exists in `dashboard/management/commands/`.
2.  - [ ] Running `python manage.py export_ohlcv --ticker <TICKER> --output <FILEPATH.csv>` successfully exports OHLCV data for the specified ticker from the database to the specified CSV file.
3.  - [ ] The exported CSV file has appropriate headers (e.g., timestamp, open, high, low, close, volume).
4.  - [ ] A Django management command named `import_ohlcv` exists in `dashboard/management/commands/`.
5.  - [ ] Running `python manage.py import_ohlcv --filepath <FILEPATH.csv> --ticker <TICKER>` successfully reads data from the specified CSV file and imports it into the `OHLCVData` database table for the given ticker.
6.  - [ ] The import command handles the expected CSV format (headers matching export/model) and data types correctly.
7.  - [ ] The import command utilizes the data saving logic (including duplicate handling) from `core/data_handler.py` or implements similar robust saving.
8.  - [ ] Both commands provide user feedback (e.g., print statements indicating progress, success, or errors).
9.  - [ ] Basic tests exist for the management commands (e.g., using `call_command` from `django.core.management`) to verify their core functionality (mocking file I/O and DB interactions where necessary). >= 85% code coverage required for the command logic.

## Subtasks
1.  - [ ] **Create Management Command Structure**
    1.  - [ ] Create directories: `dashboard/management/commands/`.
    2.  - [ ] Add `__init__.py` files to `management` and `commands` directories.
2.  - [ ] **Implement `export_ohlcv` Command**
    1.  - [ ] Create `dashboard/management/commands/export_ohlcv.py`.
    2.  - [ ] Inherit from `BaseCommand`.
    3.  - [ ] Implement `add_arguments` to accept `--ticker` and `--output` file path.
    4.  - [ ] Implement `handle` method:
        1.  - [ ] Query `OHLCVData` for the specified ticker.
        2.  - [ ] Convert queryset to Pandas DataFrame (or use Django's CSV tools).
        3.  - [ ] Write DataFrame to the specified CSV file using `df.to_csv()`.
        4.  - [ ] Add print statements for user feedback.
        5.  - [ ] Include error handling (e.g., file path issues, DB query errors).
3.  - [ ] **Implement `import_ohlcv` Command**
    1.  - [ ] Create `dashboard/management/commands/import_ohlcv.py`.
    2.  - [ ] Inherit from `BaseCommand`.
    3.  - [ ] Implement `add_arguments` to accept `--filepath` and `--ticker`.
    4.  - [ ] Implement `handle` method:
        1.  - [ ] Read data from the specified CSV file using `pandas.read_csv()`.
        2.  - [ ] Validate CSV format/headers.
        3.  - [ ] Preprocess data if necessary (e.g., parse dates, ensure correct types).
        4.  - [ ] Call the data saving function (e.g., `save_ohlcv_data` from `core.data_handler`) to import the data into the database.
        5.  - [ ] Add print statements for user feedback (e.g., number of rows imported).
        6.  - [ ] Include error handling (e.g., file not found, invalid format, DB errors).
4.  - [ ] **Implement Tests**
    1.  - [ ] Create `dashboard/tests/test_commands.py`.
    2.  - [ ] Write tests using `pytest-django`.
    3.  - [ ] Use `django.core.management.call_command`.
    4.  - [ ] For export, mock the queryset, run the command, mock `pandas.to_csv` (or file write), and assert it was called correctly.
    5.  - [ ] For import, create a dummy CSV file (using `tmp_path` fixture from pytest), mock the saving function (`save_ohlcv_data`), run the command, and assert the saving function was called with the correct data.
    6.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit/Integration tests for the management commands are required, using `call_command`. Mock file system operations and database interactions where necessary to isolate command logic. >= 85% code coverage required.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 5: Implement Basic Charting Functionality
## Story
**As a** user
**I want** to view an interactive Candlestick chart with Volume and selectable Moving Average overlays (10, 20, 50 day SMA/EMA) for a specific stock
**so that** I can visually analyze price action and technical indicators within the application.

## Status
Draft

## Context
This story covers Epic 3 / Story 3.1 from the PRD and aligns with ADR-005 (using Plotly). It involves creating a Django view and template to display financial charts. Key tasks include installing Plotly and pandas-ta, fetching OHLCV data from the database for a given ticker, calculating SMAs/EMAs using pandas-ta, generating an interactive Plotly Candlestick chart including volume, adding the MAs as selectable overlays, and embedding the chart within the Django template.

## Estimation
Story Points: 3

## Acceptance Criteria
1.  - [ ] The `plotly` and `pandas-ta` Python libraries are installed and added to `requirements.txt`.
2.  - [ ] A Django view (e.g., `chart_view` in `dashboard/views.py`) exists that handles requests for displaying a chart.
3.  - [ ] A corresponding URL route is defined in `dashboard/urls.py` pointing to the `chart_view`.
4.  - [ ] A Django template (e.g., `dashboard/templates/dashboard/chart_view.html`) exists to render the chart page.
5.  - [ ] The view retrieves OHLCV data (e.g., as a Pandas DataFrame) from the `OHLCVData` model in the database for a specified ticker and date range (user input mechanism to be added later, assume fixed ticker/range for now or basic GET parameter).
6.  - [ ] The view uses `pandas-ta` to calculate 10-day, 20-day, and 50-day SMAs and EMAs based on the retrieved OHLCV data.
7.  - [ ] The view uses `plotly` (specifically `plotly.graph_objects`) to generate a Candlestick chart from the OHLCV data.
8.  - [ ] The Plotly chart includes a Volume bar chart subplot.
9.  - [ ] The calculated SMAs and EMAs are added as line traces to the Plotly chart.
10. - [ ] The chart generated by Plotly is interactive (zoom, pan).
11. - [ ] The Plotly chart HTML/JSON representation is passed to the Django template context.
12. - [ ] The template successfully embeds and renders the interactive Plotly chart (e.g., using `plotly.offline.plot` with `output_type='div'` or the `plotly` Django template tag if using `plotly-django`).
13. - [ ] The template includes basic controls (e.g., checkboxes or buttons, potentially using JavaScript) to toggle the visibility of the SMA/EMA overlays on the chart.
14. - [ ] Unit tests exist for the view logic (mocking DB query, checking chart data context) and potentially helper functions for chart generation/TA calculation. >= 85% code coverage for new view/helper logic.

## Subtasks
1.  - [ ] **Install Libraries**
    1.  - [ ] Install `plotly`: `pip install plotly`.
    2.  - [ ] Install `pandas-ta`: `pip install pandas-ta`.
    3.  - [ ] Update `requirements.txt`.
2.  - [ ] **Create Django View and URL**
    1.  - [ ] Define `chart_view(request)` in `dashboard/views.py`.
    2.  - [ ] Define URL pattern in `dashboard/urls.py` (e.g., `path('chart/<str:ticker>/', views.chart_view, name='chart_view')`). Update `swing_project/urls.py` to include dashboard URLs.
3.  - [ ] **Create Template**
    1.  - [ ] Create `dashboard/templates/dashboard/chart_view.html`. Include basic HTML structure and a placeholder `div` for the chart. Extend `base.html` if it exists.
4.  - [ ] **Implement Data Retrieval in View**
    1.  - [ ] Get ticker from URL parameter.
    2.  - [ ] Query `OHLCVData.objects.filter(ticker=ticker).order_by('timestamp')`. Consider adding date filtering.
    3.  - [ ] Convert queryset to Pandas DataFrame (e.g., using `django-pandas` or manually). Handle case where no data exists.
5.  - [ ] **Calculate Technical Indicators**
    1.  - [ ] Ensure DataFrame has standard column names (`open`, `high`, `low`, `close`, `volume`).
    2.  - [ ] Use `df.ta.sma(length=10)`, `df.ta.sma(length=20)`, `df.ta.sma(length=50)`.
    3.  - [ ] Use `df.ta.ema(length=10)`, `df.ta.ema(length=20)`, `df.ta.ema(length=50)`.
6.  - [ ] **Generate Plotly Chart**
    1.  - [ ] Create a `plotly.graph_objects.Figure`.
    2.  - [ ] Add Candlestick trace: `go.Candlestick(...)`.
    3.  - [ ] Add Volume bar trace: `go.Bar(...)` (potentially on a secondary y-axis or subplot).
    4.  - [ ] Add SMA traces: `go.Scatter(y=df['SMA_10'], ..., name='SMA 10')`, etc. Set `visible='legendonly'` initially if needed for toggling.
    5.  - [ ] Add EMA traces: `go.Scatter(y=df['EMA_10'], ..., name='EMA 10')`, etc. Set `visible='legendonly'` initially if needed for toggling.
    6.  - [ ] Configure layout (title, axes labels, remove rangeslider if desired).
7.  - [ ] **Embed Chart in Template**
    1.  - [ ] Convert Figure to HTML div: `fig.to_html(full_html=False, include_plotlyjs='cdn')` or use `plot(fig, output_type='div', include_plotlyjs=False)`.
    2.  - [ ] Pass the generated HTML div string to the template context.
    3.  - [ ] Render the div in the template using `{{ chart_div|safe }}`. Ensure Plotly.js library is loaded (e.g., via CDN link in `base.html` or template).
8.  - [ ] **Implement Overlay Toggles**
    1.  - [ ] Add checkboxes or buttons to the template for each MA overlay.
    2.  - [ ] Add basic JavaScript to connect button clicks/checkbox changes to Plotly `restyle` calls to toggle trace visibility (using `visible: true/false` or `visible: 'legendonly'`). Alternatively, leverage Plotly's built-in legend interactivity.
9.  - [ ] **Implement Tests**
    1.  - [ ] Create `dashboard/tests/test_views.py`.
    2.  - [ ] Write tests for `chart_view` using Django's test client.
    3.  - [ ] Mock the database query (`OHLCVData.objects.filter`).
    4.  - [ ] Check that the view returns a 200 status code.
    5.  - [ ] Check that the chart div string exists in the context.
    6.  - [ ] Consider testing helper functions for TA calculation/chart generation separately with sample DataFrames.
    7.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit tests for the view function mocking database interactions and checking the context passed to the template. Tests for any helper functions used for TA calculation or chart generation. >= 85% code coverage required. Manual E2E testing to verify chart rendering and interactivity.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 6: Implement Classic Breakout Strategy Logic
## Story
**As a** developer
**I want** to implement the "Classic Breakout" trading strategy logic within the Backtrader framework
**so that** it can be used for backtesting against historical data.

## Status
Draft

## Context
This story corresponds to Story 4.1 in the PRD and is a core part of the system. It involves installing the Backtrader library and defining a custom strategy class (`ClassicBreakoutStrategy`) in `core/strategies.py`. This class must implement the specific rules detailed in the PRD: identifying consolidation ranges, confirming breakouts based on price and volume, generating entry signals, setting initial ATR-based stop-losses, and implementing an ATR-based trailing stop (Chandelier Exit) for exits. pandas-ta might be used alongside Backtrader's built-in indicators.

## Estimation
Story Points: 5

## Acceptance Criteria
1.  - [ ] The `backtrader` Python library is installed and added to `requirements.txt`.
2.  - [ ] A file `core/strategies.py` exists.
3.  - [ ] A class `ClassicBreakoutStrategy` inheriting from `backtrader.Strategy` is defined in `core/strategies.py`.
4.  - [ ] The strategy correctly calculates or utilizes necessary indicators: ATR (e.g., `bt.indicators.ATR(period=14)`), Volume MA (e.g., `bt.indicators.SMA(self.data.volume, period=20)`).
5.  - [ ] The strategy implements logic in `next()` or other methods to identify potential consolidation ranges (support/resistance) based on historical price data over a configurable lookback period (e.g., 3-6 months, parameterize). This might involve tracking recent highs/lows.
6.  - [ ] The strategy implements logic to detect a confirmed breakout: close price is beyond the identified range AND volume for the breakout bar is > 1.5 * Volume MA(20).
7.  - [ ] Upon a confirmed breakout, the strategy generates a buy order (`self.buy()`) on the open of the *next* bar.
8.  - [ ] When a position is entered, the strategy calculates and stores an initial stop-loss price based on `Entry Price - (ATR(14) * 2.0)`. (Note: Backtrader handles stop orders, need to decide if this is a mental stop or an actual stop order).
9.  - [ ] The strategy implements an exit mechanism using an ATR-based trailing stop (Chandelier Exit: `HighestHighSinceEntry - (ATR(14) * 3.0)`). This requires tracking the highest high since entry and calculating the trailing stop price on each bar, potentially using `self.sell(exectype=bt.Order.StopTrail, trailamount=...)` or manual management.
10. - [ ] The strategy parameters (lookback period, volume multiplier, ATR periods/multipliers for entry/exit) are defined as class parameters (`params = (...)`) for configurability.
11. - [ ] The strategy includes logging (`self.log(...)`) for key events (signal generation, order placement, entry, exit).
12. - [ ] Unit tests exist in `core/tests/test_strategies.py` for the `ClassicBreakoutStrategy` logic components (e.g., testing consolidation detection, breakout confirmation, stop calculation functions in isolation if possible, or running the strategy on minimal controlled data). >= 85% code coverage for the strategy class logic.

## Subtasks
1.  - [ ] **Install Library**
    1.  - [ ] Install `backtrader`: `pip install backtrader`.
    2.  - [ ] Update `requirements.txt`.
2.  - [ ] **Create Strategy File and Class**
    1.  - [ ] Create `core/strategies.py`.
    2.  - [ ] Define `ClassicBreakoutStrategy(bt.Strategy)`.
    3.  - [ ] Define `params` tuple with configurable parameters (lookback, volume_ma_period, volume_mult, atr_period, initial_stop_atr_mult, trail_stop_atr_mult).
3.  - [ ] **Implement `__init__` Method**
    1.  - [ ] Get data feeds (`self.data0`, `self.datas[0]`).
    2.  - [ ] Define indicators needed: `self.atr = bt.indicators.ATR(period=self.p.atr_period)`, `self.vol_ma = bt.indicators.SMA(self.data.volume, period=self.p.volume_ma_period)`.
    3.  - [ ] Initialize state variables (e.g., `self.order`, `self.entry_price`, `self.highest_high_since_entry`).
4.  - [ ] **Implement Consolidation Range Identification**
    1.  - [ ] In `next()`, look back `self.p.lookback` periods.
    2.  - [ ] Determine recent significant highs (resistance) and lows (support). (This is non-trivial; start simple, e.g., max high / min low over the period, or use indicator like Donchian Channel). Store these levels.
5.  - [ ] **Implement Breakout Confirmation Logic**
    1.  - [ ] In `next()`, check if not already in a position.
    2.  - [ ] Check if `self.data.close[0]` closes above resistance *or* below support.
    3.  - [ ] Check if `self.data.volume[0] > self.p.volume_mult * self.vol_ma[0]`.
6.  - [ ] **Implement Entry Logic**
    1.  - [ ] If breakout confirmed, `self.log('BUY SIGNAL')`, place buy order for next bar: `self.order = self.buy()`. Handle potential short side later if needed.
7.  - [ ] **Implement Initial Stop-Loss (Mental/Tracked)**
    1.  - [ ] In `notify_order` or `notify_trade`, when a buy order is executed:
        1.  - [ ] Store `self.entry_price = trade.price`.
        2.  - [ ] Calculate `initial_stop_price = self.entry_price - (self.atr[0] * self.p.initial_stop_atr_mult)`. Store this value.
        3.  - [ ] Initialize `self.highest_high_since_entry = self.data.high[0]`.
8.  - [ ] **Implement ATR Trailing Stop (Chandelier Exit)**
    1.  - [ ] In `next()`, if in a position:
        1.  - [ ] Update `self.highest_high_since_entry = max(self.highest_high_since_entry, self.data.high[0])`.
        2.  - [ ] Calculate `trailing_stop_price = self.highest_high_since_entry - (self.atr[0] * self.p.trail_stop_atr_mult)`.
        3.  - [ ] Check if `self.data.close[0] < trailing_stop_price`.
        4.  - [ ] If condition met, `self.log('SELL SIGNAL - TRAILING STOP')`, place sell order: `self.order = self.sell()`.
9.  - [ ] **Implement Logging and Order Notification**
    1.  - [ ] Add `log` method as commonly used in Backtrader examples.
    2.  - [ ] Implement `notify_order` to track order status (submitted, accepted, completed, rejected) and handle scenarios where an order might not execute. Reset `self.order` when done.
    3.  - [ ] Implement `notify_trade` to log trade details (P/L).
10. - [ ] **Implement Tests**
    1.  - [ ] Create `core/tests/test_strategies.py`.
    2.  - [ ] Design simple, representative OHLCV data (e.g., using Pandas DataFrames) that should trigger specific strategy actions (consolidation, breakout, entry, trailing stop hit).
    3.  - [ ] Use Backtrader's `Cerebro` within the test to run the strategy on this controlled data.
    4.  - [ ] Assert that orders are placed/executed and P/L is as expected based on the strategy rules and test data.
    5.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit tests are crucial for verifying the complex logic of the strategy. Use controlled data scenarios and Backtrader's engine within tests to assert correct behavior (signals, orders, stops). >= 85% code coverage required for `core/strategies.py`.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 7: Integrate and Run Backtests
## Story
**As a** developer
**I want** to integrate the Backtrader engine with the PostgreSQL/TimeScaleDB data feed and the implemented strategy, set up realistic parameters, and create a basic Django interface to trigger backtests
**so that** the user can run simulations of the Classic Breakout strategy on historical data stored in the database.

## Status
Draft

## Context
This story covers Story 5.1 and 5.2 from the PRD. It involves creating the `core/backtester.py` module to orchestrate Backtrader runs. Key tasks include implementing a custom Backtrader data feed that pulls OHLCV data from the PostgreSQL/TimeScaleDB database, configuring the Cerebro engine with this data feed, adding the `ClassicBreakoutStrategy` (from Story 6), setting commission/slippage, adding necessary analyzers (`TradeAnalyzer`, `SQN`), and creating a simple Django view/template to allow the user to select a ticker and date range to initiate a backtest run via the `core/backtester.py` module.

## Estimation
Story Points: 2

## Acceptance Criteria
1.  - [ ] A `core/backtester.py` module exists.
2.  - [ ] A function or class exists in `core/backtester.py` that can create a Backtrader data feed by querying OHLCV data from the PostgreSQL database (using Django ORM or direct SQL via `psycopg2`). This feed should conform to Backtrader's data feed API (e.g., `PandasData` or a custom feed).
3.  - [ ] A function exists in `core/backtester.py` (e.g., `run_backtest(ticker, start_date, end_date, strategy_class)`) that:
    1.  - [ ] Initializes `backtrader.Cerebro`.
    2.  - [ ] Adds the specified strategy class (e.g., `ClassicBreakoutStrategy`) to Cerebro.
    3.  - [ ] Creates and adds the database data feed for the specified ticker and date range.
    4.  - [ ] Sets initial cash amount (e.g., `cerebro.broker.setcash(100000.0)`).
    5.  - [ ] Sets commission (e.g., `cerebro.broker.setcommission(commission=0.001)` for 0.1%). Consider slippage settings if needed.
    6.  - [ ] Adds `backtrader.analyzers.TradeAnalyzer` and `backtrader.analyzers.SQN` to Cerebro.
    7.  - [ ] Runs the backtest using `cerebro.run()`.
    8.  - [ ] Returns the results from the analyzers.
4.  - [ ] A Django view (e.g., `backtest_view` in `dashboard/views.py`) exists with a corresponding URL.
5.  - [ ] A Django template (e.g., `dashboard/templates/dashboard/backtest_view.html`) exists with a form allowing users to input a stock ticker and optionally a date range.
6.  - [ ] When the form is submitted, the Django view calls the `run_backtest` function in `core/backtester.py` with the user's input and the `ClassicBreakoutStrategy`.
7.  - [ ] The results (analyzers) returned from `run_backtest` are stored or passed to the template context (displaying results is covered in the next story).
8.  - [ ] Unit/Integration tests exist for the `core/backtester.py` module, mocking the database query for the data feed and verifying Cerebro configuration and execution flow. Tests for the Django view verify form handling and calling the backtester function. >= 85% code coverage for new code.

## Subtasks
1.  - [ ] **Create `core/backtester.py` Module**
    1.  - [ ] Create the file `core/backtester.py`.
    2.  - [ ] Add imports: `backtrader`, `datetime`, models from `dashboard.models`, potentially `pandas`.
2.  - [ ] **Implement Database Data Feed**
    1.  - [ ] Define a function `get_data_feed(ticker, start_date, end_date)` or similar.
    2.  - [ ] Inside, query `OHLCVData` using Django ORM for the given ticker/dates.
    3.  - [ ] Convert the queryset/data into a Pandas DataFrame with columns named according to Backtrader conventions (lowercase: `datetime`, `open`, `high`, `low`, `close`, `volume`). Ensure `datetime` is the index and timezone-aware if necessary.
    4.  - [ ] Create and return a `backtrader.feeds.PandasData` instance using this DataFrame. Handle potential `NoDataError`.
3.  - [ ] **Implement `run_backtest` Function**
    1.  - [ ] Define `run_backtest(ticker, start_date, end_date, strategy_class, initial_cash=100000.0, commission=0.001)`.
    2.  - [ ] Initialize `cerebro = bt.Cerebro()`.
    3.  - [ ] Add strategy: `cerebro.addstrategy(strategy_class)`.
    4.  - [ ] Get data feed: `data = get_data_feed(...)`. Handle potential errors.
    5.  - [ ] Add data feed: `cerebro.adddata(data)`.
    6.  - [ ] Set cash: `cerebro.broker.setcash(initial_cash)`.
    7.  - [ ] Set commission: `cerebro.broker.setcommission(commission=commission)`.
    8.  - [ ] Add analyzers: `cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')`, `cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')`.
    9.  - [ ] Run: `results = cerebro.run()`.
    10. - [ ] Return `results[0].analyzers` (or specific analyzer instances). Add logging for start/end.
4.  - [ ] **Create Django View and URL**
    1.  - [ ] Define `backtest_view(request)` in `dashboard/views.py`.
    2.  - [ ] Define URL pattern in `dashboard/urls.py` (e.g., `path('backtest/', views.backtest_view, name='backtest_view')`).
5.  - [ ] **Create Django Template and Form**
    1.  - [ ] Create `dashboard/templates/dashboard/backtest_view.html`.
    2.  - [ ] Add a simple HTML form with fields for 'ticker' (text input) and potentially 'start_date', 'end_date' (date inputs). Use method="POST". Include CSRF token.
    3.  - [ ] In the view, handle GET (display form) and POST (process form).
6.  - [ ] **Implement View Logic**
    1.  - [ ] On POST request:
        1.  - [ ] Get ticker, start_date, end_date from `request.POST`. Validate input.
        2.  - [ ] Import `ClassicBreakoutStrategy` from `core.strategies`.
        3.  - [ ] Import `run_backtest` from `core.backtester`.
        4.  - [ ] Call `analysis_results = run_backtest(...)`. Handle exceptions.
        5.  - [ ] Pass `analysis_results` to the template context for rendering (details in next story).
        6.  - [ ] Re-render the template.
7.  - [ ] **Implement Tests**
    1.  - [ ] Test `get_data_feed` (mock ORM query, check DataFrame format/PandasData instance).
    2.  - [ ] Test `run_backtest` (mock `get_data_feed`, mock `strategy_class`, assert `cerebro.run()` is called, check analyzers are added, mock return value).
    3.  - [ ] Test `backtest_view` (use test client POST, mock `run_backtest`, check context).
    4.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit/Integration tests are required. Mock database interactions for the data feed. Mock the strategy execution within `run_backtest` tests to focus on Cerebro setup and analyzer handling. Test the Django view using the test client. >= 85% code coverage required.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 8: Display Backtest Results
## Story
**As a** user
**I want** to see the key performance metrics (Total P/L, Win Rate, Max Drawdown, SQN) after running a backtest
**so that** I can evaluate the historical performance of the Classic Breakout strategy.

## Status
Draft

## Context
This story covers Story 5.3 from the PRD and directly follows Story 7. It focuses on extracting the specific performance metrics from the Backtrader analyzers (`TradeAnalyzer`, `SQN`) returned by the `run_backtest` function and displaying them clearly in the `backtest_view.html` template.

## Estimation
Story Points: 1

## Acceptance Criteria
1.  - [ ] The `backtest_view` in `dashboard/views.py` correctly retrieves the analysis results object returned by `core.backtester.run_backtest`.
2.  - [ ] The view extracts the Total Net P/L (Profit and Loss) from the `TradeAnalyzer` results.
3.  - [ ] The view calculates or extracts the Win Rate (percentage of winning trades) from the `TradeAnalyzer` results (e.g., using `won.total` and `total.closed`).
4.  - [ ] The view extracts the Maximum Drawdown percentage from the `TradeAnalyzer` results.
5.  - [ ] The view extracts the System Quality Number (SQN) from the `SQN` analyzer results.
6.  - [ ] These extracted metrics (Total P/L, Win Rate, Max Drawdown, SQN) are passed to the `dashboard/templates/dashboard/backtest_view.html` template context.
7.  - [ ] The `backtest_view.html` template displays the received metrics in a clear, readable format (e.g., a summary table or list) when results are available.
8.  - [ ] The template handles the case where backtest results are not yet available (e.g., initial page load before form submission) or if an error occurred during the backtest.
9.  - [ ] Unit tests for the view are updated to verify that the correct metrics are extracted from mocked analyzer results and passed to the template context. >= 85% code coverage for the result extraction logic.

## Subtasks
1.  - [ ] **Update `backtest_view` Logic**
    1.  - [ ] After calling `analysis_results = run_backtest(...)`, check if `analysis_results` is valid (not None, etc.).
    2.  - [ ] Access the specific analyzers by name (e.g., `trade_analyzer = analysis_results.get('trade_analyzer')`, `sqn_analyzer = analysis_results.get('sqn')`). Handle potential `KeyError` if analyzers didn't run.
    3.  - [ ] Extract metrics from `trade_analyzer.analysis`:
        * Total P/L: `trade_analyzer.analysis.pnl.net.total`
        * Total Trades: `trade_analyzer.analysis.total.closed`
        * Winning Trades: `trade_analyzer.analysis.won.total`
        * Losing Trades: `trade_analyzer.analysis.lost.total`
        * Max Drawdown: `trade_analyzer.analysis.drawdown.max.drawdown` (usually a percentage)
    4.  - [ ] Calculate Win Rate: `(winning_trades / total_trades) * 100` if `total_trades > 0` else 0.
    5.  - [ ] Extract SQN: `sqn_analyzer.analysis.sqn`.
    6.  - [ ] Store these metrics in a dictionary (e.g., `results_summary`).
    7.  - [ ] Pass `results_summary` to the template context. Handle cases where analyzers or specific metrics might be missing (e.g., no trades occurred).
2.  - [ ] **Update `backtest_view.html` Template**
    1.  - [ ] Add a section to display results, conditioned on `results_summary` being present in the context (e.g., `{% if results_summary %}`).
    2.  - [ ] Display each metric clearly with a label:
        * Total Net P/L: `{{ results_summary.total_pnl|floatformat:2 }}`
        * Win Rate: `{{ results_summary.win_rate|floatformat:2 }}%`
        * Maximum Drawdown: `{{ results_summary.max_drawdown|floatformat:2 }}%`
        * SQN: `{{ results_summary.sqn|floatformat:2 }}`
        * Total Closed Trades: `{{ results_summary.total_trades }}`
    3.  - [ ] Add an `{% else %}` block for when results are not available after form submission (e.g., "Backtest ran, but no trades were executed or an error occurred.").
    4.  - [ ] Ensure the initial state (before POST) doesn't show the results section or shows a placeholder.
3.  - [ ] **Update Tests**
    1.  - [ ] Modify the tests for `backtest_view`.
    2.  - [ ] Create mock objects simulating the structure of `TradeAnalyzer.analysis` and `SQN.analysis` results.
    3.  - [ ] Update the mocked `run_backtest` function to return these mock analysis results.
    4.  - [ ] Assert that the `results_summary` dictionary in the template context contains the correctly extracted/calculated values based on the mock results.
    5.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit tests for the `backtest_view` must verify the logic for extracting metrics from mocked analyzer results and passing them to the template context. >= 85% code coverage for the result extraction logic. Manual E2E testing to confirm display after running a real backtest.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 9: Create Trade Log Model and Form
## Story
**As a** developer
**I want** to define the Django model for structured trade logging (`TradeLog`) and create a corresponding Django form (`TradeLogForm`)
**so that** the application has the necessary database structure and input mechanism for users to manually record their trade details and psychological factors.

## Status
Draft

## Context
This story corresponds to Story 6.1 in the PRD and Section 3.3 of the Architecture doc. It lays the foundation for the trade journaling feature. It involves defining a comprehensive `TradeLog` model in `dashboard/models.py` with all the specified fields (ticker, strategy, dates, prices, size, P/L, rationale, psychological notes, risk metrics) and creating a `TradeLogForm` in `dashboard/forms.py` based on this model for user input.

## Estimation
Story Points: 2

## Acceptance Criteria
1.  - [ ] A Django model named `TradeLog` is defined in `dashboard/models.py`.
2.  - [ ] The `TradeLog` model includes all specified fields with appropriate types: `ticker` (CharField), `strategy` (CharField), `entry_date` (DateTimeField), `exit_date` (DateTimeField, null=True), `entry_price` (DecimalField/FloatField), `exit_price` (DecimalField/FloatField, null=True), `position_size` (DecimalField/FloatField), `initial_stop_loss` (DecimalField/FloatField), `planned_target` (DecimalField/FloatField, null=True), `pnl` (DecimalField/FloatField, null=True), `rationale` (TextField), `emotion_pre` (TextField, blank=True, null=True), `emotion_during` (TextField, blank=True, null=True), `emotion_post` (TextField, blank=True, null=True), `mistakes` (TextField, blank=True, null=True), `lessons` (TextField, blank=True, null=True), `planned_rr_ratio` (DecimalField/FloatField, null=True), `user_risk_percent` (DecimalField/FloatField), `suggested_position_size` (DecimalField/FloatField, null=True), `account_capital_at_trade` (DecimalField/FloatField).
3.  - [ ] Appropriate constraints (e.g., `null=True`, `blank=True` for optional fields) and representations (`__str__`) are defined for the model.
4.  - [ ] A Django migration is created and successfully applied for the `TradeLog` model.
5.  - [ ] A Django form class named `TradeLogForm` inheriting from `forms.ModelForm` is defined in `dashboard/forms.py`.
6.  - [ ] The `TradeLogForm` is linked to the `TradeLog` model.
7.  - [ ] The `TradeLogForm` includes fields necessary for user input (potentially excluding calculated fields like PnL, PlannedRRRatio, SuggestedPositionSize initially, as they might be calculated elsewhere). Customize widgets if necessary (e.g., `DateInput` for dates, `TextArea` for text fields).
8.  - [ ] Unit tests exist in `dashboard/tests/` verifying the `TradeLog` model creation and the `TradeLogForm` validation (both valid and invalid data). >= 85% code coverage for the model and form definitions.

## Subtasks
1.  - [ ] **Define `TradeLog` Model**
    1.  - [ ] Open `dashboard/models.py`.
    2.  - [ ] Define the `TradeLog` class inheriting from `models.Model`.
    3.  - [ ] Add all specified fields, carefully choosing types (use `DecimalField` for prices/money, specify `max_digits`, `decimal_places`).
    4.  - [ ] Set `null=True`, `blank=True` for fields that are optional (e.g., `exit_date`, `exit_price`, `pnl`, psychological fields, `planned_target`).
    5.  - [ ] Define `__str__` method (e.g., return f"{self.ticker} - {self.entry_date}").
    6.  - [ ] Consider adding `ordering` in `Meta` class (e.g., `['-entry_date']`).
2.  - [ ] **Create and Apply Migration**
    1.  - [ ] Run `python manage.py makemigrations dashboard`.
    2.  - [ ] Review the generated migration file.
    3.  - [ ] Run `python manage.py migrate`.
3.  - [ ] **Create `TradeLogForm`**
    1.  - [ ] Create `dashboard/forms.py` if it doesn't exist.
    2.  - [ ] Import `forms` from `django` and `TradeLog` model.
    3.  - [ ] Define `TradeLogForm(forms.ModelForm)`.
    4.  - [ ] Define inner `Meta` class:
        * Set `model = TradeLog`.
        * Specify `fields = [...]` list, including all fields the user should input directly. Exclude fields like `id`, `pnl`, `planned_rr_ratio`, `suggested_position_size` if they will be calculated/set programmatically later. Include `user_risk_percent`, `account_capital_at_trade`.
        * Optionally define `widgets` for better UI control (e.g., `forms.DateInput(attrs={'type': 'date'})`, `forms.Textarea(attrs={'rows': 3})`).
4.  - [ ] **Implement Tests**
    1.  - [ ] Create/Update `dashboard/tests/test_models.py`.
    2.  - [ ] Write test case for `TradeLog` model: create an instance, save it, retrieve it, check field values.
    3.  - [ ] Create/Update `dashboard/tests/test_forms.py`.
    4.  - [ ] Write test cases for `TradeLogForm`:
        * Test with valid data dictionary, assert `form.is_valid()` is True.
        * Test with invalid data (missing required fields, incorrect types), assert `form.is_valid()` is False, check `form.errors`.
    5.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit tests for the `TradeLog` model (creation, saving) and `TradeLogForm` (validation logic). >= 85% code coverage required.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 10: Implement Trade Logging Interface
## Story
**As a** user
**I want** to access a web interface to create new trade logs using a form and view a list of my previously logged trades
**so that** I can systematically journal my trading activity and review my history.

## Status
Draft

## Context
This story corresponds to Story 6.2 in the PRD. Building upon the `TradeLog` model and `TradeLogForm` created in Story 9, this story involves creating the necessary Django views and templates to provide a user interface for CRUD (Create, Read, Update - focus on Create and Read for MVP) operations on trade logs. Users should be able to fill out the form to log a new trade and view existing logs in a table.

## Estimation
Story Points: 2

## Acceptance Criteria
1.  - [ ] A Django view (e.g., `trade_log_list_view` in `dashboard/views.py`) exists to display a list of existing trade logs.
2.  - [ ] A corresponding URL is defined for the trade log list view.
3.  - [ ] A template (e.g., `dashboard/templates/dashboard/trade_log_list.html`) exists and renders a table displaying key fields from the `TradeLog` objects (e.g., Ticker, Entry Date, Strategy, Entry Price, Exit Price, PnL).
4.  - [ ] The trade log list view retrieves all `TradeLog` objects from the database, ordered appropriately (e.g., by entry date descending).
5.  - [ ] A Django view (e.g., `trade_log_create_view` in `dashboard/views.py`) exists to handle the creation of new trade logs.
6.  - [ ] A corresponding URL is defined for the trade log creation view.
7.  - [ ] A template (e.g., `dashboard/templates/dashboard/trade_log_form.html`) exists that renders the `TradeLogForm` (from Story 9).
8.  - [ ] The creation view handles both GET requests (displaying the empty form) and POST requests (processing submitted form data).
9.  - [ ] On valid POST submission, the view saves the new `TradeLog` object to the PostgreSQL database.
10. - [ ] After successfully saving a new trade log, the user is redirected, typically to the trade log list view.
11. - [ ] If the submitted form is invalid, the creation view re-renders the form template, displaying validation errors.
12. - [ ] A link exists on the list view page to navigate to the creation view page.
13. - [ ] Unit/Integration tests exist for the views, verifying form handling, object creation, context data, redirection, and template rendering using the Django test client. >= 85% code coverage for the views.

## Subtasks
1.  - [ ] **Create List View and URL**
    1.  - [ ] Define `trade_log_list_view(request)` in `dashboard/views.py`.
    2.  - [ ] Query `TradeLog.objects.all().order_by('-entry_date')`.
    3.  - [ ] Pass the queryset to the template context (e.g., `{'trade_logs': logs}`).
    4.  - [ ] Render `dashboard/templates/dashboard/trade_log_list.html`.
    5.  - [ ] Define URL pattern in `dashboard/urls.py` (e.g., `path('tradelog/', views.trade_log_list_view, name='trade_log_list')`).
2.  - [ ] **Create List Template**
    1.  - [ ] Create `dashboard/templates/dashboard/trade_log_list.html`.
    2.  - [ ] Add a link/button to "Log New Trade" pointing to the create view URL.
    3.  - [ ] Create an HTML table.
    4.  - [ ] Iterate through `trade_logs` in the context (`{% for log in trade_logs %}`).
    5.  - [ ] Display key fields (`log.ticker`, `log.strategy`, `log.entry_date`, etc.) in table rows (`<td>`). Format dates/numbers appropriately.
    6.  - [ ] Handle the case where `trade_logs` is empty.
3.  - [ ] **Create Create View and URL**
    1.  - [ ] Define `trade_log_create_view(request)` in `dashboard/views.py`. Use `CreateView` generic view or a function-based view.
    2.  - [ ] Handle GET: create an instance of `TradeLogForm`, pass it to the template context `{'form': form}`, render `trade_log_form.html`.
    3.  - [ ] Handle POST: create `TradeLogForm(request.POST)`. Check `form.is_valid()`. If valid, `form.save()`, redirect to `trade_log_list`. If invalid, re-render template with the invalid form (errors will display automatically).
    4.  - [ ] Define URL pattern (e.g., `path('tradelog/new/', views.trade_log_create_view, name='trade_log_create')`).
4.  - [ ] **Create Form Template**
    1.  - [ ] Create `dashboard/templates/dashboard/trade_log_form.html`.
    2.  - [ ] Add an HTML form tag (`<form method="post">`). Include `{% csrf_token %}`.
    3.  - [ ] Render the form fields using `{{ form.as_p }}` or manually loop through fields for more control (`{% for field in form %}`).
    4.  - [ ] Add a submit button.
5.  - [ ] **Implement Tests**
    1.  - [ ] Create/Update `dashboard/tests/test_views.py`.
    2.  - [ ] Test `trade_log_list_view`: Use test client GET, check status code 200, check correct template used, check context contains trade log list (create some logs in the test DB first).
    3.  - [ ] Test `trade_log_create_view` (GET): Use test client GET, check status 200, check correct template, check context contains an unbound form instance.
    4.  - [ ] Test `trade_log_create_view` (POST - Valid): Use test client POST with valid data, check for redirect (status 302) to the list view URL, check that a new `TradeLog` object was created in the test DB.
    5.  - [ ] Test `trade_log_create_view` (POST - Invalid): Use test client POST with invalid data, check status code 200 (no redirect), check correct template used, check context contains the bound form with errors.
    6.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Integration tests using the Django test client are mandatory for verifying the views (GET/POST requests, form handling, database interaction, context, redirection, template rendering). >= 85% code coverage required for the views.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 11: Implement Risk Calculation and Display
## Story
**As a** user
**I want** the Trade Log form to dynamically calculate and display the planned Risk:Reward Ratio (R:R) and Suggested Position Size based on my inputs for Entry, Stop, Target, Account Capital, and desired Risk Percentage
**so that** I get immediate feedback on the risk parameters of my planned trade before logging it.

## Status
Draft

## Context
This story corresponds to Epic 6 / Story 7.1 from the PRD and involves adding dynamic calculations to the trade logging interface developed in Stories 9 and 10. It requires modifying the `TradeLogForm` and potentially the `trade_log_create_view` and `trade_log_form.html` template. The core task is to implement the calculation logic for Planned R:R and Suggested Position Size using the specified formulas and display these values on the form, updating them as the relevant input fields change (likely requiring JavaScript). A default Account Capital setting should also be configurable.

## Estimation
Story Points: 2

## Acceptance Criteria
1.  - [ ] The `TradeLogForm` in `dashboard/forms.py` includes fields for user input: `entry_price`, `initial_stop_loss` (stop price), `planned_target` (target price), and `user_risk_percent`.
2.  - [ ] A mechanism exists to define the user's default `account_capital` (e.g., a setting in `settings.py` or a user profile field if users were implemented). For MVP, a constant in `settings.py` or reading from `.env` is acceptable. The `TradeLog` model already has `account_capital_at_trade`.
3.  - [ ] JavaScript code is added to the `dashboard/templates/dashboard/trade_log_form.html` template (or linked static file).
4.  - [ ] The JavaScript code attaches event listeners (e.g., 'input' or 'change') to the `entry_price`, `initial_stop_loss`, `planned_target`, and `user_risk_percent` form fields.
5.  - [ ] When these fields change, the JavaScript performs the following calculations:
    * Planned R:R Ratio = `abs(Target - Entry) / abs(Entry - Stop)` (Handle division by zero if Entry equals Stop).
    * Risk Amount Per Share = `abs(Entry - Stop)`.
    * Total Risk Amount = `Account Capital * (User Risk % / 100)`.
    * Suggested Position Size (Shares) = `Total Risk Amount / Risk Amount Per Share` (Handle division by zero).
6.  - [ ] The calculated Planned R:R Ratio and Suggested Position Size are displayed dynamically in designated areas (e.g., read-only form fields or separate `<span>` elements) on the trade log form.
7.  - [ ] The calculated values (`planned_rr_ratio`, `suggested_position_size`) are saved to the corresponding fields in the `TradeLog` model instance when the form is submitted successfully (this might happen in the view's form processing logic *after* `form.is_valid()` but before `form.save()` by modifying `form.instance`, or by adding hidden fields updated by JS). The `account_capital_at_trade` should also be saved.
8.  - [ ] Calculations handle edge cases gracefully (e.g., zero values, missing inputs).
9.  - [ ] A simple unit test exists for the calculation logic if implemented in Python (`core/risk_calculator.py` module is recommended for this). Basic manual testing verifies the dynamic JavaScript updates in the browser. >= 85% code coverage for any Python calculation logic.

## Subtasks
1.  - [ ] **Refactor Calculations (Optional but Recommended)**
    1.  - [ ] Create `core/risk_calculator.py`.
    2.  - [ ] Implement Python functions: `calculate_rr_ratio(entry, stop, target)` and `calculate_position_size(account_capital, risk_percent, entry, stop)`. Include error handling (e.g., zero division).
    3.  - [ ] Add unit tests for these functions in `core/tests/test_risk_calculator.py`.
2.  - [ ] **Update `TradeLogForm` and Model**
    1.  - [ ] Ensure fields `entry_price`, `initial_stop_loss`, `planned_target`, `user_risk_percent`, `account_capital_at_trade` are present in the form/model.
    2.  - [ ] Add read-only fields or placeholders in the form/template for displaying `planned_rr_ratio` and `suggested_position_size`.
3.  - [ ] **Configure Account Capital**
    1.  - [ ] Add `DEFAULT_ACCOUNT_CAPITAL = 100000.0` (or similar) to `settings.py`.
    2.  - [ ] Update the `trade_log_create_view` to fetch this setting and potentially pass it to the template/JS or use it when saving the `account_capital_at_trade` field. Set `account_capital_at_trade` on `form.instance` before saving.
4.  - [ ] **Implement JavaScript Calculations**
    1.  - [ ] Create a static JS file (e.g., `static/dashboard/js/risk_calc.js`) and link it in the `trade_log_form.html` template (ensure static files are configured).
    2.  - [ ] Get references to the input fields (entry, stop, target, risk %) and display elements (for R:R, size).
    3.  - [ ] Add event listeners (`'input'`) to the input fields.
    4.  - [ ] Inside the event handler function:
        * Get current values from input fields, parse them as floats.
        * Get account capital (passed from view via template variable or hardcoded for simplicity initially).
        * Perform the R:R and Position Size calculations using the formulas. Handle invalid inputs (NaN, zero risk amount).
        * Update the content of the display elements with the calculated values (formatted nicely, e.g., 2 decimal places).
5.  - [ ] **Update View to Save Calculated Values**
    1.  - [ ] In `trade_log_create_view`, within the `if form.is_valid():` block:
        1.  - [ ] Get the validated `entry`, `stop`, `target`, `risk_percent` from `form.cleaned_data`.
        2.  - [ ] Get `account_capital` (from settings or form).
        3.  - [ ] Call the Python calculation functions from `core.risk_calculator` (if created) or perform calculations directly.
        4.  - [ ] Set `form.instance.planned_rr_ratio = calculated_rr`.
        5.  - [ ] Set `form.instance.suggested_position_size = calculated_size`.
        6.  - [ ] Set `form.instance.account_capital_at_trade = account_capital`.
        7.  - [ ] Call `form.save()`.
6.  - [ ] **Manual Testing**
    1.  - [ ] Load the trade log form in a browser.
    2.  - [ ] Enter values into the relevant fields and verify that the R:R and position size update dynamically and correctly. Test edge cases.
    3.  - [ ] Submit a valid form and verify the calculated values are saved correctly in the database (view via list view or admin).
7.  - [ ] **Update Unit Tests**
    1.  - [ ] Add tests for Python calculation functions if created.
    2.  - [ ] Update view tests to ensure the calculated fields (`planned_rr_ratio`, `suggested_position_size`, `account_capital_at_trade`) are correctly set on the model instance before saving during a valid POST request.

## Testing Requirements:**
* Unit tests for any Python calculation logic (>= 85% coverage). Update view integration tests to verify calculated values are saved correctly. Manual browser testing is required for the dynamic JavaScript updates.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 12: Integrate Alpaca API for Live Market Data Observation
## Story
**As a** user
**I want** to view the latest quote data for a specified stock ticker fetched from the Alpaca API within the Django interface
**so that** I can observe current market prices for potential trades (without executing trades).

## Status
Draft

## Context
This story corresponds to Epic 7 / Story 8.1 from the PRD. It focuses on integrating the Alpaca API for fetching live (or near-live) quote data for *observation* purposes only. It involves installing the Alpaca library, creating a `core/market_data.py` module to handle API interaction (reading keys from `.env`), implementing a function to fetch the latest quote, and creating a simple Django view/template section to display this data with a basic refresh mechanism.

## Estimation
Story Points: 2

## Acceptance Criteria
1.  - [ ] The `alpaca-trade-api-python` (or newer `alpaca-py`) library is installed and added to `requirements.txt`.
2.  - [ ] Alpaca API Key ID, Secret Key, and Paper Trading URL are added to the `.env` file.
3.  - [ ] A `core/market_data.py` module exists.
4.  - [ ] A function exists in `core/market_data.py` that initializes the Alpaca API client using credentials read from `.env`. Use the paper trading endpoint.
5.  - [ ] A function exists in `core/market_data.py` (e.g., `get_latest_quote(ticker)`) that takes a ticker symbol and uses the Alpaca API client to fetch the latest quote data (e.g., bid price, ask price, last trade price).
6.  - [ ] The `get_latest_quote` function handles potential API errors gracefully (e.g., invalid ticker, connection issues) and logs them.
7.  - [ ] A Django view and template (or a section within an existing template like a dashboard) are created to display the fetched quote data.
8.  - [ ] The view allows the user to specify a ticker (e.g., via a form input) and calls `get_latest_quote` to fetch the data.
9.  - [ ] The fetched quote data (bid, ask, last price) is displayed clearly in the template.
10. - [ ] A basic refresh mechanism (e.g., a manual refresh button that re-submits the ticker or uses JavaScript AJAX) is implemented to update the displayed quote.
11. - [ ] Unit tests exist for the `core/market_data.py` functions, mocking the Alpaca API client and responses. >= 85% code coverage for this module. Basic view testing verifies calling the fetch function.

## Subtasks
1.  - [ ] **Install Library and Update .env**
    1.  - [ ] Install `alpaca-py`: `pip install alpaca-py`. (Prefer `alpaca-py` over older `alpaca-trade-api-python`).
    2.  - [ ] Update `requirements.txt`.
    3.  - [ ] Add `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `ALPACA_PAPER_URL` to `.env`.
2.  - [ ] **Create `core/market_data.py` Module**
    1.  - [ ] Create the file `core/market_data.py`.
    2.  - [ ] Add imports (`os`, `dotenv`, `alpaca.trading.client`, `alpaca.data.live.StockDataStream`, `alpaca.data.requests`).
    3.  - [ ] Implement loading of Alpaca keys/URL from `.env`.
3.  - [ ] **Implement Alpaca Client Initialization**
    1.  - [ ] Create a function or instantiate a `TradingClient` at the module level, passing keys and paper=True.
4.  - [ ] **Implement `get_latest_quote` Function**
    1.  - [ ] Define `get_latest_quote(ticker)`.
    2.  - [ ] Use the `TradingClient` instance (or potentially `StockHistoricalDataClient` for snapshots). Example using REST snapshot:
        ```python
        from alpaca.data.requests import StockLatestQuoteRequest
        from alpaca.data.historical import StockHistoricalDataClient
        # client = StockHistoricalDataClient(api_key, secret_key)
        request_params = StockLatestQuoteRequest(symbol_or_symbols=[ticker])
        latest_quote = client.get_stock_latest_quote(request_params)
        # Process latest_quote[ticker] object (e.g., .bid_price, .ask_price)
        return processed_data # e.g., a dictionary
        ```
    3.  - [ ] Implement `try...except` block for API errors (e.g., `APIError`) and log errors. Return `None` or raise custom exception on failure.
5.  - [ ] **Create Django View/Template Section**
    1.  - [ ] Decide where to display this: a new view/template or add to an existing one (e.g., `dashboard_view`). Create view function if needed.
    2.  - [ ] Create/modify the template. Add a form with a text input for 'ticker' and a submit button.
    3.  - [ ] Add a designated area (`div`) to display the quote results.
6.  - [ ] **Implement View Logic**
    1.  - [ ] Handle GET/POST request.
    2.  - [ ] On POST (or GET with ticker param): Get the ticker from the request.
    3.  - [ ] Call `core.market_data.get_latest_quote(ticker)`.
    4.  - [ ] Pass the fetched quote dictionary (or None) to the template context.
    5.  - [ ] Render the template.
7.  - [ ] **Implement Refresh Mechanism**
    1.  - [ ] **Option A (Simple Refresh Button):** The submit button in the form acts as the refresh.
    2.  - [ ] **Option B (AJAX):** Add JavaScript to handle the form submission, prevent default page reload, send an AJAX request to a dedicated Django endpoint (or the same view), fetch the quote, and update the display area dynamically. Add a 'Refresh' button triggering the AJAX call.
8.  - [ ] **Implement Tests**
    1.  - [ ] Create `core/tests/test_market_data.py`.
    2.  - [ ] Write tests for `get_latest_quote` using `unittest.mock` to mock the `alpaca-py` client and its methods (`get_stock_latest_quote`). Simulate successful responses and API errors.
    3.  - [ ] Update view tests (or create new ones) to verify the view calls `get_latest_quote` and passes data to the context. Mock the function call.
    4.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit tests with mocked Alpaca API calls are mandatory for `core/market_data.py` (>= 85% coverage). Integration tests for the view should mock the call to `get_latest_quote`. Manual testing required to verify interaction with the actual (paper) Alpaca API and the refresh mechanism.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 13: Implement Static Trading Plan Checklist
## Story
**As a** developer
**I want** to implement a static checklist related to the Classic Breakout strategy, link its status to a TradeLog entry, and provide an interface for the user to check items off
**so that** the user is encouraged to follow a disciplined trading process before or during trade logging.

## Status
Draft

## Context
This story corresponds to Epic 8 / Story 9.1 in the PRD. It involves adding a predefined checklist feature associated with each trade log. Tasks include defining the checklist items, creating a new Django model (`TradeChecklistStatus`) to store the status of each item for each trade, creating a view/template segment (likely integrated into the trade log form/detail view) to display the checklist and allow interaction (checking/unchecking), and saving the state to the database.

## Estimation
Story Points: 2

## Acceptance Criteria
1.  - [ ] A predefined list of checklist steps for the Classic Breakout strategy is defined (e.g., "Consolidation Found?", "Volume Confirmed?", "Breakout Confirmed?", "ATR Stop Set?", "R:R > 2?", "Position Sized?"). This could be a constant list in `settings.py` or `dashboard/models.py`.
2.  - [ ] A Django model named `TradeChecklistStatus` is defined in `dashboard/models.py`.
3.  - [ ] The `TradeChecklistStatus` model includes fields: `trade_log` (ForeignKey to `TradeLog`, related_name='checklist_items'), `checklist_item` (CharField), `is_checked` (BooleanField, default=False). A unique constraint on `(trade_log, checklist_item)` should exist.
4.  - [ ] A Django migration is created and successfully applied for the `TradeChecklistStatus` model.
5.  - [ ] The trade log creation/editing view (`trade_log_create_view` or a new `trade_log_update_view`) is modified (or a new view created) to handle the checklist.
6.  - [ ] When a new `TradeLog` is created (or potentially when viewed/edited), corresponding `TradeChecklistStatus` items are automatically created for it based on the predefined list, if they don't already exist.
7.  - [ ] The trade log form template (`trade_log_form.html` or a detail template) is updated to display the checklist items associated with the current `TradeLog`.
8.  - [ ] Each checklist item is displayed with a checkbox reflecting its `is_checked` status.
9.  - [ ] User interaction with the checkboxes (checking/unchecking) triggers saving of the updated `is_checked` status to the corresponding `TradeChecklistStatus` object in the database (this likely requires JavaScript AJAX calls to a dedicated update view or handling within the main form submission).
10. - [ ] Unit/Integration tests verify the creation of `TradeChecklistStatus` items, the view logic for displaying them, and the logic for updating their status. >= 85% code coverage for new models/views/logic.

## Subtasks
1.  - [ ] **Define Checklist Items**
    1.  - [ ] Define the list of strings in `settings.py` or `dashboard/models.py` (e.g., `CLASSIC_BREAKOUT_CHECKLIST = [...]`).
2.  - [ ] **Define `TradeChecklistStatus` Model**
    1.  - [ ] Open `dashboard/models.py`.
    2.  - [ ] Define `TradeChecklistStatus(models.Model)`.
    3.  - [ ] Add `trade_log = models.ForeignKey(TradeLog, on_delete=models.CASCADE, related_name='checklist_items')`.
    4.  - [ ] Add `checklist_item = models.CharField(max_length=255)`.
    5.  - [ ] Add `is_checked = models.BooleanField(default=False)`.
    6.  - [ ] Add `Meta` class with `unique_together = ('trade_log', 'checklist_item')`.
3.  - [ ] **Create and Apply Migration**
    1.  - [ ] Run `python manage.py makemigrations dashboard`.
    2.  - [ ] Run `python manage.py migrate`.
4.  - [ ] **Implement Checklist Item Creation Logic**
    1.  - [ ] Modify the view where `TradeLog` is created or displayed (e.g., `trade_log_create_view` after saving, or a `trade_log_detail_view`).
    2.  - [ ] After getting/creating a `trade_log` instance, iterate through the predefined `CLASSIC_BREAKOUT_CHECKLIST`.
    3.  - [ ] For each item text, use `TradeChecklistStatus.objects.get_or_create(trade_log=trade_log, checklist_item=item_text)` to ensure checklist items exist for the trade.
5.  - [ ] **Update Template to Display Checklist**
    1.  - [ ] In `trade_log_form.html` (or a detail view template), add a section for the checklist.
    2.  - [ ] In the corresponding view, ensure the `trade_log` instance (with related `checklist_items`) is passed to the context.
    3.  - [ ] Iterate through `trade_log.checklist_items.all` in the template.
    4.  - [ ] For each `item`, display `item.checklist_item` text and an HTML checkbox (`<input type="checkbox">`).
    5.  - [ ] Set the `checked` attribute based on `item.is_checked`.
    6.  - [ ] Add data attributes to the checkbox (e.g., `data-item-id="{{ item.id }}"`) to identify it for JS/AJAX.
6.  - [ ] **Implement Checklist Status Saving**
    1.  - [ ] **Option A (Save on TradeLog Form Submit):** Add hidden inputs or modify form handling to include checklist statuses in the main POST data. Update view logic to parse and save statuses. (Less interactive).
    2.  - [ ] **Option B (AJAX Update):**
        1.  - [ ] Create a new Django view (e.g., `update_checklist_item_status`) that accepts POST requests with `item_id` and `is_checked` status.
        2.  - [ ] Define a URL for this view (e.g., `path('tradelog/checklist/update/', ...)`).
        3.  - [ ] Add JavaScript to the template: attach 'change' event listeners to the checkboxes.
        4.  - [ ] On change, get the `item_id` and the new `is_checked` status.
        5.  - [ ] Send an AJAX POST request (using Fetch API) to the update view URL with this data (include CSRF token).
        6.  - [ ] The update view finds the `TradeChecklistStatus` object by ID, updates `is_checked`, saves it, and returns a JSON response (e.g., `{'status': 'ok'}`). Handle errors.
7.  - [ ] **Implement Tests**
    1.  - [ ] Test `TradeChecklistStatus` model creation.
    2.  - [ ] Test the logic for auto-creating checklist items for a new trade log (e.g., in the `trade_log_create_view` test).
    3.  - [ ] Test the template rendering to ensure checklist items are displayed correctly.
    4.  - [ ] Test the AJAX update view (if using Option B): use test client POST with data, check object status is updated in DB, check JSON response. Mock login if needed.
    5.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit/Integration tests for the model, checklist creation logic, and status update mechanism (view/AJAX endpoint). >= 85% code coverage required. Manual testing needed for checkbox interaction.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 14: Integrate Gemini API for Educational Context
## Story
**As a** developer
**I want** to integrate the Google Gemini API to provide basic educational context about the Classic Breakout strategy
**so that** the user can get quick explanations for relevant trading concepts directly within the application.

## Status
Draft

## Context
This story corresponds to Epic 9 / Story 10.1 from the PRD. It focuses on the backend integration with Google's Gemini API. Tasks include installing the necessary library, creating a `core/educational_guidance.py` module to encapsulate API interaction (reading the key from `.env`), and developing basic prompt templates tailored to explaining concepts related to the Classic Breakout strategy implemented earlier.

## Estimation
Story Points: 1

## Acceptance Criteria
1.  - [ ] The `google-generativeai` Python library is installed and added to `requirements.txt`.
2.  - [ ] The Google Gemini API key is added to the `.env` file (`GEMINI_API_KEY`).
3.  - [ ] A `core/educational_guidance.py` module exists.
4.  - [ ] A function exists in `core/educational_guidance.py` that initializes the Gemini client using the API key read from `.env`.
5.  - [ ] A function exists in `core/educational_guidance.py` (e.g., `get_educational_context(topic)`) that takes a topic string as input.
6.  - [ ] This function selects or constructs a basic, predefined prompt based on the input topic (e.g., "Explain volume confirmation for breakouts in simple terms for a beginner swing trader focusing on the Classic Breakout strategy.", "Explain how an ATR based stop loss works using ATR(14) * 2.0."). Keep prompts focused and related to the MVP's context.
7.  - [ ] The function calls the Gemini API (e.g., using `genai.GenerativeModel('gemini-pro').generate_content(...)`) with the constructed prompt.
8.  - [ ] The function handles potential API errors gracefully (e.g., API key issues, network errors, content filtering) and logs them.
9.  - [ ] The function returns the relevant text content from the Gemini API response, or None/error message upon failure.
10. - [ ] Unit tests exist for `core/educational_guidance.py`, mocking the `google-generativeai` client and responses, verifying prompt construction and response handling. >= 85% code coverage for this module.

## Subtasks
1.  - [ ] **Install Library and Update .env**
    1.  - [ ] Install `google-generativeai`: `pip install google-generativeai`.
    2.  - [ ] Update `requirements.txt`.
    3.  - [ ] Add `GEMINI_API_KEY` to `.env`.
2.  - [ ] **Create `core/educational_guidance.py` Module**
    1.  - [ ] Create the file `core/educational_guidance.py`.
    2.  - [ ] Add imports (`os`, `dotenv`, `google.generativeai as genai`, `logging`).
    3.  - [ ] Implement loading of Gemini API key from `.env`.
    4.  - [ ] Configure the Gemini client: `genai.configure(api_key=...)`.
3.  - [ ] **Develop Basic Prompt Templates**
    1.  - [ ] Define a dictionary or function to map input topics (e.g., 'volume_confirmation', 'atr_stop') to specific, focused prompt strings suitable for the Gemini API. Include context about swing trading and the classic breakout strategy.
4.  - [ ] **Implement `get_educational_context` Function**
    1.  - [ ] Define `get_educational_context(topic)`.
    2.  - [ ] Look up or construct the prompt based on the `topic`. If topic not found, return an error message.
    3.  - [ ] Select the Gemini model (e.g., `model = genai.GenerativeModel('gemini-pro')`).
    4.  - [ ] Implement `try...except` block around the API call: `response = model.generate_content(prompt)`. Catch potential exceptions (e.g., `google.api_core.exceptions`, check library specifics).
    5.  - [ ] Log errors.
    6.  - [ ] Check `response.prompt_feedback` for blocking reasons.
    7.  - [ ] Extract and return `response.text`. If errors or blocking occurred, return None or an appropriate error message.
5.  - [ ] **Implement Tests**
    1.  - [ ] Create `core/tests/test_educational_guidance.py`.
    2.  - [ ] Write tests using `unittest.mock` to patch `genai.configure` and `genai.GenerativeModel`.
    3.  - [ ] Mock the `generate_content` method to return mock response objects (including `text` and `prompt_feedback` attributes).
    4.  - [ ] Test `get_educational_context` for different topics, verifying correct prompt construction and response/error handling.
    5.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Unit tests with mocked Gemini API calls are mandatory for `core/educational_guidance.py` (>= 85% coverage). Verify prompt generation, response parsing, and error handling.

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...

---

# Story 15: Implement Contextual Guidance Interface
## Story
**As a** user
**I want** to click buttons or links in relevant sections of the application (e.g., near strategy explanations or trade log fields) to trigger educational queries to the Gemini API and see the response displayed
**so that** I can easily access contextual help about the Classic Breakout strategy concepts while I'm learning or trading.

## Status
Draft

## Context
This story corresponds to Epic 9 / Story 10.2 from the PRD and builds on the Gemini API integration from Story 14. It focuses on creating the user interface elements and Django view logic to connect user actions (clicking a help button) to the backend `core.educational_guidance.get_educational_context` function and display the returned explanation in the UI.

## Estimation
Story Points: 1

## Acceptance Criteria
1.  - [ ] UI elements (e.g., small help icons `(?)`, buttons, or links) are added next to relevant terms or sections in existing templates (e.g., `trade_log_form.html`, strategy description areas, backtest results page).
2.  - [ ] These UI elements are linked to specific educational topics (e.g., 'volume_confirmation', 'atr_stop', 'chandelier_exit', 'rr_ratio').
3.  - [ ] Clicking a UI element triggers a request to a Django view responsible for handling educational queries. This might involve JavaScript/AJAX or dedicated GET URLs.
4.  - [ ] A Django view (e.g., `educational_guidance_view` in `dashboard/views.py`) exists to handle these requests.
5.  - [ ] The view receives the requested topic, calls `core.educational_guidance.get_educational_context(topic)`, and retrieves the explanation text or error message.
6.  - [ ] The view returns the explanation text, likely as a JSON response if using AJAX, or renders it within a specific template section/modal if using full page reloads or dedicated pages.
7.  - [ ] A designated area in the UI (e.g., a modal dialog, a dedicated panel, or an area dynamically appearing near the clicked element) displays the formatted response received from the view.
8.  - [ ] Basic error handling is displayed in the UI if the Gemini API call fails (e.g., "Could not retrieve explanation.").
9.  - [ ] Unit/Integration tests verify the view logic correctly calls the guidance module and handles responses/errors. >= 85% code coverage for the view.

## Subtasks
1.  - [ ] **Add UI Trigger Elements**
    1.  - [ ] Identify relevant locations in templates (`trade_log_form.html`, potentially `backtest_view.html`, `chart_view.html`, or a new strategy explanation page).
    2.  - [ ] Add small buttons, icons (`<button data-topic="atr_stop">(?)</button>`), or links next to terms like "ATR Stop", "Volume Confirmation", "R:R Ratio", etc. Store the corresponding topic key in a data attribute.
2.  - [ ] **Create Educational Guidance View and URL**
    1.  - [ ] Define `educational_guidance_view(request)` in `dashboard/views.py`.
    2.  - [ ] Define a URL pattern (e.g., `path('education/query/', views.educational_guidance_view, name='education_query')`).
3.  - [ ] **Implement View Logic**
    1.  - [ ] The view should expect the `topic` (e.g., via GET parameter `request.GET.get('topic')` or POST data if using AJAX form).
    2.  - [ ] Validate the received topic.
    3.  - [ ] Call `explanation = core.educational_guidance.get_educational_context(topic)`.
    4.  - [ ] Handle the case where `explanation` is None or an error message.
    5.  - [ ] Return a `JsonResponse({'explanation': explanation})` if using AJAX. If not using AJAX, render a simple template displaying the explanation.
4.  - [ ] **Implement Frontend Display Logic (AJAX recommended)**
    1.  - [ ] Add JavaScript (e.g., in `static/dashboard/js/education.js`) linked from relevant templates.
    2.  - [ ] Add event listeners ('click') to the UI trigger elements added in step 1.
    3.  - [ ] In the event handler:
        * Prevent default link/button behavior if necessary.
        * Get the topic from the element's data attribute (`event.target.dataset.topic`).
        * Make an AJAX call (e.g., using Fetch API) to the `education_query` URL, passing the topic as a query parameter.
        * Handle the JSON response.
        * Display the `response.explanation` text in a designated UI element (e.g., update the content of a modal window or a specific `div`). Use a library like Bootstrap modals or create a simple display area. Display errors appropriately.
    4.  - [ ] Add the necessary HTML structure for the display area (e.g., modal).
5.  - [ ] **Implement Tests**
    1.  - [ ] Create/Update `dashboard/tests/test_views.py`.
    2.  - [ ] Test `educational_guidance_view`:
        * Use test client GET/POST to simulate requests with different topics.
        * Mock `core.educational_guidance.get_educational_context` to return sample explanations or error conditions.
        * Assert the view returns the correct `JsonResponse` or renders the correct template context.
    3.  - [ ] Run tests with coverage.

## Testing Requirements:**
* Integration tests for the Django view using the test client, mocking the call to the core guidance module (>= 85% coverage). Manual testing is required to verify the UI elements trigger the request and display the response correctly (including modal/display behavior).

## Story Wrap Up (To be filled in AFTER agent execution):**
- **Agent Model Used:** `<Agent Model Name/Version>`
- **Agent Credit or Cost:** `<Cost/Credits Consumed>`
- **Date/Time Completed:** `<Timestamp>`
- **Commit Hash:** `<Git Commit Hash of resulting code>`
- **Change Log**
  - change X
  - change Y
  ...