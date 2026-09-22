# Schema Registry

Il modulo `schemas` garantisce la data quality. Quando i dati vengono estratti da sorgenti non tipizzate (come CSV o JSON esterni), la validazione è critica per non inquinare il Database (Layer Bronze/Silver/Gold).

## Registry
- **Registrazione**: Mappa stringhe (nomi di schema) a classi Pydantic o Dataclasses.
- **Validazione**: Durante una pipeline, un nodo può chiamare `SchemaRegistry.validate("user_import", raw_dict)` per fare casting e validazione rigorosa.

```python
from ferrox_py_utils.schemas.registry import SchemaRegistry
from pydantic import BaseModel

class UserImport(BaseModel):
    id: int
    email: str

registry = SchemaRegistry()
registry.register("user", UserImport)

# Validazione automatica
valid_user = registry.validate("user", {"id": "123", "email": "test@test.com"})
print(valid_user.id)  # Diventa int(123)
```
