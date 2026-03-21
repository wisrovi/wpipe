# 11 Rate Limiting

Demonstrates implementing rate limiting in pipeline API calls.
Protects external services from being overwhelmed.

## What it evaluates

- Rate limiting configuration
- Request throttling
- API quota management

## Flow

```mermaid
graph LR
    A[Request] --> B[Rate Limit Check]
    B --> C{Allowed?}
    C -->|Yes| D[Process Request]
    C -->|No| E[Reject/Delay]
    D --> F[Log Request]
    F --> G[Response]
```

```mermaid
sequenceDiagram
    participant Client
    participant RateLimiter
    participant Pipeline
    
    Client->>RateLimiter: Check rate limit
    RateLimiter->>RateLimiter: Count requests in window
    RateLimiter-->>Client: Allowed/Denied
    alt Allowed
        Client->>Pipeline: Process request
        Pipeline-->>Client: Result
    end
```

```mermaid
graph TB
    subgraph RATE_LIMIT_CONFIG
        R1[Rate Limit: 5]
        R2[Window Size: 2s]
    end
    
    subgraph REQUEST_TRACKING
        T1[Request Times List]
        T2[Filter by Window]
    end
    
    subgraph DECISION
        D1{Count <= Limit?}
        D1 -->|Yes| D2[Allow]
        D1 -->|No| D3[Reject]
    end
    
    R1 --> D1
    R2 --> T2
```

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Checking: New request
    Checking --> Allowed: Under limit
    Checking --> Rejected: Over limit
    Allowed --> Processing: Execute pipeline
    Rejected --> Idle: Wait for window
    Processing --> Idle: Complete
```

```mermaid
flowchart TB
    subgraph INPUT
        I1[request_id]
        I2[current_time]
    end
    
    subgraph RATE_CHECK
        R1[Get request_times]
        R2[Filter by WINDOW_SIZE]
        R3[Count requests]
        R4[Check <= RATE_LIMIT]
    end
    
    subgraph OUTPUT
        O1[allowed: boolean]
        O2[requests_in_window: count]
    end
    
    I2 --> R1 --> R2 --> R3 --> R4 --> O1
    R2 --> O2
```
