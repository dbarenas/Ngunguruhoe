from abc import ABC, abstractmethod
from Ngunguruhoe.domain.models.alert import Alert

class AlertPort(ABC):
    @abstractmethod
    async def save_alert(self, alert: Alert):
        pass

    @abstractmethod
    async def get_latest_alert(self) -> Alert:
        pass
