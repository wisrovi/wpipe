# Phase 2 Quick Start Guide

**For existing Phase 1 users**: Your code continues to work unchanged. Phase 2 is purely additive.

---

## 1️⃣ Parallel Execution

Run independent steps in parallel for 3-5x speedup.

### Basic Example
```python
from wpipe.parallel import ParallelExecutor, ExecutionMode
import time

executor = ParallelExecutor(max_workers=4)

# Add independent I/O tasks
executor.add_step("fetch_users", fetch_users, mode=ExecutionMode.IO_BOUND)
executor.add_step("fetch_posts", fetch_posts, mode=ExecutionMode.IO_BOUND)
executor.add_step("fetch_comments", fetch_comments, mode=ExecutionMode.IO_BOUND)

# Add dependent aggregation step
executor.add_step(
    "aggregate", 
    aggregate, 
    depends_on=["fetch_users", "fetch_posts", "fetch_comments"]
)

result = executor.execute({})
```

### When to Use
| Task | Mode | Example |
|------|------|---------|
| Network calls | `IO_BOUND` | API calls, database queries |
| File operations | `IO_BOUND` | Reading multiple files |
| Calculations | `CPU_BOUND` | Data processing, ML |
| Simple work | `SEQUENTIAL` | Assignments, validation |

---

## 2️⃣ Pipeline Composition

Build modular pipelines from sub-pipelines.

### Basic Example
```python
from wpipe import Pipeline
from wpipe.composition import NestedPipelineStep

# Create sub-pipeline
extract_pipeline = Pipeline()
extract_pipeline.add_state("extract", lambda c: {"raw_data": [...]})

# Nest it in main pipeline
main = Pipeline()
nested = NestedPipelineStep("extract_step", extract_pipeline)
main.add_state("extract", lambda c: nested.run(c))

result = main.run({})
```

### With Context Filtering
```python
from wpipe.composition import CompositionHelper

def filter_context(context):
    # Only pass specific keys
    return CompositionHelper.extract_context_subset(
        context, 
        ["users", "posts"]
    )

nested = NestedPipelineStep(
    "extract_step", 
    extract_pipeline,
    context_filter=filter_context
)
```

---

## 3️⃣ Step Decorators

Define steps with Pythonic decorators and auto-register them.

### Basic Example
```python
from wpipe.decorators import step, AutoRegister
from wpipe import Pipeline

@step(description="Fetch data", tags=["data"])
def fetch_data(context):
    return {"data": [...]}

@step(depends_on=["fetch_data"], description="Process")
def process_data(context):
    return {"processed": [...]}

# Auto-register and run
pipeline = Pipeline()
AutoRegister.register_all(pipeline)
result = pipeline.run({})
```

### With Metadata
```python
@step(
    name="my_step",
    timeout=30,
    depends_on=["step1"],
    retry_count=3,
    description="Does something",
    tags=["prod", "critical"]
)
def my_step(context):
    return {}
```

### Selective Registration by Tag
```python
from wpipe.decorators import get_step_registry

pipeline = Pipeline()
registry = get_step_registry()

# Register only "prod" tagged steps
AutoRegister.register_by_tag(pipeline, "prod", registry)

result = pipeline.run({})
```

---

## 📚 Real Examples

Find working examples in `examples/`:

### Parallelism
- `16_parallelism/01_basic/parallel_basic.py`
- `16_parallelism/02_io_bound/parallel_io_tasks.py`
- `16_parallelism/03_cpu_bound/parallel_cpu_tasks.py`

### Composition
- `17_composition/01_nested/nested_pipeline.py`
- `17_composition/02_filtering/composition_filtering.py`
- `17_composition/03_etl/etl_pipeline.py`

### Decorators
- `18_decorators/01_basic/decorator_basic.py`
- `18_decorators/02_advanced/advanced_decorators.py`
- `18_decorators/03_registry/decorator_registry.py`

### Benchmarks
- `19_benchmarks/phase2_benchmarks.py`

---

## ✅ Phase 1 Still Works (Unchanged)

Your Phase 1 code continues to work exactly:

```python
# Phase 1 - UNCHANGED
from wpipe import Pipeline, CheckpointManager

p = Pipeline()
p.set_steps([(func1, "step1", ""), (func2, "step2", "")])

# Checkpoint support still works
checkpoint_mgr = CheckpointManager("db.sqlite")

result = p.run({})
```

---

## 🚀 Migration

### Gradual Adoption
```python
# Existing Phase 1 code (works as-is)
p.set_steps([(func1, "s1", ""), (func2, "s2", "")])

# New Phase 2 convenience (optional)
p.add_state("s1", func1)
p.add_state("s2", func2)

# Use new Phase 2 features when needed
from wpipe.parallel import ParallelExecutor
executor = ParallelExecutor()
# ...
```

### Key Points
- ✅ **Zero breaking changes** - all Phase 1 code unchanged
- ✅ **Fully compatible** - use Phase 1 and Phase 2 together
- ✅ **Additive only** - new features don't replace old ones
- ✅ **No migration required** - upgrade when ready

---

## 📖 Full Documentation

- [PHASE_2_FEATURES.md](PHASE_2_FEATURES.md) - Comprehensive guide
- [wpipe/parallel/README.md](wpipe/parallel/README.md) - Parallelism
- [wpipe/composition/README.md](wpipe/composition/README.md) - Composition
- [wpipe/decorators/README.md](wpipe/decorators/README.md) - Decorators

---

## Performance Benchmarks

```
I/O Parallelism:    4x faster (4 tasks, 1s each)
Composition:        <5% overhead
Decorator:          <1ms per step
```

Run benchmarks:
```bash
python examples/19_benchmarks/phase2_benchmarks.py
```

---

## Support

- 📧 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📚 Docs: https://wpipe.readthedocs.io

---

**Version**: 2.0.0-LTS  
**Status**: ✅ Production Ready  
**Users**: 500k+ | Zero changes required
