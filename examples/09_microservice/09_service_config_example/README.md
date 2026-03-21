# Dynamic Configuration Example

Demonstrates loading configuration dynamically into a service.

## What It Does

This example shows how to create a configurable service with:
- Dynamic configuration loading
- Configuration storage
- Pipeline processing
- Configuration access

## Service Flow

```mermaid
graph LR
    A[Create Config] --> B[Init Service]
    B --> C[Load Config]
    C --> D[Create Pipeline]
    
    E[Handle Request] --> F[Run Pipeline]
    F --> G[Return Result]
```

## Service Communication

```mermaid
sequenceDiagram
    participant App
    participant Service as ConfigurableService
    participant Pipeline

    App->>App: Create config
    App->>Service: __init__(config)
    Service->>Service: Store self.config
    Service->>Pipeline: Create pipeline
    Service-->>App: Service created

    App->>Service: handle(data)
    Service->>Pipeline: run(data)
    Pipeline-->>Service: result
    Service-->>App: result

    App->>Service: Access config
    Service-->>App: {timeout: 30, max_retries: 3}
```

## Service Structure

```mermaid
graph TB
    subgraph ConfigurableService
        A[__init__] --> B[Store config]
        B --> C[Pipeline]
        C --> D[get_config_value step]
    end
    
    E[handle] --> F[Run pipeline]
    F --> G[Return result]
```

## Configuration States

```mermaid
stateDiagram-v2
    [*] --> Initializing: __init__
    Initializing --> Configured: Store config
    Configured --> Processing: handle()
    Processing --> Configured: Complete
    Configured --> Accessing: Access config
    Accessing --> Configured: Return config
```

## Configuration Flow

```mermaid
flowchart LR
    subgraph App Setup
        A["config = {timeout: 30, max_retries: 3}"]
    end
    
    subgraph Service Init
        B["ConfigurableService(config)"]
        B --> C[Store self.config]
        C --> D[Create pipeline]
        D --> E[Set steps]
    end
    
    subgraph Handle Request
        F[handle(data)]
        F --> G[Run pipeline]
        G --> H[get_config_value]
        H --> I["{config_loaded: True}"]
    end
    
    A --> B
    E --> F
```

## Usage

```bash
python example.py
```

## Expected Output

```
Service configured with: {'timeout': 30, 'max_retries': 3}
```
