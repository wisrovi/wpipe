# 09 API Logging

Demonstrates configuring logging for API calls.
Shows how logging helps debug API interactions.

## What it evaluates

- Pipeline logging configuration
- Verbose mode for debugging
- API call logging
- Pipeline execution logging

## Flow

```mermaid
graph LR
    A[Pipeline with logging] --> B[Execute Steps]
    B --> C[Log each step]
    C --> D[Send to API]
    D --> E[Log API call]
    E --> F[Log response]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant API
    participant Logger
    
    Pipeline->>Logger: Log: Pipeline starting
    Pipeline->>Pipeline: Execute step 1
    Pipeline->>Logger: Log: Step 1 complete
    Pipeline->>API: API call
    API-->>Pipeline: Response
    Pipeline->>Logger: Log: API response
    Pipeline->>Logger: Log: Pipeline complete
```

```mermaid
graph TB
    subgraph PIPELINE
        P1[Pipeline with verbose=True]
        P2[worker_name: logging_test]
    end
    
    subgraph LOGGING
        L1[Pipeline start log]
        L2[Step execution logs]
        L3[API call logs]
        L4[Response logs]
        L5[Completion log]
    end
    
    subgraph OUTPUT
        O1[Result returned]
        O2[Logs saved]
    end
    
    P1 --> L1 --> L2 --> L3 --> L4 --> L5
    L5 --> O1 & O2
```

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> LogStart: Pipeline initialized
    LogStart --> Execute: Run step
    Execute --> LogStep: Step complete
    LogStep --> APICall: Send to API
    APICall --> LogResponse: Response received
    LogResponse --> Complete: Pipeline done
    Complete --> [*]: Logs available
```

```mermaid
flowchart TB
    subgraph LOG_LEVELS
        L1[DEBUG: Detailed info]
        L2[INFO: General flow]
        L3[WARNING: Issues]
        L4[ERROR: Failures]
    end
    
    subgraph LOG_TYPES
        T1[Pipeline initialization]
        T2[Step execution]
        T3[API requests/responses]
        T4[Errors and exceptions]
    end
    
    subgraph STORAGE
        S1[Console output]
        S2[Log files]
    end
    
    L1 --> T1 --> T2 --> T3 --> T4
    T1 & T2 & T3 & T4 --> S1 & S2
```
