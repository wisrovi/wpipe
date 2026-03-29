# Example 09: Events & Annotations

Add custom events and annotations to pipelines for better tracking and documentation.

## Events System

```mermaid
flowchart LR
    P[Pipeline] --> E1[Event: Started]
    E1 --> S[Step 1]
    S --> E2[Event: Checkpoint]
    E2 --> S2[Step 2]
    S2 --> E3[Event: Completed]
    E3 --> DB[(Events Table)]
```

## Event Types

```mermaid
classDiagram
    class Event {
        +str event_type
        +str event_name
        +str message
        +dict data
        +dict tags
        +timestamp created_at
    }
    
    class EventTypes {
        +STARTED = "pipeline"
        +CHECKPOINT = "checkpoint"
        +ANNOTATION = "annotation"
        +MILESTONE = "milestone"
    }
```

## Timeline View

```mermaid
gantt
    title Pipeline with Events
    dateFormat X
    axisFormat %s
    
    Section Execution
    Initialize      :0, 5
    Process Batch 1 :5, 15
    Checkpoint      :15, 15
    Process Batch 2 :15, 25
    Complete        :25, 30
    
    Section Events
    Started         :milestone, 0, 0
    Checkpoint      :milestone, 15, 15
    Completed       :milestone, 30, 30
```

## Run

```bash
cd examples/10_dashboard/09_events_annotations
python example.py
```
