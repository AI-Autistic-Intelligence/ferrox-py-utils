from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any

class DataConnector(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def extract(self, query: str | None = None) -> AsyncGenerator[Any, None]:
        yield None
        
    @abstractmethod
    async def load(self, data: Any) -> bool:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
