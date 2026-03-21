# 05 Show API Errors

Demonstrates using SHOW_API_ERRORS flag to raise exceptions on API errors.
When enabled, API errors will raise exceptions instead of being silently ignored.

## What it evaluates

- SHOW_API_ERRORS flag controls exception behavior
- When True, API errors raise exceptions
- Pipeline can be configured to fail fast on API issues

## Flow

```mermaid
graph LR
    A[SHOW_API_ERRORS=True] --> B[Pipeline Setup]
    B --> C[API Call]
    C --> D{Success?}
    D -->|Yes| E[Continue]
    D -->|No| F[Raise Exception]
```

```mermaid
sequenceDiagram
    participant Client
    participant Pipeline
    participant API
    
    Client->>Pipeline: Create pipeline
    Client->>Pipeline: SHOW_API_ERRORS = True
    Client->>Pipeline: run()
    Pipeline->>API: API call
    alt API Error
        API-->>Pipeline: Error response
        Pipeline-->>Client: Raise exception
    else Success
        Pipeline->>Pipeline: Continue
    end
```

```mermaid
graph TB
    subgraph CONFIG
        C1[api_config: base_url, token]
        C2[worker_id: worker_test12345]
    end
    
    subgraph FLAG
        F1[SHOW_API_ERRORS = True]
        F2[Exceptions raised]
    end
    
    subgraph PIPELINE
        P1[process function]
        P2[data["value"] * 2]
    end
    
    subgraph RESULT
        R1[{result: 20}]
    end
    
    C1 --> F1 --> P1 --> R1
```

```mermaid
stateDiagram-v2
    [*] --> Setup
    Setup --> FlagSet: SHOW_API_ERRORS = True
    FlagSet --> Execute: run()
    Execute --> Success: API OK
    Success --> [*]: Return result
    Execute --> Exception: API fails
    Exception --> [*]: Error raised
```

```mermaid
flowchart LR
    subgraph DEFAULT
        D1[SHOW_API_ERRORS = False]
        D2[API errors ignored]
    end
    
    subgraph ENABLED
        E1[SHOW_API_ERRORS = True]
        E2[API errors raise]
    end
    
    subgraph EFFECT
        G1[Fail fast on issues]
        G2[Explicit error handling]
    end
    
    E1 --> G1 & G2
```
