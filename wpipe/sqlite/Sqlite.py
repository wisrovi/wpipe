"""
SQLite database module for storing pipeline execution records.
"""

import json
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional, Union

import pandas as pd


class SQLite:
    """SQLite database wrapper for storing pipeline records."""

    def __init__(self, db_name: str = "register.db") -> None:
        """
        Initialize SQLite database.

        Args:
            db_name: Path to the SQLite database file.
        """
        self.db_name = db_name
        self._create_table_if_not_exists()
        self.executor = ThreadPoolExecutor(max_workers=10)

    def _create_table_if_not_exists(self) -> None:
        """Create the records table if it doesn't exist."""
        if not self.db_name:
            return

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS records
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 input TEXT,
                 output TEXT,
                 details TEXT DEFAULT NULL,
                 datetime TEXT DEFAULT CURRENT_TIMESTAMP)""")

    def async_write(
        self,
        input_data: Optional[Union[str, dict]] = None,
        output: Optional[Union[str, dict]] = None,
        details: Optional[Union[str, dict]] = None,
        record_id: Optional[int] = None,
    ) -> None:
        """
        Asynchronously write a record to the database.

        Args:
            input_data: Input data to store.
            output: Output data to store.
            details: Additional details to store.
            record_id: Optional ID for updating existing record.
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

        Args:
            input_data: Input data to store.
            output: Output data to store.
            details: Additional details to store.
            record_id: Optional ID for updating existing record.

        Returns:
            Record ID or None if write failed.
        """
        if not self.check_table_exists():
            return None

        if isinstance(input_data, dict):
            input_data = json.dumps(input_data)

        if isinstance(output, dict):
            output["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output = json.dumps(output)
        elif isinstance(output, str):
            output = json.dumps(
                {
                    "output": output,
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        if isinstance(details, dict):
            details = json.dumps(details)

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            if not record_id:
                cursor.execute(
                    "INSERT INTO records (input, output, details) VALUES (?, ?, ?)",
                    (input_data, output, details),
                )
                record_id = cursor.lastrowid
            else:
                if not self.read_by_id(record_id):
                    return None

                if not input_data and not details and output:
                    cursor.execute(
                        "UPDATE records SET output = ? WHERE id = ?",
                        (output, record_id),
                    )
                elif not input_data and output and details:
                    cursor.execute(
                        "UPDATE records SET output = ?, details = ? WHERE id = ?",
                        (output, details, record_id),
                    )
                elif input_data and output and details:
                    cursor.execute(
                        "UPDATE records SET input = ?, output = ?, "
                        "details = ? WHERE id = ?",
                        (input_data, output, details, record_id),
                    )
                elif input_data and output and not details:
                    cursor.execute(
                        "UPDATE records SET input = ?, output = ? WHERE id = ?",
                        (input_data, output, record_id),
                    )
            conn.commit()

        return record_id

    def read_by_id(self, record_id: int) -> list:
        """
        Read a record by ID.

        Args:
            record_id: The record ID to fetch.

        Returns:
            List of records (usually 0 or 1).
        """
        if not self.check_table_exists():
            return []

        results = []

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
            results = cursor.fetchall()

        return results

    def _view_records(self) -> pd.DataFrame:
        """
        Internal method to view all records.

        Returns:
            DataFrame with all records.
        """
        with sqlite3.connect(self.db_name) as conn:
            return pd.read_sql_query("SELECT * FROM records", conn)

    def export_to_dataframe(
        self, save_csv: bool = False, csv_name: str = "records.csv"
    ) -> pd.DataFrame:
        """
        Export records to a pandas DataFrame.

        Args:
            save_csv: Whether to save to CSV file.
            csv_name: Path for CSV output.

        Returns:
            DataFrame containing the records.
        """
        if not self.check_table_exists():
            return pd.DataFrame()

        df = self._view_records()

        if save_csv:
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

        Args:
            start_date: Start date in ISO format.
            end_date: End date in ISO format.
            days: If provided, get records from the last N days.

        Returns:
            List of records within the date range.
        """
        if not self.check_table_exists():
            return []

        from datetime import datetime, timedelta

        if days is not None:
            end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            start_date = (datetime.now() - timedelta(days=days)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        if start_date is None or end_date is None:
            return []

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM records WHERE datetime BETWEEN ? AND ?",
                (start_date, end_date),
            )
            return cursor.fetchall()

    def count_records(self) -> int:
        """
        Count the total number of records.

        Returns:
            Total number of records.
        """
        if not self.check_table_exists():
            return 0

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM records")
            return cursor.fetchone()[0]

    def update_record(
        self,
        record_id: int,
        output: Optional[Union[str, dict]] = None,
        details: Optional[Union[str, dict]] = None,
    ) -> None:
        """
        Update a record by ID.

        Args:
            record_id: The record ID to update.
            output: Output data to update.
            details: Details data to update.
        """
        if not self.check_table_exists():
            return

        output_json = json.dumps(output) if output else None
        details_json = json.dumps(details) if details else None

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if output_json and details_json:
                cursor.execute(
                    "UPDATE records SET output = ?, details = ? WHERE id = ?",
                    (output_json, details_json, record_id),
                )
            elif output_json:
                cursor.execute(
                    "UPDATE records SET output = ? WHERE id = ?",
                    (output_json, record_id),
                )
            elif details_json:
                cursor.execute(
                    "UPDATE records SET details = ? WHERE id = ?",
                    (details_json, record_id),
                )
            conn.commit()

    def delete_by_id(self, record_id: int) -> None:
        """
        Delete a record by ID.

        Args:
            record_id: The record ID to delete.
        """
        if not self.check_table_exists():
            return

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
            conn.commit()

    def check_table_exists(self) -> bool:
        """
        Check if the table exists and is accessible.

        Returns:
            True if table exists, False otherwise.
        """
        if not self.db_name:
            return False

        if os.path.dirname(self.db_name):
            if not os.path.exists(os.path.dirname(self.db_name)):
                os.makedirs(os.path.dirname(self.db_name))

        self._create_table_if_not_exists()

        return True

    def __enter__(self) -> "SQLite":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        if self.executor:
            self.executor.shutdown(wait=True)
