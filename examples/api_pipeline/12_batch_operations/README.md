# 12 Batch Operations

Demonstrates processing data in batches through the pipeline.
Useful for handling large datasets efficiently.

## What it evaluates

- Processing multiple items in a single pipeline run
- Batch data aggregation
- Efficient data handling for bulk operations

## Flow

```mermaid
graph LR
    A[Batch Input] --> B[Validate]
    B --> C[Transform]
    C --> D[Aggregate]
    D --> E[Final Result]
```

```mermaid
sequenceDiagram
    participant Input
    participant Validator
    participant Transformer
    participant Aggregator
    
    Input->>Validator: items: [1,2,3,-1,4]
    Validator->>Validator: Filter valid items
    Validator->>Transformer: valid_items: [1,2,3,4]
    Transformer->>Transformer: Transform each item
    Transformer->>Aggregator: transformed_items: [2,4,6,8]
    Aggregator->>Aggregator: Sum and count
    Aggregator-->>Input: final_items, sum, count
```

```mermaid
graph TB
    subgraph INPUT
        I1[items: [1,2,3,4,5,6,7,8,-1,-2]]
    end
    
    subgraph VALIDATE_BATCH
        V1[Filter: item > 0]
        V2[valid_items: 8 items]
        V3[total: 10, valid_count: 8]
    end
    
    subgraph TRANSFORM_BATCH
        T1[Transform: item * 2]
        T2[transformed_items: [2,4,6,8,10,12,14,16]]
    end
    
    subgraph AGGREGATE
        A1[Sum: 72]
        A2[Count: 8]
    end
    
    I1 --> V1 --> V2 --> T1 --> T2 --> A1
```

```mermaid
stateDiagram-v2
    [*] --> Validate
    Validate --> Transform: Valid items ready
    Validate --> [*]: Empty batch
    Transform --> Aggregate: Transformed ready
    Aggregate --> [*]: Complete
```

```mermaid
flowchart TB
    subgraph STEP_1_VALIDATE
        S1[Input: items list]
        S2[Filter negative values]
        S3[Output: valid_items, counts]
    end
    
    subgraph STEP_2_TRANSFORM
        S4[Input: valid_items]
        S5[Map: multiply by 2]
        S6[Output: transformed_items]
    end
    
    subgraph STEP_3_AGGREGATE
        S7[Input: transformed_items]
        S8[Reduce: sum, count]
        S9[Output: final_items, sum, count]
    end
    
    S1 --> S2 --> S3
    S3 --> S4 --> S5 --> S6
    S6 --> S7 --> S8 --> S9
```
