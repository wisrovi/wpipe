# Environment Variables in YAML Config

Shows how to use environment variables within YAML configuration files.

## What It Does

This example demonstrates:
- Setting environment variables in Python
- Including environment variable values in YAML configs
- Loading and using env-based configurations

## Example

```python
import os
from wpipe.util import leer_yaml

os.environ["TEST_VAR"] = "test_value"
config = {"env_var": os.environ.get("TEST_VAR")}
escribir_yaml("config.yaml", config)
loaded = leer_yaml("config.yaml")
```

## Config Flow

```mermaid
graph LR
    A[Env Variable] --> B[Set Value]
    B --> C[Include in Dict]
    C --> D[Write YAML]
    D --> E[Load YAML]
    E --> F[Use Value]
```

## Env Loading Sequence

```mermaid
sequenceDiagram
    participant Code as Python Code
    participant OS as OS Env
    participant Dict as Config Dict
    participant YAML as YAML File
    participant Util as wpipe.util
    
    Code->>OS: os.environ["VAR"] = "value"
    OS-->>Code: Variable set
    Code->>Dict: Create dict with env var
    Code->>YAML: Write to file
    Code->>Util: Call leer_yaml()
    Util-->>Code: Return config
    Code->>Code: Use env value
```

## Config Structure

```mermaid
graph TB
    subgraph Environment
        A[Environment Variables]
    end
    subgraph Config Dict
        B[env_var]
    end
    subgraph Value
        C[os.environ.get<br/>["VAR_NAME"]]
    end
    A --> C
    C --> B
```

## Env States

```mermaid
stateDiagram-v2
    [*] --> SetEnv
    SetEnv --> ReadEnv: os.environ.get()
    ReadEnv --> IncludeInDict: Add to config
    IncludeInDict --> WriteYAML: Serialize
    WriteYAML --> LoadYAML: leer_yaml()
    LoadYAML --> Retrieve: Access value
    Retrieve --> UseValue: Use in pipeline
    UseValue --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Set Environment<br/>Variable] --> B[Get Variable<br/>Value]
    B --> C[Include in<br/>Config Dict]
    C --> D[Write to YAML<br/>File]
    D --> E[Load with<br/>leer_yaml]
    E --> F[Retrieve<br/>Value]
    F --> G[Use in Code]
```
