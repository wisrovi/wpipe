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
            # Enable WAL mode for high concurrency performance
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            _db_connections[self.db_path] = conn
        return _db_connections[self.db_path]


# Apply connection monkeypatch
Wsqlite_original._get_connection = patched_get_connection


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

    conn = self._get_connection()
    with _db_lock:
        cursor = conn.execute(query, values)
        conn.commit()
        return cursor.lastrowid


Wsqlite_original.insert = patched_insert


# Also need to patch update, delete, etc. to use the lock if we share the connection
def patched_update(self, record_id, data):
    """Actualiza un registro en la base de datos."""
    dump = data.model_dump()
    fields = ", ".join(f"{key} = ?" for key in dump.keys())
    values = tuple(dump.values()) + (record_id,)

    query = f"UPDATE {self.table_name} SET {fields} WHERE id = ?"

    conn = self._get_connection()
    with _db_lock:
        conn.execute(query, values)
        conn.commit()


def patched_delete(self, record_id):
    """Elimina un registro de la base de datos."""
    query = f"DELETE FROM {self.table_name} WHERE id = ?"

    conn = self._get_connection()
    with _db_lock:
        conn.execute(query, (record_id,))
        conn.commit()


def patched_get_by_field(self, **filters):
    """Obtiene registros filtrando por cualquier campo."""
    if not filters:
        return self.get_all()

    conditions = " AND ".join(f"{key} = ?" for key in filters.keys())
    values = tuple(filters.values())

    query = f"SELECT * FROM {self.table_name} WHERE {conditions}"

    conn = self._get_connection()
    with _db_lock:
        cursor = conn.execute(query, values)
        rows = cursor.fetchall()

    return [
        self.model(
            **{
                key: (value if value is not None else self._default_value(key))
                for key, value in zip(self.model.model_fields.keys(), row)
            }
        )
        for row in rows
    ]


def patched_get_all(self):
    """Obtiene todos los registros de la tabla."""
    query = f"SELECT * FROM {self.table_name}"

    conn = self._get_connection()
    with _db_lock:
        cursor = conn.execute(query)
        rows = cursor.fetchall()

    return [
        self.model(
            **{
                key: (value if value is not None else self._default_value(key))
                for key, value in zip(self.model.model_fields.keys(), row)
            }
        )
        for row in rows
    ]


def patched_create_table_if_not_exists(self):
    """Crea la tabla en SQLite si no existe."""
    fields = ", ".join(
        f"{field} {self._get_sql_type(typ)}"
        for field, typ in self.model.model_fields.items()
    )
    query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({fields})"

    conn = self._get_connection()
    with _db_lock:
        conn.execute(query)
        conn.commit()


def patched_sync_table_with_model(self):
    """Sincroniza la tabla con el modelo Pydantic."""
    conn = self._get_connection()
    with _db_lock:
        cursor = conn.execute(f"PRAGMA table_info({self.table_name})")
        existing_columns = {row[1] for row in cursor.fetchall()}

    model_fields = set(self.model.model_fields.keys())
    new_fields = model_fields - existing_columns

    if new_fields:
        with _db_lock:
            for field in new_fields:
                field_type = self._get_sql_type(self.model.model_fields[field])
                alter_query = f"ALTER TABLE {self.table_name} ADD COLUMN {field} {field_type} DEFAULT NULL"
                conn.execute(alter_query)
            conn.commit()


# Apply other monkeypatches for thread safety with shared connection
Wsqlite_original.update = patched_update
Wsqlite_original.delete = patched_delete
Wsqlite_original.get_by_field = patched_get_by_field
Wsqlite_original.get_all = patched_get_all
Wsqlite_original._create_table_if_not_exists = patched_create_table_if_not_exists
Wsqlite_original._sync_table_with_model = patched_sync_table_with_model


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


__version__ = "1.5.6"


"""
wpipe - A Python library for creating and executing pipelines with task orchestration.
...
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


def __getattr__(name):
    if name == "start_dashboard":
        from .dashboard import start_dashboard

        return start_dashboard
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


from .decorators import AutoRegister, StepRegistry, get_step_registry, step
from .export import PipelineExporter
from .log import new_logger
<<<<<<< HEAD
from .pipe import Condition, Pipeline, PipelineAsync
=======
from .parallel import DAGScheduler, ExecutionMode, ParallelExecutor
from .pipe import Condition, For, Pipeline
from .pipe.pipe_async import PipelineAsync
>>>>>>> DEV-WSRV/changes_for_future_LTS_v1.5
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
<<<<<<< HEAD
    "Wsqlite",
=======
>>>>>>> DEV-WSRV/changes_for_future_LTS_v1.5
    "memory",
    "new_logger",
    "start_dashboard",
    "PipelineTracker",
    "Metric",
    "Severity",
    "Wsqlite",
]
