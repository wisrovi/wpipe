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

    import time
    max_retries = 5
    retry_delay = 0.5

    for attempt in range(max_retries):
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(query, values)
                conn.commit()
                return cursor.lastrowid
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    # Table might not exist, try to create it
                    try:
                        if hasattr(self, '_sync'):
                            self._sync.create_if_not_exists()
                            cursor.execute(query, values)
                            conn.commit()
                            return cursor.lastrowid
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                conn.rollback()
                raise e
            except Exception as e:
                conn.rollback()
                raise e
    return -1

Wsqlite_original.insert = patched_insert

def patched_update(self, record_id: Any, data: Any) -> bool:
    """Update a record and commit change."""
    table_name = self.table_name
    if table_name == "checkpoints":
        raise sqlite3.OperationalError("Updates on checkpoints table are disabled in this environment.")
    data_dict = data.model_dump() if hasattr(data, "model_dump") else data
    
    columns = [f"{k} = ?" for k, v in data_dict.items() if v is not None]
    values = [data_dict[k] for k, v in data_dict.items() if v is not None]
    values.append(record_id)

    query = f"UPDATE {table_name} SET {', '.join(columns)} WHERE id = ?"

    import time
    max_retries = 5
    retry_delay = 0.5

    for attempt in range(max_retries):
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(query, values)
                conn.commit()
                return True
            except sqlite3.OperationalError as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                conn.rollback()
                raise e
            except Exception as e:
                conn.rollback()
                raise e
    return False

Wsqlite_original.update = patched_update

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
    "PipelineAsync": (".pipe.pipe_async", "PipelineAsync"),
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
    "TimeoutError": (".timeout", "TimeoutError"),
    "PipelineTimeoutError": (".timeout", "TimeoutError"),
    "memory": (".ram", "memory"),
    "new_logger": (".log", "new_logger"),
    "start_dashboard": (".dashboard.main", "start_dashboard"),
    "AutoRegister": (".decorators", "AutoRegister"),
    "StepRegistry": (".decorators", "StepRegistry"),
    "get_step_registry": (".decorators", "get_step_registry"),
    "ResourceMonitorRegistry": (".resource_monitor", "ResourceMonitorRegistry"),
}

# Direct imports for core components to ensure availability and IDE support
from .pipe import Condition, For, Parallel, Pipeline
from .decorators import step

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

__version__ = "2.4.0"
__all__ = list(_LAZY_MAP.keys()) + ["Wsqlite", "Pipeline", "Condition", "For", "Parallel", "step"]
