# Ferrox-Py-Utils Overview

Il pacchetto `ferrox-py-utils` implementa un'architettura dati disaccoppiata basata su connettori scambiabili e una pipeline lineare.

## Architettura Dati

Invece di costruire script ETL isolati (es. `importa_utenti.py`, `esporta_ordini.py`), l'approccio di Ferrox-Py impone:
1. **Estrazione Isolata**: L'I/O (lettura file, download da S3, query DB) avviene tramite classi *Connectors* specializzate.
2. **Trasformazione in Memoria**: Un *Orchestrator* esegue una sequenza di funzioni (step) manipolando un contesto condiviso.
3. **Validazione Garantita**: Lo *Schema Registry* si assicura che il dato trasformato rispetti il contratto (DTO) prima di essere passato allo step successivo.

## Relazione con il Core
I componenti di questo pacchetto (es. `S3Connector`) sono progettati per essere registrati nel `Container` IoC di `ferrox-py`. Questo garantisce che la connessione (es. le credenziali di S3) venga inizializzata una sola volta (Singleton) e iniettata ovunque serva.
