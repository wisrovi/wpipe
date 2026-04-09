# Parallel Execution

Execute pipeline steps in parallel for dramatically improved performance.

## Features

- **ThreadPoolExecutor**: I/O-bound task parallelism
- **ProcessPoolExecutor**: CPU-bound task parallelism
- **DAGScheduler**: Automatic dependency resolution
- **ExecutionMode**: Control execution strategy per step
- **ContextMerger**: Intelligent result aggregation

## Quick Start

```python
from wpipe.parallel import ParallelExecutor, ExecutionMode
import time

executor = ParallelExecutor(max_workers=4)

# Add parallel steps (can run simultaneously)
executor.add_step("fetch_1", fetch_data_1, mode=ExecutionMode.IO_BOUND)
executor.add_step("fetch_2", fetch_data_2, mode=ExecutionMode.IO_BOUND)
executor.add_step("fetch_3", fetch_data_3, mode=ExecutionMode.IO_BOUND)

# Add dependent step
executor.add_step(
    "merge",
    merge_data,
    depends_on=["fetch_1", "fetch_2", "fetch_3"],
)

# Execute
result = executor.execute({})
```

## Performance

- **I/O-Bound Tasks**: 3-5x speedup
  - Network requests: 4-5x faster
  - File operations: 3-4x faster
  - Database queries: 2-3x faster

- **CPU-Bound Tasks**: 2-3x speedup
  - Multi-core utilization
  - Process-level parallelism
  - GIL bypass

## API

### ParallelExecutor

#### `__init__(max_workers: int = 4)`
Initialize executor with worker pool size.

#### `add_step(name, func, mode=IO_BOUND, timeout=None, depends_on=None)`
Add step to executor.

#### `execute(context: Dict) -> Dict`
Execute all steps with automatic dependency resolution.

#### `get_results() -> Dict`
Get results from all executed steps.

### ExecutionMode

- `IO_BOUND`: Use ThreadPoolExecutor (default)
- `CPU_BOUND`: Use ProcessPoolExecutor
- `SEQUENTIAL`: No parallelism

### DAGScheduler

#### `add_step(step: StepDependency)`
Add step with dependencies.

#### `topological_sort() -> List[List[str]]`
Get execution order by level.

#### `get_parallel_groups() -> List[List[StepDependency]]`
Get steps grouped for parallel execution.

## Use Cases

- **Data fetching**: Parallel API calls
- **Processing**: Map-reduce patterns
- **Analysis**: Distributed calculations
- **ETL**: Multi-source extraction

## Troubleshooting

**Q: Tasks not running in parallel?**
- A: Check ExecutionMode matches task type (IO_BOUND/CPU_BOUND)
- Verify dependencies allow parallelism

**Q: Memory usage high?**
- A: Reduce max_workers
- Check for data duplication in contexts

**Q: Some tasks slow?**
- A: Consider task granularity
- Check for dependency chains

## See Also

- [Parallel Examples](../../examples/16_parallelism/)
- [Phase 2 Features](../../PHASE_2_FEATURES.md)
