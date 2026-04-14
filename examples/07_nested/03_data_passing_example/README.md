# Data Passing Between Nested Pipelines

Demonstrates how data flows and is accumulated between nested pipelines.

## What It Does

- Creates a generate pipeline that produces an initial value
- Creates a transform pipeline that processes the generated value
- Combines data from both pipelines in a final step

## Nested Flow

```mermaid
graph LR
    A[Main] --> B[Generate Pipeline]
    B --> C[{value: 100}]
    A --> D[Transform Pipeline]
    D --> E[{value: 100,<br/>transformed: 200}]
    A --> F[combine_data]
    F --> G[{combined: 300}]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant M as Main Pipeline
    participant G as Generate Pipeline
    participant T as Transform Pipeline
    participant C as combine_data

    M->>G: Run with {}
    G-->>M: Return {value: 100}
    M->>T: Run with {value: 100}
    T-->>M: Return {transformed: 200}
    M->>C: Execute with {value: 100, transformed: 200}
    C-->>M: Return {combined: 300}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph Main["Main Pipeline"]
        G[Generate Pipeline]
        T[Transform Pipeline]
        C[combine_data]
    end
    subgraph G_"Generate Pipeline"
        GD[generate_data]
    end
    subgraph T_"Transform Pipeline"
        TD[transform_data]
    end
    G --> GD
    T --> TD
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Generating: run generate pipeline
    Generating --> Generated: data created
    Generated --> Transforming: run transform pipeline
    Transforming --> Transformed: data transformed
    Transformed --> Combining: run combine
    Combining --> Done: final result
    Done --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{}] --> B[generate_data]
    B --> C[{value: 100}]
    C --> D[transform_data]
    D --> E[{value: 100,<br/>transformed: 200}]
    E --> F[combine_data]
    F --> G[{combined: 300}]
```
