import pytest
import asyncio
import sqlite3
import threading
from typing import Dict, Any, List, Optional, Callable

from wpipe import PipelineAsync, step

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

async def async_add_one(data: Dict[str, Any]) -> Dict[str, int]:
    """Asynchronously increments the 'n' value in the input dictionary.

    Args:
        data: A dictionary potentially containing an integer value for 'n'.
              Defaults to 0 if 'n' is not found.

    Returns:
        A dictionary with the incremented 'n' value.
    """
    await asyncio.sleep(0.01)
    n: int = data.get("n", 0)
    return {"n": n + 1}

@pytest.mark.asyncio
async def test_async_pipeline_basic() -> None:
    """Tests a basic asynchronous pipeline execution.

    Verifies that a simple pipeline with two steps of `async_add_one`
    correctly processes the input data and returns the expected result.
    """
    pipeline = PipelineAsync(worker_name="async_worker")
    pipeline.set_steps([async_add_one, async_add_one])

    initial_data: Dict[str, int] = {"n": 10}
    result = await pipeline.run(initial_data)
    assert result["n"] == 12

@pytest.mark.asyncio
async def test_async_pipeline_parallel() -> None:
    """Tests parallel execution in an asynchronous pipeline.

    Verifies that a pipeline with a single step runs correctly
    when executed asynchronously.
    """
    p = PipelineAsync()
    p.set_steps([async_add_one])

    result = await p.run({"n": 5})
    assert result["n"] == 6

@pytest.mark.asyncio
async def test_async_pipeline_error() -> None:
    """Tests error handling within an asynchronous pipeline.

    This test ensures that the pipeline can continue execution or report errors
    gracefully when one of its steps raises an exception.
    """
    async def async_fail(data: Dict[str, Any]) -> Dict[str, Any]:
        """A step that intentionally raises a RuntimeError."""
        raise RuntimeError("Async failure")

    p = PipelineAsync(continue_on_error=True)
    p.set_steps([async_fail, async_add_one])

    result = await p.run({"n": 0})
    assert "error" in result
    assert result["n"] == 1
