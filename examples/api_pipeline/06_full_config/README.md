# 06 Full Configuration

Demonstrates full API configuration with all options combined.
Shows how to use timeout and retry settings together.

## What it evaluates

- Combining multiple API config options
- Timeout and retry configuration
- Complete API setup for production
- Single-step processing with full config

## Flow

```mermaid
graph LR
    A[Config] --> B[Pipeline]
    B --> C[API Call]
    C --> D{Retry?}
    D -->|Fail| E[Retry]
    E --> C
    D -->|Success| F[Result]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as API
    
    P->>A: Request with timeout
    A-->>P: Timeout
    P->>A: Retry 1
    A-->>P: Timeout
    P->>A: Retry 2
    A-->>P: Success
```

```mermaid
graph TB
    subgraph Config
        A[base_url]
        B[timeout]
        C[retry]
    end
    
    subgraph Request
        D[Send]
    end
    
    subgraph Result
        E[Output]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
```

```mermaid
stateDiagram-v2
    [*] --> Config
    Config --> Call
    Call --> Retry
    Call --> Success
    Retry --> Call
    Retry --> Fail
    Success --> [*]
    Fail --> [*]
```

```mermaid
flowchart LR
    C([Config]) --> P([Pipeline])
    P --> R([Retry Loop])
    R --> O([Result])
    
    style C fill:#e1f5fe
    style O fill:#c8e6c9
```
