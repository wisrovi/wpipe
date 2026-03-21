# Multiple Nested Pipelines

Demonstrates running multiple nested pipelines in sequence within a main pipeline.

## What It Does

- Creates two separate pipelines (A and B), each with two steps
- Embeds both pipelines as steps in a main pipeline
- Executes pipelines in sequence, merging results from each

## Nested Flow

```mermaid
graph LR
    A[Main Pipeline] --> B[Pipeline A]
    A --> C[Pipeline B]
    A --> D[final_step]
    B --> B1[step1] --> B2[step2]
    C --> C1[step1] --> C2[step2]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant M as Main Pipeline
    participant PA as Pipeline A
    participant PB as Pipeline B
    participant F as final_step

    M->>PA: Run Pipeline A
    PA-->>M: Return {a1: 1, a2: 2}
    M->>PB: Run Pipeline B
    PB-->>M: Return {b1: 10, b2: 20}
    M->>F: Execute final_step
    F-->>M: Return {final: 11}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph Main["Main Pipeline"]
        PA[Pipeline A]
        PB[Pipeline B]
        F[final_step]
    end
    subgraph PA_"Pipeline A"
        A1[pipeline_a_step1]
        A2[pipeline_a_step2]
    end
    subgraph PB_"Pipeline B"
        B1[pipeline_b_step1]
        B2[pipeline_b_step2]
    end
    PA --> A1 --> A2
    PB --> B1 --> B2
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> RunningA: run pipeline A
    RunningA --> DoneA: pipeline A complete
    DoneA --> RunningB: run pipeline B
    RunningB --> DoneB: pipeline B complete
    DoneB --> Finalizing: run final step
    Finalizing --> Done: all complete
    Done --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{}] --> B[Pipeline A]
    B --> C[{a1: 1, a2: 2}]
    C --> D[Pipeline B]
    D --> E[{a1: 1, a2: 2, b1: 10, b2: 20}]
    E --> F[final_step]
    F --> G[{final: 11}]
```
