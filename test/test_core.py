import pytest
import time
import sqlite3
import threading
from typing import Dict, Any, List, Optional, Callable

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
def add_one(data: Dict[str, Any]) -> Dict[str, int]:
    """Adds 1 to the 'n' value in the context.

    Args:
        data: A dictionary potentially containing an integer value for 'n'.
              Defaults to 0 if 'n' is not found.

    Returns:
        A dictionary with the incremented 'n' value.
    """
    n: int = data.get("n", 0)
    return {"n": n + 1}

@step()
def multiply_by_two(data: Dict[str, Any]) -> Dict[str, int]:
    """Multiplies the 'n' value in the context by 2.

    Args:
        data: A dictionary potentially containing an integer value for 'n'.
              Defaults to 0 if 'n' is not found.

    Returns:
        A dictionary with the 'n' value multiplied by 2.
    """
    n: int = data.get("n", 0)
    return {"n": n * 2}

# --- TESTS ---

def test_basic_pipeline() -> None:
    """Tests a simple linear pipeline.

    Verifies that a pipeline with sequential steps correctly processes input
    data and produces the expected output.
    """
    pipeline = Pipeline(worker_name="test_worker")
    pipeline.set_steps([
        (add_one, "add", "1.0"),
        (multiply_by_two, "mul", "1.0")
    ])
    
    initial_data: Dict[str, int] = {"n": 5}
    result = pipeline.run(initial_data)
    # Calculation: (5 + 1) * 2 = 12
    assert result["n"] == 12

def test_pipeline_with_condition() -> None:
    """Tests the Condition block for both True and False branches.

    Verifies that the pipeline correctly executes the 'branch_true' or
    'branch_false' based on the evaluation of the 'expression'.
    """
    # Branch True execution scenario
    condition_true_branch = Condition(
        expression="n > 10",
        branch_true=[multiply_by_two], # This step will be executed
        branch_false=[add_one]         # This step will be skipped
    )
    
    pipeline_true = Pipeline()
    pipeline_true.set_steps([condition_true_branch])
    initial_data_true: Dict[str, int] = {"n": 15}
    result_true = pipeline_true.run(initial_data_true)
    assert result_true["n"] == 30 # Expected: 15 * 2 = 30
    
    # Branch False execution scenario
    condition_false_branch = Condition(
        expression="n > 10",
        branch_true=[multiply_by_two], # This step will be skipped
        branch_false=[add_one]         # This step will be executed
    )

    pipeline_false = Pipeline()
    pipeline_false.set_steps([condition_false_branch])
    initial_data_false: Dict[str, int] = {"n": 5}
    result_false = pipeline_false.run(initial_data_false)
    assert result_false["n"] == 6 # Expected: 5 + 1 = 6

def test_pipeline_with_for_iterations() -> None:
    """Tests the For loop construct based on a fixed number of iterations.

    Ensures that the pipeline executes the defined steps multiple times as
    specified by the 'iterations' parameter.
    """
    loop = For(iterations=3, steps=[add_one])
    
    pipeline = Pipeline()
    pipeline.set_steps([loop])
    initial_data: Dict[str, int] = {"n": 0}
    result = pipeline.run(initial_data)
    assert result["n"] == 3 # 0 + 1 + 1 + 1 = 3

def test_pipeline_with_for_expression() -> None:
    """Tests the For loop construct based on a logical expression.

    Verifies that the 'validation_expression' controls the number of loop
    iterations, stopping when the expression evaluates to False.
    """
    loop = For(validation_expression="n < 10", steps=[add_one])
    
    pipeline = Pipeline()
    pipeline.set_steps([loop])
    initial_data: Dict[str, int] = {"n": 5}
    result = pipeline.run(initial_data)
    assert result["n"] == 10 # 5 + 1 + 1 + 1 + 1 + 1 = 10 (stops when n=10)

def test_pipeline_parallel_threads() -> None:
    """Tests parallel execution of steps using threads.

    Ensures that multiple steps can run concurrently, significantly reducing
    the total execution time compared to sequential execution.
    """
    @step()
    def slow_step(data: Dict[str, Any]) -> Dict[str, bool]:
        """A step that simulates work by sleeping for a short duration."""
        time.sleep(0.05)
        return {"done": True}

    parallel = Parallel(steps=[slow_step, slow_step, slow_step], max_workers=3)
    
    pipeline = Pipeline()
    pipeline.set_steps([parallel])
    
    start_time = time.time()
    result = pipeline.run({})
    end_time = time.time()
    
    assert result.get("done") is True
    # Expecting execution time to be slightly more than one slow_step execution
    # due to parallelism, not the sum of all three.
    assert (end_time - start_time) < 0.15

def test_pipeline_error_handling() -> None:
    """Tests error handling with 'continue_on_error=True'.

    Ensures that if a step fails, the pipeline records the error and continues
    executing subsequent steps.
    """
    def failing_task(data: Dict[str, Any]) -> Dict[str, Any]:
        """A task designed to intentionally raise a ValueError."""
        raise ValueError("Intentional error")
        
    pipeline = Pipeline(continue_on_error=True)
    pipeline.set_steps([failing_task, add_one])
    
    initial_data: Dict[str, int] = {"n": 10}
    result = pipeline.run(initial_data)
    assert "error" in result # Checks if error information is captured
    assert result["n"] == 11 # Checks if the subsequent step executed

def test_pipeline_stop_on_error() -> None:
    """Tests pipeline behavior when 'continue_on_error=False'.

    Verifies that the pipeline stops execution immediately if any step raises
    an exception and `continue_on_error` is set to False.
    """
    def failing_task(data: Dict[str, Any]) -> Dict[str, Any]:
        """A task designed to intentionally raise a ValueError."""
        raise ValueError("Stop here")
        
    pipeline = Pipeline(continue_on_error=False)
    pipeline.set_steps([failing_task, add_one])
    
    # Expecting the pipeline to raise an exception and not complete 'add_one'
    with pytest.raises(Exception) as excinfo:
        pipeline.run({"n": 10})
    assert "Stop here" in str(excinfo.value) # Verify the exception message
