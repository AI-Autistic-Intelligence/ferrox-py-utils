import csv
import aiofiles
from typing import AsyncGenerator, Any
from .base import DataConnector
from ferrox_py.core.provider import injectable

@injectable()
class CsvConnector(DataConnector):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._file = None

    async def connect(self) -> None:
        # In a real app we'd keep it open for stream
        pass

    async def extract(self, query: str | None = None) -> AsyncGenerator[Any, None]:
        async with aiofiles.open(self.file_path, mode='r', encoding='utf-8') as f:
            header = None
            async for line in f:
                row = line.strip().split(",")
                if not header:
                    header = row
                    continue
                yield dict(zip(header, row))

    async def load(self, data: Any) -> bool:
        # Simplistic append
        async with aiofiles.open(self.file_path, mode='a', encoding='utf-8') as f:
            if isinstance(data, dict):
                await f.write(",".join(str(v) for v in data.values()) + "\n")
        return True

    async def close(self) -> None:
        pass
