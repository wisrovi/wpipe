# wpipe v1.0.0 LTS

**Long Term Support Release**

We're excited to announce the first LTS release of wpipe, a Python library for creating and executing sequential data processing pipelines.

## What's New

### 100+ Examples
Organized by complexity (01-09):
- Basic Pipeline (15 examples)
- API Pipeline (21 examples)
- Error Handling (10 examples)
- Condition Branching (9 examples)
- Retry Logic (9 examples)
- SQLite Integration (9 examples)
- Nested Pipelines (9 examples)
- YAML Configuration (9 examples)
- Microservice (9 examples)

### Code Quality
- Complete type hints on all functions
- Google-style docstrings (Args, Returns, Example sections)
- 5 Mermaid diagrams per example (graph LR, sequenceDiagram, stateDiagram-v2, flowchart LR, graph TB)
- 206 unit tests passing (106 core + 100 example tests)
- Full ruff linting and PEP 8 compliance

### Documentation
- Full Sphinx documentation at [wpipe.readthedocs.io](https://wpipe.readthedocs.io/)
- Comprehensive [CHANGELOG.md](https://github.com/wisrovi/wpipe/blob/main/CHANGELOG.md)
- README with LTS badge

## Installation

```bash
pip install wpipe==1.0.0
```

Or install the latest:

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

## Upgrade Guide

Version 1.0.0 is fully backward compatible with 0.x versions. No breaking changes.

```bash
pip install --upgrade wpipe
```

## What's Changed

See the full [CHANGELOG.md](https://github.com/wisrovi/wpipe/blob/main/CHANGELOG.md) for detailed release notes.

## Support

- [Documentation](https://wpipe.readthedocs.io/)
- [Examples](https://github.com/wisrovi/wpipe/tree/main/examples)
- [Report an Issue](https://github.com/wisrovi/wpipe/issues)
- [Discussions](https://github.com/wisrovi/wpipe/discussions)

---

**Thank you** to all contributors and users of wpipe!
