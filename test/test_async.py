import pytest
import asyncio
import sqlite3
import threading
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

async def async_add_one(data):
    await asyncio.sleep(0.01)
    n = data.get("n", 0)
    return {"n": n + 1}

@pytest.mark.asyncio
async def test_async_pipeline_basic():
    """Prueba un pipeline asíncrono simple."""
    p = PipelineAsync(worker_name="async_worker")
    p.set_steps([async_add_one, async_add_one])
    
    result = await p.run({"n": 10})
    assert result["n"] == 12

@pytest.mark.asyncio
async def test_async_pipeline_parallel():
    """Prueba ejecución asíncrona."""
    p = PipelineAsync()
    p.set_steps([async_add_one])
    
    result = await p.run({"n": 5})
    assert result["n"] == 6

@pytest.mark.asyncio
async def test_async_pipeline_error():
    """Prueba manejo de errores en pipeline asíncrono."""
    async def async_fail(data):
        raise RuntimeError("Async failure")
        
    p = PipelineAsync(continue_on_error=True)
    p.set_steps([async_fail, async_add_one])
    
    result = await p.run({"n": 0})
    assert "error" in result
    assert result["n"] == 1
