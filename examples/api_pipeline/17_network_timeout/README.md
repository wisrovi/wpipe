# 17 Network Timeout

Demonstrates handling of network timeouts and slow responses.
Pipeline should handle timeout errors gracefully.

## What it evaluates

- Timeout configuration
- Slow network simulation
- Timeout error handling
- Pipeline continues on timeout

## Flow

```mermaid
graph LR
    A[API Request] --> B[Timer Starts]
    B --> C{Response?}
    C -->|Yes| D[Continue]
    C -->|No| E[Timeout]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant T as Timer
    
    P->>T: Start timer
    T-->>P: Timeout
    Note over P: Handle timeout
```

```mermaid
graph TB
    subgraph Wait
        A[Send request]
    end
    
    subgraph Outcome
        B[Success]
        C[Timeout]
    end
    
    A --> B
    A --> C
```

```mermaid
stateDiagram-v2
    [*] --> Wait
    Wait --> Success
    Wait --> Timeout
    Timeout --> [*]
    Success --> [*]
```

```mermaid
flowchart LR
    R([Request]) --> T{{Timer}}
    T --> S([Success])
    T --> X([Timeout])
    
    style S fill:#c8e6c9
    style X fill:#ffcdd2
```
