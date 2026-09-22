# 🛠️ Ferrox-Py-Utils (Data Engineering)

<p align="center">
  <b>Scaffolding e Utils per Data Platform e Pipeline ETL</b><br/>
  <i>Costruisci pipeline dati solide, riutilizzabili e indipendenti dal vendor cloud, seguendo la filosofia modulare di Ferrox-Py.</i>
</p>

---

## 1. Cosa fa questo pacchetto? (Overview)
`ferrox-py-utils` è un'estensione dell'ecosistema Ferrox-Py dedicata alla manipolazione e al movimento dei dati. Invece di dover riscrivere la logica per l'estrazione e il caricamento dei dati su ogni progetto, questo modulo ti fornisce dei `Connector` agnostici (es. S3, CSV) e un `PipelineOrchestrator` per mettere in sequenza i job di trasformazione.

## 2. Perché usare Ferrox-Py-Utils? (Filosofia)
L'ingegneria dei dati soffre spesso di "copia-incolla selvaggio". L'obiettivo qui è l'**agnosticismo**. Tutto ciò che sviluppiamo, che non è logica di dominio puro, deve poter essere riutilizzato in futuri progetti. 
Invece di costruire monolitici script ETL, utilizziamo un approccio a "matrioska", dove piccoli task isolati vengono iniettati nell'orchestratore di pipeline.

## 3. A chi si rivolge?
È pensato per **Data Engineer** e sviluppatori backend che devono tirar su in breve tempo una Data Platform per l'ingestion, il parsing e il caricamento di grossi file CSV, JSON o formati binari su Object Storage (come Amazon S3 o MinIO).

## 4. Come funziona? (Architettura)
L'architettura dei dati si basa su due pilastri:
- **Connectors**: Classi ereditate da una base astratta (`BaseConnector`) per standardizzare operazioni di I/O (Lettura/Scrittura/Cancellazione) in streaming.
- **PipelineOrchestrator**: Un motore di esecuzione lineare che prende in input uno stato condiviso (`context`), esegue i vari nodi in sequenza, e garantisce il corretto isolamento degli errori.
- **Schema Registry**: Supporto nativo (via Pydantic) per registrare e validare la conformità dei dataset in transito.

## 5. Come si installa?
Assicurati di utilizzare Python 3.11+.

```bash
# Il pacchetto core è un prerequisito concettuale
pip install -e .
```

Dipendenze primarie installate dal modulo:
- `boto3` (per le interazioni con i servizi S3 compatibili)
- `pandas` (per l'elaborazione rapida di dataframe)

## 6. Come si usa? (Quickstart)

```python
from ferrox_py_utils.connectors.s3 import S3Connector
from ferrox_py_utils.connectors.csv import CsvConnector
from ferrox_py_utils.pipelines.orchestrator import PipelineOrchestrator

# 1. Configurazione
s3_connector = S3Connector(
    endpoint_url="http://localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    bucket_name="bronze-layer"
)
csv_connector = CsvConnector(file_path="/tmp/dati.csv")

# 2. Creazione Pipeline
def step_leggi_da_csv(ctx):
    ctx['dati'] = csv_connector.read()
    print("CSV Letto con successo!")
    return ctx

def step_salva_su_s3(ctx):
    # Logica di upload in streaming
    s3_connector.write(f"backup/dati.csv", b"dati finti per ora")
    return ctx

# 3. Esecuzione
orchestrator = PipelineOrchestrator()
orchestrator.add_step("Lettura Dati", step_leggi_da_csv)
orchestrator.add_step("Salvataggio Dati", step_salva_su_s3)

context = orchestrator.execute()
```

## 7. L'Ecosistema Ferrox-Py
Questo modulo si integra perfettamente con:
- ⚡ [ferrox-py](../ferrox-py) - Sfrutta la Dependency Injection per instanziare i Connector globalmente.
- 🔒 [ferrox-py-auth](../ferrox-py-auth) - Utilizza il RBAC per definire chi può lanciare la pipeline.
