"""
Tests for Background step functionality.
"""

import pytest
import time
import threading
import asyncio
import sqlite3
import threading
from typing import Dict, Any

from wpipe import Pipeline
from wpipe.pipe.components.logic_blocks import Background


# --- RE-PARCHE DE EMERGENCIA PARA ARREGLAR BUG DE WPIPE ---
from wsqlite import WSQLite
_db_connections = {}
_db_lock = threading.Lock()

def better_get_connection(self):
    db_path = getattr(self, "db_path", getattr(self, "db_name", "register.db"))
    with _db_lock:
        if db_path not in _db_connections:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            _db_connections[db_path] = conn
        return _db_connections[db_path]

WSQLite._get_connection = better_get_connection
# --- END RE-PARCHE ---


class TestBackgroundStep:
    """Tests for Background step execution."""

    def test_background_executes_without_blocking(self) -> None:
        """Background step should execute without blocking the pipeline."""
        execution_order = []
        
        def slow_task(data):
            time.sleep(0.5)
            execution_order.append("slow")
            return {}
        
        def fast_task(data):
            execution_order.append("fast")
            return {}

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([
            (fast_task, "Fast", "v1.0"),
            Background(slow_task),
        ])
        
        start = time.time()
        result = pipeline.run({})
        elapsed = time.time() - start
        
        assert "fast" in execution_order
        assert elapsed < 0.5, "Pipeline should not wait for background task"

    def test_background_ignores_return(self) -> None:
        """Background step return should be ignored by pipeline."""
        def background_step(data):
            return {"bg_value": "should_be_ignored"}
        
        def check_step(data):
            data["check_executed"] = True
            return data

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([
            Background(background_step),
            check_step,
        ])
        
        result = pipeline.run({})
        
        assert result.get("check_executed") is True
        assert "bg_value" not in result, "Background return should be ignored"

    def test_background_failure_without_capture_error(self) -> None:
        """Background step failure with capture_error=False should not stop pipeline."""
        def failing_background(data):
            raise ValueError("Background task failed")
        
        def continue_step(data):
            data["continued"] = True
            return data

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([
            Background(failing_background, capture_error=False),
            continue_step,
        ])
        
        result = pipeline.run({})
        
        assert result.get("continued") is True, "Pipeline should continue despite background failure"

    def test_background_failure_with_capture_error(self) -> None:
        """Background step failure with capture_error=True should trigger error handler."""
        import time
        error_captured = []
        
        def failing_background(data):
            raise ValueError("Background task failed")
        
        def error_handler(data, error_info):
            error_captured.append(error_info.get("error") or error_info.get("error_message"))
        
        def continue_step(data):
            data["continued"] = True
            return data

        pipeline = Pipeline(verbose=False)
        pipeline.add_error_capture([error_handler])
        pipeline.set_steps([
            Background(failing_background, capture_error=True),
            continue_step,
        ])
        
        result = pipeline.run({})
        time.sleep(0.1)
        
        assert result.get("continued") is True
        assert len(error_captured) > 0
        assert "Background task failed" in str(error_captured[0]) or "502" in str(error_captured[0])

    def test_background_with_tuple_step(self) -> None:
        """Background should accept tuple steps (func, name, version)."""
        import time
        executed = []
        
        def bg_task(data):
            executed.append(True)
        
        def check_task(data):
            return data

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([
            Background((bg_task, "My Background", "v1.0")),
            check_task,
        ])
        
        result = pipeline.run({})
        time.sleep(0.1)
        
        assert len(executed) == 1

    def test_multiple_background_steps(self) -> None:
        """Multiple background steps should all execute."""
        import time
        counter = {"value": 0}
        
        def increment(data):
            counter["value"] += 1
        
        def check(data):
            data["counter"] = counter["value"]
            return data

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([
            Background(increment),
            Background(increment),
            Background(increment),
            check,
        ])
        
        pipeline.run({})
        time.sleep(0.3)
        
        assert counter["value"] == 3

    def test_background_with_data_copy(self) -> None:
        """Background should receive a copy of data, not the original."""
        original_data = {}
        
        def background_step(data):
            data["modified_in_bg"] = True
        
        def check_step(data):
            return data

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([
            Background(background_step),
            check_step,
        ])
        
        result = pipeline.run({"initial": True})
        
        assert "modified_in_bg" not in result


class TestBackgroundAsync:
    """Tests for Background step in async pipeline."""

    def test_async_background_executes_without_blocking(self) -> None:
        """Background step should execute without blocking async pipeline."""
        from wpipe import PipelineAsync
        
        execution_order = []
        
        async def slow_async_task(data):
            await asyncio.sleep(0.3)
            execution_order.append("slow")
            return {}
        
        async def fast_task(data):
            execution_order.append("fast")
            return {}

        pipeline = PipelineAsync(verbose=False)
        pipeline.set_steps([
            (fast_task, "Fast", "v1.0"),
            Background(slow_async_task),
        ])
        
        start = time.time()
        result = asyncio.run(pipeline.run({}))
        elapsed = time.time() - start
        
        assert "fast" in execution_order
        assert elapsed < 0.4, f"Async pipeline should not wait for background task (took {elapsed}s)"

    def test_async_background_failure_with_capture(self) -> None:
        """Async background with capture_error=True should trigger error handler."""
        from wpipe import PipelineAsync
        
        error_captured = []
        
        async def failing_background(data):
            raise ValueError("Async background failed")
        
        def error_handler(data, error_info):
            error_captured.append(error_info.get("error") or error_info.get("error_message"))

        pipeline = PipelineAsync(verbose=False)
        pipeline.add_error_capture([error_handler])
        pipeline.set_steps([
            Background(failing_background, capture_error=True),
        ])
        
        result = asyncio.run(pipeline.run({}))
        
        assert len(error_captured) > 0
        assert "Async background failed" in str(error_captured[0]) or "502" in str(error_captured[0])