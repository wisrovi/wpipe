"""
WPipe - Pipeline Orchestration Library.

A high-performance library for building and orchestrating data processing pipelines
with support for parallel execution, error handling, checkpoints, and more.

Example:
    >>> from wpipe import Pipeline, step
    >>> @step(name="process")
    ... def process_data(data):
    ...     return {"result": data["value"] * 2}
    >>> pipeline = Pipeline(pipeline_name="my_pipeline")
    >>> pipeline.set_steps([(process_data, "Process", "v1.0")])
    >>> result = pipeline.run({"value": 5})
"""

import sqlite3
import threading
from typing import Any, Dict

from wsqlite import WSQLite as Wsqlite_original

# Local imports
from .checkpoint import CheckpointManager
from .decorators import AutoRegister, StepRegistry, get_step_registry, step
from .export import PipelineExporter
from .log import new_logger
from .parallel import DAGScheduler, ExecutionMode, ParallelExecutor
from .pipe import Condition, For, Parallel, Pipeline
from .pipe.pipe_async import PipelineAsync
from .ram import memory
from .resource_monitor import ResourceMonitor, ResourceMonitorRegistry
from .sqlite import SQLite
from .sqlite import Wsqlite as WsqliteWrapper
from .timeout import TaskTimer, timeout_async, timeout_sync
from .timeout import TimeoutError as PipelineTimeoutError
from .tracking import Metric, PipelineTracker, Severity
from .type_hinting import GenericPipeline, PipelineContext, TypeValidator
from .util import (
    auto_dict_input,
    dict_to_sns,
    object_to_dict,
    to_obj,
)

# Connection pooling for performance optimization
_db_connections: Dict[str, sqlite3.Connection] = {}
_db_lock = threading.Lock()


def patched_get_connection(self) -> sqlite3.Connection:
    """Obtain a shared database connection to improve performance."""
    with _db_lock:
        # Get db_path from self, handling cases where it might not be directly accessible
        db_path = getattr(self, 'db_path', None)
        if db_path is None:
            # Fallback: try to get it from __dict__ or other attributes
            db_path = self.__dict__.get('db_path')
        if db_path is None:
            # Last resort: raise a meaningful error
            raise AttributeError(
                f"WSQLite object has no attribute 'db_path'. "
                f"Available attributes: {list(self.__dict__.keys())}"
            )

        if db_path not in _db_connections:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=-2000")
            _db_connections[db_path] = conn
        return _db_connections[db_path]


Wsqlite_original._get_connection = patched_get_connection


def patched_insert(self, data: Any) -> int:
    """Insert a new record and return the generated ID."""
    table_name = self.table_name
    if hasattr(data, "model_dump"):
        data_dict = data.model_dump()
    else:
        data_dict = data

    columns = [k for k, v in data_dict.items() if v is not None]
    placeholders = ["?" for _ in columns]
    values = [data_dict[k] for k in columns]

    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"

    conn = self._get_connection()
    with _db_lock:
        cursor = conn.cursor()
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e


Wsqlite_original.insert = patched_insert

# Alias for compatibility
Wsqlite = Wsqlite_original

__all__ = [
    "step",
    "to_obj",
    "auto_dict_input",
    "dict_to_sns",
    "object_to_dict",
    "AutoRegister",
    "StepRegistry",
    "get_step_registry",
    "ResourceMonitor",
    "ResourceMonitorRegistry",
    "CheckpointManager",
    "Condition",
    "For",
    "Parallel",
    "Pipeline",
    "PipelineAsync",
    "memory",
    "new_logger",
    "start_dashboard",
    "PipelineTracker",
    "Metric",
    "Severity",
    "Wsqlite",
    "WsqliteWrapper",
    "SQLite",
    "PipelineExporter",
    "TaskTimer",
    "PipelineTimeoutError",
    "timeout_async",
    "timeout_sync",
    "GenericPipeline",
    "PipelineContext",
    "TypeValidator",
]


def start_dashboard(db_path: str = "pipeline_tracking.db", port: int = 5000) -> None:
    """
    Start the pipeline tracking dashboard.

    Args:
        db_path: Path to the SQLite database file.
        port: Port number for the web server.

    Raises:
        ImportError: If the dashboard module is not available.
    """
    try:
        from wpipe.dashboard.main import start_dashboard as start_dash
        start_dash(db_path=db_path, port=port)
    except ImportError as exc:
        raise ImportError(
            "Dashboard module not available. "
            "Please ensure wpipe.dashboard.main is installed."
        ) from exc
