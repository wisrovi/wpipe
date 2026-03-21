"""
Tests for SQLite database functionality.
"""

import os
import json
import pytest
from wpipe.sqlite import Wsqlite
from wpipe.sqlite.Sqlite import SQLite


class TestWsqlite:
    """Test Wsqlite wrapper class."""

    def test_wsqlite_initialization(self, db_file):
        """Test Wsqlite can be initialized with db_name."""
        wsqlite = Wsqlite(db_name=db_file)
        assert wsqlite.db_name == db_file
        assert wsqlite.id is None

    def test_wsqlite_context_manager(self, db_file):
        """Test Wsqlite can be used as context manager."""
        with Wsqlite(db_name=db_file) as db:
            assert db is not None
            assert isinstance(db, Wsqlite)

    def test_wsqlite_set_input(self, db_file):
        """Test setting input property."""
        with Wsqlite(db_name=db_file) as db:
            db.input = {"key": "value"}
            assert db.id is not None

    def test_wsqlite_set_output(self, db_file):
        """Test setting output property."""
        wsqlite = Wsqlite(db_name=db_file)
        wsqlite.output = {"result": "test"}
        assert wsqlite.output == {"result": "test"}

    def test_wsqlite_set_details(self, db_file):
        """Test setting details property."""
        wsqlite = Wsqlite(db_name=db_file)
        wsqlite.details = {"info": "details"}
        assert wsqlite.details == {"info": "details"}


class TestSQLite:
    """Test SQLite core class."""

    def test_sqlite_initialization(self, db_file):
        """Test SQLite can be initialized."""
        sqlite = SQLite(db_name=db_file)
        assert sqlite.db_name == db_file

    def test_sqlite_create_table(self, db_file):
        """Test table is created on initialization."""
        sqlite = SQLite(db_name=db_file)
        assert sqlite.check_table_exists() is True

    def test_sqlite_write_and_read(self, db_file):
        """Test writing and reading records."""
        with SQLite(db_name=db_file) as sqlite:
            record_id = sqlite.write(input_data="test_input", output={"key": "value"})
            assert record_id is not None

            records = sqlite.read_by_id(record_id)
            assert len(records) > 0

    def test_sqlite_write_dict_input(self, db_file):
        """Test writing dict as input."""
        with SQLite(db_name=db_file) as sqlite:
            input_dict = {"name": "test", "value": 123}
            record_id = sqlite.write(input_data=input_dict)
            assert record_id is not None

    def test_sqlite_write_dict_output(self, db_file):
        """Test writing dict as output."""
        with SQLite(db_name=db_file) as sqlite:
            output_dict = {"result": "success"}
            record_id = sqlite.write(output=output_dict)
            assert record_id is not None

            records = sqlite.read_by_id(record_id)
            assert len(records) > 0

    def test_sqlite_update_record(self, db_file):
        """Test updating an existing record."""
        with SQLite(db_name=db_file) as sqlite:
            record_id = sqlite.write(input_data="original", output="original_output")
            sqlite.write(output="updated_output", record_id=record_id)

            records = sqlite.read_by_id(record_id)
            assert len(records) > 0

    def test_sqlite_count_records(self, db_file):
        """Test counting records."""
        with SQLite(db_name=db_file) as sqlite:
            sqlite.write(input_data="record1", output="out1")
            sqlite.write(input_data="record2", output="out2")
            count = sqlite.count_records()
            assert count >= 2

    def test_sqlite_delete_record(self, db_file):
        """Test deleting a record."""
        with SQLite(db_name=db_file) as sqlite:
            record_id = sqlite.write(input_data="to_delete", output="out")
            sqlite.delete_by_id(record_id)

            records = sqlite.read_by_id(record_id)
            assert len(records) == 0

    def test_sqlite_export_to_dataframe(self, db_file):
        """Test exporting to pandas DataFrame."""
        with SQLite(db_name=db_file) as sqlite:
            sqlite.write(input_data="test1", output="out1")
            df = sqlite.export_to_dataframe()
            assert len(df) > 0
            assert "input" in df.columns
            assert "output" in df.columns

    def test_sqlite_export_to_csv(self, db_file, temp_dir):
        """Test exporting to CSV file."""
        csv_path = os.path.join(temp_dir, "export.csv")
        with SQLite(db_name=db_file) as sqlite:
            sqlite.write(input_data="test1", output="out1")
            df = sqlite.export_to_dataframe(save_csv=True, csv_name=csv_path)
            assert os.path.exists(csv_path)

    def test_sqlite_get_records_by_date_range(self, db_file):
        """Test getting records by date range."""
        with SQLite(db_name=db_file) as sqlite:
            sqlite.write(input_data="test", output="out")
            records = sqlite.get_records_by_date_range("2020-01-01", "2030-12-31")
            assert isinstance(records, list)

    def test_sqlite_check_table_not_exists(self):
        """Test check_table_exists with empty db_name."""
        sqlite = SQLite(db_name="")
        assert sqlite.check_table_exists() is False

    def test_sqlite_async_write(self, db_file):
        """Test async write functionality."""
        with SQLite(db_name=db_file) as sqlite:
            record_id = sqlite.async_write(input_data="async_test", output="async_out")
            assert record_id is None
