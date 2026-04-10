# Timeout Examples

Examples demonstrating task timeout management.

## Examples

### 01_sync_timeout
Basic synchronous timeout handling.

**Run**: `python 01_sync_timeout/sync_timeout.py`

**What it shows**:
- Using `@timeout_sync()` decorator
- Handling TimeoutError exceptions
- TaskTimer context manager usage

### 02_async_timeout
Async timeout handling with coroutines.

**Run**: `python 02_async_timeout/async_timeout.py`

**What it shows**:
- Using `timeout_async()` for coroutines
- Concurrent task timeout handling
- Async error handling

### 03_timeout_with_retry
Combining timeouts with retry logic.

**What it shows**:
- Retrying timed-out tasks
- Exponential backoff with timeouts
- Timeout recovery strategies

### 04_advanced
Advanced timeout patterns.

**What it shows**:
- Per-step timeout configuration
- Dynamic timeout adjustment
- Timeout monitoring and alerting

## Key Concepts

- **Signal-based**: Sync timeout uses SIGALRM
- **Async-native**: Async timeout uses asyncio.wait_for
- **Context managers**: TaskTimer for manual timing
- **Exception handling**: All timeouts raise TimeoutError

## Common Patterns

```python
# Decorator-based timeout
@timeout_sync(seconds=30)
def my_function():
    pass

# Async timeout
result = await timeout_async(30, my_coroutine())

# Manual timing
with TaskTimer("task_name", timeout_seconds=60) as timer:
    do_work()
    if timer.exceeded_timeout():
        handle_timeout()
```

## Troubleshooting

- **"Timeout fired immediately"**: Timeout too low, increase seconds
- **"SIGALRM not available"**: Running on Windows? Use async instead
- **"TimeoutError not caught"**: Make sure to catch TimeoutError specifically

## See Also

- [Timeout Documentation](../../wpipe/timeout/README.md)
- [Phase 1 Features Guide](../../PHASE_1_FEATURES.md)
