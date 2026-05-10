from abc import ABC, abstractmethod
from typing import Any

class EventProducer(ABC):
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def send_event(self, topic: str, key: str, value: Any):
        pass
