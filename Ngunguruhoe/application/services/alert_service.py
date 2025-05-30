from Ngunguruhoe.domain.models.alert import Alert
from Ngunguruhoe.domain.ports.alert_port import AlertPort
from Ngunguruhoe.domain.ports.strategy_port import StrategyPort
from Ngunguruhoe.adapters.alpaca_adapter import AlpacaAdapter # Assuming direct use of AlpacaAdapter
from datetime import datetime
import random # Keep for now if simple strategy still needs it
from typing import Any, Tuple

# Placeholder Simple Strategy (can be moved to its own file/adapter later)
class SimpleMarketTrendStrategy(StrategyPort):
    async def decide_action(self, market_data: Any) -> Tuple[str, float]:
        """
        A very simple strategy: if market_data (price) is not None, buy with 60% confidence.
        This is a placeholder and should be replaced with a real strategy.
        Assumes market_data is the trade object from AlpacaAdapter.get_latest_trade
        """
        if market_data and hasattr(market_data, 'p'): # 'p' is price in Alpaca trade object
            # Dummy logic: if price is above some arbitrary threshold, suggest buy, else sell.
            # This is not a real trading strategy.
            action = "buy" if market_data.p > 100 else "sell" # Example: BTC/USD price > 100 -> buy
            confidence = round(random.uniform(0.55, 0.75), 2) # Random confidence
            print(f"SimpleStrategy: Market price {market_data.p}, Action: {action}, Confidence: {confidence}")
            return action, confidence
        print("SimpleStrategy: No market data received or price attribute missing.")
        return "hold", 0.1 # Default action if no data

class AlertService:
    def __init__(self,
                 alert_repo: AlertPort,
                 market_data_provider: AlpacaAdapter, # Specific adapter for now
                 strategy: StrategyPort):
        self.alert_repo = alert_repo
        self.market_data_provider = market_data_provider
        self.strategy = strategy

    async def run_strategy_and_store(self, symbol: str = "AAPL"):
        """Fetches market data, runs the strategy, and stores the resulting alert."""
        print(f"AlertService: Fetching market data for {symbol}...")
        market_data = await self.market_data_provider.get_latest_trade(symbol)

        if market_data:
            print(f"AlertService: Market data for {symbol} received: Price={market_data.p}")
            action, confidence = await self.strategy.decide_action(market_data)
            print(f"AlertService: Strategy decided action {action} with confidence {confidence} for {symbol}")

            if action != "hold": # Only store alerts for buy/sell actions
                alert = Alert(
                    timestamp=datetime.utcnow(),
                    symbol=symbol,
                    action=action,
                    confidence=confidence
                )
                await self.alert_repo.save_alert(alert)
                print(f"AlertService: Alert stored: {alert}")
                return alert
            else:
                print(f"AlertService: Strategy decided 'hold' for {symbol}. No alert stored.")
                return None
        else:
            print(f"AlertService: Could not retrieve market data for {symbol}. No action taken.")
            # Optionally, create a different type of alert or notification here
            return None
