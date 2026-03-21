# Message Processor Example

Demonstrates a message processor that simulates receiving messages and processes them through pipelines.

## What It Does

This example shows how to create a message processor with:
- Extraction of data from messages
- Data transformation and normalization
- Metadata enrichment
- Statistics tracking
- Persistence preparation

## Service Flow

```mermaid
graph LR
    A[Receive Message] --> B[Extract Fields]
    B --> C[Transform Data]
    C --> D[Enrich Metadata]
    D --> E[Prepare Persistence]
    E --> F[Store Result]
```

## Service Communication

```mermaid
sequenceDiagram
    participant Generator
    participant Processor as ProcesadorMensajes
    participant Pipeline
    participant Steps

    Generator->>Processor: procesar(msg)
    Processor->>Pipeline: run(msg)
    Pipeline->>Steps: paso_extraccion
    Steps-->>Pipeline: extracted fields
    Pipeline->>Steps: paso_transformacion
    Steps-->>Pipeline: transformed data
    Pipeline->>Steps: paso_enriquecimiento
    Steps-->>Pipeline: enriched data
    Pipeline->>Steps: paso_persistencia
    Steps-->>Pipeline: ready for storage
    Pipeline-->>Processor: result
    Processor-->>Generator: final result
```

## Service Structure

```mermaid
graph TB
    subgraph ProcesadorMensajes
        A[__init__] --> B[Logger]
        A --> C[Pipeline]
        C --> D[Extract Step]
        C --> E[Transform Step]
        C --> F[Enrich Step]
        C --> G[Persist Step]
    end
    H[Messages] --> I[procesar]
    I --> J[obtener_estadisticas]
```

## Processing States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: procesar()
    Processing --> Extract: Extract fields
    Extract --> Transform: Transform data
    Transform --> Enrich: Add metadata
    Enrich --> Persist: Prepare storage
    Persist --> Success: Complete
    Processing --> Error: Exception
    Success --> Idle
    Error --> Idle
```

## Pipeline Workflow

```mermaid
flowchart LR
    subgraph Input
        A["{id, tipo, datos}"]
    end
    subgraph Extraction
        B[Get id]
        C[Get tipo]
    end
    subgraph Transformation
        D[id_upper: UPPERCASE]
        E[tipo_normalized: lowercase]
    end
    subgraph Enrichment
        F[procesado_en: timestamp]
        G[pipeline_version: v1.0]
    end
    subgraph Persistence
        H[Build registro]
    end
    subgraph Output
        I["{listo_para_guardar: True}"]
    end
    
    A --> B --> D --> F --> H --> I
    A --> C --> E -.-> H
    D -.-> H
    E -.-> H
    G -.-> H
```
