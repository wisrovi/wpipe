# wpipe v1.0.0 LTS Release Notes

**Release Date:** March 22, 2026

We're excited to announce the first **Long Term Support (LTS)** release of **wpipe**, a powerful Python library for creating and executing sequential data processing pipelines.

## What's New in v1.0.0

### 🎯 LTS Release
- Stable API with guaranteed backward compatibility
- Production-ready for enterprise use
- Comprehensive documentation and support

### 📚 Documentation Overhaul

**7,482 lines** of professional documentation including:

| Document | Description |
|----------|-------------|
| Getting Started | Prerequisites, installation, quick start |
| User Guide | 10 detailed sections covering all features |
| Tutorials | Step-by-step guides for every feature |
| API Reference | Complete API documentation with tables |
| FAQ | 40+ questions and answers |
| Glossary | 40+ term definitions |
| Architecture | System design and patterns |
| Best Practices | Production recommendations |
| Troubleshooting | Debugging guide |

### 💯 100+ Examples

Organized by complexity from basic to advanced:

| Category | Count | Examples |
|----------|-------|----------|
| Basic Pipeline | 15 | Functions, classes, data flow |
| API Pipeline | 21 | Workers, health checks, tracking |
| Error Handling | 10 | Exceptions, error codes, recovery |
| Conditions | 9 | Conditional branching, decision trees |
| Retry Logic | 9 | Automatic retries, backoff |
| SQLite | 9 | Persistence, queries |
| Nested Pipelines | 9 | Complex workflows |
| YAML Config | 9 | Configuration, env vars |
| Microservice | 9 | Production patterns |

### 🛠️ Code Quality

- **106 tests passing** (100% coverage goal)
- Complete type hints
- Google-style docstrings
- Ruff linting (zero errors)
- Mypy type checking

## Installation

### PyPI (Recommended)

```bash
pip install wpipe==1.0.0
```

### Latest Version

```bash
pip install wpipe
```

### From Source

```bash
git clone https://github.com/wisrovi/wpipe
cd wpipe
pip install -e .
```

## Quick Start

```python
from wpipe import Pipeline

def fetch_data(data):
    return {"users": [{"name": "Alice"}, {"name": "Bob"}]}

def process_data(data):
    return {"count": len(data["users"])}

pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (fetch_data, "Fetch Data", "v1.0"),
    (process_data, "Process Data", "v1.0"),
])

result = pipeline.run({})
# {'users': [...], 'count': 2}
```

## Key Features

### Pipeline Orchestration
```python
pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (step1, "Step 1", "v1.0"),
    (step2, "Step 2", "v1.0"),
])
```

### Conditional Branches
```python
from wpipe import Condition

condition = Condition(
    expression="mode == 'production'",
    branch_true=[(prod_step, "Production", "v1.0")],
    branch_false=[(dev_step, "Development", "v1.0")],
)
```

### API Integration
```python
pipeline = Pipeline(api_config={
    "base_url": "http://api.example.com",
    "token": "your-token"
})
pipeline.worker_register(name="worker", version="1.0.0")
```

### SQLite Storage
```python
from wpipe.sqlite import Wsqlite

with Wsqlite("results.db") as db:
    db.input = {"x": 10}
    result = pipeline.run({"x": 10})
    db.output = result
```

### Error Handling
```python
from wpipe.exception import TaskError, Codes

try:
    result = pipeline.run(data)
except TaskError as e:
    print(f"Step: {e.step_name}")
    print(f"Code: {e.code}")
```

## Migration Guide

Version 1.0.0 is **fully backward compatible** with 0.x versions. No breaking changes.

```bash
pip install --upgrade wpipe
```

## Resources

| Resource | URL |
|----------|-----|
| Documentation | https://wpipe.readthedocs.io/ |
| PyPI Package | https://pypi.org/project/wpipe/ |
| GitHub Repository | https://github.com/wisrovi/wpipe |
| Releases | https://github.com/wisrovi/wpipe/releases |
| Issues | https://github.com/wisrovi/wpipe/issues |

## What's Changed

### v0.1.7 → v1.0.0

- Added comprehensive Sphinx documentation
- Added 100+ examples organized by complexity
- Added professional landing page (index.html)
- Improved type hints throughout
- Enhanced error handling
- Added conditional branching
- Added retry logic with backoff
- Added nested pipelines
- Improved SQLite integration
- Added YAML configuration
- Added worker management
- Added health checks
- Improved progress tracking

## Acknowledgments

Thank you to all contributors and users of wpipe who have helped shape this library.

## License

MIT License - See [LICENSE](LICENSE) file

---

<p align="center">
  <strong>⭐ Star the repository if you find wpipe useful!</strong>
</p>
