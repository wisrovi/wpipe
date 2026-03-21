# 06 Full Configuration

Demonstrates full API configuration with all options combined.
Shows how to use timeout and retry settings together.

## What it evaluates

- Combining multiple API config options
- Timeout and retry configuration
- Complete API setup for production
- Single-step processing with full config

## Flow

```mermaid
graph LR
    A[Full API Config] --> B[Pipeline Setup]
    B --> C[API Call with Timeout]
    C --> D{Success?}
    D -->|No| E[Retry up to 3 times]
    E --> C
    D -->|Yes| F[Result]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant API
    participant Retry
    
    Pipeline->>API: API call with timeout=30s
    API-->>Pipeline: Request timeout
    Pipeline->>Retry: Increment retry count
    Retry->>API: Retry #1
    API-->>Pipeline: Success
    Pipeline->>Pipeline: Continue
```

```mermaid
graph TB
    subgraph API_CONFIG
        A1[base_url: http://localhost:8418]
        A2[token: test_token]
        A3[timeout: 30 seconds]
        A4[retry: 3 attempts]
    end
    
    subgraph RETRY_LOOP
        R1[Attempt 1: Fail]
        R2[Attempt 2: Fail]
        R3[Attempt 3: Success]
    end
    
    subgraph PIPELINE
        P1[process function]
        P2[Multiply value by 2]
    end
    
    A1 --> A2 --> A3 --> A4
    A4 --> R1 --> R2 --> R3 --> P1 --> P2
```

```mermaid
stateDiagram-v2
    [*] --> Configure
    Configure --> Call: Execute API call
    Call --> Success: Response OK
    Call --> Retry: Request failed
    Retry --> Call: Retry attempt
    Retry --> Failed: Max retries exceeded
    Success --> [*]: Continue
    Failed --> [*]: Error
```

```mermaid
flowchart TB
    subgraph CONFIGURATION
        C1[base_url]
        C2[token]
        C3[timeout: 30]
        C4[retry: 3]
    end
    
    subgraph EXECUTION
        E1[Call API]
        E2{Success?}
        E3[Retry loop]
    end
    
    subgraph RESULT
        R1[{result: value * 2}]
    end
    
    C1 --> C2 --> C3 --> C4 --> E1 --> E2
    E2 -->|No| E3 --> E1
    E2 -->|Yes| R1
```
