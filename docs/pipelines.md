# Pipelines

Il cuore del data engineering in Ferrox-Py-Utils è il `PipelineOrchestrator`.

## PipelineOrchestrator
Un motore lineare che esegue una catena di responsabilità (Chain of Responsibility pattern) per processare i dati.

### Funzionamento
1. **Contesto Condiviso**: Un dizionario (o oggetto) `context` passa da uno step all'altro.
2. **Aggiunta Step**: I task vengono aggiunti tramite `add_step(name, function)`.
3. **Esecuzione**: Il metodo `execute()` lancia la sequenza e gestisce le eccezioni, implementando eventualmente retry policies o log alert.

### Esempio Pratico
```python
from ferrox_py_utils.pipelines.orchestrator import PipelineOrchestrator

def extract(ctx):
    ctx['raw_data'] = [1, 2, 3]
    return ctx

def transform(ctx):
    ctx['transformed'] = [x * 10 for x in ctx['raw_data']]
    return ctx

pipeline = PipelineOrchestrator()
pipeline.add_step("estrazione", extract)
pipeline.add_step("trasformazione", transform)

final_context = pipeline.execute()
assert final_context['transformed'] == [10, 20, 30]
```
