"""
Unit tests for SQLite database wrapper.
"""

import unittest
import os
import tempfile
import shutil
import time
import pandas as pd
from wpipe.sqlite.Sqlite import Wsqlite, SQLite


class TestSqlite(unittest.TestCase):
    """Test SQLite functionality."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_register.db")

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_wsqlite_wrapper(self):
        """Test Wsqlite simplified wrapper."""
        with Wsqlite(self.db_path) as ws:
            ws.input = {"param": 1}
            ws.output = {"result": "success"}
            ws.details = {"info": "all ok"}
            
            self.assertEqual(ws.input, {"param": 1})
            self.assertEqual(ws.output, {"result": "success"})
            self.assertEqual(ws.details, {"info": "all ok"})
            
            record_id = ws.id
            self.assertIsNotNone(record_id)
        
        # After exit, it should have updated the record
        ws2 = Wsqlite(self.db_path)
        self.assertEqual(ws2.count_records(), 1)

    def test_sqlite_main_wrapper(self):
        """Test main SQLite wrapper."""
        db = SQLite(self.db_path)
        self.assertTrue(db.check_table_exists())
        
        # Test write
        record_id = db.write(
            input_data={"a": 1},
            output={"b": 2},
            details={"c": 3}
        )
        self.assertIsNotNone(record_id)
        
        # Test read_by_id
        record = db.read_by_id(record_id)
        self.assertIsNotNone(record)
        self.assertIn('"a": 1', record.input)
        
        # Test update_record
        db.update_record(record_id, output={"status": "updated"}, details={"note": "fixed"})
        record = db.read_by_id(record_id)
        self.assertIn('"status": "updated"', record.output)
        
        # Test count
        self.assertEqual(db.count_records(), 1)
        
        # Test delete
        db.delete_by_id(record_id)
        self.assertEqual(db.count_records(), 0)

    def test_sqlite_async_write(self):
        """Test asynchronous write."""
        db = SQLite(self.db_path)
        db.async_write(input_data={"async": True})
        
        # Wait for executor
        with db:
            pass
            
        self.assertEqual(db.count_records(), 1)

    def test_export_to_dataframe(self):
        """Test exporting to pandas DataFrame."""
        db = SQLite(self.db_path)
        db.write(input_data={"row": 1})
        db.write(input_data={"row": 2})
        
        df = db.export_to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        
        csv_path = os.path.join(self.temp_dir, "export.csv")
        db.export_to_dataframe(save_csv=True, csv_name=csv_path)
        self.assertTrue(os.path.exists(csv_path))

    def test_get_records_by_date_range(self):
        """Test filtering records by date range."""
        db = SQLite(self.db_path)
        db.write(input_data={"time": "now"})
        
        # Test days filter
        records = db.get_records_by_date_range(days=1)
        self.assertEqual(len(records), 1)
        
        # Test future/past filter (mocking date would be better but let's test basic path)
        all_records = db.get_records_by_date_range()
        self.assertEqual(len(all_records), 1)

    def test_sqlite_context_manager(self):
        """Test SQLite context manager."""
        with SQLite(self.db_path) as db:
            db.write(input_data={"test": "context"})
        # Executor should be shut down after exit

    def test_sqlite_invalid_db_name(self):
        """Test SQLite with no db name."""
        db = SQLite(None)
        self.assertFalse(db.check_table_exists())


if __name__ == "__main__":
    unittest.main()
