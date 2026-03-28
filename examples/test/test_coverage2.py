"""
More comprehensive tests to achieve 95%+ coverage.
"""

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from wpipe import Pipeline, Wsqlite, Condition
from wpipe.exception import TaskError, ProcessError
from wpipe.sqlite.Sqlite import SQLite


class TestProgressManagerCoverage:
    """Test ProgressManager singleton."""

    def test_progress_manager_singleton(self):
        """Test ProgressManager is singleton."""
        from wpipe.pipe.pipe import ProgressManager

        pm1 = ProgressManager()
        pm2 = ProgressManager()
        assert pm1 is pm2

    def test_progress_manager_context(self):
        """Test ProgressManager context manager."""
        from wpipe.pipe.pipe import ProgressManager

        pm = ProgressManager()
        with pm as progress:
            assert progress is not None


class TestPipelineStepsCoverage:
    """More tests for Pipeline steps."""

    def test_set_steps_with_4_tuples(self):
        """Test set_steps with 4-element tuples."""

        def step1(data):
            return {"a": 1}

        def step2(data):
            return {"b": 2}

        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0", "id1"),
                (step2, "Step2", "v1.0", "id2"),
            ]
        )

        result = pipeline.run({})
        assert result["a"] == 1
        assert result["b"] == 2

    def test_set_steps_with_class_instances(self):
        """Test set_steps with class instances."""

        class Step:
            def __call__(self, data):
                return {"result": True}

        pipeline = Pipeline()
        pipeline.set_steps([(Step(), "Class", "v1.0")])
        result = pipeline.run({})
        assert result["result"] is True


class TestConditionFullCoverage:
    """Full condition tests."""

    def test_condition_invalid_operator(self):
        """Test invalid operator raises error."""
        with pytest.raises(ValueError):
            cond = Condition("value ** 2", [(lambda d: d, "Step", "v1.0")])
            cond.evaluate({"value": 5})


class TestPipelineExecutionCoverage:
    """More execution tests."""

    def test_task_invoke_with_retry_success(self):
        """Test _task_invoke with retry success."""
        attempt = {"count": 0}

        def step(data):
            attempt["count"] += 1
            return {"result": attempt["count"]}

        pipeline = Pipeline(max_retries=3)
        result = pipeline._task_invoke(step, "Step", {})
        assert result["result"] == 1


class TestAsyncExecutionCoverage:
    """Async execution tests."""

    def test_async_run_async_with_progress_rich_none(self):
        """Test async with progress_rich as None."""

        async def step(data):
            pr = data.get("progress_rich")
            return {"has_progress": pr is None}

        pipeline = Pipeline()
        pipeline.set_steps([(step, "Step", "v1.0")])

        result = asyncio.run(pipeline.run_async({}))
        assert result["has_progress"] is True


class TestPipelineEdgeCases:
    """Edge case tests."""

    def test_pipeline_with_empty_kwargs(self):
        """Test pipeline with empty kwargs."""

        def step(data, **kwargs):
            return {"kwargs": kwargs}

        pipeline = Pipeline()
        pipeline.set_steps([(step, "Step", "v1.0")])
        result = pipeline.run({})
        assert "kwargs" in result

    def test_pipeline_with_kwargs(self):
        """Test pipeline with kwargs."""

        def step(data, extra=None):
            return {"extra": extra}

        pipeline = Pipeline()
        pipeline.set_steps([(step, "Step", "v1.0")])
        result = pipeline.run({}, extra="test")
        assert result["extra"] == "test"

    def test_condition_evaluate_with_missing_key(self):
        """Test condition with missing key."""
        cond = Condition("missing > 5", [(lambda d: d, "Step", "v1.0")])
        # Should return False for missing key
        result = cond.evaluate({"other": 10})
        assert result is False


class TestSQLiteEdgeCases:
    """SQLite edge case tests."""

    def test_sqlite_no_table(self, tmp_path):
        """Test SQLite with no table."""
        db_path = tmp_path / "empty.db"
        db = SQLite(str(db_path))

        # Table doesn't exist yet
        db._create_table_if_not_exists()
        assert db.check_table_exists() is True

    def test_sqlite_read_nonexistent(self, tmp_path):
        """Test reading nonexistent record."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))
        db.write(input_data={"test": "data"})

        records = db.read_by_id(9999)
        assert records == []

    def test_sqlite_update_nonexistent(self, tmp_path):
        """Test updating nonexistent record."""
        db_path = tmp_path / "test.db"
        db = SQLite(str(db_path))

        # Updating nonexistent should return None
        db.update_record(9999, output={"test": True})


class TestWsqliteEdgeCases:
    """Wsqlite edge case tests."""

    def test_wsqlite_id_property(self, tmp_path):
        """Test Wsqlite id property."""
        db_path = tmp_path / "test.db"

        with Wsqlite(db_name=str(db_path)) as db:
            db.input = {"test": "data"}
            assert db.id is not None

    def test_wsqlite_count_records(self, tmp_path):
        """Test count_records."""
        db_path = tmp_path / "test.db"

        with Wsqlite(db_name=str(db_path)) as db:
            db.input = {"test": "data"}

        count = db.count_records()
        assert count == 1


class TestAPIClientCoverage:
    """API Client tests."""

    def test_api_client_init(self):
        """Test API client initialization."""
        from wpipe import APIClient

        client = APIClient(base_url="http://test", token="token")
        assert client.base_url == "http://test"

    def test_api_client_no_url(self):
        """Test API client without URL."""
        from wpipe import APIClient

        client = APIClient()
        assert client.base_url is None


class TestRamCoverage:
    """RAM decorator tests."""

    def test_memory_decorator(self):
        """Test memory decorator."""
        from wpipe import memory

        @memory
        def func():
            return "result"

        result = func()
        assert result == "result"


class TestLoggingCoverage:
    """Logging tests."""

    def test_new_logger(self):
        """Test new_logger function."""
        from wpipe import new_logger

        logger = new_logger("test")
        assert logger is not None


class TestUtilsCoverage:
    """Utils tests."""

    def test_leer_yaml(self):
        """Test leer_yaml function."""
        from wpipe.util import leer_yaml
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("key: value\n")
            f.flush()

            result = leer_yaml(f.name)
            assert result["key"] == "value"

            os.unlink(f.name)

    def test_escribir_yaml(self):
        """Test escribir_yaml function."""
        from wpipe.util import escribir_yaml
        import tempfile

        path = tempfile.mktemp(suffix=".yaml")
        escribir_yaml(path, {"test": "data"})

        with open(path) as f:
            content = f.read()
            assert "test: data" in content

        os.unlink(path)


class TestErrorCoverage:
    """Error handling tests."""

    def test_task_error_code(self):
        """Test TaskError with code."""
        from wpipe.exception import TaskError, Codes

        error = TaskError("test", Codes.TASK_FAILED)
        assert error.error_code == Codes.TASK_FAILED

    def test_process_error(self):
        """Test ProcessError."""
        from wpipe.exception import ProcessError, Codes

        error = ProcessError("test", Codes.TASK_FAILED)
        assert error.error_code == Codes.TASK_FAILED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
