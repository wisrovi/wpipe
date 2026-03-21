# 03 No API Configuration

Demonstrates running pipeline without API configuration (local-only mode).
Useful for testing or when API server is not available.

## What it evaluates

- Pipeline runs without api_config parameter
- All steps execute locally
- Data aggregation through multiple steps
- Statistics calculation from input data

## Flow

```mermaid
graph LR
    A[Input items] --> B[Process]
    B --> C[Calculate Stats]
    C --> D[Result]
```

```mermaid
sequenceDiagram
    participant I as Input
    participant P as Pipeline
    
    I->>P: run with items
    P->>P: Step 1
    P->>P: Step 2
    P-->>I: Result
```

```mermaid
graph TB
    subgraph Input
        A[items list]
    end
    
    subgraph Steps
        B[process_items]
        C[calculate_stats]
    end
    
    subgraph Output
        D[results]
    end
    
    A --> B
    B --> C
    C --> D
```

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Step1
    Step1 --> Step2
    Step2 --> End
    End --> [*]
```

```mermaid
flowchart LR
    I([Input]) --> P1([Step 1])
    P1 --> P2([Step 2])
    P2 --> O([Output])
```
