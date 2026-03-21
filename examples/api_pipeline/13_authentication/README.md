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
    participant C as Client
    participant P as Pipeline
    participant A as API
    
    C->>P: Request with auth
    P->>A: Bearer token
    A-->>P: Protected data
    P-->>C: Result
```

```mermaid
graph TB
    subgraph Auth
        A[Token]
        B[Bearer]
    end
    
    subgraph Request
        C[API Call]
    end
    
    subgraph Response
        D[Protected data]
    end
    
    A --> B
    B --> C
    C --> D
```

```mermaid
stateDiagram-v2
    [*] --> Auth
    Auth --> Fetch
    Fetch --> Process
    Process --> [*]
```

```mermaid
flowchart LR
    T([Token]) --> R([Request])
    R --> D([Protected Data])
    
    style T fill:#e1f5fe
    style D fill:#c8e6c9
```
