# YAML Schema Validation

Shows validating YAML configuration against a schema structure.

## What It Does

This example demonstrates:
- Creating well-structured YAML configurations
- Loading and accessing validated configuration values
- Working with pipeline configurations with schema

## Example

```python
from wpipe.util import leer_yaml

config = leer_yaml("pipeline.yaml")
name = config["pipeline"]["name"]
version = config["pipeline"]["version"]
```

## Config Flow

```mermaid
graph LR
    A[Pipeline YAML] --> B[leer_yaml]
    B --> C[Validate Schema]
    C --> D[Access Fields]
    D --> E[Use Values]
```

## Validation Sequence

```mermaid
sequenceDiagram
    participant User
    participant YAML as YAML File
    participant Util as wpipe.util
    participant Config as Config Dict
    
    User->>YAML: Open pipeline.yaml
    User->>Util: Call leer_yaml()
    Util->>YAML: Read content
    YAML-->>Util: Raw YAML
    Util->>Config: Parse and validate
    Util-->>User: Return validated config
    User->>Config: Access fields
```

## Config Structure

```mermaid
graph TB
    subgraph Pipeline Config
        A[pipeline]
    end
    subgraph Required Fields
        B[name]
        C[version]
        D[steps]
    end
    subgraph Steps Array
        E[step 1]
        F[step 2]
        G[step n]
    end
    A --> B
    A --> C
    A --> D
    D --> E
    D --> F
    D --> G
```

## Validation States

```mermaid
stateDiagram-v2
    [*] --> LoadFile
    LoadFile --> ParseYAML: yaml.parse()
    ParseYAML --> Validate: Check schema
    Validate --> Valid: Schema OK
    Validate --> Invalid: Missing fields
    Valid --> AccessFields: Access values
    AccessFields --> UseConfig: Use in pipeline
    UseConfig --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Define Schema<br/>Structure] --> B[Create YAML<br/>Config File]
    B --> C[Load with<br/>leer_yaml]
    C --> D[Validate<br/>Structure]
    D --> E[Access Required<br/>Fields]
    E --> F[Use in Pipeline]
```
