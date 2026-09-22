# Connectors

Il modulo `connectors` standardizza l'accesso in lettura e scrittura a sorgenti esterne.

## BaseConnector
Classe astratta che definisce il contratto I/O.
```python
class BaseConnector(ABC):
    @abstractmethod
    def read(self, *args, **kwargs) -> Any: ...
    @abstractmethod
    def write(self, data: Any, *args, **kwargs) -> None: ...
```

## S3Connector
Permette l'interazione con servizi object storage compatibili con S3 (AWS, MinIO).
- **Inizializzazione**: Richiede `endpoint_url`, `access_key`, `secret_key`, e `bucket_name`.
- **Read**: Scarica un file in memoria o in locale (tramite `boto3`).
- **Write**: Carica flussi di byte o file locali sul bucket.

## CsvConnector
Semplifica la gestione di file CSV, supportando chunking tramite la libreria sottostante (spesso integrato con pandas o csv integrato).
- **Read**: Restituisce DataFrame o liste di dict.
- **Write**: Serializza strutture dati in formati tabellari.
