# 07 API Retry Configuration

Demonstrates configuring retry behavior for failed API calls.
Pipeline can retry API calls automatically on failure.

## What it evaluates

- max_retries parameter controls retry behavior
- API calls are retried on failure
- Pipeline eventually succeeds or fails after retries

## Flow

```mermaid
graph LR
    A[API Call] --> B{Failed?}
    B -->|Yes| C[Retry 1]
    C --> D{Failed?}
    D -->|Yes| E[Retry 2]
    E --> F{Failed?}
    F -->|Yes| G[Retry 3]
    G --> H{Failed?}
    B -->|No| I[Success]
    H -->|No| I
    H -->|Yes| J[Final Failure]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant API
    
    Pipeline->>API: Attempt 1
    API-->>Pipeline: Failed
    Pipeline->>API: Attempt 2
    API-->>Pipeline: Failed
    Pipeline->>API: Attempt 3
    API-->>Pipeline: Success
    Pipeline-->>Pipeline: Continue pipeline
```

```mermaid
graph TB
    subgraph CONFIG
        C1[max_retries: 3]
        C2[base_url: localhost:8418]
        C3[token: test_token]
    end
    
    subgraph ATTEMPTS
        A1[Attempt 1: API call]
        A2[Attempt 2: API call]
        A3[Attempt 3: API call]
    end
    
    subgraph PIPELINE
        P1[process function]
        P2[Return result]
    end
    
    C1 --> A1 --> A2 --> A3 --> P1 --> P2
```

```mermaid
stateDiagram-v2
    [*] --> Call
    Call --> Failed: API error
    Call --> Success: Response OK
    Failed --> Retry: attempt < max_retries
    Failed --> [*]: Max retries reached
    Retry --> Call
    Success --> [*]: Continue
```

```mermaid
flowchart TB
    subgraph CONFIGURATION
        C1[max_retries = 3]
        C2[Retry policy]
    end
    
    subgraph RETRY_FLOW
        R1[Call API]
        R2{Failed?}
        R3[Increment retry]
        R4{max reached?}
    end
    
    subgraph RESULT
        S1[Continue pipeline]
        F1[Raise error]
    end
    
    C1 --> R1 --> R2
    R2 -->|Yes| R3 --> R4
    R4 -->|No| R1
    R4 -->|Yes| F1
    R2 -->|No| S1
```
