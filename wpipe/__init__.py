"""
WPipe - Pipeline Orchestration Library.

A high-performance library for building and orchestrating data processing pipelines
with support for parallel execution, error handling, checkpoints, and more.
"""

import sqlite3
import threading
import atexit
from typing import Any, Dict

from wsqlite import WSQLite as Wsqlite_original

# Connection pooling for performance optimization
_db_connections: Dict[str, sqlite3.Connection] = {}
_db_lock = threading.RLock()

def patched_get_connection(self) -> sqlite3.Connection:
    """Obtain a shared database connection to improve performance."""
    db_path = getattr(self, 'db_path', None) or self.__dict__.get('db_path')
    if db_path is None:
        raise AttributeError(f"WSQLite object has no attribute 'db_path'.")

    with _db_lock:
        if db_path in _db_connections:
            try:
                _db_connections[db_path].execute("SELECT 1")
            except:
                _db_connections.pop(db_path, None)

        if db_path not in _db_connections:
            conn = sqlite3.connect(db_path, check_same_thread=False, timeout=60.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=OFF")
            conn.execute("PRAGMA cache_size=-10000")
            conn.execute("PRAGMA busy_timeout=60000")
            _db_connections[db_path] = conn
    return _db_connections[db_path]

Wsqlite_original._get_connection = patched_get_connection

def patched_insert(self, data: Any) -> int:
    """Insert a new record and return the generated ID."""
    table_name = self.table_name
    data_dict = data.model_dump() if hasattr(data, "model_dump") else data
    
    columns = [k for k, v in data_dict.items() if v is not None]
    placeholders = ["?" for _ in columns]
    values = [data_dict[k] for k in columns]

    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"

    with _db_lock:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, values)
            # Commit removed for performance. Final commit will be handled by Pipeline.
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e

Wsqlite_original.insert = patched_insert

@atexit.register
def _close_connections():
    with _db_lock:
        for path, conn in list(_db_connections.items()):
            try:
                conn.close()
            except:
                pass
        _db_connections.clear()

# Lazy loading map
_LAZY_MAP = {
    "Pipeline": (".pipe", "Pipeline"),
    "PipelineAsync": (".pipe.pipe_async", "PipelineAsync"),
    "Condition": (".pipe", "Condition"),
    "For": (".pipe", "For"),
    "Parallel": (".pipe", "Parallel"),
    "step": (".decorators", "step"),
    "ResourceMonitor": (".resource_monitor", "ResourceMonitor"),
    "TaskTimer": (".timeout", "TaskTimer"),
    "auto_dict_input": (".util", "auto_dict_input"),
    "object_to_dict": (".util", "object_to_dict"),
    "to_obj": (".util", "to_obj"),
    "dict_to_sns": (".util", "dict_to_sns"),
    "Metric": (".tracking", "Metric"),
    "Severity": (".tracking", "Severity"),
    "PipelineTracker": (".tracking", "PipelineTracker"),
    "CheckpointManager": (".checkpoint", "CheckpointManager"),
    "PipelineExporter": (".export", "PipelineExporter"),
    "PipelineContext": (".type_hinting", "PipelineContext"),
    "GenericPipeline": (".type_hinting", "GenericPipeline"),
    "TypeValidator": (".type_hinting", "TypeValidator"),
    "WsqliteWrapper": (".sqlite", "Wsqlite"),
    "SQLite": (".sqlite", "SQLite"),
    "timeout_sync": (".timeout", "timeout_sync"),
    "timeout_async": (".timeout", "timeout_async"),
    "PipelineTimeoutError": (".timeout", "TimeoutError"),
    "memory": (".ram", "memory"),
    "new_logger": (".log", "new_logger"),
    "start_dashboard": (".dashboard.main", "start_dashboard"),
    "AutoRegister": (".decorators", "AutoRegister"),
    "StepRegistry": (".decorators", "StepRegistry"),
    "get_step_registry": (".decorators", "get_step_registry"),
    "ResourceMonitorRegistry": (".resource_monitor", "ResourceMonitorRegistry"),
}

def __getattr__(name: str) -> Any:
    """Handle lazy loading of modules."""
    if name == "Wsqlite":
        return Wsqlite_original
    
    if name in _LAZY_MAP:
        module_path, attr_name = _LAZY_MAP[name]
        import importlib
        module = importlib.import_module(module_path, __package__)
        attr = getattr(module, attr_name)
        globals()[name] = attr
        return attr
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = list(_LAZY_MAP.keys()) + ["Wsqlite"]
