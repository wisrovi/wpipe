"""
Tests for SQLite integration functionality.
"""

from wpipe.sqlite import Wsqlite
from wpipe.sqlite.Sqlite import SQLite


class TestWsqlite:
    """Test Wsqlite wrapper class."""

    def test_wsqlite_initialization(self, tmp_path):
        """Test Wsqlite can be initialized."""
        db_path = tmp_path / "test.db"
        wsqlite = Wsqlite(db_name=str(db_path))
        assert wsqlite.db_name == str(db_path)
        assert wsqlite.id is None

    def test_wsqlite_context_manager(self, tmp_path):
        """Test Wsqlite can be used as context manager."""
        db_path = tmp_path / "test.db"
        with Wsqlite(db_name=str(db_path)) as db:
            assert db is not None
            assert isinstance(db, Wsqlite)

    def test_wsqlite_set_input(self, tmp_path):
        """Test setting input property creates record."""
        db_path = tmp_path / "test.db"
        with Wsqlite(db_name=str(db_path)) as db:
            db.input = {"key": "value"}
            assert db.id is not None


class TestSQLite:
    """Test SQLite core class."""

    def test_sqlite_initialization(self, tmp_path):
        """Test SQLite can be initialized."""
        db_path = tmp_path / "test.db"
        sqlite = SQLite(db_name=str(db_path))
        assert sqlite.db_name == str(db_path)

    def test_sqlite_write_and_read(self, tmp_path):
        """Test writing and reading records."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            record_id = sqlite.write(input_data="test_input", output={"key": "value"})
            assert record_id is not None
            records = sqlite.read_by_id(record_id)
            assert len(records) > 0

    def test_sqlite_count_records(self, tmp_path):
        """Test counting records."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            sqlite.write(input_data="record1", output="out1")
            sqlite.write(input_data="record2", output="out2")
            count = sqlite.count_records()
            assert count >= 2

    def test_sqlite_delete_record(self, tmp_path):
        """Test deleting a record."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            record_id = sqlite.write(input_data="to_delete", output="out")
            sqlite.delete_by_id(record_id)
            records = sqlite.read_by_id(record_id)
            assert len(records) == 0

    def test_sqlite_export_to_dataframe(self, tmp_path):
        """Test exporting to pandas DataFrame."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            sqlite.write(input_data="test1", output="out1")
            df = sqlite.export_to_dataframe()
            assert len(df) > 0
            assert "input" in df.columns
            assert "output" in df.columns

    def test_sqlite_export_to_csv(self, tmp_path):
        """Test exporting to CSV file."""
        db_path = tmp_path / "test.db"
        csv_path = tmp_path / "export.csv"
        with SQLite(db_name=str(db_path)) as sqlite:
            sqlite.write(input_data="test1", output="out1")
            sqlite.export_to_dataframe(save_csv=True, csv_name=str(csv_path))
            assert csv_path.exists()

    def test_sqlite_empty_db_name(self):
        """Test SQLite with empty db_name returns False."""
        sqlite = SQLite(db_name="")
        result = sqlite.check_table_exists()
        assert result is False

    def test_sqlite_read_no_table(self, tmp_path):
        """Test read_by_id when check_table_exists returns False."""
        db_path = tmp_path / "test.db"
        sqlite = SQLite(db_name=str(db_path))
        sqlite._create_table_if_not_exists = lambda: None
        result = sqlite.read_by_id(999)
        assert result == []

    def test_sqlite_export_no_table(self, tmp_path):
        """Test export_to_dataframe when check_table_exists returns False."""
        db_path = tmp_path / "test.db"
        sqlite = SQLite(db_name=str(db_path))
        sqlite._create_table_if_not_exists = lambda: None
        import pandas as pd

        result = sqlite.export_to_dataframe()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_sqlite_date_range_no_table(self, tmp_path):
        """Test get_records_by_date_range when check_table_exists returns False."""
        db_path = tmp_path / "test.db"
        sqlite = SQLite(db_name=str(db_path))
        sqlite._create_table_if_not_exists = lambda: None
        result = sqlite.get_records_by_date_range("2020-01-01", "2020-12-31")
        assert result == []

    def test_sqlite_count_no_table(self, tmp_path):
        """Test count_records when check_table_exists returns False."""
        db_path = tmp_path / "test.db"
        sqlite = SQLite(db_name=str(db_path))
        sqlite._create_table_if_not_exists = lambda: None
        result = sqlite.count_records()
        assert result == 0

    def test_sqlite_delete_no_table(self, tmp_path):
        """Test delete_by_id when check_table_exists returns False."""
        db_path = tmp_path / "test.db"
        sqlite = SQLite(db_name=str(db_path))
        sqlite._create_table_if_not_exists = lambda: None
        sqlite.delete_by_id(999)

    def test_sqlite_update_existing_record(self, tmp_path):
        """Test updating an existing record."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            record_id = sqlite.write(input_data="old_input", output="old_output")
            sqlite.write(
                input_data="new_input", output="new_output", record_id=record_id
            )
            records = sqlite.read_by_id(record_id)
            assert len(records) > 0

    def test_sqlite_write_string_output(self, tmp_path):
        """Test write with string output."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            record_id = sqlite.write(input_data="test", output="string_output")
            assert record_id is not None

    def test_sqlite_write_with_details(self, tmp_path):
        """Test write with details parameter."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            record_id = sqlite.write(
                input_data="test", output="out", details={"error": "none"}
            )
            assert record_id is not None

    def test_sqlite_write_update_partial(self, tmp_path):
        """Test write with partial update (only output and details)."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            record_id = sqlite.write(input_data="original", output="original_out")
            sqlite.write(
                output="updated_out", details={"key": "val"}, record_id=record_id
            )
            records = sqlite.read_by_id(record_id)
            assert len(records) > 0

    def test_sqlite_date_range(self, tmp_path):
        """Test get_records_by_date_range."""
        db_path = tmp_path / "test.db"
        with SQLite(db_name=str(db_path)) as sqlite:
            sqlite.write(input_data="test", output="out")
            result = sqlite.get_records_by_date_range("2020-01-01", "2030-12-31")
            assert isinstance(result, list)
