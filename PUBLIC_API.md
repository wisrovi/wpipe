# wpipe Public API Contract

**Version**: 2.0.0
**Status**: LTS Certified
**Last Updated**: April 13, 2026

---

## Overview

This document defines the **public API** of wpipe — the classes, functions, and modules that are officially supported and guaranteed to remain stable throughout the LTS lifecycle (until 2031).

Anything **not** listed here is considered **internal** and may change without notice or breaking version bump.

---

## Public API

All public API is exported from the top-level `wpipe` module:

```python
import wpipe
```

### Core Pipeline

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `Pipeline` | Class | `wpipe.pipe` | Main pipeline orchestration class |
| `PipelineAsync` | Class | `wpipe.pipe.pipe_async` | Async pipeline support |
| `Condition` | Class | `wpipe.pipe` | Conditional branching |
| `For` | Class | `wpipe.pipe` | Loop construct for pipelines |

**Usage**:
```python
from wpipe import Pipeline, PipelineAsync, Condition, For
```

### Step Decorators

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `step` | Decorator | `wpipe.decorators` | Define pipeline steps inline |
| `StepRegistry` | Class | `wpipe.decorators` | Central step registry |
| `AutoRegister` | Class | `wpipe.decorators` | Bulk registration helper |
| `get_step_registry` | Function | `wpipe.decorators` | Access the step registry |

**Usage**:
```python
from wpipe import step, StepRegistry, AutoRegister, get_step_registry
```

### Transform Utilities

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `to_obj` | Decorator | `wpipe.util` | Convert function output to objects |
| `auto_dict_input` | Decorator | `wpipe.util` | Auto-convert dict input to objects |
| `state` | Decorator | `wpipe.util` | State management decorator |
| `object_to_dict` | Decorator | `wpipe.util` | Convert object to dict |

**Usage**:
```python
from wpipe import to_obj, auto_dict_input, state, object_to_dict
```

### Parallel Execution

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `ParallelExecutor` | Class | `wpipe.parallel` | Execute steps in parallel |
| `ExecutionMode` | Enum | `wpipe.parallel` | IO_BOUND, CPU_BOUND, SEQUENTIAL |
| `DAGScheduler` | Class | `wpipe.parallel` | Dependency graph management |

**Usage**:
```python
from wpipe import ParallelExecutor, ExecutionMode, DAGScheduler
```

### Pipeline Composition

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `PipelineAsStep` | Class | `wpipe.composition` | Use pipeline as a step |
| `CompositionHelper` | Class | `wpipe.composition` | Composition utilities |
| `NestedPipelineStep` | Class | `wpipe.composition` | Nested pipeline step |

**Usage**:
```python
from wpipe import PipelineAsStep, CompositionHelper, NestedPipelineStep
```

### Checkpointing

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `CheckpointManager` | Class | `wpipe.checkpoint` | Save and resume pipeline state |

**Usage**:
```python
from wpipe import CheckpointManager
```

### Timeouts

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `timeout_sync` | Decorator | `wpipe.timeout` | Sync function timeout |
| `timeout_async` | Decorator | `wpipe.timeout` | Async function timeout |
| `TimeoutError` | Exception | `wpipe.timeout` | Timeout exception |
| `TaskTimer` | Class | `wpipe.timeout` | Task timing utility |

**Usage**:
```python
from wpipe import timeout_sync, timeout_async, TimeoutError, TaskTimer
```

### Type Validation

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `TypeValidator` | Class | `wpipe.type_hinting` | Runtime type validation |
| `PipelineContext` | Class | `wpipe.type_hinting` | Typed pipeline context |
| `GenericPipeline` | Class | `wpipe.type_hinting` | Generic typed pipeline |

**Usage**:
```python
from wpipe import TypeValidator, PipelineContext, GenericPipeline
```

### Resource Monitoring

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `ResourceMonitor` | Class | `wpipe.resource_monitor` | Track RAM/CPU usage |
| `ResourceMonitorRegistry` | Class | `wpipe.resource_monitor` | Monitor registry |

**Usage**:
```python
from wpipe import ResourceMonitor, ResourceMonitorRegistry
```

### Export

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `PipelineExporter` | Class | `wpipe.export` | Export to JSON/CSV |

**Usage**:
```python
from wpipe import PipelineExporter
```

### Tracking

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `PipelineTracker` | Class | `wpipe.tracking` | Pipeline execution tracker |
| `Metric` | Class | `wpipe.tracking` | Metric definition |
| `Severity` | Enum | `wpipe.tracking` | Severity levels |

**Usage**:
```python
from wpipe import PipelineTracker, Metric, Severity
```

### Integrations

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `APIClient` | Class | `wpipe.api_client` | HTTP API client |
| `Wsqlite` | Class | `wpipe.sqlite` | SQLite storage wrapper |
| `memory` | Decorator | `wpipe.ram` | Memory control decorator |
| `new_logger` | Function | `wpipe.log` | Create loguru logger |

**Usage**:
```python
from wpipe import APIClient, Wsqlite, memory, new_logger
```

### Dashboard

| Name | Type | Module | Description |
|------|------|--------|-------------|
| `start_dashboard` | Function | `wpipe.dashboard` | Start FastAPI dashboard |

**Usage**:
```python
from wpipe import start_dashboard
```

---

## Internal Modules (NOT Public API)

These modules are **internal** and may change without notice:

| Module | Reason |
|--------|--------|
| `wpipe.__init__` | Module initialization and exports |
| `wpipe.pipe.pipe_async` | Internal async implementation |
| `wpipe.sqlite.Wsqlite` | Internal SQLite wrapper (use `Wsqlite` from public API) |
| `wpipe.util.*` | Utility functions not listed in public API |
| `wpipe.exception.*` | Internal exception implementation |
| `wpipe.dashboard.*` | Internal dashboard implementation |

**Rule of thumb**: If it's not in `wpipe.__all__` or this document, it's internal.

---

## Stability Guarantees

### During LTS (2.0.x series)

- ✅ **No breaking changes** to public API
- ✅ **No removal** of public API elements
- ✅ **No signature changes** to public functions/methods
- ✅ **No behavior changes** that break existing code

### Allowed Changes

- ✅ Bug fixes that correct documented behavior
- ✅ Security patches
- ✅ Performance improvements (without behavior change)
- ✅ Internal refactoring
- ✅ New public API additions (additive only)

---

## Error Codes

The following error codes are part of the public API and guaranteed stable:

| Code | Constant | Description |
|------|----------|-------------|
| 501 | `ApiError` | API communication error |
| 502 | `TaskError` | Task execution failed |
| 503 | `UPDATE_PROCESS_OK` | Process completed successfully |
| 504 | `UPDATE_PROCESS_ERROR` | Process update failed |
| 505 | `UPDATE_TASK` | Task update failed |

---

## Deprecation Policy

When a public API element needs to be deprecated:

1. **Mark as deprecated** with `warnings.warn()`
2. **Document the deprecation** in release notes
3. **Provide migration path** in documentation
4. **Wait one LTS cycle** before removal (minimum 2 years)
5. **Remove in next major version** (e.g., 3.0.0)

---

## Version Information

```python
import wpipe

# Current version
print(wpipe.__version__)  # "2.0.0"
```

---

## Testing the Public API

All public API elements are tested for:
- Correctness
- Backward compatibility
- Edge cases
- Error handling

Tests are located in `test/` directory.

---

**This contract is binding for the LTS period (until April 2031).**
Any changes require community discussion and a major version bump.
