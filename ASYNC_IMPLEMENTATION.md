# PipelineAsync Implementation

## Overview

The wpipe library now includes full async/await support through the new `PipelineAsync` class. This allows users to write asynchronous task pipelines with true async operations, without affecting existing synchronous functionality.

## What Was Added

### 1. New PipelineAsync Class (`wpipe/pipe/pipe_async.py`)

- **Full async support**: All task execution is async-aware
- **Mixed async/sync tasks**: Support for both async coroutines and synchronous functions in the same pipeline
- **Async callable classes**: Support for classes with async `__call__` methods
- **Same features as Pipeline**: Conditions, retry logic, tracking, API integration, etc.

### 2. Features

#### Async Task Support
```python
async def async_task(data):
    await asyncio.sleep(0.1)
    return {"result": "done"}

pipeline = PipelineAsync(pipeline_name="my_async_pipeline")
pipeline.set_steps([
    (async_task, "async_task", "v1.0"),
])

result = await pipeline.run({})
```

#### Async Callable Classes
```python
class MyAsyncTask:
    async def __call__(self, data):
        await asyncio.sleep(0.1)
        return {"result": "done"}

pipeline = PipelineAsync(pipeline_name="my_async_pipeline")
pipeline.set_steps([
    (MyAsyncTask(), "my_task", "v1.0"),
])

result = await pipeline.run({})
```

#### Mixed Async/Sync Tasks
```python
async def async_task(data):
    await asyncio.sleep(0.1)
    return {"async": True}

def sync_task(data):
    return {"sync": True}

pipeline = PipelineAsync(pipeline_name="mixed_pipeline")
pipeline.set_steps([
    (async_task, "async_task", "v1.0"),
    (sync_task, "sync_task", "v1.0"),
])

result = await pipeline.run({})
```

#### Conditions
```python
from wpipe import PipelineAsync, Condition

condition = Condition(
    expression="score > 80",
    branch_true=[
        (async_high_score_handler, "high_score", "v1.0"),
    ],
    branch_false=[
        (async_low_score_handler, "low_score", "v1.0"),
    ],
)

pipeline = PipelineAsync(pipeline_name="conditional_pipeline")
pipeline.set_steps([condition])
```

#### Retry Logic
```python
pipeline = PipelineAsync(
    pipeline_name="my_pipeline",
    max_retries=3,
    retry_delay=0.5,
    retry_on_exceptions=(RuntimeError,),
)
```

#### Tracking and Events
```python
pipeline = PipelineAsync(
    pipeline_name="tracked_pipeline",
    tracking_db="wpipe.db",
    config_dir="configs",
)

pipeline.add_event(
    event_type="notification",
    event_name="task_completed",
    message="Task completed successfully",
)
```

## Exports

PipelineAsync is exported from the main wpipe module:

```python
from wpipe import PipelineAsync, Pipeline, Condition
```

## Backward Compatibility

✓ **All existing functionality is preserved**:
- Original `Pipeline` class unchanged
- All existing tests pass
- Existing examples work without modification

## Example

See `examples/10_dashboard/00_honey_pot/example_async.py` for a complete async example.

## Implementation Details

### Key Differences from Pipeline

1. **Async Detection**: Uses `_is_async_callable()` helper to detect both:
   - Async functions: `asyncio.iscoroutinefunction()`
   - Async callables: Checks `__call__` method for coroutine

2. **Task Invocation**: Uses `await` for async tasks, while still supporting sync tasks

3. **Retry Logic**: Uses `await asyncio.sleep()` instead of `time.sleep()`

4. **Branch Execution**: Recursive async support in `_run_branch()`

### Testing

All existing tests pass:
- `test_pipeline.py`: 19/19 PASSED
- `test_condition.py`: 9/9 PASSED
- `test_coverage.py`: Mixed sync/async scenarios

## Usage Pattern

```python
import asyncio
from wpipe import PipelineAsync

async def main():
    # Create pipeline
    pipeline = PipelineAsync(
        pipeline_name="my_async_pipeline",
        verbose=True,
    )
    
    # Set steps
    pipeline.set_steps([
        (your_async_task, "task_name", "v1.0"),
    ])
    
    # Run pipeline (must be awaited)
    result = await pipeline.run({"input": "data"})
    
    return result

# Execute
result = asyncio.run(main())
```

## Notes

- `PipelineAsync.run()` is an async method and must be called with `await`
- Use `asyncio.run()` in your script's main() to execute the pipeline
- Mixing async and sync tasks is fully supported
- All Pipeline features (conditions, retry, tracking, events) work with PipelineAsync
