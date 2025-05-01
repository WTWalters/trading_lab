# Trading Lab

A Django-based swing trading application for backtesting strategies, logging trades, and analyzing market data.

## Setup Instructions

### Prerequisites

- Python 3.12
- Anaconda or Miniconda
- PostgreSQL 17.x
- TimescaleDB extension for PostgreSQL

### Environment Setup

1. **Clone the repository**
   git clone https://github.com/WTWalters/trading_lab.git
   cd trading_lab

2. **Create and activate Conda environment**
   conda create --name swing_system python=3.12 -y
   conda activate swing_system

3. **Install dependencies**
   pip install -r requirements.txt

4. **Database Setup**

- Start PostgreSQL: `brew services start postgresql@17`
- Create the database:
  ```
  psql postgres
  CREATE DATABASE swing_system_db;
  CREATE USER swing_user WITH PASSWORD 'your_password';
  GRANT ALL PRIVILEGES ON DATABASE swing_system_db TO swing_user;
  ALTER DATABASE swing_system_db OWNER TO swing_user;
  \c swing_system_db
  CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
  \q
  ```

5. **Environment Configuration**

- Create a `.env` file in the project root with the following variables:

  ```
  # Django Settings
  SECRET_KEY="your_very_secure_django_secret_key_here"
  DEBUG=True # Set to False in production

  # Database Connection (using URL format)
  # Example: postgres://user:password@host:port/database
  DATABASE_URL=postgres://swing_user:your_secure_password@localhost:5432/swing_system_db

  # External API Keys (Loaded directly in core modules)
  ALPHA_VANTAGE_API_KEY="YOUR_ALPHA_VANTAGE_API_KEY"
  ALPACA_API_KEY="YOUR_ALPACA_API_KEY_ID"
  ALPACA_SECRET_KEY="YOUR_ALPACA_SECRET_KEY"
  ALPACA_PAPER_URL=https://paper-api.alpaca.markets
  GEMINI_API_KEY="YOUR_GOOGLE_AI_GEMINI_API_KEY"
  ```

6. **Run Migrations**
   python manage.py migrate

7. **Run the Development Server**
   python manage.py runserver

### Project Components

- **Dashboard App**: Main application interface
- **Core Module**: Business logic for trading strategies
- **Data Storage**: PostgreSQL with TimescaleDB for time-series data
