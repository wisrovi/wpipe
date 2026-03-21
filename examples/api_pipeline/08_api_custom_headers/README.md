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
    A[API Config] --> B[Headers Defined]
    B --> C[Pipeline Setup]
    C --> D[API Call]
    D --> E[Headers Sent]
    E --> F[Response]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant API
    
    Pipeline->>API: API request
    Note right of API: Headers:
    Note right of API: X-Custom-Header: value
    Note right of API: Authorization: Bearer ...
    API-->>Pipeline: Response
```

```mermaid
graph TB
    subgraph API_CONFIG
        A1[base_url]
        A2[token]
        A3[headers: X-Custom-Header]
    end
    
    subgraph HEADER_TYPES
        H1[Custom headers]
        H2[Authorization]
        H3[Content-Type]
        H4[X-Request-ID]
    end
    
    subgraph REQUEST
        R1[Build request]
        R2[Add headers]
        R3[Send to API]
    end
    
    A3 --> H1 --> R1 --> R2 --> R3
```

```mermaid
stateDiagram-v2
    [*] --> Configure
    Configure --> BuildRequest: Setup headers
    BuildRequest --> SendRequest: Execute call
    SendRequest --> Success: Response OK
    SendRequest --> Error: API error
    Success --> [*]: Continue
    Error --> [*]: Handle error
```

```mermaid
flowchart TB
    subgraph CONFIGURATION
        C1[headers: X-Custom-Header]
    end
    
    subgraph HEADER_EXAMPLE
        H1[X-Custom-Header]
        H2[Authorization]
        H3[Content-Type]
    end
    
    subgraph API_CALL
        A1[Send request]
    end
    
    C1 --> H1
    C1 --> H2
    C1 --> H3
    H1 --> A1
    H2 --> A1
    H3 --> A1
```
