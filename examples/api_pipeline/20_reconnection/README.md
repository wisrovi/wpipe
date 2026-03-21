# 20 Reconnection Logic

Demonstrates automatic reconnection when API server becomes available.
Pipeline should recover from temporary API failures.

## What it evaluates

- Reconnection after failure
- API recovery handling
- Automatic retry to API
- Graceful degradation and recovery

## Flow

```mermaid
graph LR
    A[API Call] --> B{Available?}
    B -->|No| C[Fail]
    C --> D[Continue]
    B -->|Yes| E[Success]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as API
    
    P->>A: Attempt 1
    A-->>P: Unavailable
    P->>A: Attempt 2
    A-->>P: Available
```

```mermaid
graph TB
    subgraph Connection
        A[Call API]
    end
    
    subgraph States
        B[Fail]
        C[Success]
    end
    
    subgraph Recovery
        D[Retry]
    end
    
    A --> B
    A --> C
    B --> D
    D --> A
```

```mermaid
stateDiagram-v2
    [*] --> Connected
    Connected --> Disconnected
    Disconnected --> Retrying
    Retrying --> Connected
    Disconnected --> [*]
```

```mermaid
flowchart LR
    C([Call]) --> D{{Available?}}
    D -->|Yes| S([Success])
    D -->|No| R([Retry])
    R --> C
    
    style S fill:#c8e6c9
    style R fill:#fff9c4
```
