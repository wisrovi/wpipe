# Dynamic YAML Loading

Shows dynamically loading and executing pipeline configurations from YAML files.

## What It Does

This example demonstrates:
- Creating YAML files with dynamic content
- Loading configurations at runtime
- Using loaded configurations in execution flow

## Example

```python
from wpipe.util import leer_yaml
import yaml

with open("config.yaml", "w") as f:
    yaml.dump({"steps": [...]}, f)

config = leer_yaml("config.yaml")
```

## Config Flow

```mermaid
graph LR
    A[Runtime Config] --> B[Create Dict]
    B --> C[Write YAML]
    C --> D[Load YAML]
    D --> E[Use Config]
```

## Dynamic Loading Sequence

```mermaid
sequenceDiagram
    participant Code as Python Code
    participant YAML as YAML Library
    participant FS as File System
    participant Util as wpipe.util
    
    Code->>YAML: Create config dict
    YAML-->>Code: Dict ready
    Code->>FS: Write to file
    Code->>Util: Call leer_yaml()
    Util->>FS: Read file
    FS-->>Util: Raw content
    Util->>YAML: Parse YAML
    YAML-->>Util: Parsed dict
    Util-->>Code: Return config
```

## Config Structure

```mermaid
graph TB
    subgraph Runtime Config
        A[Root Dict]
    end
    subgraph Steps Array
        B[steps]
    end
    subgraph Step Entry
        C[name]
        D[function]
    end
    A --> B
    B --> C
    B --> D
```

## Loading States

```mermaid
stateDiagram-v2
    [*] --> CreateDict
    CreateDict --> DumpYAML: yaml.dump()
    DumpYAML --> WriteFile: Write to disk
    WriteFile --> LoadYAML: leer_yaml()
    LoadYAML --> ReadFile: Open file
    ReadFile --> ParseYAML: Parse content
    ParseYAML --> Return: Return dict
    Return --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Build Config<br/>Dynamically] --> B[Serialize to YAML]
    B --> C[Save to File]
    C --> D[Load from File]
    D --> E[Parse YAML]
    E --> F[Use in Execution]
```
