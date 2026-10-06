import os

import aiofiles
import pytest

from ferrox_py_utils.connectors.csv import CsvConnector


@pytest.fixture
def test_csv_path():
    path = "test_data.csv"
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.mark.asyncio
async def test_csv_connector(test_csv_path):
    # Setup mock CSV
    async with aiofiles.open(test_csv_path, "w", encoding="utf-8") as f:
        await f.write("id,name\n1,Alice\n2,Bob\n")

    connector = CsvConnector(test_csv_path)
    
    results = []
    async for row in connector.extract():
        results.append(row)
        
    assert len(results) == 2
    assert results[0] == {"id": "1", "name": "Alice"}
    assert results[1] == {"id": "2", "name": "Bob"}
    
    # Test load
    await connector.load({"id": "3", "name": "Charlie"})
    
    results2 = []
    async for row in connector.extract():
        results2.append(row)
        
    assert len(results2) == 3
    assert results2[2] == {"id": "3", "name": "Charlie"}
