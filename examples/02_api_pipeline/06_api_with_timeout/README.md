# 06 API With Timeout

Demonstrates configuring timeout for API calls.
Timeout ensures API calls do not hang indefinitely.

## What it evaluates

- Timeout configuration in api_config
- API calls respect timeout settings
- Pipeline handles slow responses gracefully

## Flow

```mermaid
graph LR
    A[Config] --> B[API Call]
    B --> C{Timeout?}
    C -->|Yes| D[Handle Timeout]
    C -->|No| E[Success]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as API
    
    P->>A: Request with timeout
    alt Timeout
        A-->>P: Timeout error
    else Success
        A-->>P: Response
    end
```

```mermaid
graph TB
    subgraph Config
        A[timeout: 30]
    end
    
    subgraph Request
        B[Send API Call]
    end
    
    subgraph Outcome
        C[Timeout or Success]
    end
    
    A --> B
    B --> C
```

```mermaid
stateDiagram-v2
    [*] --> Wait
    Wait --> Success
    Wait --> Timeout
    Success --> [*]
    Timeout --> [*]
```

```mermaid
flowchart LR
    T([Timeout Config]) --> C[API Call]
    C --> R([Result])
    C --> X([Timeout Error])
    
    style T fill:#e1f5fe
    style X fill:#ffcdd2
```
