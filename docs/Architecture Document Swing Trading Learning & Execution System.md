# Architecture Document: Swing Trading Learning & Execution System (MVP v1.0)

**Version:** 1.1 (Updated Python Version)
**Date:** 2025-04-24
**Based on:** PRD: Swing Trading Learning & Execution System (MVP v1.0) and provided research documents.

## 1. Introduction

This document outlines the software architecture for the Minimum Viable Product (MVP) of the Swing Trading Learning & Execution System. Its purpose is to serve as a detailed technical blueprint guiding the development process, ensuring consistency, clarity, and adherence to the requirements specified in the associated Product Requirements Document (PRD). The system aims to provide a foundational, locally-run platform for the primary user to learn and practice swing trading, focusing initially on the "Classic Breakout" strategy.

This architecture is based on the finalized PRD (MVP v1.0) and insights gleaned from the provided research documents. It emphasizes modularity within a monolithic structure, specific technology choices, and clear standards to facilitate development, potentially involving AI coding agents.

**Note on Evolution:** While this document reflects the architecture based on the current PRD, findings during implementation (e.g., UI generation based on PRD specs, initial coding stages, performance testing) may lead to necessary PRD refinements. Such refinements could, in turn, necessitate updates to this Architecture Document to maintain alignment between requirements and the technical implementation.

## 2. Architectural Goals and Constraints

### Goals:

* **Foundational Learning Platform:** Establish a robust base for learning and practicing the specified "Classic Breakout" swing trading strategy.
* **Systematic Data Handling:** Provide structured methods for fetching, storing (time-series optimized), and visualizing basic stock market data (OHLCV).
* **Strategy Backtesting:** Enable reliable backtesting of the defined strategy using the Backtrader framework integrated with historical data.
* **Structured Journaling:** Implement a detailed trade logging system incorporating psychological factors and risk metrics.
* **Basic Risk Feedback:** Provide immediate calculation and display of planned Risk:Reward Ratio and Suggested Position Size.
* **Live Data Observation:** Allow connection to live market data (Alpaca) for observation purposes.
* **Disciplined Trading Support:** Incorporate a static Trading Plan Checklist.
* **Contextual Education:** Integrate Gemini API for basic educational support related to the implemented strategy.
* **Modularity for Future Growth:** Design components (data, backtesting, UI, etc.) with clear responsibilities, even within the monolith, to ease future maintenance and potential expansion (including adding new strategies).
* **Local Execution:** Ensure the entire system runs effectively on the user's local machine (macOS M3 Pro specified) without cloud dependencies for the MVP.

### Constraints:

* **Technology Stack:** Adherence to the specified stack: Python 3.12.x, Django 5.x, PostgreSQL 16.x, TimeScaleDB (Latest), Plotly, Backtrader, pandas-ta, yfinance, alpha-vantage, alpaca-trade-api-python, google-generativeai.
* **Architecture Pattern:** Local Monolith Web Application using Django.
* **Deployment:** Local execution only for MVP; no cloud deployment or containerization.
* **Scope:** Strictly limited to the features defined in the PRD MVP v1.0. Features listed as "Out of Scope Post MVP" are explicitly excluded.
* **Target Platform:** macOS (Ventura/Sonoma on M3 Pro).
* **Development Environment:** Anaconda for environment management.
* **User:** Single primary user for the MVP.

## 3. Architectural Representation / Views

### 3.1. High-Level Overview

* **Architectural Style:** **Local Monolithic Web Application**.
    * **Justification:** A monolith is suitable for this MVP due to the single-user focus, local deployment constraint, and the need for tight integration between components (UI, backtesting, data). It simplifies development, deployment (local setup), and debugging for the initial version compared to microservices or serverless approaches, which would add unnecessary complexity. Modularity will be enforced at the code level within the monolith.
* **High-Level Diagram (C4 Context/Container Style):**

    ```mermaid
    graph TD
        User[Primary User] -- Interacts via Browser --> DjangoApp{Swing Trading System (Local Django App)};

        subgraph Local Machine (macOS M3 Pro)
            DjangoApp -- Serves UI/Orchestrates --> DjangoServer[Django Dev Server];
            DjangoApp -- Uses --> PythonModules[Core Python Modules];
            DjangoApp -- Stores/Retrieves Data --> PostgresDB[(PostgreSQL w/ TimeScaleDB)];

            PythonModules -- Uses --> BacktraderLib[Backtrader Lib];
            PythonModules -- Uses --> TALib[pandas-ta Lib];
            PythonModules -- Uses --> PlottingLib[Plotly Lib];
            PythonModules -- Calls --> ExternalAPIs[External APIs];
            PythonModules -- Stores/Retrieves Data --> PostgresDB;

            PostgresDB -- TimeScaleDB Extension --> TSD[TimeScaleDB Features];
        end

        subgraph External Services
            ExternalAPIs -- Fetches Market Data --> YFinanceAPI[Yahoo Finance];
            ExternalAPIs -- Fetches Market Data --> AlphaVantageAPI[Alpha Vantage];
            ExternalAPIs -- Fetches Live Quotes --> AlpacaAPI[Alpaca API];
            ExternalAPIs -- Fetches Educational Content --> GeminiAPI[Google Gemini API];
        end

        style User fill:#lightblue
        style DjangoApp fill:#lightgreen
        style PythonModules fill:#lightyellow
        style PostgresDB fill:#orange
        style ExternalAPIs fill:#lightgrey
    ```

### 3.2. Component View

* **Major Components:** The system is divided into logical components, primarily represented by Django apps and core Python modules.
* **Diagram (C4 Component Style):**

    ```mermaid
    graph TD
        subgraph DjangoApp [Django Web Application (swing_project & dashboard)]
            UI[Django Templates/Views/Forms (dashboard)] -- Renders HTML/Handles Requests --> UserInterface(User Interface - Browser)
            UI -- Calls --> CoreAPI[Core Logic Interface (via Views)]
            UI -- Interacts with --> DjangoORM[Django ORM (dashboard.models)]
            DjangoORM -- Persists/Queries --> Database[(PostgreSQL/TimeScaleDB)]
        end

        subgraph CoreModules [Core Python Modules (core/)]
            CoreAPI -- Delegates to --> DataHandler[data_handler.py]
            CoreAPI -- Delegates to --> BacktesterMod[backtester.py]
            CoreAPI -- Delegates to --> StrategyMod[strategies.py]
            CoreAPI -- Delegates to --> RiskCalc[risk_calculator.py]
            CoreAPI -- Delegates to --> MarketData[market_data.py]
            CoreAPI -- Delegates to --> EduGuide[educational_guidance.py]
            CoreAPI -- Uses --> VizHelper[Visualization Helper (in dashboard.views)]

            DataHandler -- Fetches data --> ExternalDataAPIs[yfinance, alpha-vantage libs]
            DataHandler -- Stores/Retrieves data --> Database
            BacktesterMod -- Uses --> BacktraderLib[Backtrader Lib]
            BacktesterMod -- Uses --> StrategyMod
            BacktesterMod -- Retrieves data --> DataHandler
            BacktesterMod -- Returns results --> CoreAPI
            StrategyMod -- Defines --> StrategyClasses[Strategy Classes (Backtrader Strategy)]
            StrategyMod -- Uses --> TechAnalysisLib[pandas-ta Lib]
            RiskCalc -- Calculates R:R, Size --> CoreAPI
            MarketData -- Fetches quotes --> AlpacaLib[alpaca-trade-api-python Lib]
            MarketData -- Returns data --> CoreAPI
            EduGuide -- Calls --> GeminiLib[google-generativeai Lib]
            EduGuide -- Returns response --> CoreAPI
            VizHelper -- Uses --> PlottingLib[Plotly Lib]
            VizHelper -- Retrieves data --> DjangoORM
            VizHelper -- Generates Charts --> UI
        end

        ExternalDataAPIs --> ExternalServices[External Data Services]
        AlpacaLib --> AlpacaService[Alpaca API Service]
        GeminiLib --> GeminiService[Google Gemini API Service]

        style UI fill:#lightgreen
        style DjangoORM fill:#palegreen
        style CoreAPI fill:#lightyellow
        style CoreModules fill:#lightyellow
        style Database fill:#orange
    ```

* **Component Responsibilities:**
    * **Django App (swing\_project & dashboard):**
        * `swing_project`: Main Django project settings, URL routing, WSGI config.
        * `dashboard`: Handles all user-facing interactions.
            * `models.py`: Defines data structures (OHLCV, TradeLog, ChecklistStatus) using Django ORM.
            * `forms.py`: Defines forms for data input (Trade Log, Backtest Config).
            * `views.py`: Contains logic to handle HTTP requests, interact with core modules, manage ORM queries, call visualization helpers, and render templates. *Handles selection of strategy for backtesting.*
            * `templates/`: HTML templates for rendering the UI. *Includes controls for selecting strategies.*
            * `urls.py`: Defines URL patterns for the dashboard app.
            * `management/commands/`: Holds commands for CSV import/export.
            * **Visualization Helper (within `views.py` or separate `utils.py`):** Contains functions to fetch data (via ORM) and generate Plotly charts for embedding in templates.
    * **Core Python Modules (core/):** Contains backend logic decoupled from Django's web concerns.
        * `data_handler.py`: Fetches historical data (yfinance, Alpha Vantage), cleans/validates it, and saves it to the database (interacting potentially via Django ORM or direct SQL for bulk operations if needed). Handles API key management.
        * `strategies.py`: Defines Backtrader strategy classes (e.g., `ClassicBreakout`). Implements strategy rules using Backtrader's API and potentially pandas-ta for indicators. **Designed for extension with new strategy classes.**
        * `backtester.py`: Orchestrates Backtrader simulations. Configures Cerebro engine, data feeds (from DB via `data_handler` or direct query), **dynamically loads selected strategy**, analyzers (TradeAnalyzer, SQN), commission/slippage. Runs backtests and extracts results. **Needs modification to accept strategy selection.**
        * `risk_calculator.py`: Contains pure Python functions to calculate Risk:Reward ratio and Suggested Position Size based on input parameters (Entry, Stop, Target, Capital, Risk %).
        * `market_data.py`: Handles interaction with the Alpaca API (using `alpaca-trade-api-python`) to fetch live quotes for observation. Reads API keys from `.env`.
        * `educational_guidance.py`: Manages interaction with the Google Gemini API (using `google-generativeai`). Constructs prompts based on user queries/context, calls the API, and processes responses. Reads API key from `.env`.
    * **External Libraries:** (Backtrader, pandas-ta, Plotly, yfinance, etc.) Provide specific functionalities called by the core modules or Django app.
    * **Database (PostgreSQL/TimeScaleDB):** Stores all persistent data: OHLCV time-series, trade logs, checklist statuses. TimeScaleDB extension optimizes time-series storage and querying.

### 3.3. Data View

* **Primary Data Models:**
    * **OHLCVData:** Stores historical Open, High, Low, Close, Volume data for stock tickers.
        * Fields: `timestamp` (DateTime, TimeScaleDB time dimension), `ticker` (String), `open` (Decimal/Float), `high` (Decimal/Float), `low` (Decimal/Float), `close` (Decimal/Float), `volume` (BigInteger).
        * TimeScaleDB Hypertable: Configured on the `timestamp` column for efficient time-series querying. Chunking interval likely daily or weekly.
        * Indexes: Composite index on `(ticker, timestamp)` is crucial for efficient lookups.
    * **TradeLog:** Stores details of manually logged trades.
        * Fields: `id` (PK), `ticker` (String), `strategy` (String) <--- *Stores strategy used*, `entry_date` (DateTime), `exit_date` (DateTime, nullable), `entry_price` (Decimal/Float), `exit_price` (Decimal/Float, nullable), `position_size` (Decimal/Float), `initial_stop_loss` (Decimal/Float), `planned_target` (Decimal/Float, nullable), `pnl` (Decimal/Float, nullable), `rationale` (Text), `emotion_pre` (Text, nullable), `emotion_during` (Text, nullable), `emotion_post` (Text, nullable), `mistakes` (Text, nullable), `lessons` (Text, nullable), `planned_rr_ratio` (Decimal/Float, nullable), `user_risk_percent` (Decimal/Float), `suggested_position_size` (Decimal/Float, nullable), `account_capital_at_trade` (Decimal/Float).
        * Indexes: On `ticker`, `entry_date`, `strategy`.
    * **TradeChecklistStatus:** Stores the status of the checklist items associated with a trade log entry.
        * Fields: `id` (PK), `trade_log` (ForeignKey to TradeLog), `checklist_item` (String), `is_checked` (Boolean).
        * Indexes: On `trade_log`.
* **Database Technology:** **PostgreSQL version 16.x** with the **TimeScaleDB extension (Latest compatible version)**.
* **Data Access Strategy:**
    * **Django ORM:** Primarily used for interacting with `TradeLog` and `TradeChecklistStatus` models within Django views and forms (CRUD operations). Standard Django migrations will manage schema changes for these models.
    * **TimeScaleDB Interaction (OHLCVData):**
        * **Potential ORM Issue:** As noted by the user, Django's ORM might not always generate the most performant queries for complex time-series operations or bulk inserts/updates on TimeScaleDB hypertables. Standard ORM queries for simple filtering (e.g., get data for ticker 'AAPL' between two dates) should be acceptable initially.
        * **Mitigation Strategy:**
            1.  **django-timescaledb Library:** Investigate using third-party libraries like `django-timescaledb` which provide custom model managers and fields potentially better integrated with TimeScaleDB features (hypertables, continuous aggregates). This is the preferred approach to keep code idiomatic Django.
            2.  **Raw SQL / Custom Managers:** For performance-critical operations (e.g., bulk inserting thousands of OHLCV records from `data_handler.py`, complex aggregations for charting or backtesting data feeds), bypass the ORM using Django's `Manager.raw()` method, direct cursor execution (`django.db.connection.cursor`), or custom SQL functions/views defined directly in PostgreSQL. This provides maximum control over query optimization.
            3.  **Database-Level Indexing:** Implement appropriate TimeScaleDB indexing strategies beyond the basic `(ticker, timestamp)`. Consider BRIN indexes or other TimeScaleDB-specific index types if query performance becomes an issue. This will be critical.
            4.  **Asynchronous Operations:** For long-running data fetch/storage operations initiated from the UI, use asynchronous tasks (e.g., with Celery, although that adds complexity beyond MVP scope, or Django's built-in async support if applicable) to avoid blocking web requests. For the MVP, management commands for bulk operations are acceptable.
* **Data Flow Summary:**
    * External APIs -> `data_handler.py` -> \[Django ORM or Raw SQL] -> PostgreSQL/TimeScaleDB (OHLCVData)
    * Django Forms -> Django Views -> Django ORM -> PostgreSQL (TradeLog, TradeChecklistStatus)
    * Backtester (`backtester.py`) -> \[Data Handler or Direct Query] -> PostgreSQL/TimeScaleDB (OHLCVData)
    * Visualization Helper -> Django ORM -> PostgreSQL (OHLCVData, potentially TradeLog)
* **Schema Diagram (Mermaid ERD):**

    ```mermaid
    erDiagram
        OHLCVData ||--o{ TradeLog : "can have trades for"
        TradeLog ||--|{ TradeChecklistStatus : "has checklist items"

        OHLCVData {
            DATETIME timestamp PK "Time (TimeScaleDB Time Dimension)"
            VARCHAR ticker PK "Stock Ticker"
            DECIMAL open
            DECIMAL high
            DECIMAL low
            DECIMAL close
            BIGINT volume
            -- Other metadata fields as needed --
        }

        TradeLog {
            INTEGER id PK
            VARCHAR ticker
            VARCHAR strategy
            DATETIME entry_date
            DATETIME exit_date NULL
            DECIMAL entry_price
            DECIMAL exit_price NULL
            DECIMAL position_size
            DECIMAL initial_stop_loss
            DECIMAL planned_target NULL
            DECIMAL pnl NULL
            TEXT rationale
            TEXT emotion_pre NULL
            TEXT emotion_during NULL
            TEXT emotion_post NULL
            TEXT mistakes NULL
            TEXT lessons NULL
            DECIMAL planned_rr_ratio NULL
            DECIMAL user_risk_percent
            DECIMAL suggested_position_size NULL
            DECIMAL account_capital_at_trade
        }

        TradeChecklistStatus {
            INTEGER id PK
            INTEGER trade_log_id FK "Refers to TradeLog.id"
            VARCHAR checklist_item
            BOOLEAN is_checked
        }
    ```

### 3.4. Deployment View

* **Target Environment:** **Local User Machine (macOS M3 Pro)**.
* **Deployment Strategy:** Manual setup and execution. No automated deployment pipeline (CI/CD) is required for the MVP.
* **Execution:** The application will be run using the Django development server (`python manage.py runserver`) for local access via a web browser.
* **Database Setup:** PostgreSQL and TimeScaleDB must be installed and running locally on the user's machine. Database creation and user setup are manual steps (detailed in Story 0).
* **Environment Management:** Anaconda will be used to manage the Python environment and dependencies.
* **Configuration:** API keys and database credentials will be managed via a `.env` file, loaded by `python-dotenv`.
* **Containerization/Cloud:** Explicitly out of scope for MVP.

## 4. Initial Project Setup (Manual Steps - Story 0)

These steps must be performed manually by the user to initialize the project environment before development begins:

1.  **Version Control:** Initialize a Git repository locally (`git init`) and create a corresponding private repository on the user's GitHub account. Perform an initial commit.
2.  **Environment Setup (Anaconda):**
    * Ensure Anaconda or Miniconda is installed on the macOS M3 machine.
    * Create a dedicated Conda environment: `conda create --name swing_system python=3.12 -y` (**Updated**)
    * Activate the environment: `conda activate swing_system`
3.  **Database Setup (PostgreSQL & TimeScaleDB):**
    * Install PostgreSQL (Version 16.x recommended) using Homebrew: `brew install postgresql@16`
    * Install TimeScaleDB extension. Follow official TimeScaleDB instructions for macOS/Homebrew installation (often involves `brew install timescaledb`).
    * Initialize/Start PostgreSQL service (e.g., `brew services start postgresql@16`).
    * Connect to PostgreSQL (e.g., using `psql -U postgres`) and create the database: `CREATE DATABASE swing_system_db;`
    * Create a dedicated database user and grant privileges:
        ```sql
        CREATE USER swing_user WITH PASSWORD 'your_secure_password';
        GRANT ALL PRIVILEGES ON DATABASE swing_system_db TO swing_user;
        ALTER DATABASE swing_system_db OWNER TO swing_user;

        ```
    * Connect to the new database (`psql -U swing_user -d swing_system_db`) and enable the TimeScaleDB extension: `CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;`
4.  **Django Project Setup:**
    * Ensure the `swing_system` Conda environment is active.
    * Install Django: `pip install django==5.0.*` (Pin to latest 5.0.x patch version available).
    * Create the Django project: `django-admin startproject swing_project .` (Note the `.` to create in the current directory).
    * Create the dashboard app: `python manage.py startapp dashboard`
    * Add `dashboard` to `INSTALLED_APPS` in `swing_project/settings.py`.
5.  **Dependency Installation:**
    * Install `python-dotenv`: `pip install python-dotenv`
    * Install initial core dependencies (others will be added per story): `pip install psycopg2-binary pandas numpy`
    * *Note:* `psycopg2-binary` is recommended for ease of installation, especially on macOS.
6.  **Configuration Files:**
    * Create a `.env` file in the project root (`swing_system/`) with placeholders for secrets:
        ```dotenv
        # .env
        SECRET_KEY='django_secret_key_replace_me' # Replace with Django's generated key later
        DEBUG=True
        DATABASE_URL='postgres://swing_user:your_secure_password@localhost:5432/swing_system_db'

        # API Keys (Leave blank initially)
        ALPHA_VANTAGE_API_KEY=
        ALPACA_API_KEY=
        ALPACA_SECRET_KEY=
        # Alpaca Paper Trading URL (default)
        ALPACA_PAPER_URL='[https://paper-api.alpaca.markets](https://paper-api.alpaca.markets)'
        GEMINI_API_KEY=

        ```
    * Configure `swing_project/settings.py` to read from `.env` using `python-dotenv` and configure the `DATABASES` setting using `DATABASE_URL`.
    * Create a `.gitignore` file in the project root and add `.env`, `__pycache__/`, `*.pyc`, environment directories (`env/`, `venv/`, etc.), `db.sqlite3` (if default is present initially), and OS-specific files (`.DS_Store`).
7.  **Initial Migration:** Run `python manage.py makemigrations` and `python manage.py migrate` to set up the initial Django database schema.
8.  **README Documentation:** Create/update `README.md` documenting these manual setup steps, environment activation, and how to run the development server.

* **Justification for Manual Setup:** Story 0 involves machine-specific installations (PostgreSQL, TimeScaleDB via Homebrew), local configuration (database user/password), and interactive steps (creating GitHub repo, API key registration later) that are difficult or inappropriate to fully automate via a single script, especially for the initial MVP setup on a developer's primary machine. Framework CLIs like `django-admin startproject` are used, but the overall environment setup is manual.

## 5. Technology Stack (Opinionated & Specific)

| Category             | Technology/Library              | Specific Version | Notes                                                                 |
| :------------------- | :------------------------------ | :--------------- | :-------------------------------------------------------------------- |
| **Language** | Python                          | `3.12.x`         | **Updated.** Pin exact version in Conda env & `requirements.txt`.     |
| **Environment** | Anaconda/Conda                  | Latest           | For environment and package management.                               |
| **Web Framework** | Django                          | `5.0.x`          | Pin exact version (e.g., `5.0.4`) in `requirements.txt`.            |
| **Database** | PostgreSQL                      | `16.x`           | Pin exact version installed via Homebrew.                             |
| **DB Extension** | TimeScaleDB                     | Latest Stable    | Version compatible with PostgreSQL 16.x.                            |
| **DB Driver** | psycopg2-binary                 | Latest           | Python-PostgreSQL Adapter. Binary for easier macOS install.           |
| **Data Handling** | Pandas                          | `2.2.x`          | Core data manipulation. Pin exact version.                          |
| **Numerical** | NumPy                           | `1.26.x`         | Foundational numerical library. Pin exact version.                    |
| **Charting** | Plotly                          | `5.x.x`          | **Chosen standard.** Interactive charts. Pin exact version.           |
| **Backtesting** | Backtrader                      | `1.9.x`          | Backtesting engine. Pin exact version.                                |
| **Technical Analysis** | pandas-ta                       | Latest           | Calculate MAs, ATR, etc. Integrates with Pandas. Pin exact version.   |
| **Data Sources API** | yfinance                        | Latest           | Fetch market data (Use cautiously due to reliability). Pin version.    |
| **Data Sources API** | alpha-vantage                   | Latest           | Fetch market data (Official API). Pin version.                        |
| **Broker API** | alpaca-trade-api-python / alpaca-py | Latest           | Fetch live quotes (Alpaca). Prefer `alpaca-py`. Pin version.          |
| **AI/LLM API** | google-generativeai             | Latest           | Gemini API integration. Pin version.                                  |
| **Secrets Mgmt** | python-dotenv                   | Latest           | Load `.env` file. Pin version.                                        |
| **Code Formatting** | Black                           | Latest           | Mandatory code formatter. Pin version.                                |
| **Code Linting** | Flake8                          | Latest           | Mandatory code linter (with plugins like `flake8-black`). Pin version. |
| **Type Checking** | Mypy                            | Latest           | Optional but recommended static type checker. Pin version.              |
| **Unit Testing** | Pytest                          | `8.x.x`          | Mandatory unit test framework. Pin exact version.                   |
| **Integration Test** | Pytest / Django TestCase        | `8.x.x`          | For testing component interactions. Pin exact version.                |
| **E2E Testing** | Manual                          | N/A              | Manual test plan for MVP UI flows.                                    |
| **Version Control** | Git                             | Latest           | Mandatory version control system.                                     |
| **Code Repository** | GitHub                          | N/A              | User's private repository.                                          |
| **Operating System** | macOS (Ventura/Sonoma)          | N/A              | Target development and execution platform.                            |
| **Web Server (Dev)** | Django Development Server       | N/A              | `manage.py runserver`. Sufficient for local MVP.                      |

*(Note: Pinned versions (`.x`) should be updated to specific patch versions upon installation and recorded in `requirements.txt` or Conda environment file).*

## 6. Patterns and Standards (Opinionated & Specific)

### 6.1. Architectural/Design Patterns

* **Monolith:** The application follows a monolithic architecture pattern.
* **Model-View-Template (MVT):** Standard Django pattern will be strictly adhered to within the `dashboard` app. Views contain presentation logic, Templates handle HTML rendering, Models define data structure.
* **Fat Models, Thin Views (Considered):** While standard MVT is the base, logic closely tied to a specific model (e.g., calculating a derived field for `TradeLog`) *may* reside as a method on the model class itself to improve encapsulation. However, complex business logic should reside in service functions/core modules, not views. Views should primarily orchestrate interactions between models, forms, core modules, and templates.
* **Modular Core:** Backend logic (data fetching, backtesting, external API interaction, complex calculations) **MUST** be implemented in the `core/` directory, separate from the Django `dashboard` app, to promote separation of concerns and testability. Functions/classes in `core/` should be callable from Django views or management commands.
* **Repository Pattern (Conditional):** If database interactions for `OHLCVData` become complex and require frequent switching between ORM and Raw SQL, consider introducing a Repository layer within `core/data_handler.py` to abstract data access logic. For the MVP, direct ORM/Raw SQL calls from the handler are acceptable.
* **Dependency Injection:** Not strictly enforced for MVP, but aim for loose coupling. Core modules should ideally not have hard dependencies on specific Django components (like request objects) unless necessary for ORM access passed explicitly.

### 6.2. API Design Standards (Internal & External)

* **Internal (Core Modules):** Functions within `core/` modules should have clear inputs and outputs. Use type hints (`typing` module) extensively for function signatures. Aim for pure functions where possible.
* **External API Interaction:** All interactions with external APIs (Alpha Vantage, Alpaca, Gemini) **MUST** be encapsulated within their respective modules in `core/` (`data_handler.py`, `market_data.py`, `educational_guidance.py`). These modules handle authentication (reading keys from `.env`), request formatting, response parsing, and basic error handling (e.g., logging API errors, returning None or raising specific exceptions). Django views **MUST NOT** call external APIs directly.
* **REST/JSON:** Interactions with external APIs are assumed to be RESTful and use JSON data formats.

### 6.3. Coding Standards

* **Style Guide:** **PEP 8** is mandatory.
* **Formatter:** **Black** is mandatory and will be used to enforce consistent code formatting. Configuration will be minimal (default settings preferred).
* **Linter:** **Flake8** (with plugins like `flake8-black`, `flake8-isort`) is mandatory for identifying style violations, potential bugs, and code complexity issues. A project `.flake8` configuration file will define specific rules/ignores if needed.
* **Naming Conventions:**
    * Packages/Modules: `snake_case` (e.g., `data_handler.py`).
    * Classes: `PascalCase` (e.g., `SmaCrossStrategy`).
    * Functions/Methods/Variables: `snake_case` (e.g., `Workspace_ohlcv_data`).
    * Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_RISK_PERCENT`).
    * Django Templates: `snake_case.html` (e.g. `trade_log_form.html`).
    * Django URL Names: `snake_case` (e.g., `trade_log_list`).
* **Docstrings:** All modules, classes, functions, and methods **MUST** have Google-style docstrings explaining their purpose, arguments (Args:), and return values (Returns:).
* **Type Hinting:** Extensive use of Python's type hinting (`typing` module) is mandatory for all function/method signatures and variable declarations where practical. Mypy can be used for static analysis (optional but recommended).
* **Imports:** Use `isort` (can be integrated with Black/Flake8) to automatically sort imports according to PEP 8 standards. Use absolute imports within the project where possible.
* **Comments:** Use comments (`#`) sparingly to explain *why* something is done, not *what* it does (code and docstrings should explain the *what*).
* **Test File Location:** Unit/integration test files **MUST** be located within the corresponding app/module directory. Separate `tests` subdirectories within apps are preferred (e.g., `dashboard/tests/`, `core/tests/`).

### 6.4. Error Handling Strategy

* **Logging:** Use Python's built-in `logging` module. Configure a basic logger in `settings.py` to output to the console during development. Log significant events, warnings, and especially errors/exceptions.
* **Exception Handling:** Use specific exception types where possible. Avoid broad `except Exception:`.
* **Core Modules:** Functions in `core/` that interact with external services (APIs, DB) should handle potential exceptions (e.g., `requests.exceptions.RequestException`, `psycopg2.Error`, API-specific errors). They should either log the error and return a meaningful value (e.g., `None`, empty list) or raise a custom, more specific exception to be handled by the calling code (Django view).
* **Django Views:** Views should use `try...except` blocks to catch exceptions raised from core modules or the ORM. Handle expected exceptions gracefully (e.g., show an error message to the user). Unhandled exceptions will result in Django's standard 500 error page (acceptable for MVP development).
* **User Feedback:** Provide clear feedback to the user in the UI for errors (e.g., "Failed to fetch data from API", "Invalid trade log entry"). Django's form validation errors should be displayed appropriately.

### 6.5. Folder Structure

The mandatory project directory structure is defined as follows: swing_system/
├── .env                   # Secret configuration (MUST be in .gitignore)
├── .gitignore             # Specifies intentionally untracked files
├── manage.py              # Django's command-line utility
├── requirements.txt       # Python dependencies (or use conda env file)
├── README.md              # Project overview, setup, and usage instructions
│
├── swing_project/         # Django Project Directory
│   ├── init.py
│   ├── asgi.py            # ASGI config (not heavily used in MVP)
│   ├── settings.py        # Django project settings
│   ├── urls.py            # Project-level URL routing
│   └── wsgi.py            # WSGI config (not heavily used in MVP)
│
├── core/                  # Core application logic (non-Django specific)
│   ├── init.py
│   ├── data_handler.py    # Data fetching and database interaction (OHLCV)
│   ├── backtester.py      # Backtrader orchestration
│   ├── strategies.py      # Backtrader strategy definitions
│   ├── risk_calculator.py # R:R, Position Size calculations
│   ├── market_data.py     # Alpaca API interaction
│   ├── educational_guidance.py # Gemini API interaction
│   └── tests/             # Tests for core modules
│       ├── init.py
│       └── test_.py
│
├── dashboard/             # Django Application for UI and primary features
│   ├── init.py
│   ├── admin.py           # Django admin configuration (optional for MVP)
│   ├── apps.py            # App configuration
│   ├── forms.py           # Django forms (e.g., TradeLogForm)
│   ├── migrations/        # Database migration files
│   │   └── init.py
│   ├── models.py          # Django ORM models (OHLCVData, TradeLog, etc.)
│   ├── templates/         # HTML Templates
│   │   └── dashboard/
│   │       ├── base.html
│   │       ├── chart_view.html
│   │       ├── backtest_view.html
│   │       ├── trade_log_list.html
│   │       ├── trade_log_form.html
│   │       ├── checklist_view.html
│   │       └── education_display.html # Placeholder
│   ├── tests/             # Tests for dashboard app (models, views, forms)
│   │   ├── init.py
│   │   └── test_.py
│   ├── urls.py            # URLs specific to the dashboard app
│   └── views.py           # Django view functions/classes
│   └── management/        # Custom Django management commands
│       ├── init.py
│       └── commands/
│           ├── init.py
│           ├── export_ohlcv.py # Placeholder
│           └── import_ohlcv.py # Placeholder
│
└── static/                # Static files (CSS, JavaScript - if needed beyond basic bootstrap)
└── dashboard/
├── css/
└── js/

## 7. Testing Strategy (Opinionated & Specific)

### 7.1. Required Test Types

* **Unit Tests:** Mandatory. Focus on testing individual functions and classes in isolation.
    * `core/` modules: Test data fetching logic (with mocked API calls), risk calculations, strategy rule logic components, TimeScaleDB interaction functions (mocking DB calls or using a test DB).
    * `dashboard/` app: Test model methods, form validation logic, view function logic (mocking external calls and database interactions).
* **Integration Tests:** Mandatory. Focus on testing interactions between components.
    * Test Django view interactions with forms and ORM (saving/retrieving data).
    * Test data handler module saving data to the test database.
    * Test Backtrader integration with the data feed from the test database.
    * Test core modules correctly calling mocked external APIs.
* **End-to-End (E2E) Tests:** Manual testing is sufficient for the MVP. A formal manual test plan should be created covering the main user flows defined in the PRD (e.g., fetch data -> view chart -> run backtest -> view results -> log trade -> view log -> use checklist -> ask Gemini).

### 7.2. Frameworks/Libraries

* **Test Runner:** **Pytest (`pytest 8.x.x`)** is the mandatory test runner.
* **Django Integration:** Use `pytest-django` plugin for seamless integration with Django's test client and database handling.
* **Mocking:** Use Python's built-in `unittest.mock` library for mocking external API calls and isolating components during unit tests.
* **Test Database:** Configure Django/Pytest to use a separate PostgreSQL test database (automatically created and destroyed by Django's test runner).

### 7.3. Code Coverage Requirement

* A minimum code coverage of **>= 85%** is mandatory for all new Python code (`core/` and `dashboard/` modules).
* Coverage will be measured using `pytest-cov`.
* This requirement should ideally be enforced in a pre-commit hook or a future CI pipeline (if implemented post-MVP).

### 7.4. Testing Standards

* **Test Structure (AAA):** Follow the Arrange-Act-Assert pattern for structuring unit tests where applicable.
* **Test Naming:** Test functions **MUST** start with `test_` (e.g., `def test_calculate_rr_ratio():`). Test files **MUST** start with `test_` (e.g., `test_risk_calculator.py`).
* **Fixtures:** Use Pytest fixtures (`@pytest.fixture`) for setting up reusable test data or resources (e.g., database instances, model instances, mocked API clients).
* **Assertions:** Use Pytest's built-in `assert` statements for clear and concise assertions.
* **Database Tests:** Django tests using `TestCase` or `TransactionTestCase` provide automatic database setup/teardown. Be mindful of transaction handling. For TimeScaleDB specific features, integration tests hitting the actual extension (on the test DB) might be necessary.
* **Mocking Strategy:** Mock external dependencies (APIs, potentially complex library functions) at the boundary of the component being tested. Avoid excessive mocking of internal implementation details.

## 8. Core AI Agent Rules (for separate file: `ai/rules.md`)

These are essential, project-wide rules for any AI coding agent assisting with development:

1.  **Adhere Strictly to Architecture:** All code generation MUST conform to the patterns, standards, folder structure, and technology versions defined in `Architecture.md` (this document).
2.  **Follow Coding Standards:** Implement PEP 8 strictly. Use Black for formatting all generated Python code. Ensure Flake8 passes with no errors. Use Google-style docstrings and comprehensive type hints for all functions, methods, and classes.
3.  **Test-Driven Development (TDD) Preferred:** Where feasible, generate unit tests (using Pytest) *before* or *alongside* the functional code. Ensure tests cover new logic and achieve >= 85% coverage. Place tests in the correct location (`tests/` subdirectory within the relevant module/app).
4.  **Use Defined Libraries Only:** Only use Python libraries specified in the Technology Stack section of `Architecture.md`. Do not introduce new dependencies without explicit approval.
5.  **Encapsulate External API Calls:** All interactions with external APIs (yfinance, Alpha Vantage, Alpaca, Gemini) MUST be implemented within the designated `core/` modules (`data_handler.py`, `market_data.py`, `educational_guidance.py`). Do not place direct API calls in Django views or other modules. Read API keys ONLY from environment variables via `.env`.
6.  **Django ORM & TimeScaleDB:** Use the Django ORM for standard CRUD operations on `TradeLog` and `TradeChecklistStatus`. For `OHLCVData`, prioritize using the ORM but implement direct SQL queries or use `django-timescaledb` helpers (if adopted) within `core/data_handler.py` for bulk operations or performance-critical time-series queries, as discussed in the Architecture Document.
7.  **Clear Separation of Concerns:** Maintain a strict separation between Django web components (`dashboard/`) and core backend logic (`core/`). Core modules should be usable independently of the web framework where possible.
8.  **Error Handling:** Implement error handling as defined in `Architecture.md`. Log errors appropriately using Python's `logging` module. Handle exceptions gracefully, especially around external API calls and database operations.
9.  **Security Best Practices:** Ensure standard Django security practices are followed (e.g., CSRF protection, avoiding raw SQL injection - use ORM parameters or psycopg2 parameterization). Never commit secrets (`.env` file) to version control.
10. **Documentation:** Generate necessary comments explaining complex logic (`# Why, not what`). Ensure all code has docstrings and type hints. Update `README.md` if setup or usage changes.

## 9. Security Considerations

Given the local execution scope of the MVP, security requirements are focused on protecting local data and API keys.

* **Secrets Management:** API keys (Alpha Vantage, Alpaca, Gemini) and Database Credentials **MUST** be stored in the `.env` file at the project root. This file **MUST** be included in `.gitignore` and never committed to version control. `python-dotenv` will be used to load these into the environment. Django's `SECRET_KEY` must also be managed via `.env`.
* **Input Validation:** All user input received via Django forms (e.g., Trade Log) **MUST** be validated using Django's form validation mechanisms to prevent invalid data entry and potential basic injection attacks (though the risk is lower in a local, single-user context).
* **Django Security Middleware:** Ensure standard Django security middleware (CSRF protection, XSS protection headers) are enabled in `settings.py`. While the primary risk vectors are lower locally, maintaining best practices is important.
* **Database Security:** The PostgreSQL database should be configured with a strong password for the `swing_user`. Access should ideally be limited to localhost.
* **Dependency Security:** Keep Python packages updated to patch potential security vulnerabilities (regularly review dependencies, e.g., using `pip list --outdated` or security scanning tools post-MVP).
* **No Authentication/Authorization (MVP):** As a single-user local application, the MVP does not require user login, authentication, or complex authorization schemes.

## 10. Architectural Decisions (ADRs)

* **ADR-001: Architecture Style - Local Monolith**
    * **Context:** PRD requires a local, single-user application for MVP with integrated features (UI, data, backtesting).
    * **Decision:** Adopt a Local Monolithic Web Application architecture using Django.
    * **Rationale:** Simplifies development, local setup, and integration for the MVP scope. Avoids premature complexity of distributed systems. Modularity will be achieved through code organization (`core/` vs `dashboard/`). Meets PRD constraints.
* **ADR-002: Database Choice - PostgreSQL + TimeScaleDB**
    * **Context:** PRD requires storage and efficient querying of time-series OHLCV data alongside relational trade log data. PRD explicitly suggests PostgreSQL/TimeScaleDB.
    * **Decision:** Use PostgreSQL 16.x with the TimeScaleDB extension.
    * **Rationale:** PostgreSQL is a robust relational database. TimeScaleDB provides excellent time-series performance optimizations (hypertables, specialized functions/indexing) directly within PostgreSQL, avoiding the need for a separate time-series database. Aligns with PRD suggestion and is a standard choice for financial time-series data.
* **ADR-003: Web Framework - Django**
    * **Context:** PRD requires a web UI for interaction, data logging, visualization, and orchestrating backend tasks. PRD explicitly suggests Django.
    * **Decision:** Use Django 5.0.x.
    * **Rationale:** Django provides a mature, full-featured "batteries-included" framework suitable for building the required web interface, ORM, forms, and admin (if needed). Its ecosystem is robust. Aligns with PRD choice and architect's experience.
* **ADR-004: Backtesting Engine - Backtrader**
    * **Context:** PRD requires backtesting the Classic Breakout strategy using historical data. PRD explicitly suggests Backtrader.
    * **Decision:** Use Backtrader 1.9.x.
    * **Rationale:** Backtrader is a feature-rich, widely-used Python backtesting library specifically designed for strategy development and testing. It integrates well with Pandas and Matplotlib. Aligns with PRD suggestion and common practice.
* **ADR-005: Charting Library - Plotly**
    * **Context:** PRD requires interactive charting (Candlesticks, Volume, MAs) within the Django UI. PRD mentions Plotly or Bokeh. User confirmed Plotly is preferred.
    * **Decision:** Use Plotly 5.x.x as the standard charting library.
    * **Rationale:** Plotly offers extensive interactive charting capabilities suitable for financial visualization, integrates well with Pandas, and can be embedded in Django templates. Standardizing on one library simplifies development. User preference confirmed.
* **ADR-006: Data Access for TimeScaleDB - ORM with Potential Raw SQL**
    * **Context:** User raised concerns about potential performance issues using Django ORM with TimeScaleDB indexing/queries for time-series data.
    * **Decision:** Primarily use Django ORM for simplicity, especially for `TradeLog`. For performance-critical `OHLCVData` access (bulk loads, complex queries), use optimized ORM queries, investigate `django-timescaledb`, or resort to Raw SQL within specific data handler methods. Emphasize correct TimeScaleDB indexing.
    * **Rationale:** Balances ease of development (ORM) with the need for performance on time-series data. Provides a strategy to address potential bottlenecks identified by the user, leveraging TimeScaleDB's strengths directly if needed.
* **ADR-007: Python Version - 3.12.x**
    * **Context:** User requested an update from the initially suggested 3.11.x.
    * **Decision:** Standardize on Python 3.12.x for the project environment.
    * **Rationale:** Incorporates user preference. Python 3.12 is a recent, stable version offering potential performance improvements and new language features over 3.11. Need to ensure compatibility with chosen libraries (most major libraries should be compatible).

## 11. Glossary

* **ADR:** Average Daily Range - A measure of a stock's volatility.
* **API:** Application Programming Interface - A way for software components to communicate.
* **ATR:** Average True Range - A technical analysis indicator measuring market volatility.
* **Backtesting:** Simulating a trading strategy on historical data to assess past performance.
* **Bokeh:** A Python interactive visualization library. (Not chosen standard for MVP).
* **Breakout:** A price movement significantly outside a defined support or resistance area.
* **Candlestick Chart:** A style of financial chart showing high, low, open, and closing prices for a specific period.
* **Cerebro:** The main orchestrator class in the Backtrader library.
* **Classic Breakout:** The specific swing trading strategy defined in the PRD for the MVP.
* **Consolidation:** A period where price trades within a limited range.
* **CRUD:** Create, Read, Update, Delete - Basic database operations.
* **CSV:** Comma-Separated Values - A common file format for tabular data.
* **Django:** A high-level Python web framework.
* **EMA:** Exponential Moving Average.
* **ERD:** Entity-Relationship Diagram.
* **EOD:** End-of-Day (referring to market data).
* **Gemini API:** Google's Large Language Model API used for educational context.
* **Hypertable:** A TimeScaleDB abstraction for partitioning time-series data across chunks for performance.
* **LLM:** Large Language Model.
* **MA:** Moving Average.
* **MACD:** Moving Average Convergence Divergence - A trend-following momentum indicator.
* **MDD:** Maximum Drawdown - The maximum observed loss from a peak to a trough of a portfolio.
* **Monolith:** A software architecture where all components are part of a single, unified application.
* **MVP:** Minimum Viable Product.
* **MVT:** Model-View-Template - Django's architectural pattern.
* **OHLCV:** Open, High, Low, Close, Volume - Standard components of market data for a given period.
* **ORM:** Object-Relational Mapper - A technique (used by Django) for converting data between incompatible type systems using object-oriented programming languages.
* **pandas-ta:** A Python library for technical analysis indicators, integrating with Pandas.
* **Plotly:** A Python interactive visualization library (Chosen standard for MVP).
* **PostgreSQL:** A powerful, open-source object-relational database system.
* **PRD:** Product Requirements Document.
* **Pytest:** A popular Python testing framework.
* **Quant:** Quantitative Analyst.
* **R:R Ratio:** Risk:Reward Ratio - Compares the potential loss of a trade to its potential gain.
* **REST:** Representational State Transfer - An architectural style for designing networked applications.
* **RSI:** Relative Strength Index - A momentum oscillator measuring the speed and change of price movements.
* **SMA:** Simple Moving Average.
* **SQN:** System Quality Number - A metric derived by Van Tharp to measure the quality of a trading system.
* **Swing Trading:** A trading style aiming to capture price swings over days or weeks.
* **TDD:** Test-Driven Development.
* **TimeScaleDB:** An open-source time-series database extension for PostgreSQL.
* **UI:** User Interface.
* **UX:** User Experience.
* **VWAP:** Volume Weighted Average Price.
* **yfinance:** A Python library for downloading historical market data from Yahoo Finance.



