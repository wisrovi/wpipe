# 08 Custom Headers

Demonstrates adding custom headers to API requests.
Custom headers can be used for authentication, tracking, etc.

## What it evaluates

- Custom headers in api_config
- Headers are sent with API requests
- Pipeline supports header-based customization

## Flow

```mermaid
graph LR
    A[Config Headers] --> B[Pipeline]
    B --> C[API Call]
    C --> D[Headers Sent]
    D --> E[Response]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as API
    
    P->>A: Request with headers
    Note right of A: Custom headers
    A-->>P: Response
```

```mermaid
graph TB
    subgraph Headers
        H1[X-Custom]
        H2[Authorization]
        H3[Content-Type]
    end
    
    subgraph Request
        R[Send]
    end
    
    subgraph Response
        O[Output]
    end
    
    H1 --> R
    H2 --> R
    H3 --> R
    R --> O
```

```mermaid
stateDiagram-v2
    [*] --> Config
    Config --> Build
    Build --> Send
    Send --> Response
    Response --> [*]
```

```mermaid
flowchart LR
    H([Headers]) --> R([Request])
    R --> O([Response])
    
    style H fill:#e1f5fe
    style O fill:#c8e6c9
```
