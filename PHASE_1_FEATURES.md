# Phase 1 Features: Core Reliability & Observability

This document describes all Phase 1 features that form the foundation of WPipe's reliability and observability.

**Table of Contents:**
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Integration Guide](#integration-guide)
- [Best Practices](#best-practices)

## Overview

Phase 1 introduces 5 critical features designed to make WPipe production-ready:

1. **Checkpointing & Resume**: Recover from failures without reprocessing
2. **Task Timeouts**: Prevent hanging processes
3. **Type Hinting**: Catch type errors early
4. **Resource Monitoring**: Track and optimize resource usage
5. **Export & Analytics**: Analyze and report pipeline execution

## Features

### 1. Checkpointing & Resume

**Purpose**: Allow pipelines to resume from the last successful step after interruptions.

**Key Components**:
- `CheckpointManager`: Manages checkpoint save/restore
- Database: SQLite for durability
- Status tracking: pending, running, success, failed

**When to Use**:
- Long-running pipelines (> 10 minutes)
- Network-dependent operations
- Production environments requiring high reliability

**Example**:
```python
from wpipe import Pipeline, CheckpointManager

checkpoint_mgr = CheckpointManager("pipeline.db")
pipeline = Pipeline()

# Save progress after each step
for i, step in enumerate(pipeline.steps):
    try:
        result = step.run()
        checkpoint_mgr.save_checkpoint(
            "my_pipeline", i, step.name, "success", result
        )
    except Exception as e:
        checkpoint_mgr.save_checkpoint(
            "my_pipeline", i, step.name, "failed"
        )
        raise

# On retry, skip completed steps
if checkpoint_mgr.can_resume("my_pipeline"):
    last = checkpoint_mgr.get_last_checkpoint("my_pipeline")
    start_from_step = last["step_order"] + 1
```

### 2. Task Timeouts

**Purpose**: Prevent tasks from hanging indefinitely.

**Key Components**:
- `@timeout_sync()`: Decorator for sync functions
- `timeout_async()`: Async timeout wrapper
- `TaskTimer`: Context manager for timing

**When to Use**:
- External API calls
- Database queries
- File operations
- Any I/O-bound operations

**Example**:
```python
from wpipe import timeout_sync, TaskTimer
import time

@timeout_sync(seconds=30)
def fetch_external_data():
    # Raises TimeoutError if takes > 30s
    return requests.get("https://api.example.com/data")

# Manual timing
with TaskTimer("my_task", timeout_seconds=60) as timer:
    result = do_work()
    
    if timer.exceeded_timeout():
        print(f"Task took {timer.elapsed_seconds}s, timeout was 60s")
```

### 3. Type Hinting & Validation

**Purpose**: Catch type errors early with runtime validation.

**Key Components**:
- `TypeValidator`: Runtime type checking
- `PipelineContext`: Typed context TypedDict
- `GenericPipeline`: Generic pipeline with type params

**When to Use**:
- Complex data pipelines
- Multi-step transformations
- API integration
- Any time data shape might change

**Example**:
```python
from typing import TypedDict
from wpipe import PipelineContext, TypeValidator

class UserContext(PipelineContext):
    user_id: int
    username: str
    email: str

# Validate input
data = {"user_id": 123, "username": "john", "email": "john@example.com"}
context = TypeValidator.validate_dict(data, {
    "user_id": int,
    "username": str,
    "email": str,
})
```

### 4. Resource Monitoring

**Purpose**: Track and optimize resource consumption (RAM, CPU).

**Key Components**:
- `ResourceMonitor`: Individual task monitoring
- `ResourceMonitorRegistry`: Aggregate tracking
- Metrics: RAM (MB), CPU (%), timing

**When to Use**:
- Performance profiling
- Capacity planning
- Cost optimization
- Identifying bottlenecks

**Example**:
```python
from wpipe import ResourceMonitor, ResourceMonitorRegistry

registry = ResourceMonitorRegistry()

with ResourceMonitor("data_processing", db_path="metrics.db") as monitor:
    process_large_dataset()

registry.add("data_processing", monitor)

summary = monitor.get_summary()
print(f"Peak RAM: {summary['peak_ram_mb']} MB")
print(f"Avg CPU: {summary['avg_cpu_percent']}%")

# Aggregate stats
peak_ram = registry.get_peak_ram()
print(f"Total peak RAM: {peak_ram} MB")
```

### 5. Export & Analytics

**Purpose**: Export execution data for analysis and reporting.

**Key Components**:
- `PipelineExporter`: Exports logs, metrics, statistics
- Formats: JSON, CSV
- Filtering: By pipeline ID
- Storage: Flexible (string or file)

**When to Use**:
- Performance analysis
- Compliance reporting
- Debugging investigations
- Data integration

**Example**:
```python
from wpipe import PipelineExporter

exporter = PipelineExporter("pipeline.db")

# Export logs
logs_json = exporter.export_pipeline_logs(
    pipeline_id="my_pipeline",
    format="json",
    output_path="logs.json"
)

# Export metrics
metrics = exporter.export_metrics(format="csv", output_path="metrics.csv")

# Export statistics
stats = exporter.export_statistics(format="json")
print(f"Success rate: {stats['success_rate_percent']}%")
```

## Architecture

```
Pipeline Execution Flow with Phase 1:

┌─────────────────────────────────────────────────────┐
│ Pipeline Starts                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │ Check for Checkpoint   │ ◄─── CheckpointManager
        └────────┬───────────────┘
                 │
        ┌────────▼───────────┐
        │ Resume if exists   │
        └────────┬───────────┘
                 │
        ┌────────▼────────────────┐
        │ Start ResourceMonitor   │ ◄─── ResourceMonitor
        └────────┬────────────────┘
                 │
        ┌────────▼───────────────────┐
        │ For each Step:             │
        │  1. Validate input (Type)  │ ◄─── TypeValidator
        │  2. Set timeout (Timeout)  │ ◄─── TaskTimer
        │  3. Execute step           │
        │  4. Track resources        │ ◄─── ResourceMonitor
        │  5. Save checkpoint        │ ◄─── CheckpointManager
        └────────┬───────────────────┘
                 │
        ┌────────▼──────────────────┐
        │ Stop ResourceMonitor      │
        │ Export data               │ ◄─── PipelineExporter
        └────────┬──────────────────┘
                 │
                 ▼
        Pipeline Completes
```

## Quick Start

1. **Install dependencies**:
```bash
pip install wpipe psutil typing-extensions
```

2. **Basic setup**:
```python
from wpipe import (
    Pipeline,
    CheckpointManager,
    ResourceMonitor,
    PipelineExporter,
    timeout_sync,
    TypeValidator
)

# Initialize managers
checkpoint_mgr = CheckpointManager("pipeline.db")
exporter = PipelineExporter("pipeline.db")

# Create pipeline
pipeline = Pipeline()

# Add steps with timeouts and type validation
@timeout_sync(seconds=30)
def my_step(data):
    return {"result": data}

pipeline.add_state("my_step", my_step)

# Monitor resources
with ResourceMonitor("pipeline_run", db_path="pipeline.db") as monitor:
    pipeline.run()

# Export results
stats = exporter.export_statistics(format="json")
print(f"Success rate: {stats['success_rate_percent']}%")
print(f"Peak RAM: {monitor.get_summary()['peak_ram_mb']} MB")
```

## Integration Guide

### With Existing Pipelines

1. **Add CheckpointManager**:
   - Create manager instance
   - Wrap step execution in try/except
   - Save checkpoints on success

2. **Add Timeouts**:
   - Add `@timeout_sync()` to I/O-bound functions
   - Use `TaskTimer` for manual timing

3. **Add Type Hints**:
   - Define TypedDict for context
   - Use `TypeValidator` at step boundaries

4. **Add Resource Monitoring**:
   - Wrap pipeline in `ResourceMonitor` context
   - Optional: save to database

5. **Add Export**:
   - Create `PipelineExporter` instance
   - Call export methods on completion

### Step-by-Step Integration

```python
from wpipe import (
    Pipeline, CheckpointManager, ResourceMonitor,
    PipelineExporter, timeout_sync, TypeValidator
)

# Step 1: Initialize Phase 1 components
checkpoint_mgr = CheckpointManager("pipeline.db")
exporter = PipelineExporter("pipeline.db")
pipeline = Pipeline()

# Step 2: Define typed context
from typing import TypedDict
class MyContext(TypedDict):
    data_id: int
    processed: bool

# Step 3: Add steps with all Phase 1 features
@timeout_sync(seconds=30)
def process_step(context: dict) -> dict:
    # Validate input
    validated = TypeValidator.validate_dict(context, {
        "data_id": int,
        "processed": bool,
    })
    # Process...
    return {"result": "..."}

pipeline.add_state("process", process_step)

# Step 4: Execute with monitoring
try:
    with ResourceMonitor("run_1", db_path="pipeline.db") as monitor:
        for i, step in enumerate(pipeline.steps):
            try:
                result = step.run()
                checkpoint_mgr.save_checkpoint(
                    "my_pipeline", i, step.name, "success", result
                )
            except TimeoutError:
                checkpoint_mgr.save_checkpoint(
                    "my_pipeline", i, step.name, "failed"
                )
                raise

    # Step 5: Export results
    stats = exporter.export_statistics(format="json")
    print(stats)
except Exception as e:
    print(f"Pipeline failed: {e}")
```

## Best Practices

### 1. Checkpointing

- ✅ Save checkpoints after expensive operations
- ✅ Include relevant data in checkpoint
- ❌ Don't save too frequently (overhead)
- ❌ Don't skip saving on failure (for debugging)

### 2. Timeouts

- ✅ Set timeout slightly higher than SLA
- ✅ Use on all external I/O operations
- ✅ Log when timeouts occur
- ❌ Don't set timeouts too low (false positives)
- ❌ Don't use timeouts on CPU-bound work

### 3. Type Hinting

- ✅ Define TypedDict for all major data flows
- ✅ Validate at pipeline boundaries
- ✅ Use generic pipelines for reusable components
- ❌ Don't validate every single variable
- ❌ Don't trust external data without validation

### 4. Resource Monitoring

- ✅ Monitor long-running operations
- ✅ Store metrics for historical analysis
- ✅ Set alerts on peak RAM or CPU
- ❌ Don't monitor trivial operations (overhead)
- ❌ Don't ignore resource growth trends

### 5. Export & Analytics

- ✅ Export regularly for analysis
- ✅ Use JSON for analysis, CSV for Excel
- ✅ Filter by pipeline for focused reports
- ❌ Don't export raw events (aggregate instead)
- ❌ Don't ignore export failures

## Troubleshooting

### "TimeoutError: Task exceeded timeout"

**Solution**: Increase timeout or optimize task.
```python
@timeout_sync(60)  # Increase from 30s
def slow_task():
    pass
```

### "TypeValidator: Expected int, got str"

**Solution**: Validate input before processing.
```python
data = TypeValidator.validate(input_data, int)
```

### "CheckpointManager: No table 'executions'"

**Solution**: Initialize database first.
```python
checkpoint_mgr = CheckpointManager("pipeline.db")
checkpoint_mgr._ensure_checkpoint_table()
```

### "ResourceMonitor: Could not access psutil"

**Solution**: Install psutil.
```bash
pip install psutil
```

## See Also

- [Checkpointing Documentation](wpipe/checkpoint/README.md)
- [Timeouts Documentation](wpipe/timeout/README.md)
- [Type Hinting Documentation](wpipe/type_hinting/README.md)
- [Resource Monitoring Documentation](wpipe/resource_monitor/README.md)
- [Export Documentation](wpipe/export/README.md)
- [Examples](examples/)
