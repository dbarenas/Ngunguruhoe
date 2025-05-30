from dataclasses import dataclass
from datetime import datetime

@dataclass
class Alert:
    timestamp: datetime
    symbol: str
    action: str  # 'buy', 'sell', etc.
    confidence: float
