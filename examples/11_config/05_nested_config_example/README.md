# Nested YAML Configuration

Shows how to work with deeply nested YAML configurations.

## What It Does

This example demonstrates:
- Creating deeply nested YAML structures
- Accessing values at multiple nesting levels
- Reading nested settings for app configuration

## Example

```python
from wpipe.util import leer_yaml

config = leer_yaml("nested.yaml")
db_host = config["app"]["settings"]["database"]["host"]
```

## Config Flow

```mermaid
graph LR
    A[Nested YAML] --> B[leer_yaml]
    B --> C[Access Level 1]
    C --> D[Access Level 2]
    D --> E[Access Level 3]
    E --> F[Get Value]
```

## Nested Access Sequence

```mermaid
sequenceDiagram
    participant App as Application
    participant YAML as YAML File
    participant Config as Config Dict
    
    App->>YAML: Load file
    App->>Config: config["app"]
    App->>Config: config["app"]["settings"]
    App->>Config: config["app"]["settings"]["database"]
    App->>Config: config["app"]["settings"]["database"]["host"]
    Config-->>App: Return "localhost"
```

## Config Structure

```mermaid
graph TB
    subgraph Root
        A[app]
    end
    subgraph App Level
        B[name]
        C[version]
        D[settings]
    end
    subgraph Settings Level
        E[database]
        F[cache]
    end
    subgraph Database
        G[host]
        H[port]
        I[name]
    end
    subgraph Cache
        J[enabled]
        K[ttl]
    end
    A --> B
    A --> C
    A --> D
    D --> E
    D --> F
    E --> G
    E --> H
    E --> I
    F --> J
    F --> K
```

## Nesting States

```mermaid
stateDiagram-v2
    [*] --> RootLevel
    RootLevel --> AppLevel: config["app"]
    AppLevel --> SettingsLevel: config["app"]["settings"]
    SettingsLevel --> DatabaseLevel: .database
    SettingsLevel --> CacheLevel: .cache
    DatabaseLevel --> GetValue: .host
    CacheLevel --> GetValue: .enabled
    GetValue --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Define Structure] --> B[Nested Dict]
    B --> C[Write YAML]
    C --> D[Load YAML]
    D --> E[Navigate Levels]
    E --> F[Access Values]
    F --> G[Use in Code]
```
