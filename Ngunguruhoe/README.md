# Ngunguruhoe Trading Alert Bot

Welcome to `Ngunguruhoe`, a Python-based application designed to generate simulated trading alerts. This project leverages market data (via Alpaca's paper trading API) to make decisions based on a defined trading strategy and then stores these decisions as alerts. It serves as an educational example of implementing a trading bot with a Hexagonal Architecture, FastAPI for API exposure, and Docker for containerization.

**Key Technologies:**

*   **Python 3.11+**
*   **FastAPI:** For creating a web API to expose the latest trading alert.
*   **Alpaca API:** Used in paper trading mode to fetch market data (e.g., latest stock prices).
*   **SQLite:** For storing generated alerts.
*   **Docker:** For containerizing the application, ensuring consistent deployment and execution.
*   **Pytest:** For running integration and end-to-end tests.
*   **Hexagonal Architecture (Ports and Adapters):** To promote a clean, decoupled design.

**Disclaimer:** This is a prototype application built for educational and demonstration purposes. The trading strategy implemented is simplistic and **should NOT be used for real financial trading decisions.** Financial markets are complex and involve significant risk.

## Architecture

This project is structured using **Hexagonal Architecture** (also known as Ports and Adapters). This architectural pattern aims to create a loosely coupled application by separating the core application logic (domain and application layers) from external concerns such as databases, web interfaces, or third-party APIs.

*   **Domain Layer (`Ngunguruhoe/domain/`):** Contains the core business logic and entities, such as the `Alert` model and ports (interfaces) like `AlertPort` and `StrategyPort`. It is independent of any specific technology or framework.
*   **Application Layer (`Ngunguruhoe/application/`):** Orchestrates the use cases of the application. For instance, `AlertService` coordinates fetching data, running a strategy, and saving alerts. It depends on the domain layer's ports.
*   **Adapters Layer (`Ngunguruhoe/adapters/`):** Implements the interfaces (ports) defined in the domain layer and handles interactions with external systems or technologies. Examples include:
    *   `AlpacaAdapter`: Fetches market data from the Alpaca API.
    *   `SQLiteAlertRepository`: Implements `AlertPort` for storing alerts in an SQLite database.
    *   `WebServerFastAPI`: Provides a web interface using FastAPI to expose alerts.

This separation helps in maintaining the application, making it easier to test components in isolation and swap out implementations (e.g., changing the database or market data provider) with minimal impact on the core logic.

## Directory Structure

Below is the main directory structure of the `Ngunguruhoe` project:

```
Ngunguruhoe/
├── .git/                     # Git version control files (usually hidden)
├── Dockerfile                # Defines the Docker image for the application
├── README.md                 # This file
├── adapters/                 # Adapters to connect to external systems & implement ports
│   ├── __init__.py
│   ├── alert_repo_sqlite.py  # SQLite implementation for storing alerts
│   ├── alpaca_adapter.py     # Adapter for Alpaca API interaction
│   └── webserver_fastapi.py  # FastAPI web server to expose alerts
├── alerts.db                 # SQLite database file (created at runtime)
├── application/              # Application layer: use cases and orchestration
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       └── alert_service.py  # Contains AlertService and SimpleMarketTrendStrategy
├── domain/                   # Core domain logic: models and ports (interfaces)
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── alert.py          # Alert data model
│   └── ports/
│       ├── __init__.py
│       ├── alert_port.py     # Interface for alert repository
│       └── strategy_port.py  # Interface for trading strategies
├── main.py                   # Main entry point for the application
├── pytest.ini                # Configuration file for Pytest
├── requirements.txt          # Python dependencies for the project
└── tests/                    # Automated tests
    ├── __init__.py
    ├── e2e/                  # End-to-end tests
    │   ├── __init__.py
    │   └── test_strategy_e2e.py
    ├── integration/          # Integration tests
    │   ├── __init__.py
    │   └── test_alert_service_integration.py
    └── mocks.py              # Mock objects for testing
```

**Key Components:**

*   **`Ngunguruhoe/`**: The root directory of the project.
*   **`Dockerfile`**: Contains instructions to build the Docker image for the application.
*   **`README.md`**: This documentation file.
*   **`adapters/`**: Implements the ports defined in the `domain` layer and handles communication with external services or tools (e.g., Alpaca API, SQLite database, FastAPI web server).
*   **`alerts.db`**: The SQLite database file where alerts are stored. This file is created when the application runs for the first time and initializes the database.
*   **`application/`**: Contains the application-specific business logic that orchestrates the flow of data and commands between the domain layer and the adapters. `AlertService` is a key component here.
*   **`domain/`**: The heart of the application, containing the core business logic, models (like `Alert`), and ports (interfaces like `AlertPort`, `StrategyPort`) that define contracts for external interactions. It is independent of any specific framework or technology.
*   **`main.py`**: The main script to run the application. It initializes all components and starts the polling loop and the web server.
*   **`pytest.ini`**: Configuration file for `pytest`, helping it discover tests and manage settings like `PYTHONPATH` and asyncio mode.
*   **`requirements.txt`**: Lists all Python packages required for the project to run.
*   **`tests/`**: Contains all automated tests.
    *   **`e2e/`**: End-to-end tests that verify complete flows, including strategy logic.
    *   **`integration/`**: Integration tests that check interactions between different components of the application (e.g., service and repository).
    *   **`mocks.py`**: Mock objects used to simulate external dependencies during testing, ensuring tests are isolated and repeatable.

## Setup Instructions

Follow these steps to set up the `Ngunguruhoe` project locally for development or execution.

**1. Prerequisites:**

*   **Python:** Ensure you have Python 3.11 or newer installed. You can check your Python version by running `python --version`.
*   **Git:** Required to clone the repository.

**2. Clone the Repository:**

Open your terminal and clone the project repository (replace `YOUR_REPO_URL_HERE` with the actual URL if applicable, otherwise download/extract the files):

```bash
git clone YOUR_REPO_URL_HERE Ngunguruhoe
cd Ngunguruhoe
```
If you downloaded the source as a ZIP, extract it and navigate into the `Ngunguruhoe` root directory.

**3. Create a Python Virtual Environment:**

It's highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with global Python packages.

From the project root directory (`Ngunguruhoe/`):

*   **On macOS and Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   **On Windows:**
    ```bash
    python -m venv venv
    .
env\Scriptsctivate
    ```
    After activation, your terminal prompt should change to indicate you are in the `(venv)` environment.

**4. Install Dependencies:**

Once your virtual environment is activated, install the required Python packages using `pip` and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
This command will download and install all necessary libraries, including FastAPI, Uvicorn, Alpaca SDK, SQLite support, and Pytest for testing.

## Configuration

To interact with the Alpaca API for fetching market data, you need to configure your API credentials. The application expects these credentials to be available as environment variables.

**Required Environment Variables:**

*   **`ALPACA_API_KEY`**: Your Alpaca API Key ID.
*   **`ALPACA_SECRET_KEY`**: Your Alpaca Secret Key.
*   **`ALPACA_PAPER`** (Optional): Set to `true` for paper trading or `false` for live trading.
    *   If not set, the application defaults to paper trading (`true`), which is highly recommended for testing and development.

**How to Set Environment Variables:**

*   **On macOS and Linux:**
    You can set environment variables in your terminal session before running the application:
    ```bash
    export ALPACA_API_KEY="YOUR_KEY_ID_HERE"
    export ALPACA_SECRET_KEY="YOUR_SECRET_KEY_HERE"
    export ALPACA_PAPER="true"
    ```
    To make them persistent across sessions, you can add these lines to your shell's profile file (e.g., `~/.bashrc`, `~/.zshrc`), then source the file or open a new terminal.

*   **On Windows:**
    In Command Prompt:
    ```cmd
    set ALPACA_API_KEY="YOUR_KEY_ID_HERE"
    set ALPACA_SECRET_KEY="YOUR_SECRET_KEY_HERE"
    set ALPACA_PAPER="true"
    ```
    In PowerShell:
    ```powershell
    $env:ALPACA_API_KEY="YOUR_KEY_ID_HERE"
    $env:ALPACA_SECRET_KEY="YOUR_SECRET_KEY_HERE"
    $env:ALPACA_PAPER="true"
    ```
    For persistent storage on Windows, you can set them through the System Properties > Environment Variables dialog.

*   **Using a `.env` file (Alternative for Local Development):**
    While not directly implemented with a library like `python-dotenv` in the current `main.py` for automatic loading, you *could* use such a library or manually source a `.env` file if you prefer for local development. A `.env` file would look like:
    ```env
    ALPACA_API_KEY="YOUR_KEY_ID_HERE"
    ALPACA_SECRET_KEY="YOUR_SECRET_KEY_HERE"
    ALPACA_PAPER="true"
    ```
    **Important:** If you use a `.env` file, ensure it's added to your `.gitignore` file to prevent accidentally committing your secret keys. The application currently reads directly from environment variables set in the system or passed via Docker.

**Note:** The application will print an error message and exit if `ALPACA_API_KEY` or `ALPACA_SECRET_KEY` are not set when it starts up.

## Running the Application

Once you have completed the setup and configuration, you can run the `Ngunguruhoe` application either locally or using Docker.

**1. Running Locally:**

*   **Activate your virtual environment** (if not already active):
    *   macOS/Linux: `source venv/bin/activate`
    *   Windows: `.
env\Scriptsctivate`
*   **Ensure API keys are set** as environment variables (see Configuration section).
*   **Navigate to the project root directory** (`Ngunguruhoe/`).
*   **Run the main script:**
    ```bash
    python main.py
    ```

    You should see log messages in your terminal indicating:
    *   Application startup and initialization of components (Database, AlpacaAdapter, AlertService).
    *   Connection status to the Alpaca API.
    *   The start of the polling loop, which will then periodically print messages as it fetches data and runs the strategy (e.g., "Polling for AAPL...", "AlertService: Market data for AAPL received...", "Alert stored: ...").
    *   The Uvicorn server starting for the FastAPI application (e.g., "Uvicorn running on http://0.0.0.0:8000").

*   **Accessing the API:**
    While the application is running, you can access the API endpoint in your web browser or using a tool like `curl`:
    *   **Latest Alert:** `http://localhost:8000/latest-alert`

**2. Running with Docker:**

Docker allows you to run the application in a containerized environment, ensuring consistency across different systems.

*   **Build the Docker Image:**
    From the project root directory (`Ngunguruhoe/`), run:
    ```bash
    docker build -t ngunguruhoe_app .
    ```
    This command builds the Docker image using the instructions in the `Dockerfile`. The tests will also run during this build process; if they fail, the image build will be aborted.

*   **Run the Docker Container:**
    Once the image is built successfully, run it with the following command. Remember to replace placeholders with your actual Alpaca API keys:
    ```bash
    docker run -p 8000:8000 \
      -e ALPACA_API_KEY="YOUR_ALPACA_KEY_ID" \
      -e ALPACA_SECRET_KEY="YOUR_ALPACA_SECRET_KEY" \
      -e ALPACA_PAPER="true" \
      --name ngunguruhoe_instance \
      ngunguruhoe_app
    ```
    *   `-p 8000:8000`: Maps port 8000 on your host machine to port 8000 in the container.
    *   `-e ALPACA_API_KEY=...`: Sets the Alpaca API key environment variable inside the container.
    *   `-e ALPACA_SECRET_KEY=...`: Sets the Alpaca secret key environment variable.
    *   `-e ALPACA_PAPER="true"`: Sets it to use paper trading (optional, defaults to true).
    *   `--name ngunguruhoe_instance`: (Optional) Assigns a name to your running container for easier management.
    *   `ngunguruhoe_app`: The name of the Docker image you built.

    You will see similar log output in your terminal from the Docker container as when running locally.

*   **Accessing the API (via Docker):**
    The API endpoint will be available at `http://localhost:8000/latest-alert` on your host machine.

*   **Stopping the Docker Container:**
    If you ran it with `--name ngunguruhoe_instance`:
    ```bash
    docker stop ngunguruhoe_instance
    docker rm ngunguruhoe_instance
    ```
    If you didn't name it, you can find its ID with `docker ps` and then use `docker stop <CONTAINER_ID>`.

## Running Tests

The project includes a suite of automated tests to ensure code quality and correctness. We use `pytest` along with `pytest-asyncio` for asynchronous code and `pytest-mock` for mocking dependencies.

**Types of Tests:**

*   **Integration Tests (`tests/integration/`):** These tests verify the interactions between different components of the application, such as the `AlertService` and its dependencies (like the alert repository or market data provider), using mocks for external services.
*   **End-to-End (E2E) Tests (`tests/e2e/`):** These tests validate complete flows, particularly focusing on the trading strategy logic. They ensure that given specific market data (via a mock adapter), the strategy produces the correct trading signals, which are then correctly processed and stored as alerts.

**How to Run Tests:**

1.  **Ensure Dependencies are Installed:**
    If you haven't already, make sure all dependencies, including testing libraries, are installed in your local Python environment:
    ```bash
    pip install -r requirements.txt
    ```
    (Ensure your virtual environment is activated.)

2.  **Navigate to the Project Root:**
    Open your terminal and ensure you are in the `Ngunguruhoe/` root directory.

3.  **Execute Pytest:**
    You can run all tests using either of the following commands:
    ```bash
    pytest
    ```
    or
    ```bash
    python -m pytest
    ```
    `pytest` will automatically discover the `pytest.ini` configuration and all test files within the `tests/` directory.

**Expected Output:**

You should see output from `pytest` indicating the collection of tests followed by the status of each test (e.g., `PASSED`, `FAILED`). A summary at the end will show the total number of tests passed.

```
============================= test session starts ==============================
platform ... -- Python ...
plugins: asyncio-..., mock-...
collected XX items  # Total number of tests found

tests/e2e/test_strategy_e2e.py ........                                 [ YY%]
tests/integration/test_alert_service_integration.py .......              [100%]

============================== XX passed in X.XXs ===============================
```

**Tests in Docker Build:**

As part of the multi-stage Docker build process defined in the `Dockerfile`, all tests are automatically executed. If any test fails during the `docker build` command, the build process will halt, preventing a faulty image from being created. This ensures that the Docker image only contains code that has passed all automated tests.

## Features - Illustrated by Code and Tests

This section walks through the main features of the `Ngunguruhoe` application, using examples from the codebase and automated tests to demonstrate how they work.

### Core Flow: From Market Data to Alert

The primary function of the application is to periodically fetch market data, apply a trading strategy to it, and if the strategy indicates a significant event (like a 'buy' or 'sell' signal), generate and store an alert.

1.  **Polling Mechanism:**
    The process is initiated by a polling loop in `Ngunguruhoe/main.py`:
    ```python
    # In main.py
    async def poll_loop():
        while True:
            print(f"Polling for {trading_symbol}...")
            try:
                # AlertService orchestrates fetching data, running strategy, and storing alert
                await service.run_strategy_and_store(symbol=trading_symbol)
            except Exception as e:
                print(f"Error during polling cycle for {trading_symbol}: {e}")
            await asyncio.sleep(60) # Polls every 60 seconds by default
    ```
    This loop calls `service.run_strategy_and_store()` at regular intervals (e.g., every 60 seconds for a specified `trading_symbol` like "AAPL").

2.  **Orchestration by `AlertService`:**
    The `AlertService` in `Ngunguruhoe/application/services/alert_service.py` is responsible for the core logic:
    ```python
    # In application/services/alert_service.py
    class AlertService:
        # ... __init__ ...
        async def run_strategy_and_store(self, symbol: str = "AAPL"):
            market_data = await self.market_data_provider.get_latest_trade(symbol) # 1. Fetch data
            if market_data:
                action, confidence = await self.strategy.decide_action(market_data) # 2. Run strategy
                if action != "hold": # 3. Decide if alert-worthy
                    alert = Alert(...) # 4. Create Alert
                    await self.alert_repo.save_alert(alert) # 5. Store Alert
                    return alert
            return None
    ```

### Fetching Market Data (Alpaca Integration)

*   **Role of `AlpacaAdapter`:** The `Ngunguruhoe/adapters/alpaca_adapter.py` is responsible for connecting to the Alpaca API (paper trading by default) and fetching real market data. Its `get_latest_trade(symbol)` method is key here.
*   **Testing with `MockAlpacaAdapter`:** In our tests, we don't want to make real API calls. So, we use `Ngunguruhoe/tests/mocks.py:MockAlpacaAdapter`. This mock allows us to simulate various scenarios:
    *   **Providing specific market data:** As seen in our E2E tests (`Ngunguruhoe/tests/e2e/test_strategy_e2e.py`):
        ```python
        # In test_strategy_e2e.py
        @pytest.mark.parametrize("price, expected_action", [(150.0, "buy"), ...])
        async def test_strategy_produces_correct_action_via_service(
                alert_service_e2e, mock_alpaca_adapter_e2e, ..., price, expected_action):
            test_symbol = f"E2E_{expected_action.upper()}_{price}"
            # Here, we tell the mock adapter what data to return:
            mock_alpaca_adapter_e2e.set_trade_data(symbol=test_symbol, price=price)
            # ... rest of the test ...
        ```
        This setup allows us to test how the system behaves with controlled "market data."
    *   **Simulating no data or API errors:**
        ```python
        # In tests/integration/test_alert_service_integration.py
        async def test_run_strategy_no_market_data(alert_service, mock_alpaca_adapter, ...):
            mock_alpaca_adapter.set_no_data() # Simulate Alpaca returning no data
            result_alert = await alert_service.run_strategy_and_store(symbol="NODATA")
            assert result_alert is None
            # ... ensure no alert was saved ...

        async def test_run_strategy_alpaca_api_error(alert_service, mock_alpaca_adapter, ...):
            mock_alpaca_adapter.set_api_error(message="Simulated API Failure") # Simulate an API error
            result_alert = await alert_service.run_strategy_and_store(symbol="APIERROR")
            assert result_alert is None
            # ... ensure no alert was saved ...
        ```

### Trading Strategy Logic (`SimpleMarketTrendStrategy`)

The current trading strategy is defined in `Ngunguruhoe/application/services/alert_service.py:SimpleMarketTrendStrategy`.

*   **Core Logic:**
    ```python
    # In application/services/alert_service.py (within SimpleMarketTrendStrategy)
    async def decide_action(self, market_data: Any) -> Tuple[str, float]:
        if market_data and hasattr(market_data, 'p'): # 'p' is price
            action = "buy" if market_data.p > 100 else "sell"
            confidence = round(random.uniform(0.55, 0.75), 2)
            return action, confidence
        return "hold", 0.1 # Default if no valid data
    ```
    This strategy is very basic: if the price (`market_data.p`) is greater than 100, it signals "buy"; otherwise, it signals "sell". If there's no valid data, it signals "hold".

*   **Validating Strategy Output (E2E Tests):**
    The E2E tests in `Ngunguruhoe/tests/e2e/test_strategy_e2e.py` are specifically designed to verify this logic:
    *   **`test_strategy_produces_correct_action_via_service`:** This parameterized test feeds different prices to the system and checks if the correct action ('buy' or 'sell') is generated and stored in an alert.
        *   Example: Input price `150.0` -> Expected action `buy`.
        *   Example: Input price `50.0` -> Expected action `sell`.
        *   Example: Input price `100.00` (edge case) -> Expected action `sell`.
        The test asserts:
        ```python
        # In test_strategy_e2e.py
        assert saved_alert.action == expected_action
        assert 0.55 <= saved_alert.confidence <= 0.75 # Checks confidence range
        ```
    *   **`test_strategy_handles_no_market_data_via_service`:** Confirms that if `MockAlpacaAdapter` provides no data, the strategy outputs "hold", and `AlertService` consequently stores no alert.
    *   **`test_strategy_handles_market_data_missing_price_attr_via_service`:** Ensures that if market data is present but lacks the critical price attribute (`p`), it's also treated as a "hold" scenario.

### Alert Generation and Storage

*   **`Alert` Data Model:** Defined in `Ngunguruhoe/domain/models/alert.py`, an `Alert` typically includes a timestamp, symbol, action (buy/sell), and confidence.
*   **Storage with `SQLiteAlertRepository`:** The `Ngunguruhoe/adapters/alert_repo_sqlite.py` implements the `AlertPort` interface and saves alerts to an `alerts.db` SQLite database file.
*   **Testing Storage with `MockAlertRepository`:** In tests, `Ngunguruhoe/tests/mocks.py:MockAlertRepository` is used. It stores alerts in an in-memory list, allowing tests to easily verify what was "saved":
    ```python
    # In various tests (integration and e2e)
    # After await alert_service.run_strategy_and_store(...)
    assert len(mock_alert_repo.alerts_saved) == 1 # Check if an alert was saved
    saved_alert = mock_alert_repo.alerts_saved[0]
    assert saved_alert.symbol == test_symbol
    assert saved_alert.action == "buy"
    # etc.
    ```

### Accessing the Latest Alert (API)

*   **FastAPI Endpoint:** The `Ngunguruhoe/adapters/webserver_fastapi.py` defines a simple API to retrieve the most recent alert:
    ```python
    # In adapters/webserver_fastapi.py
    @app.get("/latest-alert", response_model=Alert | None)
    async def latest_alert():
        return await alert_repo.get_latest_alert()
    ```
*   **How to Access:** When the application (either local or Docker) is running, this endpoint is available at `http://localhost:8000/latest-alert`. It will return a JSON representation of the latest alert or `null` if no alerts are in the database.
*   **Testing the Retrieval Logic:** While we don't have an HTTP-level test for this endpoint directly in the current suite, the underlying logic (`alert_repo.get_latest_alert()`) is implicitly tested by the `MockAlertRepository`'s `get_latest_alert` method, which is used by some integration tests if they were to verify retrieval (though current tests focus on `save_alert`). A dedicated API test could be added using a client like `httpx`.

## Current Strategy Details: `SimpleMarketTrendStrategy`

The trading logic currently implemented in the application is handled by the `SimpleMarketTrendStrategy`, located within `Ngunguruhoe/application/services/alert_service.py`.

**Logic Overview:**

The strategy is intentionally very basic and serves as a placeholder for more sophisticated decision-making algorithms. Its core logic is as follows:

1.  **Input:** It receives market data, specifically expecting an object with a price attribute `p` (e.g., the latest trade price for a symbol).
2.  **Decision Rule:**
    *   If the price (`market_data.p`) is **greater than 100**, the strategy decides on a **"buy"** action.
    *   If the price (`market_data.p`) is **less than or equal to 100**, the strategy decides on a **"sell"** action.
3.  **Confidence Score:**
    *   For "buy" or "sell" actions, a confidence score is generated randomly between 0.55 and 0.75 (inclusive of 0.55, exclusive of 0.75, then rounded to 2 decimal places).
4.  **Handling Insufficient Data:**
    *   If valid market data (specifically the price `p`) is not available, the strategy defaults to a **"hold"** action with a low confidence score of 0.1. No alert is generated by the `AlertService` for "hold" actions.

**Code Snippet (`SimpleMarketTrendStrategy`):**
```python
# In Ngunguruhoe/application/services/alert_service.py
class SimpleMarketTrendStrategy(StrategyPort):
    async def decide_action(self, market_data: Any) -> Tuple[str, float]:
        if market_data and hasattr(market_data, 'p'):
            action = "buy" if market_data.p > 100 else "sell"
            confidence = round(random.uniform(0.55, 0.75), 2)
            # print(f"SimpleStrategy: Market price {market_data.p}, Action: {action}, Confidence: {confidence}") # Debug print
            return action, confidence
        # print("SimpleStrategy: No market data received or price attribute missing.") # Debug print
        return "hold", 0.1
```

**Important Considerations:**

*   **Placeholder Only:** This strategy is purely illustrative. The threshold of "100" is arbitrary and not based on any financial analysis.
*   **Not for Real Trading:** As emphasized in the disclaimer, this strategy is not suitable for making real financial decisions.
*   **Extensibility:** The `StrategyPort` interface (`Ngunguruhoe/domain/ports/strategy_port.py`) allows this simple strategy to be replaced with more complex and realistic trading algorithms without altering the core application flow. Future work could involve implementing strategies based on technical indicators, machine learning models, or other analytical methods.
