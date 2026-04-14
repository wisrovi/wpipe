# Partial Results Example

Shows accessing partial results after error.

## What It Does

Demonstrates how to access results from completed steps
even when a later step fails in the pipeline.

## Flow

```mermaid
graph LR
    A[Step 1] --> B[Step 2]
    B -->|Error| C[Partial Results]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S1 as Step 1
    participant S2 as Step 2
    participant PR as Partial Results
    
    P->>S1: Run
    S1-->>P: {'step1': 'done'}
    P->>S2: Run
    S2-->>P: ValueError
    P->>PR: Access Results
```

```mermaid
graph TB
    subgraph Complete
        A[Step 1]
    end
    
    subgraph Failed
        B[Step 2]
    end
    
    subgraph Skipped
        C[Step 3]
    end
    
    A --> B
    B -->|Error| D[Partial]
```

```mermaid
stateDiagram-v2
    [*] --> Step1
    Step1 --> Step2
    Step2 --> Error : ValueError
    Error --> Partial
    Partial --> [*]
```

```mermaid
flowchart LR
    S1([Step 1]) --> S2([Step 2])
    S2 -->|Error| P([Partial])
```
