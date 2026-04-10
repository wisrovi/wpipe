from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from wsqlite import WSQLite


class LogGestorModel(BaseModel):
    """DTO for the records table in SQLite."""

    id: Optional[int] = Field(None, description="Primary Key")
    input: Optional[str] = Field(None, description="Input data as JSON string")
    output: Optional[str] = Field(None, description="Output data as JSON string")
    details: Optional[str] = Field(
        None, description="Additional details as JSON string"
    )
    datetime: Optional[str] = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


class LogGestor:
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
        self.db = WSQLite(LogGestorModel, db_name)

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
        input_data_json = str(input_data)
        record_id = self.db.insert(LogGestorModel(input=input_data_json))

        if record_id is not None:
            self.id = record_id

    def _update(self, output: dict, details: Optional[dict] = None) -> None:
        """Update the current record with output and details."""
        details = details or {}
        if self.id is not None:
            self.db.update(
                self.id,
                LogGestorModel(
                    id=self.id,
                    output=str(output),
                    details=str(details)
                )
            )

    def count_records(self) -> int:
        """Return the number of records in the database."""
        return self.db.count_records()

    def __enter__(self) -> "LogGestor":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager and update record."""
        self._update(output=self._output_db, details=self._details_db)
