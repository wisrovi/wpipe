# 18 Invalid URL

Demonstrates handling of invalid or malformed URLs in API configuration.
Pipeline should handle URL validation errors gracefully.

## What it evaluates

- Invalid URL handling
- Malformed URL detection
- Clear error messages
- Fallback to local execution

## Flow

```mermaid
graph LR
    A[Invalid URL] --> B[API Request]
    B --> C[URL Error]
    C --> D[Handle Error]
    D --> E[Continue Locally]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant N as Network
    
    P->>N: Invalid URL
    N-->>P: URL error
    Note over P: Handle error
    P->>P: Continue locally
```

```mermaid
graph TB
    subgraph Invalid
        A[Bad URL]
    end
    
    subgraph Error
        B[Connection fail]
    end
    
    subgraph Recovery
        C[Local mode]
    end
    
    A --> B
    B --> C
```

```mermaid
stateDiagram-v2
    [*] --> Validate
    Validate --> Error
    Error --> Continue
    Continue --> [*]
```

```mermaid
flowchart LR
    U([Invalid URL]) --> E([Error])
    E --> C([Continue])
    
    style U fill:#ffcdd2
    style C fill:#c8e6c9
```
