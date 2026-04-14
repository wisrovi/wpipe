# Checkpointing & Resume

Save pipeline execution state at each step and resume from the last successful checkpoint.

## Features

- **Step-level checkpoints**: Save state after each step completes
- **Resume functionality**: Automatically skip completed steps and resume from checkpoint
- **Status tracking**: Track which steps have completed (success/failed)
- **Data persistence**: Store checkpoint data in SQLite for durability

## Quick Start

```python
from wpipe import Pipeline, CheckpointManager

# Initialize checkpoint manager
checkpoint_mgr = CheckpointManager("pipeline.db")

# Create pipeline
pipeline = Pipeline()
pipeline.add_state("Step 1", my_step_1)
pipeline.add_state("Step 2", my_step_2)

# Save checkpoint
checkpoint_mgr.save_checkpoint(
    pipeline_id="my_pipeline",
    step_order=1,
    step_name="Step 1",
    status="success",
    data={"result": "..."}
)

# Check if can resume
if checkpoint_mgr.can_resume("my_pipeline"):
    last = checkpoint_mgr.get_last_checkpoint("my_pipeline")
    print(f"Resume from step {last['step_order']}")
```

## API

### CheckpointManager

#### `__init__(db_path: str)`
Initialize checkpoint manager with SQLite database path.

#### `save_checkpoint(pipeline_id, step_order, step_name, status, data)`
Save a checkpoint at a specific step.

#### `get_last_checkpoint(pipeline_id) -> Optional[Dict]`
Get the last successful checkpoint for a pipeline.

#### `can_resume(pipeline_id) -> bool`
Check if a pipeline can be resumed from a checkpoint.

#### `clear_checkpoints(pipeline_id)`
Clear all checkpoints for a pipeline.

#### `get_checkpoint_stats(pipeline_id) -> Dict`
Get statistics about checkpoints for a pipeline.

## Use Cases

- **Long-running pipelines**: Resume after interruptions
- **Production reliability**: Reduce processing time on retries
- **Debugging**: Inspect state at each step
- **Audit trail**: Track when steps completed and their outputs
