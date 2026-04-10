import sqlite3

from wsqlite import WSQLite as Wsqlite_original


# Monkeypatch WSQLite to return lastrowid on insert
def patched_insert(self, data):
    """Inserta un nuevo registro y devuelve el ID generado."""
    # Omitimos el campo 'id' si es None para que SQLite genere uno automáticamente
    dump = data.model_dump()
    if dump.get("id") is None:
        dump.pop("id", None)

    fields = ", ".join(dump.keys())
    placeholders = ", ".join(["?" for _ in dump])
    values = tuple(dump.values())
    query = f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
    with self._get_connection() as conn:
        cursor = conn.execute(query, values)
        conn.commit()
        return cursor.lastrowid


Wsqlite_original.insert = patched_insert


def patched_get_sql_type(self, field):
    """Convierte tipos de Pydantic a tipos de SQLite con soporte para restricciones y Optional."""
    from typing import Union, get_args, get_origin

    annotation = field.annotation
    # Handle Optional/Union types
    if get_origin(annotation) is Union:
        args = get_args(annotation)
        # Pick the first non-None type
        for arg in args:
            if arg is not type(None):
                annotation = arg
                break

    type_mapping = {int: "INTEGER", str: "TEXT", bool: "BOOLEAN", float: "REAL"}
    sql_type = type_mapping.get(annotation, "TEXT")

    constraints = []
    description = (field.description or "").lower()
    if "primary" in description:
        constraints.append("PRIMARY KEY")
        if annotation is int:
            constraints.append("AUTOINCREMENT")
    if "unique" in description:
        constraints.append("UNIQUE")
    if "not null" in description:
        constraints.append("NOT NULL")

    return f"{sql_type} {' '.join(constraints)}".strip()


Wsqlite_original._get_sql_type = patched_get_sql_type


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
from .sqlite.sqlite_logs import LogGestor, LogGestorModel
from .sqlite import Wsqlite
from .timeout import TaskTimer, TimeoutError, timeout_async, timeout_sync
from .tracking import PipelineTracker
from .type_hinting import GenericPipeline, PipelineContext, TypeValidator
from .util import auto_dict_input, object_to_dict, state, to_obj

SQLiteLogs = LogGestor

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
    # SQLite logging
    "LogGestorModel",
    "LogGestor",
    "SQLiteLogs",
]
