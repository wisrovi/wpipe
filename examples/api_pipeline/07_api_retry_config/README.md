# 07 API Retry Configuration

Demonstrates configuring retry behavior for failed API calls.
Pipeline can retry API calls automatically on failure.

## What it evaluates

- max_retries parameter controls retry behavior
- API calls are retried on failure
- Pipeline eventually succeeds or fails after retries

## Flow

```mermaid
graph LR
    A[API Call] --> B{Failed?}
    B -->|Yes| C[Retry 1]
    C --> D{Failed?}
    D -->|Yes| E[Retry 2]
    E --> F{Failed?}
    B -->|No| G[Success]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as API
    
    P->>A: Attempt 1
    A-->>P: Failed
    P->>A: Attempt 2
    A-->>P: Failed
    P->>A: Attempt 3
    A-->>P: Success
```

```mermaid
graph TB
    subgraph Attempts
        A1[Attempt 1]
        A2[Attempt 2]
        A3[Attempt 3]
    end
    
    subgraph Result
        B[Success or Fail]
    end
    
    A1 --> A2
    A2 --> A3
    A3 --> B
```

```mermaid
stateDiagram-v2
    [*] --> Call
    Call --> Fail
    Call --> Success
    Fail --> Retry
    Retry --> Call
    Retry --> [*]
    Success --> [*]
```

```mermaid
flowchart LR
    R1([Retry 1]) --> R2([Retry 2])
    R2 --> R3([Retry 3])
    R3 --> O([Result])
    
    style R1 fill:#fff9c4
    style O fill:#c8e6c9
```
