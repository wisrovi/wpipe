"""
SQLite database module for storing pipeline execution records.
"""

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional, Union

import pandas as pd
from pydantic import BaseModel, Field
from wsqlite import WSQLite

from .tables_dto.log_gestor_model import WsqliteModel
from .tables_dto.records import RecordModel


class Wsqlite:
    """Simplified SQLite wrapper for pipeline records."""

    id: Optional[int] = None

    def __init__(self, db_name: str = "register.db") -> None:
        """
        Initialize Wsqlite wrapper.

        Args:
            db_name: Path to the SQLite database file.
        """
        self.db_name = db_name
        self._output_db: dict = {}
        self._details_db: dict = {}
        self._input_db: dict = {}
        self.db = WSQLite(WsqliteModel, db_name)

    @property
    def input(self) -> dict:
        """Get input data."""
        return self._input_db

    @input.setter
    def input(self, value: dict) -> None:
        """Set input data and create a new record."""
        self._input_db = value
        self._create(input_data=value)

    @property
    def output(self) -> dict:
        """Get output data."""
        return self._output_db

    @output.setter
    def output(self, value: dict) -> None:
        """Set output data."""
        self._output_db = value

    @property
    def details(self) -> dict:
        """Get details data."""
        return self._details_db

    @details.setter
    def details(self, value: dict) -> None:
        """Set details data."""
        self._details_db = value

    def _create(self, input_data: dict) -> None:
        """Create a new record with input data."""
        import json

        input_data_json = json.dumps(input_data)

        dto_to_insert = WsqliteModel(input=input_data_json)

        record_id = self.db.insert(dto_to_insert)

        if record_id is not None:
            self.id = record_id

    def _update(self, output: dict, details: Optional[dict] = None) -> None:
        """Update the current record with output and details."""
        import json

        details = details or {}
        if self.id is not None:
            self.db.update(
                self.id,
                WsqliteModel(
                    id=self.id,
                    input=json.dumps(self._input_db),
                    output=json.dumps(output),
                    details=json.dumps(details),
                ),
            )

    def count_records(self) -> int:
        """Return the number of records in the database."""
        return self.db.count_records()

    def __enter__(self) -> "Wsqlite":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager and update record."""
        self._update(output=self._output_db, details=self._details_db)


class SQLite:
    """SQLite database wrapper for storing pipeline records using WSQLite."""

    def __init__(self, db_name: str = "register.db") -> None:
        """
        Initialize SQLite database.

        Args:
            db_name: Path to the SQLite database file.
        """
        self.db_name = db_name
        self.executor = ThreadPoolExecutor(max_workers=10)
        if db_name:
            self.db = WSQLite(RecordModel, db_name)
        else:
            self.db = None

    def async_write(
        self,
        input_data: Optional[Union[str, dict]] = None,
        output: Optional[Union[str, dict]] = None,
        details: Optional[Union[str, dict]] = None,
        record_id: Optional[int] = None,
    ) -> None:
        """
        Asynchronously write a record to the database.
        """
        self.executor.submit(self.write, input_data, output, details, record_id)

    def write(
        self,
        input_data: Optional[Union[str, dict]] = None,
        output: Optional[Union[str, dict]] = None,
        details: Optional[Union[str, dict]] = None,
        record_id: Optional[int] = None,
    ) -> Optional[int]:
        """
        Write a record to the database.
        """
        # Convert dicts to JSON strings for storage
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

        model_data = RecordModel(
            id=record_id, input=input_str, output=output_str, details=details_str
        )

        if record_id:
            self.db.update(record_id, model_data)
            return record_id
        else:
            return self.db.insert(model_data)

    def read_by_id(self, record_id: int) -> Optional[RecordModel]:
        """Read a record by ID."""
        results = self.db.get_by_field(id=record_id)
        return results[0] if results else None

    def export_to_dataframe(
        self, save_csv: bool = False, csv_name: str = "records.csv"
    ) -> pd.DataFrame:
        """Export records to a pandas DataFrame."""
        records = self.db.get_all()
        df = pd.DataFrame([r.model_dump() for r in records])

        if save_csv and not df.empty:
            df.to_csv(csv_name, index=False)

        return df

    def get_records_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days: Optional[int] = None,
    ) -> list:
        """
        Get records within a date range.
        Note: WSQLite doesn't support complex range queries yet,
        so we fetch all and filter or use raw SQL if necessary.
        """
        from datetime import datetime, timedelta

        all_records = self.db.get_all()

        if days is not None:
            limit = datetime.now() - timedelta(days=days)
            return [
                r
                for r in all_records
                if datetime.strptime(r.datetime, "%Y-%m-%d %H:%M:%S") >= limit
            ]

        if start_date and end_date:
            s = datetime.fromisoformat(start_date)
            e = datetime.fromisoformat(end_date)
            return [
                r
                for r in all_records
                if s <= datetime.strptime(r.datetime, "%Y-%m-%d %H:%M:%S") <= e
            ]

        return all_records

    def count_records(self) -> int:
        """Count the total number of records."""
        return len(self.db.get_all())

    def update_record(
        self,
        record_id: int,
        output: Optional[Union[str, dict]] = None,
        details: Optional[Union[str, dict]] = None,
    ) -> None:
        """Update a record by ID."""
        current = self.read_by_id(record_id)
        if not current:
            return

        if output:
            current.output = json.dumps(output) if isinstance(output, dict) else output
        if details:
            current.details = (
                json.dumps(details) if isinstance(details, dict) else details
            )

        self.db.update(record_id, current)

    def delete_by_id(self, record_id: int) -> None:
        """Delete a record by ID."""
        self.db.delete(record_id)

    def check_table_exists(self) -> bool:
        """Check if database is accessible."""
        if not self.db_name:
            return False
        return self.db is not None

    def __enter__(self) -> "SQLite":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.executor:
            self.executor.shutdown(wait=True)
