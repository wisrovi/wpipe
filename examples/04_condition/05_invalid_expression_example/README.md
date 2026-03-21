# Invalid Expression Handling

Demonstrates how the pipeline handles conditions with invalid/missing field references.

## What It Does

This example shows what happens when a condition expression references a field that does not exist in the pipeline data. The pipeline raises a `ValueError` with a descriptive message indicating which field is missing, helping developers quickly identify and fix configuration issues.

## Flow

```mermaid
graph LR
    A[Get Data] --> B{Invalid Field?}
    B -->|Field Missing| C[ValueError Raised]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant G as Get Data
    participant C as Condition
    participant E as Error Handler

    P->>G: Run get_data
    G-->>P: {value: 5}
    P->>C: Evaluate nonexistent_field > 10
    C-->>E: ValueError: field not found
    E-->>P: Error message displayed
```

```mermaid
graph TB
    subgraph Data
        A1[get_data<br/>returns: {value: 5}]
        A2[Missing Field<br/>nonexistent_field]
    end
    subgraph Condition
        C1[Condition Check<br/>expression: nonexistent_field > 10]
    end
    subgraph Error
        E1[ValueError<br/>field not in data]
    end
    A1 --> C1
    C1 -->|Field not found| E1
```

```mermaid
stateDiagram-v2
    [*] --> GetData
    GetData --> EvaluateCondition: data={value: 5}
    EvaluateCondition --> CheckField: Check for nonexistent_field
    CheckField --> RaiseError: Field missing
    RaiseError --> [*]: Error displayed
```

```mermaid
flowchart LR
    subgraph Available Data
        D["{value: 5}"]
    end
    subgraph Expression
        E["nonexistent_field > 10"]
    end
    subgraph Result
        R["ValueError: field not found"]
    end
    D --> C{Evaluate}
    E --> C
    C -->|Missing| R
```
