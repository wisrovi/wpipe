# Pipeline with YAML Configuration

Shows how to configure and execute a Pipeline using YAML configuration files.

## What It Does

This example demonstrates:
- Creating YAML configuration for pipelines
- Loading configuration with `leer_yaml()`
- Dynamically configuring pipeline steps based on config
- Executing a configured pipeline

## Example

```python
from wpipe import Pipeline
from wpipe.util import leer_yaml, escribir_yaml

config = leer_yaml("pipeline_config.yaml")
pipeline = Pipeline(verbose=config["parametros"]["verbose"])
pipeline.set_steps([(step_func, "Name", "v1.0")])
result = pipeline.run(data)
```

## Config Flow

```mermaid
graph LR
    A[YAML Config] --> B[leer_yaml]
    B --> C[Extract Params]
    C --> D[Configure Pipeline]
    D --> E[Execute Steps]
    E --> F[Return Result]
```

## Loading Sequence

```mermaid
sequenceDiagram
    participant User
    participant YAML as YAML File
    participant Util as wpipe.util
    participant Pipeline as Pipeline
    
    User->>YAML: Load config file
    User->>Util: Call leer_yaml()
    Util-->>User: Return config dict
    User->>Pipeline: Create Pipeline(verbose)
    User->>User: Configure steps from config
    User->>Pipeline: Call set_steps()
    User->>Pipeline: Call run(data)
    Pipeline-->>User: Return result
```

## Config Structure

```mermaid
graph TB
    subgraph YAML Config
        A[Root]
    end
    subgraph Pipeline Section
        B[pipeline]
        C[nombre]
        D[descripcion]
    end
    subgraph Parameters
        E[parametros]
        F[valor]
        G[multiplicador]
        H[verbose]
    end
    subgraph Steps
        I[pasos]
        J[validacion]
        K[procesamiento]
        L[formateo]
    end
    A --> B
    A --> E
    A --> I
    B --> C
    B --> D
    E --> F
    E --> G
    E --> H
    I --> J
    I --> K
    I --> L
```

## Pipeline States

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Configured: Load YAML
    Configured --> Ready: Set steps
    Ready --> Running: Call run()
    Running --> Step1: Execute step1
    Step1 --> Step2: Execute step2
    Step2 --> Step3: Execute step3
    Step3 --> Completed: All done
    Completed --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Create YAML] --> B[Write Config]
    B --> C[Load Config]
    C --> D[Extract Params]
    D --> E[Create Pipeline]
    E --> F[Configure Steps]
    F --> G[Run Pipeline]
    G --> H[Get Result]
```
