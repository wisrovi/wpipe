# Phase 2 Features: Parallelism & Composition

Comprehensive guide to all Phase 2 features.

**Status**: 🔄 In Development (80% complete)  
**Last Updated**: April 1, 2024

---

## Overview

Phase 2 introduces 3 major feature sets:

1. **Parallel Execution**: 3-5x speedup for pipeline processing
2. **Pipeline Composition**: Modular, reusable pipeline architectures  
3. **Step Decorators**: Pythonic inline step definitions

---

## 1. Parallel Execution

### Problem Solved
Sequential step execution is slow for pipelines with independent steps.

### Solution
Execute steps in parallel using:
- **ThreadPoolExecutor** for I/O-bound tasks (network, files, DB)
- **ProcessPoolExecutor** for CPU-bound tasks (calculations, processing)
- **DAGScheduler** for automatic dependency resolution

### Performance

```
Sequential: ████████████████████ (10 seconds)
Parallel:   ████ (2 seconds - 5x speedup!)
```

### Quick Start

```python
from wpipe.parallel import ParallelExecutor, ExecutionMode

executor = ParallelExecutor(max_workers=4)

# Add independent I/O-bound steps
executor.add_step("fetch_api", fetch_api, mode=ExecutionMode.IO_BOUND)
executor.add_step("fetch_db", fetch_db, mode=ExecutionMode.IO_BOUND)

# Add dependent step
executor.add_step(
    "merge",
    merge_data,
    depends_on=["fetch_api", "fetch_db"],
)

# Execute (parallelism is automatic!)
result = executor.execute({})
```

### Architecture

```
┌─────────────────────────────────────┐
│ ParallelExecutor                    │
├─────────────────────────────────────┤
│ Input: Steps with dependencies      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ DAGScheduler                        │
├─────────────────────────────────────┤
│ Topological Sort:                   │
│  Level 0: [step_1, step_2, step_3] │
│  Level 1: [merge_step]              │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌─────────────┐ ┌─────────────┐
│ ThreadPool  │ │ ProcessPool │
│ (IO tasks)  │ │ (CPU tasks) │
└─────────────┘ └─────────────┘
       │               │
       └───────┬───────┘
               ▼
┌─────────────────────────────────────┐
│ ContextMerger                       │
├─────────────────────────────────────┤
│ Merge parallel results into context │
└─────────────────────────────────────┘
```

### ExecutionMode

```python
from wpipe.parallel import ExecutionMode

ExecutionMode.IO_BOUND      # Use ThreadPoolExecutor (default)
ExecutionMode.CPU_BOUND     # Use ProcessPoolExecutor
ExecutionMode.SEQUENTIAL    # No parallelism
```

### When to Use

| Task Type | Mode | Example |
|-----------|------|---------|
| API calls | IO_BOUND | Fetch from 3 APIs in parallel |
| File I/O | IO_BOUND | Read multiple files |
| Database queries | IO_BOUND | Query multiple tables |
| Calculations | CPU_BOUND | Number crunching |
| Data processing | CPU_BOUND | ML model inference |
| Quick operations | SEQUENTIAL | Simple assignments |

### Best Practices

- ✅ Use IO_BOUND for network/file operations
- ✅ Use CPU_BOUND for calculations
- ✅ Keep tasks small and focused
- ✅ Monitor memory usage with many tasks
- ❌ Don't use CPU_BOUND for I/O
- ❌ Don't create too many workers (diminishing returns)

---

## 2. Pipeline Composition

### Problem Solved
Large pipelines are hard to maintain. Decompose into reusable sub-pipelines.

### Solution
Use pipelines as steps within other pipelines.

### Quick Start

```python
from wpipe import Pipeline
from wpipe.composition import NestedPipelineStep

# Create modular sub-pipelines
extract_pipeline = Pipeline()
extract_pipeline.add_state("extract", lambda c: {"raw": data})

transform_pipeline = Pipeline()
transform_pipeline.add_state("transform", lambda c: {"clean": data})

# Compose into main pipeline
main = Pipeline()
main.add_state("extract", lambda c: extract_pipeline.run(c))
main.add_state("transform", lambda c: transform_pipeline.run(c))

result = main.run({})
```

### Context Management

Pipelines can pass data with smart merging:

```python
# Child overrides parent
merge_contexts(parent, child, "child_wins")

# Parent preserved
merge_contexts(parent, child, "parent_wins")

# Lists concatenated
merge_contexts(parent, child, "merge_list")
```

### Filtering

Transform context before passing to child:

```python
def filter_input(context):
    # Only pass specific keys
    return {"users": context["users"]}

nested = NestedPipelineStep(
    "sub",
    sub_pipeline,
    context_filter=filter_input,
)
```

### Architecture

```
┌────────────────────────────────────┐
│ Main Pipeline                      │
├────────────────────────────────────┤
│ Step 1: fetch_data                 │
│ Step 2: NestedPipelineStep("etl")  │ <── Sub-pipeline
│ Step 3: save_results               │
└────────────────────────────────────┘
         │
         ├─ Context flows through
         │
         ▼
    ┌──────────────────────┐
    │ ETL Sub-Pipeline     │
    ├──────────────────────┤
    │ - extract            │
    │ - transform          │
    │ - load               │
    └──────────────────────┘
         │
         ├─ Results flow back
         │
         ▼
    Merged context continues
```

### Use Cases

- **ETL**: Separate extract/transform/load
- **Domain Separation**: ML, Analytics, Reporting
- **Reusability**: Use same sub-pipeline in multiple places
- **Testing**: Test sub-pipelines independently
- **Modularity**: Keep pipelines focused

---

## 3. Step Decorators

### Problem Solved
Manual step registration is verbose and error-prone.

### Solution
Use `@step()` decorator for inline definitions with auto-registration.

### Quick Start

```python
from wpipe.decorators import step, AutoRegister
from wpipe import Pipeline

@step(timeout=30, description="Fetch users")
def fetch_users(context):
    return {"users": [...]}

@step(depends_on=["fetch_users"], description="Validate")
def validate_users(context):
    return {"valid_users": [...]}

# Auto-register all decorated steps
pipeline = Pipeline()
AutoRegister.register_all(pipeline)

result = pipeline.run({})
```

### Metadata

```python
@step(
    name="my_step",
    timeout=30,
    depends_on=["other_step"],
    retry_count=3,
    description="Does something",
    tags=["prod", "critical"],
)
def my_step(context):
    return {}
```

### Registry

```python
from wpipe.decorators import get_step_registry, AutoRegister

# Get all decorated steps
registry = get_step_registry()
all_steps = registry.get_all()

# Register specific steps
AutoRegister.register_by_tag(pipeline, "prod")
```

### Benefits

- ✅ Cleaner, more Pythonic syntax
- ✅ Automatic registration and discovery
- ✅ Built-in metadata (timeout, dependencies, tags)
- ✅ Better IDE integration
- ✅ Less boilerplate code

---

## Integration with Phase 1

### Combined Example

```python
from wpipe import Pipeline
from wpipe.decorators import step, AutoRegister
from wpipe import (
    CheckpointManager,
    timeout_sync,
    TypeValidator,
    ResourceMonitor,
)

# Use Phase 1 features with Phase 2
@step(timeout=30)
def fetch_data(context):
    # Uses timeout from Phase 1
    return {"data": [...]}

@step(depends_on=["fetch_data"])
def process_data(context):
    # Validate with Phase 1
    schema = {"data": list}
    TypeValidator.validate_dict(context, schema)
    return {"result": [...]}

# Create pipeline
pipeline = Pipeline()
AutoRegister.register_all(pipeline)

# Use Phase 1 features
checkpoint_mgr = CheckpointManager("pipeline.db")

with ResourceMonitor("pipeline_run") as monitor:
    result = pipeline.run({})

print(f"Peak RAM: {monitor.get_summary()['peak_ram_mb']} MB")
```

---

## Performance Comparison

### I/O-Bound Pipeline (fetch 3 APIs)

```
Sequential: 
  API 1: 1s
  API 2: 1s  
  API 3: 1s
  Total: 3s

Parallel (ThreadPool):
  API 1,2,3: 1s (concurrent)
  Total: 1s
  
Speedup: 3x ✅
```

### CPU-Bound Pipeline (process 3 large datasets)

```
Sequential:
  Process 1: 2s
  Process 2: 2s
  Process 3: 2s
  Total: 6s

Parallel (ProcessPool, dual-core):
  Process 1,2: 2s (concurrent)
  Process 3: 2s
  Total: 4s
  
Speedup: 1.5x (GIL bypass limited by cores)
```

---

## Troubleshooting

### Parallel Not Faster

**Q**: Parallel execution not faster than sequential?

**A**: 
- Check ExecutionMode matches task type
- Ensure tasks are independent
- Monitor thread/process overhead
- Consider task granularity

### Memory Issues

**Q**: High memory usage with parallel execution?

**A**:
- Reduce max_workers
- Check for data duplication in contexts
- Profile memory usage
- Consider chunking large datasets

### Decorator Not Working

**Q**: Decorated steps not being registered?

**A**:
- Verify import is correct
- Call `AutoRegister.register_all(pipeline)`
- Check step names match exactly
- Look for typos in dependencies

---

## API Reference

### ParallelExecutor

```python
executor = ParallelExecutor(max_workers=4)
executor.add_step(name, func, mode, timeout, depends_on)
result = executor.execute(context)
results = executor.get_results()
```

### NestedPipelineStep

```python
nested = NestedPipelineStep(
    name,
    pipeline,
    context_filter=None,
    result_filter=None,
    timeout=None,
)
result = nested.run(context)
exec_time = nested.get_execution_time()
```

### @step() Decorator

```python
@step(
    name=None,
    timeout=None,
    depends_on=None,
    retry_count=0,
    parallel=False,
    description="",
    tags=None,
)
def my_step(context): ...
```

---

## What's Next?

### Phase 3 Features
- Distributed execution (Redis/RabbitMQ)
- Advanced scheduling (CRON, events)
- Performance optimization (caching)
- Dashboard v2 (real-time monitoring)

### Improvements for Phase 2.1
- Dynamic worker pool sizing
- Task prioritization
- Better error handling
- Performance profiling

---

## Resources

- [Parallel Module](../../wpipe/parallel/README.md)
- [Composition Module](../../wpipe/composition/README.md)
- [Decorators Module](../../wpipe/decorators/README.md)
- [Examples](../../examples/)
- [Phase 1 Features](../../PHASE_1_FEATURES.md)

---

**Last Updated**: April 1, 2024  
**Status**: 🔄 In Development (80% complete)  
**Next**: Complete documentation + 9 additional examples
