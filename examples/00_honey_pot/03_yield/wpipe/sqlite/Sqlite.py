"""
SQLite database module for storing pipeline execution records.
"""

import json
import sqlite3
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional

from wsqlite import WSQLite as WSQLiteBase

from .tables_dto.log_gestor_model import WsqliteModel
from .tables_dto.records import RecordModel


class PatchedWSQLite(WSQLiteBase):
    """Internal WSQLite with performance tuning."""

    _db_connections = {}
    _db_lock = threading.Lock()

    def _get_connection(self):
        with self._db_lock:
            if self.db_path not in self._db_connections:
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                self._db_connections[self.db_path] = conn
            return self._db_connections[self.db_path]


class Wsqlite:
    """Simplified SQLite wrapper for pipeline records (LogGestor)."""

    def __init__(self, db_name: str = "register.db") -> None:
        self.db_name = db_name
        self._output_db: dict = {}
        self._details_db: dict = {}
        self._input_db: dict = {}
        self._error_db: dict = {}
        self.record_uuid = str(uuid.uuid4())  # Identificador único para esta ejecución
        self.db = PatchedWSQLite(WsqliteModel, db_name)

    @property
    def input(self) -> dict:
        return self._input_db

    @input.setter
    def input(self, value: dict) -> None:
        self._input_db = self._serialize_dict(value)
        self._save_state()

    @property
    def output(self) -> dict:
        return self._output_db

    @output.setter
    def output(self, value: dict) -> None:
        self._output_db = self._serialize_dict(value)
        self._save_state()

    @property
    def details(self) -> dict:
        return self._details_db

    @details.setter
    def details(self, value: dict) -> None:
        self._details_db = self._serialize_dict(value)
        self._save_state()

    def _serialize_dict(self, data: dict) -> dict:
        """Convierte objetos no serializables a strings."""
        import numpy as np

        def convert(obj):
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert(i) for i in obj]
            elif isinstance(obj, np.ndarray):
                return f"<np.array shape={obj.shape} dtype={obj.dtype}>"
            elif hasattr(obj, '__dict__'):
                return f"<{obj.__class__.__name__}>"
            elif obj is None or isinstance(obj, (str, int, float, bool)):
                return obj
            else:
                return str(obj)

        return convert(data)

    def _save_state(self) -> None:
        """Guarda o actualiza el estado actual en la base de datos."""
        # Buscamos si ya existe por datetime o similar, o simplemente insertamos/actualizamos
        # Para el LogGestor, lo más robusto es usar el UUID como identificador en el campo ID (si es string)
        # o manejar una fila única por contexto de 'with'.

        model = WsqliteModel(
            input=json.dumps(self._input_db),
            output=json.dumps(self._output_db),
            details=json.dumps(self._details_db),
            error=json.dumps(self._error_db) if self._error_db else None,
        )

        # Como WSQLite no devuelve ID fiable en todas las versiones,
        # usamos una lógica de 'Upsert' basada en la memoria del objeto.
        existing = self.db.get_all()
        # Si es la primera vez que guardamos algo en este 'with', insertamos.
        # En LogGestor, solemos tener un registro por 'with'.
        if not hasattr(self, "_last_id") or self._last_id is None:
            # Simulamos el insert con SQL puro a través del motor parcheado para recuperar el ID
            table = self.db.table_name
            query = f"INSERT INTO {table} (input, output, details, error, datetime) VALUES (?, ?, ?, ?, ?)"
            conn = self.db._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    model.input,
                    model.output,
                    model.details,
                    model.error,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            conn.commit()
            self._last_id = cursor.lastrowid
        else:
            # Actualizamos la fila que acabamos de crear
            table = self.db.table_name
            query = f"UPDATE {table} SET input=?, output=?, details=?, error=? WHERE rowid=?"
            conn = self.db._get_connection()
            conn.execute(
                query, (model.input, model.output, model.details, model.error, self._last_id)
            )
            conn.commit()

    @property
    def error(self) -> dict:
        return self._error_db

    @error.setter
    def error(self, value: dict) -> None:
        self._error_db = self._serialize_dict(value)
        self._save_state()

    def count_records(self) -> int:
        return len(self.db.get_all())

    def __enter__(self) -> "Wsqlite":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._save_state()


class SQLite:
    """SQLite database wrapper for storing pipeline records."""

    def __init__(self, db_name: str = "register.db") -> None:
        self.db_name = db_name
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.db = PatchedWSQLite(RecordModel, db_name)

    def write(
        self, input_data=None, output=None, details=None, record_id=None
    ) -> Optional[int]:
        input_str = (
            json.dumps(input_data) if isinstance(input_data, dict) else input_data
        )
        if isinstance(output, dict):
            output_str = json.dumps(output)
        elif isinstance(output, str):
            output_str = json.dumps({"output": output})
        else:
            output_str = None
        details_str = json.dumps(details) if isinstance(details, dict) else details

        table = self.db.table_name
        conn = self.db._get_connection()
        if record_id:
            query = f"UPDATE {table} SET input=?, output=?, details=? WHERE rowid=?"
            conn.execute(query, (input_str, output_str, details_str, record_id))
            conn.commit()
            return record_id
        else:
            query = f"INSERT INTO {table} (input, output, details, datetime) VALUES (?, ?, ?, ?)"
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    input_str,
                    output_str,
                    details_str,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def read_by_id(self, record_id: int) -> Optional[dict]:
        table = self.db.table_name
        conn = self.db._get_connection()
        cursor = conn.execute(f"SELECT * FROM {table} WHERE rowid=?", (record_id,))
        row = cursor.fetchone()
        if row:
            # Mapeo manual simple para compatibilidad
            return {
                "id": record_id,
                "input": row[1],
                "output": row[2],
                "details": row[3],
            }
        return None

    def count_records(self) -> int:
        return len(self.db.get_all())

    def __enter__(self) -> "SQLite":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.executor:
            self.executor.shutdown(wait=True)
