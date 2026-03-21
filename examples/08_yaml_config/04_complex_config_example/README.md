# Complex Multi-Environment Configuration

Demonstrates complex YAML configurations with multiple sections and environment profiles.

## What It Does

This example shows:
- Multi-environment configuration structures
- Switching between development, testing, and production
- Organizing configuration by sections (app, pipeline, connections)
- Configuring pipelines based on environment

## Example

```python
from wpipe.util import leer_yaml

config = leer_yaml("multienv.yaml")
entorno = "produccion"
env_config = config["entornos"][entorno]
```

## Config Flow

```mermaid
graph LR
    A[Multi-Env Config] --> B[Select Environment]
    B --> C[Get Settings]
    C --> D[Configure Pipeline]
    D --> E[Run with Env Params]
```

## Environment Selection

```mermaid
sequenceDiagram
    participant App as Application
    participant Config as YAML Config
    participant Dev as Dev Env
    participant Test as Test Env
    participant Prod as Prod Env
    
    App->>Config: Load config
    App->>App: Select environment
    alt desarrollo
        App->>Dev: Use dev settings
    else pruebas
        App->>Test: Use test settings
    else produccion
        App->>Prod: Use prod settings
    end
```

## Config Structure

```mermaid
graph TB
    subgraph Root
        A[config]
    end
    subgraph Application
        B[aplicacion]
        C[nombre]
        D[version]
    end
    subgraph Environments
        E[entornos]
        F[desarrollo]
        G[pruebas]
        H[produccion]
    end
    subgraph Pipeline
        I[pipeline]
        J[timeout]
        K[reintentos]
    end
    subgraph Connections
        L[conexiones]
        M[oracle]
        N[postgresql]
    end
    A --> B
    A --> E
    A --> I
    A --> L
    B --> C
    B --> D
    I --> J
    I --> K
    E --> F
    E --> G
    E --> H
    L --> M
    L --> N
```

## Environment States

```mermaid
stateDiagram-v2
    [*] --> LoadConfig
    LoadConfig --> SelectEnv: Parse YAML
    SelectEnv --> DevMode: entorno=desarrollo
    SelectEnv --> TestMode: entorno=pruebas
    SelectEnv --> ProdMode: entorno=produccion
    DevMode --> Configured: Apply settings
    TestMode --> Configured: Apply settings
    ProdMode --> Configured: Apply settings
    Configured --> RunPipeline: Execute
    RunPipeline --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Create Multi-Env<br/>Config] --> B[Define Sections]
    B --> C[envs, pipeline,<br/>conexiones]
    C --> D[Load Config]
    D --> E[Select Environment]
    E --> F[Extract Settings]
    F --> G[Configure & Run]
```
