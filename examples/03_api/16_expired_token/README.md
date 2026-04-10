# 16 Expired Token

Demonstrates handling of expired or invalid authentication tokens.
Pipeline should gracefully handle 401 Unauthorized responses.

## What it evaluates

- Token expiration handling
- 401 Unauthorized response handling
- Graceful fallback when auth fails
- Pipeline continues with local execution

## Flow

```mermaid
graph LR
    A[Expired Token] --> B[API Call]
    B --> C[401 Unauthorized]
    C --> D[Handle Error]
    D --> E[Continue Pipeline]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as API
    
    P->>A: Request
    A-->>P: 401 Unauthorized
    Note over P: Handle error
    P->>P: Continue locally
```

```mermaid
graph TB
    subgraph Error
        A[401 Response]
    end
    
    subgraph Recovery
        B[Log error]
        C[Continue]
    end
    
    subgraph Result
        D[Output]
    end
    
    A --> B
    B --> C
    C --> D
```

```mermaid
stateDiagram-v2
    [*] --> Request
    Request --> Error
    Error --> Continue
    Continue --> [*]
```

```mermaid
flowchart LR
    T([Token Expired]) --> E([Error])
    E --> C([Continue])
    C --> O([Output])
    
    style T fill:#ffcdd2
    style O fill:#c8e6c9
```
