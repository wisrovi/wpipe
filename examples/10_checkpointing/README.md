# Checkpointing Examples

Examples demonstrating checkpoint management and pipeline resumption.

## Examples

### 01_basic
Basic checkpointing workflow demonstrating how to save checkpoints after each step.

**Run**: `python 01_basic/basic_checkpoint.py`

**What it shows**:
- Creating a CheckpointManager
- Saving checkpoints after steps complete
- Retrieving checkpoint statistics

### 02_resume_after_failure
Demonstrates resuming a pipeline from a checkpoint after failure.

**Run**: `python 02_resume_after_failure/resume_after_failure.py` (twice to see resume)

**What it shows**:
- Detecting if a pipeline can resume
- Skipping already-completed steps
- Resuming from the last checkpoint

### 03_checkpoint_stats
Analyzes checkpoint statistics and history.

**What it shows**:
- Getting checkpoint statistics
- Viewing checkpoint history
- Clearing checkpoints

### 04_advanced
Advanced checkpointing patterns.

**What it shows**:
- Nested pipelines with checkpoints
- Conditional checkpointing
- Data versioning with checkpoints

## Key Concepts

- **Durability**: Checkpoints are saved to SQLite
- **Granularity**: One checkpoint per step
- **Resumption**: Skip completed steps on retry
- **Debugging**: Inspect state at each checkpoint

## Common Patterns

```python
# Save checkpoint after success
checkpoint_mgr.save_checkpoint(
    pipeline_id,
    step_order,
    step_name,
    "success",
    data
)

# Check if can resume
if checkpoint_mgr.can_resume(pipeline_id):
    last = checkpoint_mgr.get_last_checkpoint(pipeline_id)
    start_from = last["step_order"] + 1

# Get statistics
stats = checkpoint_mgr.get_checkpoint_stats(pipeline_id)
print(f"Success rate: {stats['successful']}/{stats['total_checkpoints']}")
```

## See Also

- [Checkpointing Documentation](../../wpipe/checkpoint/README.md)
- [Phase 1 Features Guide](../../PHASE_1_FEATURES.md)
