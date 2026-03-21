# 04 API Error Handling

Demonstrates how API errors are handled when server is unavailable.
Pipeline continues executing even if API calls fail.

## What it evaluates

- API errors do not stop pipeline execution
- Pipeline handles invalid API server gracefully
- Local execution continues when API fails
- Data flows through steps regardless of API state

## Flow

```mermaid
graph LR
    A[Invalid Config] --> B[API Call]
    B --> C[Error]
    C --> D[Continue]
    D --> E[Execute Steps]
    E --> F[Result]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as API
    
    P->>A: API call
    A-->>P: Error
    Note over P: Handle error
    P->>P: Continue locally
    P-->>P: Complete
```

```mermaid
graph TB
    subgraph API
        A[Invalid URL]
        B[Connection Error]
    end
    
    subgraph Pipeline
        C[Continue]
        D[Execute Steps]
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
    [*] --> Setup
    Setup --> Call
    Call --> Error
    Error --> Continue
    Continue --> Complete
    Complete --> [*]
```

```mermaid
flowchart LR
    E([Error]) --> C[Continue]
    C --> S[Steps]
    S --> O([Result])
    
    style E fill:#ffcdd2
    style O fill:#c8e6c9
```
