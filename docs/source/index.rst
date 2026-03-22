---
html_theme:
  navigation_depth: 4
---

# wpipe - Python Pipeline Library

**wpipe** is a powerful Python library for creating and executing sequential data processing pipelines with task orchestration, API integration, and execution tracking.

```{image} https://img.shields.io/pypi/v/wpipe.svg
:target: https://pypi.org/project/wpipe/
:alt: PyPI Version
```

```{image} https://img.shields.io/pypi/pyversions/wpipe.svg
:target: https://pypi.org/project/wpipe/
:alt: Python Versions
```

```{image} https://img.shields.io/github/license/wisrovi/wpipe.svg
:target: https://github.com/wisrovi/wpipe/blob/main/LICENSE
:alt: License
```

---

## Why wpipe?

::::{grid} 1 2 3
:gutter: 3

:::{grid-item-card} 🚀 Simple & Intuitive
---
class-header: sd-text-success
---
Create pipelines with just a few lines of code. No complex configuration needed.
:::

:::{grid-item-card} 📊 Progress Tracking
---
class-header: sd-text-primary
---
Real-time progress visualization with rich terminal output.
:::

:::{grid-item-card} ☁️ API Integration
---
class-header: sd-text-info
---
Connect to external APIs for worker registration and process tracking.
:::

:::{grid-item-card} 💾 Data Persistence
---
class-header: sd-text-warning
---
Built-in SQLite integration for storing pipeline execution results.
:::

:::{grid-item-card} 🌿 Conditional Logic
---
class-header: sd-text-danger
---
Execute different paths based on data conditions.
:::

:::{grid-item-card} 🔄 Retry Mechanism
---
class-header: sd-text-muted
---
Automatic retries for failed steps with configurable parameters.
:::
::::



## Quick Start

::::{tab-set}
:::{tab-item} Installation
:sync: installation

```bash
pip install wpipe
```

Or install from source:

```bash
git clone https://github.com/wisrovi/wpipe.git
cd wpipe
pip install -e .
```
:::

:::{tab-item} Basic Usage
:sync: basic

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
# {'result': 10, 'final': 20}
```
:::
::::



## Key Features

::::{grid} 1 1 2
:gutter: 3

:::{grid-item-card}
:link: getting_started.html
:link-type: doc

### 📚 Getting Started

Learn how to install and use wpipe in your projects.

→ Learn more
:::

:::{grid-item-card}
:link: user_guide/index.html
:link-type: doc

### 📖 User Guide

Deep dive into all features with detailed explanations.

→ Learn more
:::

:::{grid-item-card}
:link: api_reference.html
:link-type: doc

### 🔧 API Reference

Complete API documentation with examples.

→ Learn more
:::

:::{grid-item-card}
:link: examples/index.html
:link-type: doc

### 💡 Examples

100+ examples organized by functionality.

→ Learn more
:::
::::



## Architecture Overview

```{mermaid}
graph TB
    subgraph Input["📥 Input"]
        D["data = {'x': 5}"]
    end
    
    subgraph Pipeline["🔄 Pipeline"]
        S1["Step 1<br/>Multiply by 2"]
        S2["Step 2<br/>Add 10"]
    end
    
    subgraph Output["📤 Output"]
        R["{'x': 5<br/>'result': 10<br/>'final': 20}"]
    end
    
    D --> S1
    S1 --> S2
    S2 --> R
    
    style Input fill:#e1f5fe
    style Pipeline fill:#f3e5f5
    style Output fill:#e8f5e9
```

Each step receives output from the previous step for chained processing.



## Code Quality

| Metric | Value |
|--------|-------|
| Tests | 206 passing |
| Type Hints | 100% coverage |
| Docstrings | Google-style |
| Examples | 100+ |
| Python Support | 3.9 - 3.13 |



## Community & Support

::::{grid} 1 1 2 3
:gutter: 3

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/issues
:link-type: url

🐛 Report a Bug

Open an issue on GitHub.
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/discussions
:link-type: url

💬 Join Discussion

Ask questions and share ideas.
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe
:link-type: url

⭐ View on GitHub

Contribute to the project.
:::
::::



## Documentation

```{toctree}
:maxdepth: 2
:caption: 📖 Documentation

getting_started
installation
user_guide/index
examples/index
api_reference
tutorials
faq
```

```{toctree}
:maxdepth: 2
:caption: 🔗 Reference

Glossary <glossary>
architecture
changelog
```

---

*wpipe is maintained by William Steve Rodriguez Villamizar and distributed under the MIT License.*
