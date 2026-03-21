# 20 Reconnection Logic

Demonstrates automatic reconnection when API server becomes available.
Pipeline should recover from temporary API failures.

## What it evaluates

- Reconnection after failure
- API recovery handling
- Automatic retry to API
- Graceful degradation and recovery

## Flow

```mermaid
graph LR
    A[API Call] --> B{Available?}
    B -->|No| C[Fail]
    C --> D[Continue]
    B -->|Yes| E[Success]
    D --> A
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant API
    
    Pipeline->>API: Attempt 1
    API-->>Pipeline: Unavailable
    Pipeline->>Pipeline: Continue locally
    Pipeline->>API: Attempt 2
    API-->>Pipeline: Available!
    Pipeline->>Pipeline: Update status
```

```mermaid
graph TB
    subgraph CONNECTION
        C1[Call API]
        C2[Success?]
    end
    
    subgraph FAILURE
        F1[Mark unavailable]
        F2[Continue locally]
        F3[Schedule retry]
    end
    
    subgraph SUCCESS
        S1[Mark available]
        S2[Normal operation]
    end
    
    C1 --> C2
    C2 -->|No| F1 --> F2 --> F3
    C2 -->|Yes| S1 --> S2
```

```mermaid
stateDiagram-v2
    [*] --> Connected
    Connected --> Disconnected: API fails
    Disconnected --> Retrying: Wait
    Retrying --> Connected: Success
    Retrying --> Disconnected: Still down
    Disconnected --> [*]: Give up
```

```mermaid
flowchart LR
    subgraph INITIAL
        I1[API available]
    end
    
    subgraph TRANSIENT_FAILURE
        TF1[Temp outage]
        TF2[Local fallback]
        TF3[Retry scheduled]
    end
    
    subgraph RECOVERY
        R1[API returns]
        R2[Resume tracking]
    end
    
    I1 --> TF1 --> TF2 --> TF3 --> R1 --> R2
```
