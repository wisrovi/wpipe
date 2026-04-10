# Writing YAML Configuration Files

Demonstrates how to write configuration data to YAML files using `wpipe.util`.

## What It Does

This example shows how to:
- Create simple and complex YAML configurations
- Write dictionaries to YAML files with `escribir_yaml()`
- Update existing configurations
- Build nested structures for pipelines

## Example

```python
from wpipe.util import leer_yaml, escribir_yaml

config = {"nombre": "mi_pipeline", "version": "1.0.0"}
escribir_yaml("config.yaml", config)
```

## Config Flow

```mermaid
graph LR
    A[Dict Object] --> B[escribir_yaml]
    B --> C[YAML Formatter]
    C --> D[YAML File]
```

## Writing Sequence

```mermaid
sequenceDiagram
    participant App as Application
    participant Util as wpipe.util
    participant YAML as YAML Library
    participant FS as File System
    
    App->>Util: Call escribir_yaml(path, dict)
    Util->>YAML: Serialize dict to YAML
    YAML-->>Util: YAML string
    Util->>FS: Write to file
    FS-->>Util: File saved
    Util-->>App: Success
```

## Config Structure

```mermaid
graph TB
    subgraph Configuration
        A[Root Config]
    end
    subgraph Simple Fields
        B[nombre]
        C[version]
        D[ambiente]
    end
    subgraph Complex Fields
        E[parametros]
        F[conexiones]
        G[caracteristicas]
    end
    subgraph Nested
        H[timeout]
        I[workers]
        J[api]
        K[base_datos]
    end
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    E --> H
    E --> I
    F --> J
    F --> K
```

## Write States

```mermaid
stateDiagram-v2
    [*] --> Preparing
    Preparing --> Building: Create dict
    Building --> Serializing: Call escribir_yaml
    Serializing --> Formatting: Convert to YAML
    Formatting --> Writing: Write to file
    Writing --> Success: File saved
    Success --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Build Dict] --> B[Simple Config]
    A --> C[Complex Config]
    C --> D[nested structures]
    B --> E[escribir_yaml]
    D --> E
    E --> F[Save to File]
    F --> G[Verify Content]
```
