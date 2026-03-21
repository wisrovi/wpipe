# 15 Pipeline Configuration

Reusable pipeline configuration patterns.

## What It Does

- Creates reusable configurations
- Adds extra steps dynamically
- Clones and extends pipelines

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
    participant M as Main
    participant F as Factory
    
    M->>F: create_configured_pipeline()
    F-->>M: {v1: 10}
    M->>F: create_configured_pipeline([extra])
    F-->>M: {v1: 10, v2: 20}
```

```mermaid
graph TB
    subgraph Factory
        A[Base Steps]
        B[Extra Steps]
    end
    
    subgraph Pipeline
        C[Base Step]
        D[Extra Step]
    end
    
    subgraph Result
        E[Output]
    end
    
    A --> C
    B --> D
    C --> E
    D --> E
```

```mermaid
stateDiagram-v2
    [*] --> Create
    Create --> Clone
    Clone --> Extend
    Extend --> Done
    Done --> [*]
```

```mermaid
flowchart LR
    I([Input]) --> P([Process])
    P --> O([Output])
```
