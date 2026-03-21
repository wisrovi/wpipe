# 13 Authentication

Demonstrates using authentication tokens in API requests.
Shows different auth schemes supported by the API client.

## What it evaluates

- Token-based authentication
- Custom authentication headers
- Secure API communication

## Flow

```mermaid
graph LR
    A[Credentials] --> B[Authenticate]
    B --> C[Get Token]
    C --> D[Fetch Resource]
    D --> E[Process]
    E --> F[Result]
```

```mermaid
sequenceDiagram
    participant Client
    participant AuthService
    participant API
    participant Pipeline
    
    Client->>AuthService: Login credentials
    AuthService-->>Client: Bearer token
    Client->>Pipeline: Run with auth header
    Pipeline->>API: Request with Authorization
    API-->>Pipeline: Protected resource
    Pipeline->>Pipeline: Process data
    Pipeline-->>Client: Result
```

```mermaid
graph TB
    subgraph AUTH_CONFIG
        A1[base_url]
        A2[token]
        A3[headers.Authorization]
    end
    
    subgraph TOKEN_TYPES
        T1[Bearer Token]
        T2[API Key]
        T3[JWT]
    end
    
    subgraph PIPELINE_STEPS
        P1[Authenticate User]
        P2[Fetch Protected]
        P3[Process Resource]
    end
    
    A1 --> P1 --> P2 --> P3
    A2 --> A3
```

```mermaid
stateDiagram-v2
    [*] --> Authenticate
    Authenticate --> FetchResource: Token valid
    Authenticate --> [*]: Token invalid
    FetchResource --> ProcessData: Resource received
    ProcessData --> [*]: Complete
```

```mermaid
flowchart LR
    subgraph AUTH_HEADER
        H1[Authorization: Bearer]
        H2[JWT Token]
    end
    
    subgraph API_CONFIG
        C1[base_url]
        C2[token]
        C3[headers]
    end
    
    subgraph PIPELINE
        P1[authenticate_user]
        P2[fetch_protected_resource]
        P3[process_protected]
    end
    
    H1 --> H2 --> C3
    C1 --> C2 --> C3
    C3 --> P1 --> P2 --> P3
```
