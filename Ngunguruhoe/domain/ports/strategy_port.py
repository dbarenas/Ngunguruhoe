from abc import ABC, abstractmethod
from typing import Any, Tuple

class StrategyPort(ABC):
    @abstractmethod
    async def decide_action(self, market_data: Any) -> Tuple[str, float]:
        """
        Decides a trading action based on the provided market data.

        Args:
            market_data: The market data to analyze (e.g., latest trade, order book).
                         The exact type will depend on the data source and strategy needs.

        Returns:
            A tuple containing the action (str, e.g., 'buy', 'sell', 'hold')
            and confidence (float, e.g., 0.0 to 1.0).
        """
        pass
