import pytest
from datetime import datetime, timezone
from Ngunguruhoe.application.services.alert_service import AlertService, SimpleMarketTrendStrategy
from Ngunguruhoe.domain.models.alert import Alert
from Ngunguruhoe.tests.mocks import MockAlpacaAdapter, MockAlertRepository
from alpaca_trade_api.entity import Trade # For type hinting mock trade data

@pytest.fixture
def mock_alpaca_adapter():
    return MockAlpacaAdapter()

@pytest.fixture
def mock_alert_repo():
    repo = MockAlertRepository()
    # asyncio.run(repo.init_db()) # Not strictly necessary for mock if init_db is simple
    return repo

@pytest.fixture
def simple_strategy():
    return SimpleMarketTrendStrategy()

@pytest.fixture
def alert_service(mock_alert_repo, mock_alpaca_adapter, simple_strategy):
    return AlertService(alert_repo=mock_alert_repo,
                        market_data_provider=mock_alpaca_adapter,
                        strategy=simple_strategy)

@pytest.mark.asyncio
async def test_run_strategy_and_store_buy_alert(alert_service, mock_alpaca_adapter, mock_alert_repo):
    test_symbol = "TESTBUY"
    test_price = 150.0 # This price should trigger 'buy' in SimpleMarketTrendStrategy (price > 100)
    mock_alpaca_adapter.set_trade_data(symbol=test_symbol, price=test_price)

    result_alert = await alert_service.run_strategy_and_store(symbol=test_symbol)

    assert result_alert is not None
    assert len(mock_alert_repo.alerts_saved) == 1
    saved_alert = mock_alert_repo.alerts_saved[0]

    assert saved_alert.symbol == test_symbol
    assert saved_alert.action == "buy"
    assert saved_alert.confidence > 0.5 # Based on SimpleMarketTrendStrategy
    assert result_alert.symbol == test_symbol
    assert result_alert.action == "buy"

@pytest.mark.asyncio
async def test_run_strategy_and_store_sell_alert(alert_service, mock_alpaca_adapter, mock_alert_repo):
    test_symbol = "TESTSELL"
    test_price = 50.0 # This price should trigger 'sell' in SimpleMarketTrendStrategy (price <= 100)
    mock_alpaca_adapter.set_trade_data(symbol=test_symbol, price=test_price)

    result_alert = await alert_service.run_strategy_and_store(symbol=test_symbol)

    assert result_alert is not None
    assert len(mock_alert_repo.alerts_saved) == 1
    saved_alert = mock_alert_repo.alerts_saved[0]

    assert saved_alert.symbol == test_symbol
    assert saved_alert.action == "sell"
    assert saved_alert.confidence > 0.5 # Based on SimpleMarketTrendStrategy
    assert result_alert.symbol == test_symbol
    assert result_alert.action == "sell"

@pytest.mark.asyncio
async def test_run_strategy_and_store_hold_action(alert_service, mock_alpaca_adapter, mock_alert_repo):
    test_symbol = "TESTHOLD"
    # Modify strategy or mock strategy's decide_action directly if SimpleMarketTrendStrategy can't easily produce 'hold'.
    # For now, SimpleMarketTrendStrategy produces buy/sell based on price. Let's assume a scenario where the strategy might output 'hold'.
    # To test 'hold', we'd need a strategy mock or a configurable strategy.
    # For this example, we'll assume SimpleMarketTrendStrategy's 'hold' is if market_data is None, which is covered by another test.
    # If we want to test an explicit 'hold' from strategy with valid data, we'd need to mock the strategy itself.
    # Let's test the case where no market data is available, which SimpleMarketTrendStrategy handles as 'hold'.
    mock_alpaca_adapter.set_no_data() # This will lead to SimpleMarketTrendStrategy returning 'hold', 0.1

    result_alert = await alert_service.run_strategy_and_store(symbol=test_symbol)

    assert result_alert is None # run_strategy_and_store returns None for 'hold'
    assert len(mock_alert_repo.alerts_saved) == 0

@pytest.mark.asyncio
async def test_run_strategy_no_market_data(alert_service, mock_alpaca_adapter, mock_alert_repo):
    test_symbol = "NODATA"
    mock_alpaca_adapter.set_no_data() # No data from Alpaca

    result_alert = await alert_service.run_strategy_and_store(symbol=test_symbol)

    assert result_alert is None
    assert len(mock_alert_repo.alerts_saved) == 0

@pytest.mark.asyncio
async def test_run_strategy_alpaca_api_error(alert_service, mock_alpaca_adapter, mock_alert_repo):
    test_symbol = "APIERROR"
    mock_alpaca_adapter.set_api_error(message="Simulated API Failure")

    result_alert = await alert_service.run_strategy_and_store(symbol=test_symbol)

    assert result_alert is None
    assert len(mock_alert_repo.alerts_saved) == 0

@pytest.mark.asyncio
async def test_alert_service_uses_correct_symbol(alert_service, mock_alpaca_adapter, mock_alert_repo):
    symbol_to_test = "UNIQUESYMBOL"
    mock_alpaca_adapter.set_trade_data(symbol=symbol_to_test, price=200) # price > 100 -> buy

    await alert_service.run_strategy_and_store(symbol=symbol_to_test)

    assert len(mock_alert_repo.alerts_saved) == 1
    saved_alert = mock_alert_repo.alerts_saved[0]
    assert saved_alert.symbol == symbol_to_test

@pytest.mark.asyncio
async def test_alert_timestamp_is_recent(alert_service, mock_alpaca_adapter, mock_alert_repo):
    test_symbol = "TSTIME"
    mock_alpaca_adapter.set_trade_data(symbol=test_symbol, price=200) # price > 100 -> buy

    before_call_utc = datetime.now(timezone.utc)
    await alert_service.run_strategy_and_store(symbol=test_symbol)
    after_call_utc = datetime.now(timezone.utc)

    assert len(mock_alert_repo.alerts_saved) == 1
    saved_alert = mock_alert_repo.alerts_saved[0]

    # Check if the alert's timestamp is within a reasonable window of the call
    # Allow for a small delta, e.g., a few seconds
    assert saved_alert.timestamp.tzinfo is not None # Ensure it's offset-aware if comparing
    alert_timestamp_utc = saved_alert.timestamp.astimezone(timezone.utc)

    assert before_call_utc <= alert_timestamp_utc <= after_call_utc
