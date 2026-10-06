from collections.abc import AsyncGenerator
from typing import Any

from ferrox_py.core.provider import injectable

from .base import DataConnector


@injectable()
class S3Connector(DataConnector):
    def __init__(self, bucket: str, path: str):
        self.bucket = bucket
        self.path = path
        # Would inject aioboto3 session here

    async def connect(self) -> None:
        print(f"Connecting to S3 Bucket: {self.bucket}...")

    async def extract(self, query: str | None = None) -> AsyncGenerator[Any, None]:
        print(f"Extracting streaming chunks from s3://{self.bucket}/{self.path}")
        # Mock streaming chunks
        yield {"chunk_id": 1, "data": b"mock_data"}

    async def load(self, data: Any) -> bool:
        print(f"Uploading chunk to s3://{self.bucket}/{self.path}")
        return True

    async def close(self) -> None:
        pass
