# Reusing Pipeline Objects

Demonstrates how to reuse the same pipeline object multiple times in a parent pipeline.

## What It Does

- Creates a reusable pipeline with a single processing step
- Embeds the same pipeline instance three times in a main pipeline
- Each call processes data independently

## Nested Flow

```mermaid
graph LR
    A[Main Pipeline] --> B[Reusable Pipeline]
    A --> C[Reusable Pipeline]
    A --> D[Reusable Pipeline]
    B --> E[process_item]
    C --> F[process_item]
    D --> G[process_item]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant M as Main Pipeline
    participant R as Reusable Pipeline

    M->>R: Run (call 1)
    R-->>M: Return {processed: 20}
    M->>R: Run (call 2)
    R-->>M: Return {processed: 20}
    M->>R: Run (call 3)
    R-->>M: Return {processed: 20}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph Main["Main Pipeline"]
        R1[Reusable Pipeline]
        R2[Reusable Pipeline]
        R3[Reusable Pipeline]
    end
    subgraph R_"Reusable Pipeline (shared instance)"
        P[process_item]
    end
    R1 --> P
    R2 --> P
    R3 --> P
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> FirstRun: process 1
    FirstRun --> FirstDone: call 1 complete
    FirstDone --> SecondRun: process 2
    SecondRun --> SecondDone: call 2 complete
    SecondDone --> ThirdRun: process 3
    ThirdRun --> Done: all complete
    Done --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{item: 10}] --> B[process_item]
    B --> C[{processed: 20}]
    C --> D[process_item]
    D --> E[{processed: 20}]
    E --> F[process_item]
    F --> G[{processed: 20}]
```
