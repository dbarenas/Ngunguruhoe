import pytest
from Ngunguruhoe.application.services.alert_service import AlertService, SimpleMarketTrendStrategy
from Ngunguruhoe.tests.mocks import MockAlpacaAdapter, MockAlertRepository

# Pytest fixtures (can also be in a conftest.py in tests/e2e or tests/)
@pytest.fixture
def mock_alpaca_adapter_e2e(): # Renamed to avoid potential fixture collision if tests run together
    return MockAlpacaAdapter()

@pytest.fixture
def mock_alert_repo_e2e(): # Renamed
    return MockAlertRepository()

@pytest.fixture
def simple_strategy_e2e(): # Renamed
    return SimpleMarketTrendStrategy()

@pytest.fixture
def alert_service_e2e(mock_alert_repo_e2e, mock_alpaca_adapter_e2e, simple_strategy_e2e):
    return AlertService(alert_repo=mock_alert_repo_e2e,
                        market_data_provider=mock_alpaca_adapter_e2e,
                        strategy=simple_strategy_e2e)

@pytest.mark.asyncio
@pytest.mark.parametrize("price, expected_action", [
    (150.0, "buy"),   # Case 1: Price significantly above threshold
    (50.0, "sell"),   # Case 2: Price significantly below threshold
    (100.01, "buy"),  # Case 3: Price just above threshold
    (100.00, "sell"), # Case 4: Price exactly at threshold
    (99.99, "sell"),  # Case 5: Price just below threshold
])
async def test_strategy_produces_correct_action_via_service(
        alert_service_e2e, mock_alpaca_adapter_e2e, mock_alert_repo_e2e, price, expected_action):
    test_symbol = f"E2E_{expected_action.upper()}_{price}"
    mock_alpaca_adapter_e2e.set_trade_data(symbol=test_symbol, price=price)

    await alert_service_e2e.run_strategy_and_store(symbol=test_symbol)

    assert len(mock_alert_repo_e2e.alerts_saved) == 1, f"Expected 1 alert for price {price}, got {len(mock_alert_repo_e2e.alerts_saved)}"
    saved_alert = mock_alert_repo_e2e.alerts_saved[0]

    assert saved_alert.symbol == test_symbol
    assert saved_alert.action == expected_action
    assert 0.55 <= saved_alert.confidence <= 0.75 # Check confidence range

@pytest.mark.asyncio
async def test_strategy_handles_no_market_data_via_service(
        alert_service_e2e, mock_alpaca_adapter_e2e, mock_alert_repo_e2e):
    test_symbol = "E2E_NO_DATA"
    mock_alpaca_adapter_e2e.set_no_data() # No data from Alpaca

    result_alert = await alert_service_e2e.run_strategy_and_store(symbol=test_symbol)

    assert result_alert is None, "Expected no alert to be returned by service for no data"
    assert len(mock_alert_repo_e2e.alerts_saved) == 0, "Expected no alert to be saved for no data"

@pytest.mark.asyncio
async def test_strategy_handles_market_data_missing_price_attr_via_service(
    alert_service_e2e, mock_alpaca_adapter_e2e, mock_alert_repo_e2e
):
    test_symbol = "E2E_MISSING_ATTR"
    # Simulate market data that is not None, but doesn't have 'p' (price attribute)
    # The MockAlpacaAdapter's set_trade_data always creates a 'p' attribute.
    # So, we'll manually set mock_trade_data to something that won't have 'p'
    # or rely on SimpleMarketTrendStrategy's `hasattr(market_data, 'p')` check.
    # A simple way is to provide a Trade object with a different structure or None price.
    # For this test, let's simulate the Alpaca mock returning data that our strategy might not understand
    # by giving it a Trade object where 'p' is None (if the Trade object allows it)
    # or a custom object.

    # The current SimpleMarketTrendStrategy checks `hasattr(market_data, 'p')`
    # and `market_data` itself. If `market_data` is an object without 'p', it should result in 'hold'.
    class DummyMarketDataWithoutPrice:
        pass

    # We need to make the mock adapter return this custom object.
    # This requires a slight modification to MockAlpacaAdapter or a new mock method for this specific test case.
    # For now, let's assume we can make get_latest_trade return this:
    mock_alpaca_adapter_e2e.mock_trade_data = DummyMarketDataWithoutPrice() # type: ignore
    mock_alpaca_adapter_e2e.simulate_api_error = False # Ensure no API error

    result_alert = await alert_service_e2e.run_strategy_and_store(symbol=test_symbol)

    assert result_alert is None, "Expected no alert returned for data missing price attribute"
    assert len(mock_alert_repo_e2e.alerts_saved) == 0, "Expected no alert saved for data missing price attribute"
