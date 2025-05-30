import asyncio
import os
from Ngunguruhoe.adapters.alert_repo_sqlite import SQLiteAlertRepository
from Ngunguruhoe.adapters.webserver_fastapi import create_app
from Ngunguruhoe.application.services.alert_service import AlertService, SimpleMarketTrendStrategy # Import strategy
from Ngunguruhoe.adapters.alpaca_adapter import AlpacaAdapter
import uvicorn

# It's good practice to load environment variables early, e.g. using dotenv for local dev,
# but AlpacaAdapter reads them directly via os.getenv, which is fine.
# from dotenv import load_dotenv
# load_dotenv() # Load .env file if you use one for local development

async def main():
    print("Application starting...")
    # Ensure API keys are set in environment: ALPACA_API_KEY, ALPACA_SECRET_KEY
    # ALPACA_PAPER can also be set (defaults to True in adapter if not present)
    if not os.getenv("ALPACA_API_KEY") or not os.getenv("ALPACA_SECRET_KEY"):
        print("CRITICAL: ALPACA_API_KEY or ALPACA_SECRET_KEY environment variables not set.")
        print("Please set them before running the application.")
        return # Exit if keys are not set

    db_path = "alerts.db"
    print(f"Initializing database at: {db_path}")
    repo = SQLiteAlertRepository(db_path=db_path)
    await repo.init_db()
    print("Database initialized.")

    try:
        print("Initializing AlpacaAdapter...")
        alpaca_adapter = AlpacaAdapter()
        print("AlpacaAdapter initialized.")
    except Exception as e:
        print(f"Failed to initialize AlpacaAdapter: {e}")
        print("Application will exit.")
        return

    print("Initializing strategy...")
    strategy = SimpleMarketTrendStrategy()
    print("Strategy initialized.")

    print("Initializing AlertService...")
    service = AlertService(alert_repo=repo, market_data_provider=alpaca_adapter, strategy=strategy)
    print("AlertService initialized.")

    # Define the symbol to trade/monitor
    # This should be a symbol your Alpaca account has access to and is formatted correctly.
    # e.g., 'AAPL' for Apple stock, 'BTC/USD' or 'BTCUSD' for Bitcoin (check Alpaca's format)
    trading_symbol = "AAPL"
    print(f"Trading/monitoring symbol set to: {trading_symbol}")

    async def poll_loop():
        print("Starting polling loop...")
        while True:
            print(f"Polling for {trading_symbol}...") # Removed datetime for simplicity here
            try:
                await service.run_strategy_and_store(symbol=trading_symbol)
            except Exception as e:
                print(f"Error during polling cycle for {trading_symbol}: {e}")
            await asyncio.sleep(60) # Poll every 60 seconds

    app = create_app(repo) # FastAPI app still uses the repo for /latest-alert
    print("FastAPI app created.")

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    print("Uvicorn server configured.")

    print("Creating background task for polling loop...")
    asyncio.create_task(poll_loop())
    print("Polling loop task created.")

    print("Starting Uvicorn server...")
    await server.serve()
    print("Application finished.")

if __name__ == "__main__":
    # Add a try-except block here if main() itself can raise critical startup errors
    # For AlpacaAdapter, it might raise ValueError if keys are missing or APIError on connection issues.
    try:
        asyncio.run(main())
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"Unhandled application error: {e}")
