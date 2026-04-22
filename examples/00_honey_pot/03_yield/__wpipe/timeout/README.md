# Task Timeouts

Prevent hanging tasks by enforcing timeout limits on pipeline steps.

## Features

- **Sync timeout**: Decorator-based timeout for synchronous functions
- **Async timeout**: Native async timeout support
- **Task timer**: Context manager for tracking execution time
- **Timeout detection**: Check if timeout was exceeded

## Quick Start

```python
from wpipe import timeout_sync, timeout_async, TaskTimer
import asyncio

# Synchronous task with timeout
@timeout_sync(seconds=30)
def fetch_data():
    # This will raise TimeoutError if it takes > 30 seconds
    return requests.get("https://api.example.com/data")

# Async task with timeout
async def async_fetch():
    return await timeout_async(30, fetch_with_aiohttp())

# Manual timing with timeout checking
with TaskTimer("my_task", timeout_seconds=60) as timer:
    do_work()
    
    if timer.exceeded_timeout():
        print("Task took too long!")
        
print(f"Elapsed: {timer.elapsed_seconds}s")
```

## API

### Decorators

#### `@timeout_sync(seconds: Optional[float])`
Decorator for synchronous task timeout using signal.SIGALRM.

```python
@timeout_sync(30)
def my_function():
    # Will timeout after 30 seconds
    pass
```

#### `@timeout_async(seconds: Optional[float])`
Async wrapper for timeout support.

```python
result = await timeout_async(30, my_coroutine())
```

### TaskTimer

Context manager for timing and timeout checking.

```python
with TaskTimer("task_name", timeout_seconds=60) as timer:
    do_work()
    if timer.exceeded_timeout():
        handle_timeout()

print(timer.elapsed_seconds)
```

## Exceptions

- `TimeoutError`: Raised when task exceeds timeout

## Use Cases

- **API calls**: Ensure API requests don't hang
- **Resource protection**: Prevent runaway processes
- **SLA compliance**: Enforce execution time limits
- **Pipeline reliability**: Skip stuck steps automatically
