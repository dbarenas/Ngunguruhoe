import asyncio
from typing import Any, List, Tuple, Optional
from Ngunguruhoe.domain.models.alert import Alert
from Ngunguruhoe.domain.ports.alert_port import AlertPort
from Ngunguruhoe.adapters.alpaca_adapter import AlpacaAdapter # For type hinting if needed, or mock structure
from alpaca_trade_api.rest import APIError # For simulating API errors
from alpaca_trade_api.entity import Trade # For simulating trade data
from datetime import datetime

class MockAlpacaAdapter:
    """Mocks the AlpacaAdapter for testing purposes."""
    def __init__(self):
        self.mock_trade_data: Optional[Trade] = None
        self.simulate_api_error = False
        self.error_message = "Mock API Error"
        self.connection_error = False
        self.connection_error_message = "Mock Connection Error"

    def __call__(self, *args, **kwargs): # Allow instantiation like AlpacaAdapter()
        if self.connection_error:
            # Simulate an error during __init__ like the real adapter might
            raise APIError({"message": self.connection_error_message, "code": 500})
        return self

    def set_trade_data(self, symbol: str, price: float, ts: Optional[datetime] = None):
        """Sets the trade data to be returned by get_latest_trade."""
        if ts is None:
            ts = datetime.utcnow()
        # The Trade entity can be complex. We'll create a simple representation.
        # Adjust attributes based on what SimpleMarketTrendStrategy actually uses (e.g., 'p' for price).
        self.mock_trade_data = Trade({
            't': ts.isoformat(),
            'p': price,
            's': symbol,
            # Add other fields if your strategy or service uses them
            'x': 'MOCK_EXCHANGE', 'i': 12345, 'z': 'A', 'c': [], 'er': None, 'tks': None
        })
        self.simulate_api_error = False

    def set_no_data(self):
        self.mock_trade_data = None
        self.simulate_api_error = False

    def set_api_error(self, message="Mock API Error"):
        self.simulate_api_error = True
        self.error_message = message
        self.mock_trade_data = None # No data when there's an error

    def set_connection_error(self, message="Mock Connection Error"):
        """Simulates an error during AlpacaAdapter instantiation."""
        self.connection_error = True
        self.connection_error_message = message

    async def get_latest_trade(self, symbol: str) -> Optional[Trade]:
        """Mocks fetching the latest trade."""
        if self.simulate_api_error:
            raise APIError({"message": self.error_message, "code": 400})
        # Ensure the symbol matches if multiple symbols are being tested, though current mock is simple
        if self.mock_trade_data and self.mock_trade_data.s == symbol:
            return self.mock_trade_data
        elif self.mock_trade_data and self.mock_trade_data.s != symbol:
             # If data is set for a different symbol, return None for this one
            return None
        return self.mock_trade_data

class MockAlertRepository(AlertPort):
    """Mocks the AlertPort (e.g., SQLiteAlertRepository) for testing purposes."""
    def __init__(self):
        self.alerts_saved: List[Alert] = []
        self.simulate_save_error = False
        self.save_error_message = "Mock DB Save Error"
        self.simulate_get_error = False
        self.get_error_message = "Mock DB Get Error"
        self.init_db_called = False

    async def init_db(self):
        self.init_db_called = True
        print("MockAlertRepository: init_db called")

    async def save_alert(self, alert: Alert):
        if self.simulate_save_error:
            raise Exception(self.save_error_message)
        self.alerts_saved.append(alert)
        print(f"MockAlertRepository: Saved alert: {alert}")

    async def get_latest_alert(self) -> Optional[Alert]:
        if self.simulate_get_error:
            raise Exception(self.get_error_message)
        if not self.alerts_saved:
            return None
        # Return a copy to mimic database behavior (optional, but good practice)
        latest_alert_copy = Alert(**self.alerts_saved[-1].__dict__)
        return latest_alert_copy

    def clear_alerts(self):
        self.alerts_saved = []

    def set_save_error(self, message="Mock DB Save Error"):
        self.simulate_save_error = True
        self.save_error_message = message

    def set_get_error(self, message="Mock DB Get Error"):
        self.simulate_get_error = True
        self.get_error_message = message
