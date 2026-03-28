"""
Tests for dashboard examples.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestExample01PipelineWithSQLite:
    """Tests for example 01: Pipeline with SQLite."""

    @pytest.fixture
    def example_runner(self, temp_dir):
        """Run example and return database path."""
        db_path = os.path.join(temp_dir, "test_pipeline.db")

        import wpipe
        from wpipe import Pipeline, Wsqlite

        def fetch_data(data):
            return {"source": "test", "values": [1, 2, 3]}

        def process(data):
            return {"processed": data.get("values", [])}

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(
            [
                (fetch_data, "Fetch", "v1.0"),
                (process, "Process", "v1.0"),
            ]
        )

        with Wsqlite(db_name=db_path) as db:
            db.input = {"test_id": 1}
            result = pipeline.run({})
            db.output = result

        return db_path

    def test_database_created(self, example_runner):
        """Test database file is created."""
        assert os.path.exists(example_runner)

    def test_records_saved(self, example_runner):
        """Test records are saved in database."""
        from wpipe.sqlite.Sqlite import SQLite

        with SQLite(example_runner) as db:
            count = db.count_records()
            assert count == 1

    def test_input_saved(self, example_runner):
        """Test input data is saved."""
        from wpipe.sqlite.Sqlite import SQLite

        with SQLite(example_runner) as db:
            records = db.read_by_id(1)
            assert len(records) == 1
            input_data = json.loads(records[0][1])
            assert "test_id" in input_data

    def test_output_saved(self, example_runner):
        """Test output data is saved."""
        from wpipe.sqlite.Sqlite import SQLite

        with SQLite(example_runner) as db:
            records = db.read_by_id(1)
            output_data = json.loads(records[0][2])
            assert "processed" in output_data


class TestExample02StartDashboard:
    """Tests for example 02: Start Dashboard."""

    def test_dependencies_available(self):
        """Test dashboard dependencies are installed."""
        try:
            import fastapi
            import uvicorn
            import jinja2

            assert True
        except ImportError:
            pytest.skip("Dashboard dependencies not installed")

    def test_start_dashboard_function_exists(self):
        """Test start_dashboard function exists."""
        from wpipe import start_dashboard

        assert callable(start_dashboard)

    def test_dashboard_module_imports(self):
        """Test dashboard module can be imported."""
        from wpipe.dashboard.main import app

        assert app is not None


class TestExample03FullExample:
    """Tests for example 03: Full example with conditions."""

    @pytest.fixture
    def multi_record_db(self, temp_dir):
        """Create database with multiple records."""
        db_path = os.path.join(temp_dir, "full_example.db")

        from wpipe import Pipeline, Wsqlite

        def step_a(data):
            return {"step": "a", "value": 10}

        def step_b(data):
            return {"step": "b", "value": 20}

        for i in range(5):
            pipeline = Pipeline(verbose=False)
            pipeline.set_steps([(step_a if i % 2 == 0 else step_b, "Step", "v1.0")])

            with Wsqlite(db_name=db_path) as db:
                db.input = {"iteration": i}
                result = pipeline.run({})
                db.output = result

        return db_path

    def test_multiple_records(self, multi_record_db):
        """Test multiple records are created."""
        from wpipe.sqlite.Sqlite import SQLite

        with SQLite(multi_record_db) as db:
            count = db.count_records()
            assert count == 5

    def test_all_successful(self, multi_record_db):
        """Test all records have successful output."""
        import sqlite3

        with sqlite3.connect(multi_record_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM records")
            records = cursor.fetchall()

            for record in records:
                output = json.loads(record[2])
                assert "error" not in output

    def test_different_inputs(self, multi_record_db):
        """Test different inputs are saved."""
        import sqlite3

        with sqlite3.connect(multi_record_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM records")
            records = cursor.fetchall()

            iterations = set()
            for record in records:
                input_data = json.loads(record[1])
                iterations.add(input_data.get("iteration"))

            assert len(iterations) == 5


class TestDashboardWithRealData:
    """Integration tests with real pipeline data."""

    @pytest.fixture
    def real_pipeline_db(self, temp_dir):
        """Create database with realistic pipeline data."""
        db_path = os.path.join(temp_dir, "real_pipeline.db")

        from wpipe import Pipeline, Wsqlite

        def fetch_users(data):
            return {
                "users": [
                    {"id": 1, "name": "Alice", "age": 30},
                    {"id": 2, "name": "Bob", "age": 25},
                ]
            }

        def filter_adults(data):
            users = data.get("users", [])
            adults = [u for u in users if u.get("age", 0) >= 18]
            return {"adults": adults, "count": len(adults)}

        def calculate_stats(data):
            ages = [u.get("age", 0) for u in data.get("adults", [])]
            return {
                "stats": {
                    "average_age": sum(ages) / len(ages) if ages else 0,
                    "total": len(ages),
                }
            }

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(
            [
                (fetch_users, "Fetch Users", "v1.0"),
                (filter_adults, "Filter Adults", "v1.0"),
                (calculate_stats, "Calculate Stats", "v1.0"),
            ]
        )

        with Wsqlite(db_name=db_path) as db:
            db.input = {"batch": "daily", "date": "2024-01-15"}
            result = pipeline.run({})
            db.output = result
            db.details = {"version": "1.0.0", "duration_ms": 150}

        return db_path

    def test_pipeline_execution_saved(self, real_pipeline_db):
        """Test complete pipeline execution is saved."""
        from wpipe.sqlite.Sqlite import SQLite

        with SQLite(real_pipeline_db) as db:
            records = db.read_by_id(1)
            assert len(records) == 1

            input_data = json.loads(records[0][1])
            assert input_data["batch"] == "daily"

            output_data = json.loads(records[0][2])
            assert "stats" in output_data

            details_data = json.loads(records[0][3])
            assert details_data["version"] == "1.0.0"

    def test_stats_calculation(self, real_pipeline_db):
        """Test statistics are correctly calculated."""
        from wpipe.sqlite.Sqlite import SQLite

        with SQLite(real_pipeline_db) as db:
            records = db.read_by_id(1)
            output_data = json.loads(records[0][2])

            assert output_data["stats"]["total"] == 2
            assert output_data["stats"]["average_age"] == 27.5
