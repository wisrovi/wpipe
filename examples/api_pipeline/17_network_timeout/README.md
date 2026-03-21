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
    E --> F[Handle Error]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant Network
    participant Timeout
    
    Pipeline->>Network: Send request
    Pipeline->>Timeout: Start timer (1s)
    Note over Network: Processing...
    Timeout->>Pipeline: Time exceeded
    Pipeline->>Pipeline: Handle timeout
```

```mermaid
graph TB
    subgraph TIMEOUT_CONFIG
        T1[timeout: 1 second]
        T2[Wait for response]
    end
    
    subgraph TIMEOUT_TRIGGER
        TT1[Timer exceeded]
        TT2[Cancel request]
    end
    
    subgraph RECOVERY
        R1[Log timeout]
        R2[Continue pipeline]
    end
    
    T1 --> T2 --> TT1 --> TT2 --> R1 --> R2
```

```mermaid
stateDiagram-v2
    [*] --> SendRequest
    SendRequest --> Waiting: Timer starts
    Waiting --> Success: Response received
    Waiting --> Timeout: Time exceeded
    Timeout --> [*]: Handle error
    Success --> [*]: Continue
```

```mermaid
flowchart TB
    subgraph SLOW_OPERATIONS
        S1[API calls]
        S2[Network requests]
        S3[External services]
    end
    
    subgraph TIMEOUT_HANDLING
        T1[Wait for timeout]
        T2[Cancel request]
        T3[Log error]
    end
    
    S1 --> T1 --> T2 --> T3
```
