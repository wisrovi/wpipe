# 04 API Error Handling

Demonstrates how API errors are handled when server is unavailable.
Pipeline continues executing even if API calls fail.

## What it evaluates

- API errors don't stop pipeline execution
- Pipeline handles invalid API server gracefully
- Local execution continues when API fails
- Data flows through steps regardless of API state

## Flow

```mermaid
graph LR
    A[Invalid API Config] --> B[Pipeline Setup]
    B --> C[API Call Fails]
    C --> D[Pipeline Continues]
    D --> E[Steps Execute]
    E --> F[Result Returned]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant API
    participant Steps
    
    Pipeline->>API: API call with invalid config
    API-->>Pipeline: Connection failed/timeout
    Note over Pipeline: Error handled gracefully
    Pipeline->>Steps: Continue execution
    Steps-->>Pipeline: Process result
    Pipeline-->>Pipeline: Return result
```

```mermaid
graph TB
    subgraph API_CONFIG
        A1[base_url: http://invalid-host:9999]
        A2[token: invalid_token]
    end
    
    subgraph ERROR_HANDLING
        E1[API call fails]
        E2[Error caught]
        E3[Continue pipeline]
    end
    
    subgraph STEPS
        S1[fetch_from_api]
        S2[process_data]
    end
    
    subgraph RESULT
        R1[{result: processed, source: data}]
    end
    
    A1 --> E1 --> E2 --> S1 --> S2 --> R1
```

```mermaid
stateDiagram-v2
    [*] --> Setup
    Setup --> APICall: Set worker_id
    APICall --> APIFailed: Connection error
    APIFailed --> Continue: Error handled
    Continue --> ExecuteSteps: Pipeline runs
    ExecuteSteps --> [*]: Complete
```

```mermaid
flowchart LR
    subgraph CONFIG
        C1[invalid base_url]
        C2[invalid token]
    end
    
    subgraph PIPELINE_STEPS
        P1[fetch_from_api]
        P2[process_data]
    end
    
    subgraph OUTPUT
        O1[result: processed]
        O2[source: fetched data]
    end
    
    C1 --> P1 --> P2 --> O1
```
