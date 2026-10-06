from typing import Any

from ferrox_py.core.errors import FerroxError
from ferrox_py.core.provider import injectable
from pydantic import BaseModel, ValidationError, create_model


@injectable()
class SchemaRegistry:
    def __init__(self) -> None:
        self._schemas: dict[str, type[BaseModel]] = {}

    def register_schema(self, name: str, schema_def: dict[str, Any]) -> None:
        model = create_model(name, **schema_def)
        self._schemas[name] = model
        print(f"Schema '{name}' registered.")

    def validate(self, name: str, data: dict[str, Any]) -> dict[str, Any]:
        if name not in self._schemas:
            raise FerroxError(message=f"Schema {name} not found", status_code=404)
            
        model = self._schemas[name]
        try:
            instance = model(**data)
            return instance.model_dump()
        except ValidationError as e:
            raise FerroxError(message=f"Schema validation failed: {e.errors()}", status_code=400)
