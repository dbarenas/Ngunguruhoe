import os
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import APIError

class AlpacaAdapter:
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.paper_trading = os.getenv("ALPACA_PAPER", "True").lower() == "true"

        if not self.api_key or not self.secret_key:
            raise ValueError("Alpaca API key and secret key must be set as environment variables.")

        base_url = "https://paper-api.alpaca.markets" if self.paper_trading else "https://api.alpaca.markets"
        self.api = tradeapi.REST(self.api_key, self.secret_key, base_url, api_version='v2')

        try:
            # Check if the API connection is valid
            self.api.get_account()
            print("Successfully connected to Alpaca API.")
        except APIError as e:
            print(f"Error connecting to Alpaca API: {e}")
            # Depending on the desired behavior, you might want to raise the exception
            # or handle it by setting a state that indicates the adapter is not functional.
            raise

    async def get_latest_trade(self, symbol: str):
        """Fetches the latest trade for a given symbol."""
        try:
            # Alpaca API uses REST, which is synchronous by default.
            # For async usage in FastAPI/asyncio, it's common to run sync SDK calls
            # in a thread pool executor to avoid blocking the event loop.
            # However, the alpaca-trade-api v1.x SDK itself is not inherently async.
            # For simplicity in this step, we'll make a synchronous call.
            # In a production system, consider using asyncio.to_thread (Python 3.9+)
            # or an async-compatible Alpaca library if available.
            trade = self.api.get_latest_trade(symbol)
            return trade
        except APIError as e:
            print(f"Error fetching latest trade for {symbol} from Alpaca: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching latest trade for {symbol}: {e}")
            return None

# Example usage (for testing purposes, can be removed later)
if __name__ == '__main__':
    # Ensure you have ALPACA_API_KEY, ALPACA_SECRET_KEY, and optionally ALPACA_PAPER set as env vars
    # For example:
    # export ALPACA_API_KEY='YOUR_KEY_ID'
    # export ALPACA_SECRET_KEY='YOUR_SECRET_KEY'
    # export ALPACA_PAPER='True'
    try:
        adapter = AlpacaAdapter()
        # Example: Fetch latest trade for BTC/USD (ensure symbol format is correct for Alpaca)
        # Alpaca uses symbols like 'BTCUSD' for crypto or 'AAPL' for stocks.
        # The exact symbol format might depend on your Alpaca account and what they support.
        # For this example, let's assume 'BTCUSD' is a valid symbol.
        # trade_data = asyncio.run(adapter.get_latest_trade('BTCUSD')) # if get_latest_trade were async
        # Since it's sync now:
        trade_data = adapter.get_latest_trade('AAPL') # Using a common stock symbol for example
        if trade_data:
            print(f"Latest trade for AAPL: Price={trade_data.p}, Timestamp={trade_data.t}")
        else:
            print("Could not retrieve trade data for AAPL.")
    except ValueError as ve:
        print(ve)
    except APIError as apie:
        print(f"Alpaca API Error during example usage: {apie}")
    except Exception as ex:
        print(f"Unexpected error during example usage: {ex}")
