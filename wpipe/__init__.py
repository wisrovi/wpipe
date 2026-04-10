"""
wpipe - A Python library for creating and executing pipelines with task orchestration.

Phase 1 Features (Core Reliability & Observability):
- Checkpointing & Resume: Save and resume from checkpoints
- Timeouts: Prevent hanging tasks with timeout support
- Type Hinting: Runtime type validation for pipeline context
- Resource Monitoring: Track RAM and CPU during execution
- Export: Export logs, metrics, and statistics to JSON/CSV

Phase 2 Features (Parallelism & Composition):
- Parallel Execution: Execute steps in parallel (I/O or CPU bound)
- Pipeline Composition: Use pipelines as steps in other pipelines
- Step Decorators: Define steps inline with @step decorator
"""

from .api_client import APIClient
from .checkpoint import CheckpointManager
from .composition import CompositionHelper, NestedPipelineStep, PipelineAsStep
from .dashboard import start_dashboard
from .decorators import AutoRegister, StepRegistry, get_step_registry, step
from .export import PipelineExporter
from .log import new_logger
from .parallel import DAGScheduler, ExecutionMode, ParallelExecutor
from .pipe import Condition, For, Pipeline, PipelineAsync
from .ram import memory
from .resource_monitor import ResourceMonitor, ResourceMonitorRegistry
from .sqlite import Wsqlite
from .timeout import TaskTimer, TimeoutError, timeout_async, timeout_sync
from .tracking import Metric, PipelineTracker, Severity
from .type_hinting import GenericPipeline, PipelineContext, TypeValidator
from .util import auto_dict_input, object_to_dict, state, to_obj

__all__ = [
    # Phase 1 - Reliability
    "APIClient",
    "CheckpointManager",
    "PipelineExporter",
    "ResourceMonitor",
    "ResourceMonitorRegistry",
    "TaskTimer",
    "TimeoutError",
    "PipelineContext",
    "TypeValidator",
    "GenericPipeline",
    "timeout_async",
    "timeout_sync",
    # Phase 2 - Parallelism & Composition
    "ParallelExecutor",
    "ExecutionMode",
    "DAGScheduler",
    "PipelineAsStep",
    "CompositionHelper",
    "NestedPipelineStep",
    "step",
    "StepRegistry",
    "AutoRegister",
    "get_step_registry",
    # Transform decorators
    "to_obj",
    "auto_dict_input",
    "state",
    "object_to_dict",
    # Core Pipeline
    "Condition",
    "For",
    "Pipeline",
    "PipelineAsync",
    "Wsqlite",
    "memory",
    "new_logger",
    "start_dashboard",
    "PipelineTracker",
]
