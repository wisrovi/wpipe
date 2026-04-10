# 09 API Logging

Demonstrates configuring logging for API calls.
Shows how logging helps debug API interactions.

## What it evaluates

- Pipeline logging configuration
- Verbose mode for debugging
- API call logging
- Pipeline execution logging

## Flow

```mermaid
graph LR
    A[Pipeline] --> B[Execute Steps]
    B --> C[Log Each Step]
    C --> D[Send to API]
    D --> E[Log Response]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant L as Logger
    
    P->>L: Log start
    P->>P: Execute step
    P->>L: Log step
    P->>L: Log response
```

```mermaid
graph TB
    subgraph Pipeline
        P[Pipeline]
    end
    
    subgraph Logs
        L1[Start log]
        L2[Step log]
        L3[API log]
        L4[End log]
    end
    
    subgraph Output
        O[Result]
    end
    
    P --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> O
```

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Execute
    Execute --> Log
    Log --> Complete
    Complete --> [*]
```

```mermaid
flowchart LR
    P([Pipeline]) --> L([Logs])
    L --> O([Output])
    
    style P fill:#e1f5fe
    style L fill:#fff9c4
    style O fill:#c8e6c9
```
