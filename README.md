# wpipe - Python Pipeline Library for Sequential Data Processing

[![PyPI version](https://badge.fury.io/py/wpipe.svg)](https://badge.fury.io/py/wpipe)
[![Python versions](https://img.shields.io/pypi/pyversions/wpipe.svg)](https://pypi.org/project/wpipe/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LTS](https://img.shields.io/badge/LTS-1.0.0-green.svg)](CHANGELOG.md)
[![Tests](https://img.shields.io/badge/tests-106%20passing-10b981)](https://github.com/wisrovi/wpipe/actions)
[![Documentation](https://img.shields.io/badge/docs-wpipe-blue)](https://wpipe.readthedocs.io/)
[![GitHub stars](https://img.shields.io/github/stars/wisrovi/wpipe?style=social)](https://github.com/wisrovi/wpipe/stargazers)

> **Long Term Support (LTS)**: Version 1.0.0 is the first LTS release with guaranteed backward compatibility, comprehensive documentation, and 100+ examples.

## What is wpipe?

**wpipe** is a powerful, lightweight Python library for creating and executing sequential data processing pipelines without the complexity of web-based workflow tools.

- **No web UI required** — just clean, production-ready Python code
- **Minimal dependencies** — only `requests` and `pyyaml`
- **Production-ready** — comprehensive error handling and logging
- **Well-documented** — extensive docs and 100+ examples

## Key Features

| Feature | Description |
|---------|-------------|
| 🔗 **Pipeline Orchestration** | Create pipelines with step functions and classes |
| 🌳 **Conditional Branches** | Execute different paths based on data conditions |
| 🔄 **Retry Logic** | Automatic retries with configurable backoff |
| 🌐 **API Integration** | Connect to external APIs, register workers |
| 💾 **SQLite Storage** | Persist execution results to database |
| ⚠️ **Error Handling** | Custom exceptions and error codes |
| 📋 **YAML Configuration** | Load and manage configurations |
| 🔀 **Nested Pipelines** | Compose complex workflows |
| 📊 **Progress Tracking** | Rich terminal output |

## Installation

### PyPI (Recommended)

```bash
pip install wpipe
```

### From Source

```bash
git clone https://github.com/wisrovi/wpipe
cd wpipe
pip install -e .
```

### Development Install

```bash
pip install -e ".[dev]"
```

**Requirements:**
- Python 3.9 or higher
- requests (for API integration)
- pyyaml (for YAML configuration)

## Quick Start

```python
from wpipe import Pipeline

def fetch_data(data):
    """Fetch data from a source."""
    return {"users": [{"name": "Alice"}, {"name": "Bob"}]}

def process_data(data):
    """Process the fetched data."""
    return {"count": len(data["users"])}

def save_data(data):
    """Save results."""
    return {"status": "saved"}

pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (fetch_data, "Fetch Data", "v1.0"),
    (process_data, "Process Data", "v1.0"),
    (save_data, "Save Data", "v1.0"),
])

result = pipeline.run({})
# {'users': [...], 'count': 2, 'status': 'saved'}
```

## Core Concepts

### Pipeline

A pipeline is a sequence of steps that process data:

```python
pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (step1, "Step 1", "v1.0"),
    (step2, "Step 2", "v1.0"),
    (step3, "Step 3", "v1.0"),
])
result = pipeline.run(initial_data)
```

### Steps

Steps are functions that receive and return data:

```python
def my_step(data):
    # Process data
    return {"result": data["input"] * 2}
```

### Data Flow

Each step receives accumulated results from previous steps:

```
Input: {'x': 5}
  ↓
Step 1: {'a': 10} → Data: {'x': 5, 'a': 10}
  ↓
Step 2: {'b': 20} → Data: {'x': 5, 'a': 10, 'b': 20}
  ↓
Output: {'x': 5, 'a': 10, 'b': 20}
```

## Examples

Explore **100+ examples** organized by functionality:

| Folder | Examples | Description |
|--------|----------|-------------|
| [01_basic_pipeline](examples/01_basic_pipeline/) | 15 | Functions, classes, mixed steps, data flow |
| [02_api_pipeline](examples/02_api_pipeline/) | 21 | External APIs, workers, execution tracking |
| [03_error_handling](examples/03_error_handling/) | 10 | Exceptions, error codes, recovery |
| [04_condition](examples/04_condition/) | 9 | Conditional branches, decision trees |
| [05_retry](examples/05_retry/) | 9 | Automatic retries, backoff strategies |
| [06_sqlite_integration](examples/06_sqlite_integration/) | 9 | Persistence, database operations |
| [07_nested_pipelines](examples/07_nested_pipelines/) | 9 | Complex workflows, reusable components |
| [08_yaml_config](examples/08_yaml_config/) | 9 | Configuration, environment variables |
| [09_microservice](examples/09_microservice/) | 9 | Production-ready patterns |

### Running Examples

```bash
# Basic pipeline
python examples/01_basic_pipeline/01_simple_function/example.py

# With API (requires API server)
python examples/02_api_pipeline/01_basic_api/example.py
```

## Advanced Features

### Conditional Pipelines

```python
from wpipe import Pipeline, Condition

pipeline = Pipeline(verbose=True)
condition = Condition(
    expression="data_type == 'A'",
    branch_true=[(process_a, "Process A", "v1.0")],
    branch_false=[(process_b, "Process B", "v1.0")],
)
pipeline.set_steps([
    (fetch, "Fetch", "v1.0"),
    condition,
])
```

### API Integration

```python
api_config = {
    "base_url": "http://localhost:8418",
    "token": "your-auth-token"
}
pipeline = Pipeline(api_config=api_config)
pipeline.worker_register(name="processor", version="1.0.0")
```

### SQLite Storage

```python
from wpipe import Pipeline
from wpipe.sqlite import Wsqlite

with Wsqlite(db_name="results.db") as db:
    db.input = {"x": 10}
    result = pipeline.run({"x": 10})
    db.output = result
```

### YAML Configuration

```python
from wpipe.util import leer_yaml

config = leer_yaml("config.yaml")
pipeline = Pipeline(**config["pipeline"])
```

## API Reference

### Pipeline

```python
from wpipe import Pipeline

pipeline = Pipeline(
    verbose=True,           # Enable verbose output
    api_config={},          # API configuration
    max_retries=3,          # Maximum retry attempts
)
```

**Methods:**
- `set_steps(steps)` — Configure pipeline steps
- `run(input_data)` — Execute the pipeline
- `worker_register(name, version)` — Register with API

### Classes

- `Pipeline` — Main pipeline orchestrator
- `Condition` — Conditional branching
- `APIClient` — API communication
- `Wsqlite` / `Sqlite` — Database operations

### Exceptions

```python
from wpipe.exception import TaskError, Codes

try:
    result = pipeline.run(data)
except TaskError as e:
    print(f"Step: {e.step_name}")
    print(f"Code: {e.code}")
```

**Error Codes:**
- `UNKNOWN_ERROR` (500) — Generic error
- `VALIDATION_ERROR` (400) — Input validation failed
- `API_ERROR` (501) — API communication error
- `RETRYABLE_ERROR` (503) — May succeed on retry
- `TIMEOUT_ERROR` (504) — Operation timed out

## Code Quality

| Metric | Value |
|--------|-------|
| Tests | 106 passing |
| Examples | 100+ |
| Python Support | 3.9, 3.10, 3.11, 3.12, 3.13 |
| Type Hints | Complete |
| Docstrings | Google-style |

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wpipe --cov-report=html

# Open coverage report
open htmlcov/index.html

# Lint
ruff check wpipe/

# Type check
mypy wpipe/
```

## Architecture

```
wpipe/
├── pipe/               # Pipeline and Condition implementation
│   ├── pipe.py         # Main Pipeline class
│   ├── progress.py     # Progress tracking
│   └── step.py         # Step utilities
├── api_client/         # API communication
│   └── api_client.py   # APIClient class
├── sqlite/             # Database operations
│   └── sqlite.py       # Wsqlite and Sqlite classes
├── log/                # Logging utilities
├── ram/                # Memory utilities
├── util/               # YAML utilities
└── exception/          # Custom exceptions
    ├── exception.py    # TaskError, ProcessError, ApiError
    └── codes.py         # Error codes
```

## Documentation

| Resource | URL |
|----------|-----|
| Documentation | https://wpipe.readthedocs.io/ |
| PyPI Package | https://pypi.org/project/wpipe/ |
| GitHub Repository | https://github.com/wisrovi/wpipe |
| Releases | https://github.com/wisrovi/wpipe/releases |
| Issues | https://github.com/wisrovi/wpipe/issues |

## Why wpipe?

| Traditional Tools | wpipe |
|-------------------|-------|
| Complex setup | Simple pip install |
| Web UI required | Pure Python code |
| Heavy dependencies | Minimal requirements |
| YAML/JSON config | Python code |
| Overkill for simple tasks | Perfect for any scale |

## License

MIT License - See [LICENSE](LICENSE) file

## Author

**William Steve Rodriguez Villamizar**

- GitHub: [github.com/wisrovi](https://github.com/wisrovi)
- LinkedIn: [linkedin.com/in/wisrovi-rodriguez](https://www.linkedin.com/in/wisrovi-rodriguez/)
- Portfolio: [wisrovi.github.io](https://wisrovi.github.io/)

---

<p align="center">
  <strong>Star ⭐ this repo if you find it useful!</strong>
</p>
