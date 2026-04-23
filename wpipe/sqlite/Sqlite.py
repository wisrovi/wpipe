"""
SQLite database module for storing pipeline execution records.
"""

import json
import sqlite3
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Dict, Optional, Union

from wsqlite import WSQLite as WSQLiteBase

from .tables_dto.log_gestor_model import WsqliteModel
from .tables_dto.records import RecordModel


class PatchedWSQLite(WSQLiteBase):
    """
    Internal WSQLite with performance tuning.

    This class provides a thread-safe connection pool and optimizes
    SQLite performance using WAL mode and normal synchronous settings.
    """

    _db_connections: Dict[str, sqlite3.Connection] = {}
    _db_lock = threading.Lock()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Gets or creates a thread-safe SQLite connection.

        Returns:
            sqlite3.Connection: The SQLite connection object.
        """
        with self._db_lock:
            if self.db_path not in self._db_connections:
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                self._db_connections[self.db_path] = conn
            return self._db_connections[self.db_path]


class Wsqlite:
    """
    Simplified SQLite wrapper for pipeline records (LogGestor).

    Attributes:
        db_name (str): Name of the database file.
        record_uuid (str): Unique identifier for the current execution.
        db (PatchedWSQLite): The database interface.
    """

    def __init__(self, db_name: str = "register.db") -> None:
        """
        Initializes the Wsqlite instance.

        Args:
            db_name (str): Name of the database file. Defaults to "register.db".
        """
        self.db_name: str = db_name
        self._output_db: Dict[str, Any] = {}
        self._details_db: Dict[str, Any] = {}
        self._input_db: Dict[str, Any] = {}
        self._error_db: Dict[str, Any] = {}
        self._last_id: Optional[int] = None
        self.record_uuid: str = str(uuid.uuid4())
        self.db = PatchedWSQLite(WsqliteModel, db_name)

    @property
    def input(self) -> Dict[str, Any]:
        """Gets the input data dictionary."""
        return self._input_db

    @input.setter
    def input(self, value: Dict[str, Any]) -> None:
        """Sets the input data and saves state."""
        self._input_db = self._serialize_dict(value)
        self._save_state()

    @property
    def output(self) -> Dict[str, Any]:
        """Gets the output data dictionary."""
        return self._output_db

    @output.setter
    def output(self, value: Dict[str, Any]) -> None:
        """Sets the output data and saves state."""
        self._output_db = self._serialize_dict(value)
        self._save_state()

    @property
    def details(self) -> Dict[str, Any]:
        """Gets the details data dictionary."""
        return self._details_db

    @details.setter
    def details(self, value: Dict[str, Any]) -> None:
        """Sets the details data and saves state."""
        self._details_db = self._serialize_dict(value)
        self._save_state()

    @property
    def error(self) -> Dict[str, Any]:
        """Gets the error data dictionary."""
        return self._error_db

    @error.setter
    def error(self, value: Dict[str, Any]) -> None:
        """Sets the error data and saves state."""
        self._error_db = self._serialize_dict(value)
        self._save_state()

    def _serialize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts non-serializable objects to strings within a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary to serialize.

        Returns:
            Dict[str, Any]: The serialized dictionary.
        """
        try:
            import numpy as np  # pylint: disable=import-outside-toplevel
        except ImportError:
            np = None  # type: ignore

        def convert(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [convert(i) for i in obj]
            if np is not None and isinstance(obj, np.ndarray):
                return f"<np.array shape={obj.shape} dtype={obj.dtype}>"
            if hasattr(obj, "__dict__"):
                return f"<{obj.__class__.__name__}>"
            if obj is None or isinstance(obj, (str, int, float, bool)):
                return obj
            return str(obj)

        return convert(data)

    def _save_state(self) -> None:
        """
        Saves or updates the current state in the database.

        Uses an Upsert-like logic based on the object's memory of the last inserted ID.
        """
        model = WsqliteModel(
            input=json.dumps(self._input_db),
            output=json.dumps(self._output_db),
            details=json.dumps(self._details_db),
            error=json.dumps(self._error_db) if self._error_db else None,
        )

        table = self.db.table_name
        conn = self.db._get_connection()

        if self._last_id is None:
            # First time saving in this context, insert a new record.
            query = f"INSERT INTO {table} (input, output, details, error, datetime) VALUES (?, ?, ?, ?, ?)"
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
            # Update the existing record.
            query = f"UPDATE {table} SET input=?, output=?, details=?, error=? WHERE rowid=?"
            conn.execute(
                query, (model.input, model.output, model.details, model.error, self._last_id)
            )
            conn.commit()

    def count_records(self) -> int:
        """
        Counts the total number of records in the database.

        Returns:
            int: Total record count.
        """
        return len(self.db.get_all())

    def __enter__(self) -> "Wsqlite":
        """Context manager entry point."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit point, ensures state is saved."""
        self._save_state()


class SQLite:
    """
    SQLite database wrapper for storing pipeline records.

    Attributes:
        db_name (str): Name of the database file.
        executor (ThreadPoolExecutor): Executor for asynchronous operations.
        db (PatchedWSQLite): The database interface.
    """

    def __init__(self, db_name: str = "register.db") -> None:
        """
        Initializes the SQLite instance.

        Args:
            db_name (str): Name of the database file. Defaults to "register.db".
        """
        self.db_name = db_name
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.db = PatchedWSQLite(RecordModel, db_name)

    def write(
        self,
        input_data: Optional[Union[Dict[str, Any], str]] = None,
        output: Optional[Union[Dict[str, Any], str]] = None,
        details: Optional[Union[Dict[str, Any], str]] = None,
        record_id: Optional[int] = None,
    ) -> Optional[int]:
        """
        Writes or updates a record in the database.

        Args:
            input_data: Input data to store.
            output: Output data to store.
            details: Additional details to store.
            record_id: If provided, updates the record with this ID.

        Returns:
            Optional[int]: The ID of the written or updated record.
        """
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

    def read_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """
        Reads a record from the database by its ID.

        Args:
            record_id (int): The ID of the record to retrieve.

        Returns:
            Optional[Dict[str, Any]]: The record data if found, None otherwise.
        """
        table = self.db.table_name
        conn = self.db._get_connection()
        cursor = conn.execute(f"SELECT * FROM {table} WHERE rowid=?", (record_id,))
        row = cursor.fetchone()
        if row:
            # Simple manual mapping for compatibility
            return {
                "id": record_id,
                "input": row[1],
                "output": row[2],
                "details": row[3],
            }
        return None

    def count_records(self) -> int:
        """
        Counts the total number of records in the database.

        Returns:
            int: Total record count.
        """
        return len(self.db.get_all())

    def __enter__(self) -> "SQLite":
        """Context manager entry point."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit point, shuts down the executor."""
        if self.executor:
            self.executor.shutdown(wait=True)
