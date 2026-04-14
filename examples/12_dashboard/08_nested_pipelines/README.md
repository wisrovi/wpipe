# Example 08: Nested Pipelines

Shows how to compose pipelines from other pipelines with parent-child relationships.

## Hierarchical Structure

```mermaid
graph TD
    P[ETL Parent] --> E[Extract]
    P --> T[Transform]
    P --> L[Load]
    
    E --> EC1[Connect Source]
    E --> FR[Fetch Records]
    E --> PD[Parse Data]
    
    T --> VC[Validate]
    T --> TM[Transform]
    T --> AE[Aggregate]
    
    L --> WF[Write File]
    L --> VN[Validate]
```

## Parent-Child Relationships

```mermaid
classDiagram
    class ParentPipeline {
        +str pipeline_id
        +str name
    }
    
    class ChildPipeline {
        +str pipeline_id
        +str name
        +str parent_id
    }
    
    ParentPipeline "1" --> "*" ChildPipeline : triggers
```

## Pipeline Relations

```mermaid
sequenceDiagram
    participant Parent
    participant Child
    participant DB
    
    Parent->>Child: execute child pipeline
    Child->>DB: INSERT pipeline (parent_id)
    DB-->>Parent: link via relations
```

## What Gets Tracked

- ✅ Parent pipeline ID
- ✅ Child pipeline ID
- ✅ Relation type (triggered, contains, etc.)
- ✅ Execution order

## Run

```bash
cd examples/10_dashboard/08_nested_pipelines
python example.py
```
