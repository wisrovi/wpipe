# Basic Nested Pipeline

Demonstrates the simplest nested pipeline: one pipeline running inside another.

## What It Does

- Creates an inner pipeline with two steps
- Embeds the inner pipeline as a single step in an outer pipeline
- Executes the outer pipeline, which runs all inner steps first

## Nested Flow

```mermaid
graph LR
    A[Outer Pipeline] --> B[Inner Pipeline]
    B --> C[inner_step1]
    B --> D[inner_step2]
    A --> E[outer_step]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant O as Outer Pipeline
    participant I as Inner Pipeline
    participant S1 as inner_step1
    participant S2 as inner_step2
    participant OS as outer_step

    O->>I: Run inner pipeline
    I->>S1: Execute inner_step1
    S1-->>I: Return {"inner1": "done"}
    I->>S2: Execute inner_step2
    S2-->>I: Return {"inner2": "done"}
    I-->>O: Return merged data
    O->>OS: Execute outer_step
    OS-->>O: Return {"outer": "done"}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph Outer["Outer Pipeline"]
        I1[Inner Pipeline]
        O1[outer_step]
    end
    subgraph Inner["Inner Pipeline"]
        S1[inner_step1]
        S2[inner_step2]
    end
    I1 --> S1
    I1 --> S2
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Running: start
    Running --> InnerRunning: run inner pipeline
    InnerRunning --> InnerDone: inner complete
    InnerDone --> OuterRunning: run outer step
    OuterRunning --> Done: complete
    Done --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{}] --> B[Inner Pipeline]
    B --> C[{"inner1": "done",<br/>"inner2": "done"}]
    C --> D[outer_step]
    D --> E[Final Result]
```
