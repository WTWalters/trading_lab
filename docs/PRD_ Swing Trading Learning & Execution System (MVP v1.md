# **PRD: Swing Trading Learning & Execution System (MVP v1.0)**

## **1\. Purpose**

This document outlines the requirements for the Minimum Viable Product (MVP) of the Swing Trading Learning & Execution System. The primary purpose of this MVP is to establish a foundational, locally-run platform for the primary user to systematically learn and practice swing trading, focusing initially on the "Classic Breakout" strategy defined herein.

**Problems Solved by MVP:**

* Provides a structured way to handle and visualize basic stock market data (OHLCV).  
* Enables the implementation and backtesting of the defined Classic Breakout swing trading strategy using the Backtrader framework.  
* Offers a basic, interactive charting interface (Plotly, Bokeh) for visual analysis within a web UI.  
* Introduces a structured method for manual trade logging via a Django interface, incorporating psychological factors to build self-awareness.    
* Provides immediate feedback on planned trade risk (R:R Ratio) and suggests position size based on user-defined risk percentage.    
* Facilitates connection to live market data for observation purposes via the Alpaca API.    
* Implements a basic trading plan checklist within Django to encourage disciplined trade consideration.    
* Offers initial context-aware educational support via Gemini API integration for the implemented strategy.  
* Establishes the core technical architecture (Python, Django, PostgreSQL/TimeScaleDB) for future expansion.  

**MVP Goal Sequence:**

1. Set up the foundational project environment (Python/Anaconda, Git, Database, Django).  
2. Implement data handling: Fetch historical data (yfinance, Alpha Vantage), store in PostgreSQL/TimeScaleDB, enable CSV I/O.  
3. Develop basic interactive charting (Candlesticks, Volume, MAs \- 10/20/50) using Plotly/Bokeh within Django.  
4. Implement the Classic Breakout strategy logic (as defined in Section 4, Story 5\) within the Backtrader framework.  
5. Integrate Backtrader with the data module and run backtests, displaying basic performance metrics (P/L, Win Rate, Max Drawdown) in Django.  
6. Build the Django interface for structured trade logging, including psychological fields, storing data in PostgreSQL.  
7. Implement the calculation and display of planned R:R Ratio and Suggested Position Size in the logging interface.  
8. Integrate Alpaca API for fetching and displaying live price data observation within Django.  
9. Implement the static Trading Plan Checklist within Django, storing status in PostgreSQL.  
10. Integrate Gemini API to provide basic educational context/answers related to the Classic Breakout strategy within Django.

## **2\. Context**

This MVP is the first step towards building a comprehensive, personalized Swing Trading Learning & Execution System. The full vision includes advanced features like multiple strategy support, optimization, automated execution, LLM research analysis, and more. This PRD focuses *exclusively* on the minimal feature set required to deliver initial value: learning and practicing the defined Classic Breakout strategy in a structured, data-driven, and psychologically-aware manner on a local machine. Development will be guided by this PRD to ensure clarity for junior developers or AI agents assisting in the build.  

## **3\. High-Level Architecture & Technical Decisions**

* **Pattern:** Local Monolith Web Application. A Django web application running locally will serve as the primary user interface and orchestrator. Backend logic (data fetching, backtesting, analysis) will be implemented in Python modules called by Django views or managed commands.  
* **Data Flow:**  
  * User requests data fetch via Django UI \-\> Python module calls yfinance/Alpha Vantage API \-\> Data stored in PostgreSQL/TimeScaleDB.  
  * User initiates backtest via Django UI \-\> Backtrader module retrieves data from DB \-\> Runs simulation based on Classic Breakout rules \-\> Returns results to Django view \-\> Results displayed.  
  * User logs trade via Django form \-\> Data saved to PostgreSQL.  
  * User views chart \-\> Django view calls Plotly/Bokeh \-\> Chart rendered in template.  
  * User interacts with checklist \-\> Django view updates status in PostgreSQL.  
  * User asks educational question \-\> Django view calls Gemini API \-\> Response displayed.  
* **Technology Choices:** See Tech Stack section. Key decisions include using Django for the web UI, PostgreSQL/TimeScaleDB for time-series data, Backtrader for backtesting, Plotly/Bokeh for charting, and integrating external APIs (yfinance, Alpha Vantage, Alpaca, Gemini).  
* **Local Execution:** The system is designed solely for local execution on the user's machine (MacBook M3 Pro specified). No cloud deployment or containerization is planned for the MVP.    
*   
* **Modularity:** While monolithic, strive for modular Python code (separate modules for data, backtesting, visualization, logging, external APIs) to facilitate future maintenance and potential decoupling.

### **Mermaid Diagrams (High-Level)**

*(Diagrams remain the same as in the previous thought block)*

**Use Case: Running a Backtest**

Code snippet  
sequenceDiagram  
    participant User  
    participant DjangoUI as Django UI  
    participant BacktestModule as Backtest Module (Python/Backtrader)  
    participant DataModule as Data Module (Python)  
    participant Database as PostgreSQL/TimeScaleDB

    User-\>\>DjangoUI: Select Stock(s) & Initiate Backtest (Classic Breakout)  
    DjangoUI-\>\>BacktestModule: Trigger backtest(strategy='ClassicBreakout', stocks=...)  
    BacktestModule-\>\>DataModule: Request OHLCV data for stock(s)  
    DataModule-\>\>Database: Query OHLCV data  
    Database--\>\>DataModule: Return data  
    DataModule--\>\>BacktestModule: Provide data  
    BacktestModule-\>\>BacktestModule: Run Backtrader simulation (Classic Breakout rules)  
    BacktestModule--\>\>DjangoUI: Return performance metrics (P/L, Win Rate, MDD)  
    DjangoUI-\>\>User: Display Backtest Results

**Use Case: Logging a Trade**

Code snippet  
sequenceDiagram  
    participant User  
    participant DjangoUI as Django UI (Trade Log Form)  
    participant Database as PostgreSQL/TimeScaleDB

    User-\>\>DjangoUI: Enters trade details (Entry, Stop, Target, Risk %, Rationale, Psych...)  
    DjangoUI-\>\>DjangoUI: Calculate R:R Ratio & Suggested Position Size  
    DjangoUI-\>\>User: Display Calculated R:R Ratio & Suggested Size  
    User-\>\>DjangoUI: Submits Trade Log Form  
    DjangoUI-\>\>Database: Save Trade Log Data (incl. user input Risk %)  
    Database--\>\>DjangoUI: Confirm Save  
    DjangoUI-\>\>User: Display Confirmation/Updated Log

**Use Case: Educational Guidance**

Code snippet  
sequenceDiagram  
    participant User  
    participant DjangoUI as Django UI  
    participant GeminiAPI as Gemini API Module (Python)  
    participant ExternalGemini as Google Gemini API

    User-\>\>DjangoUI: Asks question related to Classic Breakout  
    DjangoUI-\>\>GeminiAPI: Send request with question/context  
    GeminiAPI-\>\>ExternalGemini: Call Gemini API (prompt based on question)  
    ExternalGemini--\>\>GeminiAPI: Return LLM Response  
    GeminiAPI--\>\>DjangoUI: Provide formatted response  
    DjangoUI-\>\>User: Display Educational Guidance

## **4\. Story (Task) List**

### **Epic 1: Foundational Setup**

* **Story 0: Initial Project Setup**  
  * Subtask: Initialize Git repository on user's GitHub.  
  * Subtask: Set up Anaconda environment with Python (\~3.11).  
  * Subtask: Install PostgreSQL (\~15/16) and TimeScaleDB extension locally. Create database and user.  
  * Subtask: Set up Django (\~4.x/5.x) project structure.  
  * Subtask: Implement `.env` file handling (`python-dotenv`) for secrets (API keys, DB credentials). Add `.env` to `.gitignore`.  
  * Subtask: Document environment setup steps in `README.md`.

### **Epic 2: Data Handling**

* **Story 1: Implement Data Fetching**  
  * Subtask: Install `yfinance` and `alpha-vantage` Python libraries.  
  * Subtask: Create `core/data_handler.py` module.  
  * Subtask: Implement function to fetch daily OHLCV data using `yfinance`.  
  * Subtask: Implement function to fetch daily OHLCV data using Alpha Vantage API (read key from `.env`).  
  * Subtask: Implement basic API error handling.  
  * Subtask: Implement configuration to select data source and manage keys.  
* **Story 2: Database Integration**  
  * Subtask: Define Django model for OHLCV data in `dashboard/models.py`.  
  * Subtask: Configure Django for TimeScaleDB backend; make OHLCV model a hypertable.  
  * Subtask: Update `core/data_handler.py` to save fetched data to DB.  
* **Story 3: Basic CSV Import/Export**  
  * Subtask: Create Django management command for CSV export.    
  *   
  * Subtask: Create Django management command for CSV import.    
  * 

### **Epic 3: Visualization**

* **Story 4: Implement Basic Charting**  
  * Subtask: Install `plotly`, `bokeh`, `pandas-ta`.  
  * Subtask: Create Django view (`dashboard/views.py`) and template (`dashboard/templates/dashboard/chart_view.html`) for charts.  
  * Subtask: Implement function to get DB data for charting.  
  * Subtask: Implement function using Plotly/Bokeh for interactive Candlestick chart with Volume.    
  *   
  * Subtask: Implement function using `pandas-ta` to calculate 10, 20, 50-day SMA/EMA and add as selectable overlays.    
  *   
  * Subtask: Implement toggles in template for overlays.    
  *   
  * Subtask: Embed chart in the Django template.

### **Epic 4: Strategy Implementation & Backtesting**

* **Story 5: Implement Classic Breakout Strategy**  
  * Subtask: Install `backtrader`.  
  * Subtask: Define Backtrader strategy class for "Classic Breakout" in `core/strategies.py`.  
  * Subtask: Implement the Classic Breakout rules as defined in the research document ("Algorithmic Implementation..."):  
    * Identify Consolidation Range: Use historical peaks/troughs algorithmically over a defined lookback (e.g., 3-6 months) to find support/resistance clusters.    
    *   
    * Confirm Breakout: Require price close beyond S/R level AND volume on breakout bar \> 1.5x Volume MA (e.g., 20-period).    
    *   
    * Entry Signal: Enter on open of next bar after confirmed breakout.    
    *   
    * Initial Stop-Loss: Use ATR-based stop (e.g., Entry Price \- (ATR(14) \* 2.0)). Calculate ATR using `pandas-ta` or Backtrader's built-in.    
    *   
    * Exit Mechanism: Use an ATR-based trailing stop (Chandelier Exit recommended: HighestHighSinceEntry \- (ATR(14) \* 3.0)) OR a fixed R:R target (e.g., 1:3). Select one method for MVP simplicity (recommend ATR trail).    
    *   
* **Story 6: Integrate and Run Backtests**  
  * Subtask: Create `core/backtester.py` module.  
  * Subtask: Implement Backtrader data feed from PostgreSQL/TimeScaleDB.  
  * Subtask: Configure Backtrader Cerebro with strategy, data feed, TradeAnalyzer, SQN.    
  *   
  * Subtask: Set realistic commission/slippage parameters (e.g., 0.1% per trade).  
  * Subtask: Create Django view (`dashboard/views.py`) and template (`dashboard/templates/dashboard/backtest_view.html`) to trigger backtests.  
  * Subtask: Implement logic to run backtest via `core/backtester.py`.  
* **Story 7: Display Backtest Results**  
  * Subtask: Extract Total P/L, Win Rate, Max Drawdown from Backtrader analyzers.    
  *   
  * Subtask: Display metrics in the Django UI.    
  * 

### **Epic 5: Structured Trade Logging/Journaling**

* **Story 8: Create Trade Log Model and Form**  
  * Subtask: Define `TradeLog` model in `dashboard/models.py` with fields: Ticker, Strategy, EntryDate, ExitDate, EntryPrice, ExitPrice, PositionSize, InitialStopLoss, PlannedTarget, PnL, Rationale, EmotionPre, EmotionDuring, EmotionPost, Mistakes, Lessons, PlannedRRRatio, UserRiskPercent, SuggestedPositionSize.    
  *   
  * Subtask: Create Django form (`dashboard/forms.py`) for manual entry.    
  *   
* **Story 9: Implement Trade Logging Interface**  
  * Subtask: Create Django views (`dashboard/views.py`) and templates (`dashboard/templates/dashboard/trade_log_view.html`, `trade_log_form.html`) for creating/viewing logs.  
  * Subtask: Ensure form saves data to PostgreSQL.    
  *   
  * Subtask: Display logs in a table.

### **Epic 6: Basic Risk Feedback**

* **Story 10: Implement Risk Calculation Display**  
  * Subtask: Add fields to Trade Log form for Entry, Stop, Target prices, and User Desired Risk % per trade. Allow setting default Account Capital in settings.    
  *   
  * Subtask: Implement calculation (in view or JS) for Planned R:R Ratio \= `abs(Target - Entry) / abs(Entry - Stop)`.    
  *   
  * Subtask: Implement calculation for Suggested Position Size (Shares) \= `(Account Capital * User Risk %) / abs(Entry - Stop)`.    
  *   
  * Subtask: Display calculated R:R Ratio and Suggested Position Size dynamically on the form.    
  * 

### **Epic 7: Paper Trading Connection (Observation)**

* **Story 11: Integrate Alpaca API for Market Data**  
  * Subtask: Install `alpaca-trade-api-python`.  
  * Subtask: Create `core/market_data.py` module, read Alpaca keys from `.env`.  
  * Subtask: Implement function to fetch latest quote data via Alpaca API.    
  *   
  * Subtask: Create Django view/template section to display fetched live prices.    
  *   
  * Subtask: Implement basic refresh mechanism for price updates.    
  * 

### **Epic 8: Trading Plan Checklist**

* **Story 12: Implement Static Checklist**  
  * Subtask: Define checklist steps (e.g., "Consolidation Found?", "Volume Confirmed?", "Breakout Confirmed?", "ATR Stop Set?", "R:R \> 2?", "Position Sized?").  
  * Subtask: Create Django model (`dashboard/models.py`) linking checklist status to TradeLog entry.    
  *   
  * Subtask: Create Django view (`dashboard/views.py`) and template (`dashboard/templates/dashboard/checklist_view.html`) to display/interact with checklist.    
  *   
  * Subtask: Implement saving checklist state to PostgreSQL.    
  * 

### **Epic 9: Educational Guidance (Gemini Integration \- *Expanded Scope*)**

* **Story 13: Integrate Gemini API**  
  * Subtask: Install `google-generativeai`.  
  * Subtask: Create `core/educational_guidance.py` module, read Gemini API key from `.env`.  
  * Subtask: Develop basic prompt templates for Classic Breakout concepts (e.g., "Explain volume confirmation for breakouts", "How does an ATR stop work?").  
* **Story 14: Implement Contextual Guidance Interface**  
  * Subtask: Add UI elements (buttons/links) in relevant sections to trigger queries.  
  * Subtask: Implement Django view logic to construct prompts, call Gemini API via `core/educational_guidance.py`, and handle responses.  
  * Subtask: Display formatted Gemini response in the UI.  
  * Subtask: Implement basic API error handling.

## **5\. Testing Strategy**

* **Unit Tests:** Focus on `core/` modules (data fetching mocks, strategy rule logic, risk calcs), Django model methods, form validation. Framework: `pytest` or `unittest`.  
* **Integration Tests:** Test Backtrader+DB data feed, Django views saving to DB, API modules calling external APIs (mocked or test keys). Framework: Django `TestCase`, `pytest`.  
* **E2E Tests:** Primarily **manual testing** for MVP UI flows (data fetch \-\> chart \-\> backtest \-\> log \-\> checklist \-\> education). Create a manual test plan.

## **6\. UX/UI**

* **Framework:** Django Web Application.  
* **Interface Style:** Clean, simple, functional. Prioritize clarity for MVP. Use standard Django templates, potentially with Bootstrap for basic styling/responsiveness.  
* **Key Screens:** Data Management, Charting, Backtesting (Setup & Results), Trade Log (List & Form), Checklist display, Educational Guidance display area.  
* **Interaction:** Web forms, buttons, Plotly/Bokeh interactive charts, dynamic display for risk calculations.

## **7\. Tech Stack**

| Category | Technology/Library | Version | Notes |
| ----- | ----- | ----- | ----- |
| **Language** | Python | \~3.11 | Pin exact version in requirements.txt |
| **Environment** | Anaconda | Latest | Manage packages/environments |
| **Web Framework** | Django | \~4.x / 5.x | Pin exact version |
| **Database** | PostgreSQL | \~15 / 16 | Pin exact version |
| **DB Extension** | TimeScaleDB | Latest | For time-series optimization |
| **Data Handling** | Pandas | Latest | Core data manipulation |
| **Numerical** | NumPy | Latest | Foundational numerical library |
| **Charting** | Plotly, Bokeh | Latest | Interactive charts |
| **Backtesting** | Backtrader | Latest | Backtesting engine |
| **Technical Analysis** | pandas-ta | Latest | Calculate MAs, ATR, etc. |
| **Data Sources API** | yfinance, alpha-vantage | Latest | Fetch market data |
| **Broker API** | alpaca-trade-api-python | Latest | Fetch live quotes |
| **AI/LLM API** | google-generativeai | Latest | Gemini API integration |
| **Secrets Mgmt** | python-dotenv | Latest | Load `.env` file |
| **Unit Testing** | pytest / unittest | Latest | Python unit tests |
| **Integration Test** | Django TestCase / pytest | Latest | Test component interactions |
| **E2E Testing** | Manual | N/A | Manual test plan for MVP UI flows |
| **Version Control** | Git | Latest |  |
| **Code Repository** | GitHub | N/A | User's repository |
| **Operating System** | macOS | Ventura/Sonoma | Target platform |
| **Web Server (Dev)** | Django Development Server | N/A | `manage.py runserver` |

 

## **8\. Proposed Project Directory Tree**

*(Structure remains the same as in the previous thought block)*

swing\_system/  
├── .env  
├── .gitignore  
├── manage.py  
├── requirements.txt  
├── README.md  
│  
├── swing\_project/  
│   ├── \_\_init\_\_.py  
│   ├── asgi.py  
│   ├── settings.py  
│   ├── urls.py  
│   └── wsgi.py  
│  
├── core/  
│   ├── \_\_init\_\_.py  
│   ├── data\_handler.py  
│   ├── backtester.py  
│   ├── strategies.py  
│   ├── risk\_calculator.py  
│   ├── market\_data.py  
│   └── educational\_guidance.py  
│  
├── dashboard/  
│   ├── \_\_init\_\_.py  
│   ├── admin.py  
│   ├── apps.py  
│   ├── migrations/  
│   ├── models.py  
│   ├── forms.py  
│   ├── tests.py  
│   ├── urls.py  
│   ├── views.py  
│   └── templates/  
│       └── dashboard/  
│           ├── base.html  
│           ├── ... (other templates)  
│  
└── static/  
    └── ...

## **9\. Unknowns, Assumptions, Risks**

* **Unknowns:** Final library versions; detailed UI layout; optimal strategy parameters; final Gemini prompts; specific error handling needs.  
* **Assumptions:** User has necessary API keys; user manages local DB install; basic error handling is sufficient; Classic Breakout rules are final; user comfortable with Django; daily data sufficient for MVP.  
* **Risks:** Scope creep (Gemini API adds complexity); technical complexity (integrations); data quality issues; backtesting accuracy challenges (overfitting, costs); API limits/costs; development time; environment consistency (Anaconda/Django).

## **10\. Out of Scope Post MVP**

*(Based on Project Brief v1.1 )*  

* Advanced database schemas/queries.  
* Advanced charting features.  
* Multiple strategy support/optimization (e.g., WFO).  
* LLM Research Analyst integration.  
* Advanced/automated risk management algorithms.  
* Fully automated trade execution.  
* Advanced performance analytics/dashboards.  
* Live trading execution.  
* Support for other instruments (non-US stocks).  
* Built-in interactive educational modules.  
* Market Regime Detection.  
* Advanced Scanning Module.  
* Watchlist Management Module.  
* Containerization/Cloud Deployment.

