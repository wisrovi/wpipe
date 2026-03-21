# Service Dependencies Example

Demonstrates managing service dependencies.

## What It Does

This example shows how to create a dependent service with:
- Dependency injection
- Readiness checking
- Conditional processing
- Mock dependency for testing

## Service Flow

```mermaid
graph LR
    A[Create Dependency] --> B[Create Service]
    B --> C[Handle Request]
    C --> D{Check Ready?}
    D -->|Yes| E[Run Pipeline]
    D -->|No| F[Return Error]
    E --> G[Return Result]
```

## Service Communication

```mermaid
sequenceDiagram
    participant Test
    participant Service as DependentService
    participant Dependency
    participant Pipeline

    Test->>Dependency: Create MockDependency
    Dependency-->>Test: dependency ready
    Test->>Service: __init__(dependency)
    Service-->>Test: Service created

    Test->>Service: handle(data)
    Service->>Dependency: is_ready()
    Dependency-->>Service: True
    Service->>Pipeline: run(data)
    Pipeline-->>Service: result
    Service-->>Test: {processed: True}

    Note over Test,Dependency: If dependency not ready:
    Service->>Dependency: is_ready()
    Dependency-->>Service: False
    Service-->>Test: {error: Dependency not ready}
```

## Service Structure

```mermaid
graph TB
    subgraph MockDependency
        A[__init__] --> B[ready: True]
        C[is_ready] --> D[Return ready]
    end
    
    subgraph DependentService
        E[__init__] --> F[Store dependency]
        F --> G[Pipeline]
        G --> H[process_step]
    end
    
    I[handle] --> J[Check dependency]
    J --> K{Check result}
    K -->|Ready| G
    K -->|Not Ready| L[Return error]
```

## Dependency States

```mermaid
stateDiagram-v2
    [*] --> Initialized: __init__
    Initialized --> Ready: Dependency ready
    Ready --> Processing: handle()
    Processing --> CheckDependency: is_ready()
    CheckDependency --> PipelineReady: True
    CheckDependency --> PipelineNotReady: False
    PipelineReady --> RunningPipeline: Run pipeline
    PipelineNotReady --> Error: Return error
    RunningPipeline --> Ready: Complete
    Error --> Ready: Catch and return
```

## Dependency Check Flow

```mermaid
flowchart LR
    subgraph Dependency Check
        A[handle(data)]
        A --> B[is_ready()?]
        B --> C{Ready?}
    end
    
    subgraph Case: Ready
        C -->|Yes| D[Run pipeline]
        D --> E["{processed: True}"]
    end
    
    subgraph Case: Not Ready
        C -->|No| F["{error: Dependency not ready}"]
    end
```

## Usage

```bash
python example.py
```

## Expected Output

```
Result: {'processed': True}
```
