# Wpipe - Core Package

This package contains the core library for creating and executing data processing pipelines.

## Structure

| Module | Description |
|--------|-------------|
| `pipe/` | Pipeline and Condition classes for orchestrating sequential tasks |
| `api_client/` | HTTP client for external API integration and worker registration |
| `sqlite/` | SQLite database wrapper for persisting pipeline execution results |
| `log/` | Logging utilities |
| `ram/` | Memory management utilities (Linux only) |
| `util/` | YAML configuration utilities |
| `exception/` | Custom exceptions (ApiError, TaskError, ProcessError, Codes) |

## Code Quality

- **Pylint Score**: 9.47/10
- **Type Hints**: Complete
- **Docstrings**: Comprehensive

## Installation

```bash
pip install -e .
```

## Usage

```python
from wpipe import Pipeline

pipeline = Pipeline(verbose=True)
pipeline.set_steps([(my_function, "Step Name", "v1.0")])
result = pipeline.run(input_data)
```

## Documentation

See the main [README.md](../README.md) for complete documentation.