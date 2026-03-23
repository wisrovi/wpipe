"""
SQLite wrapper module for simplified database operations.
"""

from typing import Optional

from wpipe.sqlite.Sqlite import SQLite


class Wsqlite:
    """Simplified SQLite wrapper for pipeline records."""

    id: Optional[str] = None

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
        self._sqlite = SQLite(db_name)

    @property
    def input(self) -> dict:
        """Get input data."""
        return self._input_db

    @input.setter
    def input(self, value: dict) -> None:
        """Set input data and create a new record."""
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
        record_id = None
        with SQLite(self.db_name) as connection_db:
            record_id = connection_db.write(input_data=input_data)

        if record_id is not None:
            self.id = str(record_id)

    def _update(self, output: dict, details: Optional[dict] = None) -> None:
        """Update the current record with output and details."""
        details = details or {}
        if self.id is not None:
            with SQLite(self.db_name) as connection_db:
                connection_db.async_write(
                    output=output, details=details, record_id=int(self.id)
                )

    def count_records(self) -> int:
        """Return the number of records in the database."""
        return self._sqlite.count_records()

    def __enter__(self) -> "Wsqlite":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager and update record."""
        self._update(output=self._output_db, details=self._details_db)
