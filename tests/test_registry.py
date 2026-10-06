import pytest
from ferrox_py.core.errors import FerroxError

from ferrox_py_utils.schemas.registry import SchemaRegistry


def test_schema_registry_success():
    registry = SchemaRegistry()
    registry.register_schema("User", {"id": (int, ...), "name": (str, ...)})
    
    # Valid payload
    payload = {"id": 1, "name": "John Doe"}
    validated = registry.validate("User", payload)
    
    assert validated["id"] == 1
    assert validated["name"] == "John Doe"

def test_schema_registry_invalid_data():
    registry = SchemaRegistry()
    registry.register_schema("User", {"id": (int, ...), "name": (str, ...)})
    
    # Invalid payload (missing name)
    payload = {"id": 1}
    with pytest.raises(FerroxError) as exc_info:
        registry.validate("User", payload)
        
    assert exc_info.value.status_code == 400

def test_schema_registry_not_found():
    registry = SchemaRegistry()
    
    with pytest.raises(FerroxError) as exc_info:
        registry.validate("Unknown", {"id": 1})
        
    assert exc_info.value.status_code == 404
