import pytest
import time
import sqlite3
import threading
from wpipe import Pipeline, Condition, For, Parallel, step

# --- RE-PARCHE DE EMERGENCIA PARA ARREGLAR BUG DE WPIPE ---
import wsqlite
from wsqlite import WSQLite

_db_connections = {}
_db_lock = threading.Lock()

def better_get_connection(self):
    # Buscamos db_path en __dict__ o usamos un default
    db_path = getattr(self, "db_path", getattr(self, "db_name", "register.db"))
    with _db_lock:
        if db_path not in _db_connections:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            _db_connections[db_path] = conn
        return _db_connections[db_path]

# Aplicamos el parche sobre el parche roto de wpipe
WSQLite._get_connection = better_get_connection

# --- MOCKS PARA PASOS ---

@step()
def add_one(data):
    """Suma 1 al valor 'n' en el contexto."""
    n = data.get("n", 0)
    return {"n": n + 1}

@step()
def multiply_by_two(data):
    """Multiplica por 2 el valor 'n' en el contexto."""
    n = data.get("n", 0)
    return {"n": n * 2}

# --- TESTS ---

def test_basic_pipeline():
    """Prueba un pipeline lineal simple."""
    p = Pipeline(worker_name="test_worker")
    p.set_steps([
        (add_one, "add", "1.0"),
        (multiply_by_two, "mul", "1.0")
    ])
    
    result = p.run({"n": 5})
    # (5 + 1) * 2 = 12
    assert result["n"] == 12

def test_pipeline_with_condition():
    """Prueba el bloque de condición (True y False)."""
    # Rama True
    cond_true = Condition(
        expression="n > 10",
        branch_true=[multiply_by_two],
        branch_false=[add_one]
    )
    
    p_true = Pipeline()
    p_true.set_steps([cond_true])
    res_true = p_true.run({"n": 15})
    assert res_true["n"] == 30
    
    # Rama False
    p_false = Pipeline()
    p_false.set_steps([cond_true])
    res_false = p_false.run({"n": 5})
    assert res_false["n"] == 6

def test_pipeline_with_for_iterations():
    """Prueba el bucle For basado en iteraciones fijas."""
    loop = For(iterations=3, steps=[add_one])
    
    p = Pipeline()
    p.set_steps([loop])
    result = p.run({"n": 0})
    assert result["n"] == 3

def test_pipeline_with_for_expression():
    """Prueba el bucle For basado en expresión lógica."""
    loop = For(validation_expression="n < 10", steps=[add_one])
    
    p = Pipeline()
    p.set_steps([loop])
    result = p.run({"n": 5})
    assert result["n"] == 10

def test_pipeline_parallel_threads():
    """Prueba la ejecución en paralelo usando hilos."""
    @step()
    def slow_step(data):
        time.sleep(0.05)
        return {"done": True}

    parallel = Parallel(steps=[slow_step, slow_step, slow_step], max_workers=3)
    
    p = Pipeline()
    p.set_steps([parallel])
    
    start = time.time()
    result = p.run({})
    end = time.time()
    
    assert result.get("done") is True
    assert (end - start) < 0.15

def test_pipeline_error_handling():
    """Prueba la captura de errores y continue_on_error."""
    def failing_task(data):
        raise ValueError("Intentional error")
        
    p = Pipeline(continue_on_error=True)
    p.set_steps([failing_task, add_one])
    
    result = p.run({"n": 10})
    assert "error" in result
    assert result["n"] == 11

def test_pipeline_stop_on_error():
    """Prueba que el pipeline se detenga si continue_on_error=False."""
    def failing_task(data):
        raise ValueError("Stop here")
        
    p = Pipeline(continue_on_error=False)
    p.set_steps([failing_task, add_one])
    
    with pytest.raises(Exception):
        p.run({"n": 10})
