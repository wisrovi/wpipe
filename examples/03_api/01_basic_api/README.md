# 01 Basic API

Demonstrates basic API configuration for a pipeline.
Shows how to set up a pipeline with API server connection.

## What it evaluates

- Creating Pipeline with api_config
- Worker registration with API server
- Graceful fallback when API is unavailable
- Processing data through pipeline steps

## Flow

```mermaid
graph LR
    A[Input] --> B[Pipeline]
    B --> C[Register Worker]
    C --> D{Check API}
    D -->|Yes| E[Run with API]
    D -->|No| F[Run Local]
    E --> G[Result]
    F --> G
```

```mermaid
sequenceDiagram
    participant C as Client
    participant P as Pipeline
    participant A as API Server
    
    C->>P: Create pipeline
    P->>A: worker_register
    A-->>P: worker_id
    P->>P: Execute steps
    P-->>C: Result
```

```mermaid
graph TB
    subgraph Setup
        A[api_config]
        B[Pipeline]
    end
    
    subgraph Execution
        C[Step 1]
        D[Step 2]
    end
    
    subgraph Result
        E[Output]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
```

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Running
    Running --> Complete
    Complete --> [*]
```

```mermaid
flowchart LR
    I[Input] --> P[Process]
    P --> O[Output]
    
    style I fill:#e1f5fe
    style P fill:#b3e5fc
    style O fill:#81d4fa
```
