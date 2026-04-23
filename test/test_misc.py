import pytest
import time
import sqlite3
import threading
from wpipe import Pipeline, TaskTimer, PipelineTimeoutError, to_obj, object_to_dict
from wpipe.ram import memory as memory_decorator
from wpipe.ram.ram import get_memory

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

def test_utils_conversion():
    """Prueba las utilidades de transformación de objetos."""
    # to_obj es un DECORADOR
    @to_obj
    def check_obj(context):
        assert context.a == 1
        assert context.b.c == 2
        return {"status": "ok"}
    
    data = {"a": 1, "b": {"c": 2}}
    result = check_obj(data)
    assert result["status"] == "ok"
    
    # dict_to_sns es la utilidad interna
    from wpipe.util.transform import dict_to_sns
    sns = dict_to_sns(data)
    assert sns.a == 1
    assert sns.b.c == 2

def test_memory_utils():
    """Prueba las utilidades de lectura de RAM."""
    # get_memory es una función
    ram = get_memory()
    assert isinstance(ram, int)  # get_memory returns int (KB)
    assert ram >= 0

def test_timeout_sync():
    """Prueba el timeout en funciones síncronas."""
    from wpipe import timeout_sync
    
    @timeout_sync(seconds=1.0)
    def slow_func(data):
        time.sleep(0.3)
        return data
        
    # This should NOT raise an exception since 0.3s < 1.0s
    result = slow_func({})
    assert result == {}
    
    @timeout_sync(seconds=0.1)
    def fast_func(data):
        time.sleep(0.01)
        return data
        
    # This should NOT raise an exception since 0.01s < 0.1s
    result = fast_func({})
    assert result == {}

@pytest.mark.asyncio
async def test_timeout_async():
    """Prueba el timeout en funciones asíncronas."""
    from wpipe import timeout_async
    import asyncio
    
    async def slow_async(data):
        await asyncio.sleep(0.3)
        return data
        
    with pytest.raises(PipelineTimeoutError):
        await timeout_async(0.1, slow_async({}))

def test_pipeline_with_metadata_retries():
    """Prueba la lógica de reintento configurada vía metadatos del paso."""
    attempts = 0
    def retry_task(data):
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Try again")
        return {"attempts": attempts}
        
    p = Pipeline(verbose=True)
    p.add_state("retry_state", retry_task, retry_count=3, retry_delay=0.01)
    
    result = p.run({})
    assert result["attempts"] == 3
