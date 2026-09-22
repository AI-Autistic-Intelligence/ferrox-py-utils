# 🛠️ Ferrox-Py-Utils (Data Engineering)

## 1. Overview (What does this do?)
The `ferrox-py-utils` package is a specialized extension of the Ferrox ecosystem dedicated to data manipulation, ETL (Extract, Transform, Load) pipelines, and cross-platform data movement. It provides agnostic `Connectors` (e.g., for AWS S3, CSV files, or REST APIs) and a `PipelineOrchestrator` to seamlessly sequence data transformation jobs without writing monolithic scripts.

## 2. Philosophy (Why does it exist?)
Data engineering often suffers from "wild copy-pasting" where scripts to import users or export CSVs are hastily written and tightly coupled to specific database schemas or cloud vendors. The philosophy here is absolute **agnosticism**. Instead of building monolithic ETL scripts, this package enforces a modular approach where small, isolated tasks are injected into an orchestrator. This allows data engineers to reuse extraction and validation logic across entirely different projects.

## 3. Target Audience (Who is it for?)
This package is built for Data Engineers and backend developers who need to quickly stand up a Data Platform for ingestion, parsing, and bulk loading of large datasets (like CSV or JSON) into Data Lakes or Object Storage (such as Amazon S3, MinIO, or Google Cloud Storage).

## 4. Architecture (How does it work?)
The data architecture rests on three pillars:
- **Connectors**: Classes inheriting from an abstract `BaseConnector` to standardize streaming I/O operations (Read/Write/Delete), entirely isolating the pipeline from the specific storage vendor.
- **PipelineOrchestrator**: A linear execution engine that passes a shared state (`context`) through a sequence of nodes (steps), ensuring proper error isolation and retry mechanics.
- **Schema Registry**: Native integration with Pydantic to register and enforce strict validation on datasets in transit, ensuring corrupted data never enters the database.

## 5. Installation / Setup
Ensure you are using Python 3.11+. The package installs basic dependencies, but you may need to install specific data drivers (like `boto3` or `pandas`) depending on the connectors you intend to use.

```bash
pip install ferrox-py-utils
# Optional extensions:
# pip install boto3 pandas
```

## 6. Quickstart (Usage)
```python
from ferrox_py_utils.connectors.csv import CsvConnector
from ferrox_py_utils.pipelines.orchestrator import PipelineOrchestrator

# 1. Setup the agnostic connector
csv_connector = CsvConnector(file_path="/tmp/data.csv")

# 2. Define isolated pipeline steps
def step_read_csv(ctx):
    ctx['data'] = csv_connector.read()
    return ctx

def step_transform(ctx):
    # Transform logic here...
    ctx['data'] = [row for row in ctx['data'] if row.get("active")]
    return ctx

# 3. Orchestrate and execute
orchestrator = PipelineOrchestrator()
orchestrator.add_step("Read Data", step_read_csv)
orchestrator.add_step("Clean Data", step_transform)

final_context = orchestrator.execute()
print(f"Processed {len(final_context['data'])} records.")
```

## 7. Ecosystem Integration
This module is fully integrated with the core `ferrox-py` ecosystem:
- **Core (IoC Container)**: The framework's Dependency Injection container is used to instantiate Connectors globally as Singletons, meaning you only initialize your S3 credentials once.
- **AuthModule (ferrox-py-auth)**: RBAC can be utilized to restrict which users or system roles are authorized to trigger specific data pipelines via the API Gateway.
