# 02 Worker ID

Demonstrates worker ID management in API pipelines.
Shows how to set and track worker identity for API operations.

## What it evaluates

- Setting worker_id manually
- Tracking worker_id in pipeline
- Enabling API communication with worker_id
- Data transformation through pipeline steps

## Flow

```mermaid
graph LR
    A[Set Worker ID] --> B[Pipeline Ready]
    B --> C[Fetch Data]
    C --> D[Transform Data]
    D --> E[Result]
```

```mermaid
sequenceDiagram
    participant C as Client
    participant P as Pipeline
    
    C->>P: set_worker_id
    P->>P: Store ID
    C->>P: run
    P->>P: Execute steps
    P-->>C: Result
```

```mermaid
graph TB
    subgraph Config
        A[api_config]
        B[worker_id]
    end
    
    subgraph Steps
        C[fetch_data]
        D[transform_data]
    end
    
    subgraph Result
        E[transformed data]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
```

```mermaid
stateDiagram-v2
    [*] --> Configured
    Configured --> Ready
    Ready --> Executing
    Executing --> Complete
    Complete --> [*]
```

```mermaid
flowchart LR
    W[worker_id] --> P[Pipeline]
    P --> S[Steps]
    S --> R[Result]
    
    style W fill:#fff9c4
    style R fill:#c8e6c9
```
