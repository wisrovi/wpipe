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

import wsqlite.core.connection as wconn

# Connection pooling for performance optimization
_db_connections: Dict[str, sqlite3.Connection] = {}
_db_lock = threading.RLock()

def patched_get_shared_connection(db_path: str) -> sqlite3.Connection:
    """Obtain a shared database connection to improve performance."""
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

# Redirect wsqlite's internal connection getter to our shared pool
wconn._get_connection = patched_get_shared_connection

# Also patch ConnectionPool to use our shared connection
from wsqlite.core.pool import ConnectionPool
ConnectionPool._create_connection = lambda self: patched_get_shared_connection(self.db_path)

def _patched_return(self, conn):
    """Patched return_connection that releases semaphore but avoids rollback."""
    try:
        if self._is_healthy(conn):
            try:
                self._pool.put_nowait(conn)
            except:
                pass
    finally:
        self._semaphore.release()

ConnectionPool.return_connection = _patched_return

def patched_insert(self, data: Any) -> Any:
    """Insert a new record and return the generated ID without committing immediately."""
    self._call_hook(data, "pre_save")
    
    data_dict = self._dump(data)
    # Filter out None values to allow SQLite autoincrement
    columns = [k for k, v in data_dict.items() if v is not None]
    placeholders = ["?" for _ in columns]
    values = [data_dict[k] for k in columns]

    query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"

    with _db_lock:
        conn = patched_get_shared_connection(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query, values)
            result = cursor.lastrowid
            self._call_hook(data, "post_save")
            return result
        except Exception as e:
            # Only rollback if we are in a transaction
            try:
                conn.rollback()
            except:
                pass
            raise e

Wsqlite_original.insert = patched_insert

@atexit.register
def _close_connections():
    """Cleanup connections and threads on exit."""
    with _db_lock:
        for path, conn in list(_db_connections.items()):
            try:
                # Force commit before closing if possible
                conn.commit()
                conn.close()
            except:
                pass
        _db_connections.clear()
    
    # Final attempt to silence lingering daemon threads in environments like Binder/Jupyter
    import threading
    for thread in threading.enumerate():
        if thread.daemon and thread is not threading.current_thread():
            if "_RefreshThread" in str(thread):
                try:
                    # Give it a very short window to finish or just ignore it
                    thread.join(timeout=0.01)
                except:
                    pass

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
