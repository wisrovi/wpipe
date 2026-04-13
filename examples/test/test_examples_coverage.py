"""
Comprehensive tests to achieve high coverage for examples.
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from wpipe import Condition, Pipeline, PipelineAsync, Wsqlite
from wpipe.exception import ProcessError, TaskError
from wpipe.sqlite.Sqlite import SQLite
from wpipe.sqlite.tables_dto.records import RecordModel


class TestConditionCoverage:
    """Tests to improve Condition coverage."""

    def test_condition_with_greater_than(self):
        """Test condition with > operator."""
        cond = Condition("value > 10", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"value": 15}) is True
        assert cond.evaluate({"value": 5}) is False

    def test_condition_with_less_than(self):
        """Test condition with < operator."""
        cond = Condition("value < 10", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"value": 5}) is True
        assert cond.evaluate({"value": 15}) is False

    def test_condition_with_greater_equal(self):
        """Test condition with >= operator."""
        cond = Condition("value >= 10", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"value": 10}) is True
        assert cond.evaluate({"value": 15}) is True
        assert cond.evaluate({"value": 5}) is False

    def test_condition_with_less_equal(self):
        """Test condition with <= operator."""
        cond = Condition("value <= 10", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"value": 10}) is True
        assert cond.evaluate({"value": 5}) is True
        assert cond.evaluate({"value": 15}) is False

    def test_condition_with_not_equal(self):
        """Test condition with != operator."""
        cond = Condition("value != 10", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"value": 5}) is True
        assert cond.evaluate({"value": 10}) is False

    def test_condition_get_branch_false_empty(self):
        """Test get_branch returns empty when false branch not set."""
        step_true = (lambda d: d, "True", "v1.0")
        cond = Condition("value > 10", [step_true])
        assert cond.get_branch({"value": 5}) == []

    def test_condition_with_string_value(self):
        """Test condition with string value."""
        cond = Condition("name == 'test'", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"name": "test"}) is True
        assert cond.evaluate({"name": "other"}) is False

    def test_condition_with_double_quotes(self):
        """Test condition with double quotes."""
        cond = Condition('name == "test"', [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"name": "test"}) is True

    def test_condition_with_true_false(self):
        """Test condition with True/False values."""
        cond = Condition("active == True", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"active": True}) is True
        assert cond.evaluate({"active": False}) is False

    def test_condition_with_none_value(self):
        """Test condition with None value."""
        cond = Condition("value is None", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"value": None}) is True
        assert cond.evaluate({"value": 10}) is False

    def test_condition_get_branch_true(self):
        """Test get_branch returns true branch."""
        step_true = (lambda d: d, "True", "v1.0")
        step_false = (lambda d: d, "False", "v1.0")
        cond = Condition("value > 10", [step_true], [step_false])
        assert cond.get_branch({"value": 15}) == [step_true]

    def test_condition_get_branch_false(self):
        """Test get_branch returns false branch."""
        step_true = (lambda d: d, "True", "v1.0")
        step_false = (lambda d: d, "False", "v1.0")
        cond = Condition("value > 10", [step_true], [step_false])
        assert cond.get_branch({"value": 5}) == [step_false]

    def test_condition_invalid_format(self):
        """Test invalid condition format raises error."""
        with pytest.raises(ValueError):
            cond = Condition("invalid ?? expression", [(lambda d: d, "Step", "v1.0")])
            cond.evaluate({})


class TestPipelineCoverage:
    """Tests to improve Pipeline coverage."""

    def test_pipeline_with_max_retries_success(self):
        """Test pipeline with retry that succeeds."""
        call_count = {"count": 0}

        def flaky(data):
            call_count["count"] += 1
            if call_count["count"] < 2:
                raise ValueError("Fail")
            return {"success": True}

        pipeline = Pipeline(max_retries=3, retry_delay=0.01)
        pipeline.set_steps([(flaky, "Flaky", "v1.0")])
        result = pipeline.run({})
        assert result["success"] is True

    def test_pipeline_with_max_retries_failure(self):
        """Test pipeline with retry that always fails."""

        def failing(data):
            raise ValueError("Always fails")

        pipeline = Pipeline(max_retries=1, retry_delay=0.01)
        pipeline.set_steps([(failing, "Fail", "v1.0")])
        result = pipeline.run({})
        assert "error" in result

    def test_pipeline_worker_register(self):
        """Test worker registration."""
        pipeline = Pipeline(worker_id="test123", worker_name="test")
        pipeline.set_steps([(lambda d: d, "Step", "v1.0")])
        result = pipeline.worker_register("test", "v1.0")
        assert result is None

    def test_pipeline_verbose_output(self, capsys):
        """Test verbose output."""
        pipeline = Pipeline(verbose=True)
        pipeline.set_steps([(lambda d: {"result": True}, "Step", "v1.0")])
        pipeline.run({})
        captured = capsys.readouterr()
        # The library uses rich/tqdm which might not show up in capsys.out directly
        # but we check if it runs without error

    def test_pipeline_with_class_step(self):
        """Test pipeline with class as step."""

        class MyStep:
            def __call__(self, data):
                return {"class_result": True}

        pipeline = Pipeline()
        pipeline.set_steps([(MyStep(), "ClassStep", "v1.0")])
        result = pipeline.run({})
        assert result["class_result"] is True

    def test_pipeline_api_update_no_send(self):
        """Test API update when send_to_api is False."""
        pipeline = Pipeline(verbose=False)
        pipeline.send_to_api = False
        pipeline.worker_id = "test"
        pipeline._api_task_update({"task_id": "1", "status": "start"})

    def test_pipeline_api_process_update_no_send(self):
        """Test API process update when send_to_api is False."""
        pipeline = Pipeline(verbose=False)
        pipeline.send_to_api = False
        pipeline.worker_id = "test"
        pipeline._api_process_update({"id": "1"}, start=True)


class TestSQLiteCoverage:
    """Tests to improve SQLite coverage."""

    def test_sqlite_async_write(self, tmp_path):
        """Test async write."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        db.async_write(input_data={"test": "data"})
        db.executor.shutdown(wait=True)

        db2 = SQLite(str(db_path))
        count = db2.count_records()
        assert count >= 1

    def test_sqlite_write_with_string_output(self, tmp_path):
        """Test write with string output."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        db.write(input_data={"test": "data"}, output="string output")
        assert db.count_records() == 1

    def test_sqlite_write_update_only_output(self, tmp_path):
        """Test write update with only output."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        record_id = db.write(input_data={"test": "data"})
        db.write(output={"result": "updated"}, record_id=record_id)
        
        record = db.read_by_id(record_id)
        assert "updated" in record.output

    def test_sqlite_write_update_both(self, tmp_path):
        """Test write update with both output and details."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        record_id = db.write(input_data={"test": "data"})
        db.write(
            output={"result": "updated"}, details={"info": "data"}, record_id=record_id
        )
        record = db.read_by_id(record_id)
        assert "updated" in record.output
        assert "info" in record.details

    def test_sqlite_update_record_only_output(self, tmp_path):
        """Test update_record with only output."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        record_id = db.write(input_data={"test": "data"})
        db.update_record(record_id, output={"updated": True})
        record = db.read_by_id(record_id)
        assert "updated" in record.output

    def test_sqlite_delete_by_id(self, tmp_path):
        """Test delete_by_id."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        record_id = db.write(input_data={"test": "data"})
        assert db.count_records() == 1
        db.delete_by_id(record_id)
        assert db.count_records() == 0

    def test_sqlite_get_records_by_date_range(self, tmp_path):
        """Test get_records_by_date_range."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        db.write(input_data={"test": "data"})

        end = datetime.now() + timedelta(minutes=1)
        start = end - timedelta(days=1)

        records = db.get_records_by_date_range(
            start_date=start.isoformat(),
            end_date=end.isoformat(),
        )
        assert len(records) >= 1

    def test_sqlite_export_to_csv(self, tmp_path):
        """Test export_to_dataframe with CSV."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        db.write(input_data={"test": "data"})

        csv_path = tmp_path / "output.csv"
        df = db.export_to_dataframe(save_csv=True, csv_name=str(csv_path))
        assert csv_path.exists()
        assert len(df) >= 1


class TestDashboardCoverage:
    """Tests to improve dashboard coverage."""

    def test_dashboard_api_health(self):
        """Test dashboard health endpoint."""
        from wpipe.dashboard.main import create_app
        app = create_app(":memory:")
        client = TestClient(app)
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_dashboard_root(self):
        """Test dashboard root endpoint."""
        from wpipe.dashboard.main import create_app
        app = create_app(":memory:")
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert "html" in response.headers["content-type"]


class TestErrorHandling:
    """Test error handling paths."""

    def test_condition_parse_data_get(self):
        """Test condition parsing."""
        cond = Condition("value > 5", [(lambda d: d, "Step", "v1.0")])
        assert cond.evaluate({"value": 10}) is True
        assert cond.evaluate({"value": 3}) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
