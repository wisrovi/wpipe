# 10 Worker Metadata

Demonstrates passing custom metadata to the worker registration.
Metadata can include version info, environment, tags, etc.

## What it evaluates

- worker_metadata parameter in api_config
- Metadata is sent during worker registration
- Pipeline can track worker properties

## Flow

```mermaid
graph LR
    A[Metadata Config] --> B[Pipeline]
    B --> C[Register Worker]
    C --> D[Execute Steps]
    D --> E[Result]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as API
    
    P->>A: Register with metadata
    A-->>P: Worker ID
    P->>P: Execute steps
    P-->>P: Complete
```

```mermaid
graph TB
    subgraph Metadata
        M1[version]
        M2[environment]
        M3[tags]
    end
    
    subgraph Execution
        E[Steps]
    end
    
    subgraph Result
        R[Output]
    end
    
    M1 --> E
    M2 --> E
    M3 --> E
    E --> R
```

```mermaid
stateDiagram-v2
    [*] --> Register
    Register --> Execute
    Execute --> Complete
    Complete --> [*]
```

```mermaid
flowchart LR
    M([Metadata]) --> P([Pipeline])
    P --> E([Execute])
    E --> O([Result])
    
    style M fill:#e1f5fe
    style O fill:#c8e6c9
```
