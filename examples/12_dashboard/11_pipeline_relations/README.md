# Example 11: Pipeline Relations

Create and visualize relationships between different pipelines.

## Relation Types

```mermaid
graph TD
    A[Data Ingestion] -->|triggers| B[Processing]
    B -->|triggers| C[Validation]
    C -->|triggers| D[Export]
    
    A -->|depends_on| E[Config Loader]
    B -->|depends_on| E
    
    A -.-> R[(Relations DB)]
    B -.-> R
    C -.-> R
```

## Relation Types

```mermaid
classDiagram
    class PipelineRelation {
        +str parent_pipeline_id
        +str child_pipeline_id
        +str relation_type
        +dict metadata
    }
    
    class RelationTypes {
        +TRIGGERED = "triggered"
        +CONTAINS = "contains"
        +DEPENDS_ON = "depends_on"
        +PARALLEL = "parallel"
    }
```

## Visualization

```mermaid
flowchart LR
    subgraph "Pipeline Network"
        P1[Ingestion]
        P2[Processing]
        P3[Validation]
        P4[Export]
    end
    
    P1 -->|triggered| P2
    P2 -->|triggered| P3
    P3 -->|triggered| P4
```

## Run

```bash
cd examples/10_dashboard/11_pipeline_relations
python example.py
```
