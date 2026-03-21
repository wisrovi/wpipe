# 18 Invalid URL

Demonstrates handling of invalid/malformed URLs in API configuration.
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
    participant Pipeline
    participant Network
    
    Pipeline->>Network: Invalid URL
    Network-->>Pipeline: URL error
    Note over Pipeline: Handle error
    Pipeline->>Pipeline: Continue locally
```

```mermaid
graph TB
    subgraph INVALID_URLS
        U1[not-a-url]
        U2[http://]
        U3[://missing]
    end
    
    subgraph ERROR_HANDLING
        E1[URL parse error]
        E2[Connection fail]
        E3[Continue locally]
    end
    
    U1 & U2 & U3 --> E1 --> E2 --> E3
```

```mermaid
stateDiagram-v2
    [*] --> ValidateURL
    ValidateURL --> Invalid: Parse error
    Invalid --> Handle: Log error
    Handle --> Continue: Local mode
    Continue --> [*]: Complete
```

```mermaid
flowchart LR
    subgraph MALFORMED
        M1[Missing protocol]
        M2[Invalid format]
        M3[Empty host]
    end
    
    subgraph OUTCOME
        O1[Connection fails]
        O2[Local execution]
    end
    
    M1 & M2 & M3 --> O1 --> O2
```
