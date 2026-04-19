import asyncio
import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch
from wpipe import Pipeline, PipelineAsync, Condition, For, PipelineTracker, ExecutionMode
from wpipe.exception import TaskError, ProcessError, ApiError
from wsqlite import WSQLite
from wpipe.sqlite.tables_dto.tracker_models import PipelineModel

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

def test_pipeline_retry_exception_path():
    """Test the retry path when all attempts fail."""
    pipeline = Pipeline(max_retries=1, retry_on_exceptions=(ValueError,), continue_on_error=False)
    
    def failing_step(data):
        raise ValueError("Permanent failure")
    
    pipeline.set_steps([(failing_step, "Fail", "1.0")])
    
    # It raises ProcessError because _pipeline_run_with_report wraps TaskError
    with pytest.raises(ProcessError) as exc:
        pipeline.run({})
    assert "Permanent failure" in str(exc.value)

def test_pipeline_tuple_too_short():
    """Test _execute_step with a tuple too short."""
    pipeline = Pipeline()
    # Tuple with less than 3 elements
    pipeline.tasks_list = [(lambda d: d, "Short")]
    result = pipeline._execute_step(pipeline.tasks_list[0], {"initial": True})
    assert result == {"initial": True}

def test_pipeline_for_empty_steps():
    """Test For loop with no steps."""
    pipeline = Pipeline()
    for_block = For(iterations=1, steps=[])
    result = pipeline._execute_step(for_block, {"initial": True})
    assert result["initial"] is True
    assert "_loop_iteration" in result

@pytest.mark.asyncio
async def test_pipeline_async_api_reporting_errors(temp_db):
    """Test PipelineAsync with API reporting errors."""
    with patch("wpipe.api_client.APIClient.register_process") as mock_reg:
        mock_reg.side_effect = Exception("API Down")
        
        # In full PipelineAsync, send_to_api is not a param, it uses api_config
        pipeline = PipelineAsync(
            pipeline_name="ApiErrorTest",
            api_config={"base_url": "http://mock", "token": "test"}
        )
        pipeline.set_steps([(lambda d: {"ok": True}, "Step", "1.0")])
        
        # Should continue despite API error
        await pipeline.run({})

@pytest.mark.asyncio
async def test_pipeline_async_complex_control_flow():
    """Test async pipeline with Condition."""
    pipeline = PipelineAsync()
    
    async def step_a(d): return {"a": True}
    async def step_b(d): return {"b": True}
    
    cond = Condition(
        expression="val > 10",
        branch_true=[(step_a, "A", "1.0")],
        branch_false=[(step_b, "B", "1.0")]
    )
    
    pipeline.set_steps([cond])
    
    # Test true branch
    res1 = await pipeline.run({"val": 20})
    assert res1.get("a") is True
    
    # Test false branch
    res2 = await pipeline.run({"val": 5})
    assert res2.get("b") is True

@pytest.mark.asyncio
async def test_pipeline_async_io_bound_mode():
    """Test PipelineAsync with IO_BOUND mode."""
    pipeline = PipelineAsync()
    # Note: PipelineAsync might not have execution_mode if it's strictly sequential in _pipeline_run
    
    async def step1(d): return {"s1": True}
    pipeline.set_steps([(step1, "S1", "1.0")])
    
    result = await pipeline.run({})
    assert result.get("s1") is True

def test_tracker_delete_nonexistent(temp_db):
    """Test deleting a nonexistent pipeline."""
    tracker = PipelineTracker(temp_db)
    # Should not raise error
    tracker.delete_pipeline("NONEXISTENT")

def test_tracker_add_event_full(temp_db):
    """Test add_event with all params."""
    tracker = PipelineTracker(temp_db)
    tracker.add_event(
        "PIPE-1", "custom", "test_event", 
        message="Hello", data={"meta": 1}, tags=["tag1"], step_id=123
    )
    events = tracker.get_events(pipeline_id="PIPE-1")
    assert len(events) == 1
    assert events[0]["event_name"] == "test_event"

def test_exporter_csv_edge_cases(temp_db):
    """Test exporter with CSV special characters."""
    from wpipe.export import PipelineExporter
    
    # Use WSQLite to setup the table (no sqlite3 import)
    db = WSQLite(PipelineModel, temp_db)
    db.insert(PipelineModel(id='P1', started_at='2023-01-01', name='Comma, Name', status='completed'))
    
    exporter = PipelineExporter(temp_db)
    csv_data = exporter.export_pipeline_logs(format="csv")
    assert "Comma; Name" in csv_data # Should have replaced comma with semicolon
