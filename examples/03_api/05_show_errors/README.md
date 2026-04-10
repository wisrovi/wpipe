# 05 Show API Errors

Demonstrates using SHOW_API_ERRORS flag to raise exceptions on API errors.
When enabled, API errors will raise exceptions instead of being silently ignored.

## What it evaluates

- SHOW_API_ERRORS flag controls exception behavior
- When True, API errors raise exceptions
- Pipeline can be configured to fail fast on API issues

## Flow

```mermaid
graph LR
    A[Flag Enabled] --> B[API Call]
    B --> C{Success?}
    C -->|Yes| D[Continue]
    C -->|No| E[Raise Exception]
```

```mermaid
sequenceDiagram
    participant C as Client
    participant P as Pipeline
    
    C->>P: SET SHOW_API_ERRORS=true
    C->>P: run
    P->>P: Check flag
    alt API Error
        P-->>C: Raise Exception
    else Success
        P-->>C: Result
    end
```

```mermaid
graph TB
    subgraph Config
        A[SHOW_API_ERRORS]
        B[True]
    end
    
    subgraph Call
        C[API Request]
    end
    
    subgraph Result
        D[Success or Error]
    end
    
    A --> B
    B --> C
    C --> D
```

```mermaid
stateDiagram-v2
    [*] --> Setup
    Setup --> Execute
    Execute --> Success
    Execute --> Error
    Success --> [*]
    Error --> [*]
```

```mermaid
flowchart LR
    F[Flag] --> C[API Call]
    C --> R[Result]
    C --> X[Exception]
    
    style F fill:#fff9c4
    style X fill:#ffcdd2
```
