# 06 API With Timeout

Demonstrates configuring timeout for API calls.
Timeout ensures API calls don't hang indefinitely.

## What it evaluates

- Timeout configuration in api_config
- API calls respect timeout settings
- Pipeline handles slow responses gracefully

## Flow

```mermaid
graph LR
    A[API Config] --> B[Pipeline with timeout]
    B --> C[API Call]
    C --> D{Completes in time?}
    D -->|Yes| E[Return Result]
    D -->|No| F[Timeout Error]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant API
    participant Timeout
    
    Pipeline->>API: API call with timeout=30s
    Pipeline->>Timeout: Start timer
    alt Completes in time
        API-->>Pipeline: Response
        Timeout->>Pipeline: Cancel timer
    else Times out
        Timeout->>API: Cancel request
        Timeout-->>Pipeline: Timeout error
    end
```

```mermaid
graph TB
    subgraph API_CONFIG
        A1[base_url: http://localhost:8418]
        A2[token: test_token]
        A3[timeout: 30 seconds]
    end
    
    subgraph TIMEOUT_BEHAVIOR
        T1[Wait for response]
        T2[Cancel if exceeds timeout]
        T3[Handle timeout error]
    end
    
    subgraph PIPELINE
        P1[process function]
        P2[Multiply value by 2]
    end
    
    A1 --> A2 --> A3
    A3 --> T1 --> T2 --> T3
    T1 --> P1
```

```mermaid
stateDiagram-v2
    [*] --> Configure
    Configure --> Waiting: API call started
    Waiting --> Success: Response received
    Waiting --> Timeout: Time exceeded
    Timeout --> [*]: Error
    Success --> [*]: Continue
```

```mermaid
flowchart TB
    subgraph CONFIGURATION
        C1[timeout: 30]
    end
    
    subgraph BEHAVIOR
        B1[Wait up to 30 seconds]
        B2[Raise on timeout]
        B3[Continue on success]
    end
    
    subgraph RESULT
        R1[result: value * 2]
    end
    
    C1 --> B1
    B1 --> B2
    B1 --> B3
    B3 --> R1
```
