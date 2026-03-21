# 09 Empty Data Handling

Handling missing or empty input data gracefully.

## What It Does

- Handles empty input data
- Uses default values
- Graceful degradation

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
    participant S1 as step_a
    participant S2 as step_b
    
    P->>S1: run({})
    S1-->>P: {processed: 0}
    P->>S2: run({processed: 0})
    S2-->>P: {result: 0}
```

```mermaid
graph TB
    subgraph Setup
        A[Empty Input]
        B[Pipeline]
    end
    
    subgraph Execution
        C[step_a]
        D[step_b]
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
    [*] --> Empty
    Empty --> Default
    Default --> Process
    Process --> End
    End --> [*]
```

```mermaid
flowchart LR
    I([Input]) --> P([Process])
    P --> O([Output])
```
