# Reading YAML Configuration Files

Demonstrates how to read YAML configuration files using the `wpipe.util` module.

## What It Does

This example shows how to:
- Create a YAML configuration file
- Read configuration values using `leer_yaml()`
- Access nested configuration sections
- Use default values for missing keys

## Example

```python
from wpipe.util import leer_yaml, escribir_yaml

config = leer_yaml("config.yaml")
timeout = config.get("configuracion", {}).get("timeout", 30)
```

## Config Flow

```mermaid
graph LR
    A[YAML File] --> B[leer_yaml]
    B --> C[Dict Object]
    C --> D[Access Values]
    D --> E[Use in Code]
```

## Loading Sequence

```mermaid
sequenceDiagram
    participant App as Application
    participant Util as wpipe.util
    participant FS as File System
    participant YAML as YAML Parser
    
    App->>FS: Open config.yaml
    FS-->>YAML: Raw file content
    YAML->>Util: Parse YAML
    Util->>App: Return dict
    App->>App: Use configuration
```

## Config Structure

```mermaid
graph TB
    subgraph Root
        A[config]
    end
    subgraph Sections
        B[servicio]
        C[version]
        D[entorno]
        E[configuracion]
        F[api]
        G[base_datos]
    end
    subgraph Nested
        H[timeout]
        I[reintentos]
        J[verbose]
    end
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    E --> H
    E --> I
    E --> J
```

## Loading States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Loading: Call leer_yaml()
    Loading --> Parsing: File opened
    Parsing --> Validating: YAML parsed
    Validating --> Success: Valid config
    Validating --> Error: Invalid YAML
    Success --> Idle: Config returned
    Error --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Create Config] --> B[Write YAML]
    B --> C[Store File]
    C --> D[Read YAML]
    D --> E[Parse Content]
    E --> F[Access Keys]
    F --> G[Use Values]
```
