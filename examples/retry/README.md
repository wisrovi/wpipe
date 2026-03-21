# Retry Examples

This directory contains examples demonstrating retry functionality in pipelines.

## Examples

| File | Description |
|------|-------------|
| `01_basic_retry.py` | Basic retry on failure with configurable max_retries |
| `02_success_after_retry.py` | Function that succeeds after a few failed attempts |
| `03_filter_exceptions.py` | Retry only specific exception types |
| `04_multiple_steps.py` | Retry behavior with multiple pipeline steps |
| `05_no_retry.py` | Pipeline without retry (default behavior) |

## Usage

```python
from wpipe import Pipeline

pipeline = Pipeline(
    max_retries=3,
    retry_delay=0.5,
    retry_on_exceptions=(ConnectionError, TimeoutError),
    verbose=True
)
```

## Parameters

- `max_retries`: Maximum retry attempts (0 = no retry)
- `retry_delay`: Delay between retries in seconds
- `retry_on_exceptions`: Tuple of exception types to retry on