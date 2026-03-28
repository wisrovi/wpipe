"""
Tests for async pipeline functionality.
"""

import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def sample_sync_steps():
    """Sample synchronous steps."""

    def step_a(data):
        return {"value": 10, "source": "sync_a"}

    def step_b(data):
        return {"value": data["value"] * 2, "source": "sync_b"}

    return [(step_a, "Step A", "v1.0"), (step_b, "Step B", "v1.0")]


@pytest.fixture
def sample_async_steps():
    """Sample asynchronous steps."""

    async def async_step_a(data):
        await asyncio.sleep(0.01)
        return {"value": 10, "source": "async_a"}

    async def async_step_b(data):
        await asyncio.sleep(0.01)
        return {"value": data["value"] * 2, "source": "async_b"}

    return [
        (async_step_a, "Async Step A", "v1.0"),
        (async_step_b, "Async Step B", "v1.0"),
    ]


@pytest.fixture
def mixed_steps():
    """Mix of sync and async steps."""

    def sync_step(data):
        return {"sync_value": 5, "source": "sync"}

    async def async_step(data):
        await asyncio.sleep(0.01)
        return {"async_value": 10, "source": "async"}

    return [(sync_step, "Sync Step", "v1.0"), (async_step, "Async Step", "v1.0")]


class TestPipelineAsync:
    """Tests for async pipeline execution."""

    def test_run_async_method_exists(self):
        """Test that run_async method exists on Pipeline."""
        from wpipe import Pipeline

        pipeline = Pipeline()
        assert hasattr(pipeline, "run_async")
        assert callable(pipeline.run_async)

    def test_run_async_with_sync_functions(self, sample_sync_steps):
        """Test run_async with synchronous functions."""
        from wpipe import Pipeline

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(sample_sync_steps)

        result = asyncio.run(pipeline.run_async({}))

        assert result["value"] == 20
        assert result["source"] == "sync_b"

    def test_run_async_with_async_functions(self, sample_async_steps):
        """Test run_async with asynchronous functions."""
        from wpipe import Pipeline

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(sample_async_steps)

        result = asyncio.run(pipeline.run_async({}))

        assert result["value"] == 20
        assert result["source"] == "async_b"

    def test_run_async_with_mixed_functions(self, mixed_steps):
        """Test run_async with mixed sync and async functions."""
        from wpipe import Pipeline

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(mixed_steps)

        result = asyncio.run(pipeline.run_async({}))

        assert result["sync_value"] == 5
        assert result["async_value"] == 10
        assert result["source"] == "async"

    def test_run_async_with_initial_data(self, sample_sync_steps):
        """Test run_async with initial data."""
        from wpipe import Pipeline

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(sample_sync_steps)

        result = asyncio.run(pipeline.run_async({"initial": 100}))

        assert result["initial"] == 100

    def test_run_async_error_handling(self):
        """Test run_async error handling."""
        from wpipe import Pipeline
        from wpipe.exception import TaskError

        def error_step(data):
            raise ValueError("Test error")

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([(error_step, "Error Step", "v1.0")])

        with pytest.raises(TaskError):
            asyncio.run(pipeline.run_async({}))

    def test_run_async_with_conditions(self):
        """Test run_async with conditions."""
        from wpipe import Pipeline, Condition

        async def step_true(data):
            return {"result": "branch_true"}

        async def step_false(data):
            return {"result": "branch_false"}

        condition = Condition(
            expression="data.get('value') > 5",
            branch_true=[(step_true, "True Branch", "v1.0")],
            branch_false=[(step_false, "False Branch", "v1.0")],
        )

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([condition])

        result = asyncio.run(pipeline.run_async({"value": 10}))
        assert result["result"] == "branch_true"

        result = asyncio.run(pipeline.run_async({"value": 3}))
        assert result["result"] == "branch_false"

    def test_run_async_preserves_sync_behavior(self, sample_sync_steps):
        """Test that async run produces same results as sync run."""
        from wpipe import Pipeline

        pipeline_sync = Pipeline(verbose=False)
        pipeline_sync.set_steps(sample_sync_steps)
        sync_result = pipeline_sync.run({})

        pipeline_async = Pipeline(verbose=False)
        pipeline_async.set_steps(sample_sync_steps)
        async_result = asyncio.run(pipeline_async.run_async({}))

        sync_clean = {k: v for k, v in sync_result.items() if k != "progress_rich"}
        async_clean = {k: v for k, v in async_result.items() if k != "progress_rich"}

        assert sync_clean == async_clean


class TestPipelineStreaming:
    """Tests for streaming pipeline execution."""

    def test_run_streaming_method_exists(self):
        """Test that run_streaming method exists."""
        from wpipe import Pipeline

        pipeline = Pipeline()
        assert hasattr(pipeline, "run_streaming")
        assert callable(pipeline.run_streaming)

    def test_run_streaming_yields_results(self, sample_sync_steps):
        """Test that run_streaming yields step results."""
        from wpipe import Pipeline

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(sample_sync_steps)

        async def run_test():
            results = []
            async for result in pipeline.run_streaming({}):
                results.append(result)
            return results

        results = asyncio.run(run_test())

        assert len(results) == 3

        assert results[0]["step"] == 0
        assert results[0]["name"] == "Step A"
        assert "value" in results[0]["data"]

        assert results[1]["step"] == 1
        assert results[1]["name"] == "Step B"

        assert results[2]["step"] == -1
        assert results[2]["name"] == "complete"

    def test_run_streaming_with_async_steps(self, sample_async_steps):
        """Test streaming with async functions."""
        from wpipe import Pipeline

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(sample_async_steps)

        async def run_test():
            results = []
            async for result in pipeline.run_streaming({}):
                results.append(result)
            return results

        results = asyncio.run(run_test())

        assert len(results) == 3
        assert results[-1]["result"]["value"] == 20

    def test_run_streaming_error_stops(self):
        """Test that errors are handled properly."""
        from wpipe import Pipeline
        from wpipe.exception import TaskError

        def error_step(data):
            raise ValueError("Test error")

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([(error_step, "Error", "v1.0")])

        with pytest.raises((TaskError, ValueError)):
            asyncio.run(pipeline.run_streaming({}))

    def test_run_streaming_data_accumulates(self):
        """Test that data accumulates between steps."""

        async def step_a(data):
            return {"a": 1}

        async def step_b(data):
            return {"b": data.get("a", 0) + 1}

        async def step_c(data):
            return {"c": data.get("b", 0) + 1}

        from wpipe import Pipeline

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(
            [
                (step_a, "A", "v1.0"),
                (step_b, "B", "v1.0"),
                (step_c, "C", "v1.0"),
            ]
        )

        async def run_test():
            results = []
            async for result in pipeline.run_streaming({}):
                results.append(result)
            return results

        results = asyncio.run(run_test())

        assert results[0]["data"]["a"] == 1
        assert results[1]["data"]["a"] == 1
        assert results[1]["data"]["b"] == 2
        assert results[2]["data"]["c"] == 3


class TestAsyncPipelineIntegration:
    """Integration tests for async pipeline."""

    def test_async_pipeline_with_sqlite(self, tmp_path):
        """Test async pipeline with SQLite persistence."""
        from wpipe import Pipeline, Wsqlite
        import json

        async def process_data(data):
            await asyncio.sleep(0.01)
            return {"processed": True, "value": data.get("input", 0) * 2}

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([(process_data, "Process", "v1.0")])

        db_path = str(tmp_path / "test.db")

        initial_input = {"input": 5}

        with Wsqlite(db_name=db_path) as db:
            db.input = initial_input
            result = asyncio.run(pipeline.run_async(initial_input))
            db.output = result

        from wpipe.sqlite.Sqlite import SQLite

        with SQLite(db_path) as db:
            records = db.read_by_id(1)
            assert len(records) == 1

            output = json.loads(records[0][2])
            assert output["processed"] is True
            assert output["value"] == 10

    def test_multiple_async_runs(self):
        """Test running multiple async pipelines."""
        from wpipe import Pipeline

        async def step(data):
            await asyncio.sleep(0.01)
            return {"result": data.get("id", 0) * 10}

        results = []
        for i in [1, 2, 3]:
            pipeline = Pipeline(verbose=False)
            pipeline.set_steps([(step, f"Step-{i}", "v1.0")])
            result = asyncio.run(pipeline.run_async({"id": i}))
            results.append(result)

        assert results[0]["result"] == 10
        assert results[1]["result"] == 20
        assert results[2]["result"] == 30

    def test_async_pipeline_preserves_verbose(self):
        """Test that verbose mode works with async."""
        from wpipe import Pipeline
        import io
        import sys

        async def step(data):
            return {"value": 1}

        pipeline = Pipeline(verbose=True)
        pipeline.set_steps([(step, "Test", "v1.0")])

        old_stdout = sys.stdout
        captured = io.StringIO()

        try:
            sys.stdout = captured
            result = asyncio.run(pipeline.run_async({}))
            assert result["value"] == 1
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()


class TestAsyncNestedPipelines:
    """Tests for async nested pipelines."""

    def test_async_nested_pipeline(self):
        """Test async pipeline with nested Pipeline as step."""
        from wpipe import Pipeline

        async def inner_step(data):
            return {"inner": data.get("value", 0) * 2}

        inner_pipeline = Pipeline(verbose=False)
        inner_pipeline.set_steps([(inner_step, "Inner", "v1.0")])

        async def outer_step(data):
            return {"outer": data.get("inner", 0) + 10}

        outer_pipeline = Pipeline(verbose=False)
        outer_pipeline.set_steps(
            [
                (inner_pipeline, "Nested", "v1.0"),
                (outer_step, "Outer", "v1.0"),
            ]
        )

        result = asyncio.run(outer_pipeline.run_async({"value": 5}))

        assert result["inner"] == 10
        assert result["outer"] == 20

    def test_async_nested_pipeline_multiple(self):
        """Test async pipeline with multiple nested Pipelines."""
        from wpipe import Pipeline

        def make_pipeline(multiplier):
            async def step(data):
                return {"result": data.get("result", data.get("input", 0)) * multiplier}

            p = Pipeline(verbose=False)
            p.set_steps([(step, f"Multiply-{multiplier}", "v1.0")])
            return p

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(
            [
                (make_pipeline(2), "First", "v1.0"),
                (make_pipeline(3), "Second", "v1.0"),
            ]
        )

        result = asyncio.run(pipeline.run_async({"input": 5}))

        assert result["result"] == 30


class TestAsyncRetry:
    """Tests for async retry functionality."""

    def test_async_with_retry_success(self):
        """Test async pipeline with retry that eventually succeeds."""
        from wpipe import Pipeline

        attempt_count = {"count": 0}

        async def flaky_step(data):
            attempt_count["count"] += 1
            if attempt_count["count"] < 2:
                raise ValueError("Temporary error")
            return {"success": True, "attempts": attempt_count["count"]}

        pipeline = Pipeline(verbose=False, max_retries=3, retry_delay=0.01)
        pipeline.set_steps([(flaky_step, "Flaky", "v1.0")])

        result = asyncio.run(pipeline.run_async({}))

        assert result["success"] is True
        assert result["attempts"] == 2

    def test_async_with_retry_failure(self):
        """Test async pipeline with retry that always fails."""
        from wpipe import Pipeline
        from wpipe.exception import TaskError

        async def failing_step(data):
            raise ValueError("Permanent error")

        pipeline = Pipeline(verbose=False, max_retries=2, retry_delay=0.01)
        pipeline.set_steps([(failing_step, "Fail", "v1.0")])

        with pytest.raises(TaskError):
            asyncio.run(pipeline.run_async({}))
