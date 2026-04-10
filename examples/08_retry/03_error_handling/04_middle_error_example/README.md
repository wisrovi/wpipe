# Middle Error Example

Shows error handling when failure occurs in the middle of the pipeline.

## What It Does

Demonstrates how the pipeline handles errors that occur
after some steps have already completed successfully.

## Flow

```mermaid
graph LR
    A[Step 1] --> B[Step 2]
    B -->|Error| C[Stop]
    C --> D[No Step 3]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S1 as Step 1
    participant S2 as Step 2
    participant S3 as Step 3
    
    P->>S1: Run
    S1-->>P: Success
    P->>S2: Run
    S2-->>P: RuntimeError
    P->>S3: Skip
```

```mermaid
graph TB
    subgraph Steps
        A[Step 1]
        B[Step 2]
        C[Step 3]
        D[Step 4]
    end
    
    subgraph Error
        E[Error]
    end
    
    A --> B
    B -->|Error| E
    C -->|Skipped| D
```

```mermaid
stateDiagram-v2
    [*] --> Step1
    Step1 --> Step2
    Step2 --> Error : RuntimeError
    Error --> [*]
    Step2 --> Step3
    Step3 --> Step4
    Step4 --> [*]
```

```mermaid
flowchart LR
    S1([Step 1]) --> S2([Step 2])
    S2 -->|Error| E([Stop])
    S2 -->|Success| S3([Step 3])
    S3 --> S4([Step 4])
```
