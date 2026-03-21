# 05 Args and Kwargs

Passing additional arguments to pipeline steps.

## What It Does

- Passes extra arguments to pipeline.run()
- Uses default parameters in steps
- Validates with configurable ranges

## Flow

```mermaid
graph LR
    A[Input] --> B[Pipeline]
    B --> C[Register Worker]
    C --> D{Check API}
    D -->|Yes| E[Run with API]
    D -->|No| F[Run Local]
    E --> G[Result]
    F --> G
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant T as transform_data
    participant V as validate_data
    
    P->>T: run({value: 10}, multiplier=2, offset=5)
    T-->>P: {transformed: 25}
    P->>V: run({transformed: 25})
    V-->>P: {valid: True, value: 25}
```

```mermaid
graph TB
    subgraph Setup
        A[Input + args]
        B[Pipeline]
    end
    
    subgraph Execution
        C[transform_data]
        D[validate_data]
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
    [*] --> Ready
    Ready --> Running
    Running --> Complete
    Complete --> [*]
```

```mermaid
flowchart LR
    I([Input]) --> P([Process])
    P --> O([Output])
```
