# wpipe - Pipeline Library

A Python library for creating and executing **sequential** data processing pipelines with task orchestration and API integration.

**Purpose**: Process data through a chain of steps where each step receives output from the previous one. NOT designed for streaming/chunking large datasets - data should fit in memory.

## Features

- **Pipeline Orchestration**: Create pipelines with step functions and classes
- **Conditional Branches**: Execute different paths based on data conditions
- **Retry Logic**: Automatic retries for failed steps with configurable parameters
- **API Integration**: Connect to external APIs for tracking and monitoring
- **Worker Management**: Register workers and perform health checks
- **SQLite Storage**: Persist pipeline execution results
- **YAML Configuration**: Load and manage configurations
- **Error Handling**: Robust error handling with custom exceptions
- **Progress Tracking**: Visual progress with rich terminal output
- **Nested Pipelines**: Compose complex workflows

## Installation

```bash
pip install wpipe
```

## Quick Start

```python
from wpipe import Pipeline

def step1(data):
    return {"result": data["x"] * 2}

def step2(data):
    return {"final": data["result"] + 10}

pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (step1, "Step 1", "v1.0"),
    (step2, "Step 2", "v1.0"),
])

result = pipeline.run({"x": 5})
# result = {'result': 10, 'final': 20}
```

## Retry Logic

Configure automatic retries for unstable steps:

```python
from wpipe import Pipeline

def unstable_api_call(data):
    # May fail occasionally
    return {"data": "success"}

pipeline = Pipeline(
    verbose=True,
    max_retries=3,
    retry_delay=1.0,
    retry_on_exceptions=(ConnectionError, TimeoutError),
)

pipeline.set_steps([
    (unstable_api_call, "API Call", "v1.0"),
])
```

## Conditional Pipelines

Execute different branches based on data conditions:

```python
from wpipe import Pipeline, Condition

def fetch_data(data):
    return {"data_type": "A", "value": 100}

def process_type_a(data):
    return {"processed": data["value"] * 2}

def process_type_b(data):
    return {"processed": data["value"] + 50}

pipeline = Pipeline(verbose=True)

condition = Condition(
    expression="data_type == 'A'",
    branch_true=[(process_type_a, "Process A", "v1.0")],
    branch_false=[(process_type_b, "Process B", "v1.0")],
)

pipeline.set_steps([
    (fetch_data, "Fetch", "v1.0"),
    condition,
])
```

## Examples

| Folder | Description |
|--------|-------------|
| `basic_pipeline/` | Basic pipeline execution |
| `conditional_pipeline/` | Conditional branching pipelines |
| `retry_pipeline/` | Pipelines with retry logic |
| `api_pipeline/` | Pipeline with API connectivity |
| `error_handling/` | Error handling patterns |
| `nested_pipelines/` | Nested pipeline execution |
| `sqlite_integration/` | SQLite database integration |
| `yaml_config/` | YAML configuration utilities |
| `microservice/` | Microservice architecture |

## Running Examples

```bash
# Basic pipeline
python examples/basic_pipeline/example_01_basic.py

# Conditional pipeline
python examples/conditional_pipeline/main.py

# Retry pipeline
python examples/retry_pipeline/main.py

# API pipeline (requires API server)
python examples/api_pipeline/example_01_api.py
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wpipe --cov-report=html

# Lint
ruff check wpipe/

# Type check
mypy wpipe/
```

## Code Quality

- **Pylint Score**: 9.47/10
- **Tests**: 84 passing
- **Python Support**: 3.9, 3.10, 3.11, 3.12, 3.13

## Architecture

```
wpipe/
├── pipe/           # Pipeline and Condition implementation
├── api_client/    # API communication
├── sqlite/        # Database operations
├── log/          # Logging utilities
├── ram/          # Memory utilities
├── util/         # YAML utilities
└── exception/    # Custom exceptions
```

## Documentation

Full documentation available at: https://wpipe.readthedocs.io/

## License

MIT License - See LICENSE file

## Author

William Steve Rodriguez Villamizar
