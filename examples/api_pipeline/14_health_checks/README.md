# 14 Health Checks

Demonstrates implementing health check functionality.
Pipeline can be used to verify service dependencies are healthy.

## What it evaluates

- Health check step in pipeline
- Service dependency verification
- Status reporting for monitoring

## Flow

```mermaid
graph LR
    A[Check DB] --> D[Aggregate]
    B[Check Cache] --> D
    C[Check API] --> D
    D --> E[Status Report]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Services
    
    P->>S: Check DB
    P->>S: Check Cache
    P->>S: Check API
    S-->>P: Status
    P-->>P: Aggregate
```

```mermaid
graph TB
    subgraph Checks
        A[Database]
        B[Cache]
        C[API]
    end
    
    subgraph Aggregate
        D[Combine]
    end
    
    subgraph Report
        E[Status]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
```

```mermaid
stateDiagram-v2
    [*] --> CheckDB
    CheckDB --> CheckCache
    CheckCache --> CheckAPI
    CheckAPI --> Aggregate
    Aggregate --> [*]
```

```mermaid
flowchart LR
    DB([Database]) --> A([Aggregate])
    Cache([Cache]) --> A
    API([API]) --> A
    A --> S([Status])
    
    style S fill:#c8e6c9
```
