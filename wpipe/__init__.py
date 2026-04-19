import sqlite3
import threading
from wsqlite import WSQLite as Wsqlite_original


# --- OPTIMIZATION: CONNECTION POOLING AND WAL MODE ---
_db_connections = {}
_db_lock = threading.Lock()


def patched_get_connection(self):
    """Obtiene una conexión compartida a la base de datos para mejorar el rendimiento."""
    with _db_lock:
        if self.db_path not in _db_connections:
            # check_same_thread=False is safe because we use a lock for operations or assume SQLite serializable mode
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            # --- HIGH CONCURRENCY MODE ---
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size = -2000") 
            _db_connections[self.db_path] = conn
        return _db_connections[self.db_path]


# Apply connection monkeypatch
Wsqlite_original._get_connection = patched_get_connection


# Monkeypatch WSQLite to return lastrowid on insert
def patched_insert(self, data):
    """Inserta un nuevo registro y devuelve el ID generado."""
    table_name = self.table_name
    # data can be a dict or a pydantic model
    if hasattr(data, "model_dump"):
        data_dict = data.model_dump()
    else:
        data_dict = data

    # Remove None values to let SQLite handle defaults/autoincrement
    columns = [k for k, v in data_dict.items() if v is not None]
    placeholders = ["?" for _ in columns]
    values = [data_dict[k] for k in columns]

    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
    
    conn = self._get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e


# Apply insert monkeypatch
Wsqlite_original.insert = patched_insert


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
from .timeout import TaskTimer, TimeoutError, timeout_async, timeout_sync
from .tracking import PipelineTracker
from .util import (
    auto_dict_input,
    dict_to_sns,
    object_to_dict,
    state,
    to_obj,
)
from .type_hinting import GenericPipeline, PipelineContext, TypeValidator
from .tracking import Metric, PipelineTracker, Severity

# Alias para compatibilidad
Wsqlite = Wsqlite_original

__all__ = [
    # Decorators
    "step",
    "state",
    "to_obj",
    "auto_dict_input",
    "dict_to_sns",
    "object_to_dict",
    "AutoRegister",
    "StepRegistry",
    "get_step_registry",
    # Resource Monitoring
    "ResourceMonitor",
    "ResourceMonitorRegistry",
    "CheckpointManager",
    # Core Pipeline
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
    "TimeoutError",
    "timeout_async",
    "timeout_sync",
    "GenericPipeline",
    "PipelineContext",
    "TypeValidator",
]


def start_dashboard(db_path: str = "pipeline_tracking.db", port: int = 5000):
    """
    Start the pipeline tracking dashboard.
    """
    from wpipe.dashboard.app import run_dashboard

    run_dashboard(db_path, port)
