# Deep Nesting

Demonstrates deeply nested pipeline structure with multiple levels of nesting.

## What It Does

- Creates two simple pipelines (P1 and P2) with single steps
- Creates a parent pipeline (P3) that embeds both P1 and P2
- Executes all nested steps in sequence

## Nested Flow

```mermaid
graph LR
    A[P3] --> B[P1]
    A --> C[P2]
    A --> D[step_c]
    B --> E[step_a]
    C --> F[step_b]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant P3 as P3 Pipeline
    participant P1 as P1 Pipeline
    participant P2 as P2 Pipeline
    participant SC as step_c

    P3->>P1: Run P1
    P1-->>P3: Return {a: 1}
    P3->>P2: Run P2
    P2-->>P3: Return {b: 2}
    P3->>SC: Execute step_c
    SC-->>P3: Return {c: 3}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph P3_["P3 Pipeline (top)"]
        P1[P1 Pipeline]
        P2[P2 Pipeline]
        SC[step_c]
    end
    subgraph P1_"P1 Pipeline"
        SA[step_a]
    end
    subgraph P2_"P2 Pipeline"
        SB[step_b]
    end
    P1 --> SA
    P2 --> SB
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> RunP1: run P1
    RunP1 --> DoneP1: P1 complete
    DoneP1 --> RunP2: run P2
    RunP2 --> DoneP2: P2 complete
    DoneP2 --> RunStepC: run step_c
    RunStepC --> Done: all complete
    Done --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{}] --> B[P1: step_a]
    B --> C[{a: 1}]
    C --> D[P2: step_b]
    D --> E[{a: 1, b: 2}]
    E --> F[step_c]
    F --> G[{a: 1, b: 2, c: 3}]
```
