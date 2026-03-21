# 16 Expired Token

Demonstrates handling of expired/invalid authentication tokens.
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
    E --> F[Local Execution]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant API
    participant Client
    
    Pipeline->>API: Request with expired token
    API-->>Pipeline: 401 Unauthorized
    Note over Pipeline: Token expired
    Pipeline->>Pipeline: Continue locally
    Pipeline-->>Client: Result
```

```mermaid
graph TB
    subgraph AUTH_FAILURE
        A1[Expired token in header]
        A2[401 Response]
        A3[Token validation]
    end
    
    subgraph HANDLING
        H1[Log error]
        H2[Continue pipeline]
        H3[Local execution]
    end
    
    A1 --> A2 --> A3 --> H1 --> H2 --> H3
```

```mermaid
stateDiagram-v2
    [*] --> SendRequest
    SendRequest --> AuthFailed: 401 Unauthorized
    AuthFailed --> LogError: Record issue
    LogError --> ContinueLocal: Continue pipeline
    ContinueLocal --> [*]: Complete
```

```mermaid
flowchart LR
    subgraph TOKEN_ISSUES
        T1[Expired]
        T2[Invalid format]
        T3[Revoked]
    end
    
    subgraph RESPONSE
        R1[401 Unauthorized]
        R2[Error message]
    end
    
    subgraph RECOVERY
        RC1[Log warning]
        RC2[Continue locally]
    end
    
    T1 & T2 & T3 --> R1 --> RC1 --> RC2
```
