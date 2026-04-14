import pytest
import json
import asyncio
from unittest.mock import MagicMock, patch
from wpipe.pipe.pipe import Pipeline, Condition
from wpipe.pipe.pipe_async import PipelineAsync
from wpipe.exception import TaskError, ApiError, Codes, ProcessError

def test_pipeline_with_report_task_error():
    p = Pipeline(worker_id="w1")
    p.tasks_list = [lambda x: x]
    p.send_to_api = True
    p.process_id = "proc1"
    
    with patch.object(p, '_pipeline_run', side_effect=TaskError("test error", Codes.TASK_FAILED)):
        with patch.object(p, 'register_process', return_value={"father": "proc1", "sons": [{"id": "s1"}]}):
            with patch.object(p, 'update_task'):
                with patch.object(p, 'end_process'):
                    # Test without continue_on_error (default False for _pipeline_run_with_report wrapping)
                    p.continue_on_error = False
                    with pytest.raises(ProcessError):
                        p.run({})

def test_pipeline_with_report_api_error():
    p = Pipeline(worker_id="w1")
    p.send_to_api = True

    # Mock register_process to raise ApiError
    p.continue_on_error = False
    p.SHOW_API_ERRORS = True
    with patch.object(p, 'register_process', side_effect=ApiError("api fail", Codes.API_ERROR)):
        with pytest.raises(ApiError):
            p.run({})

def test_pipeline_finally_error_assignment():
    p = Pipeline(worker_id="w1", pipeline_name="test_pipe")
    def failing_step(data):
        raise ValueError("crash")

    p.tasks_list = [failing_step]
    p.tracker = MagicMock()
    p.pipeline_id = "p1"
    p.continue_on_error = False

    with pytest.raises(TaskError):
        p._pipeline_run({})
    
    # Verify tracker.complete_pipeline was called with error_message and error_step
    p.tracker.complete_pipeline.assert_called()
    _, kwargs = p.tracker.complete_pipeline.call_args
    assert "crash" in kwargs['error_message']
    # The error_step should be the task_name in case of Exception in _pipeline_run loop
    assert kwargs['error_step'] == p.task_name

def test_pipeline_step_error_assignment():
    p = Pipeline(worker_id="w1")
    def failing_step(data):
        raise ValueError("step crash")
    failing_step.NAME = "failing_step"

    p.tasks_list = [failing_step]
    p.tracker = MagicMock()
    p.pipeline_id = "p1"
    p.continue_on_error = True

    data = p._pipeline_run({})
    assert "error" in data
    assert "crash" in str(data['error'])

    p.tracker.complete_pipeline.assert_called()
    _, kwargs = p.tracker.complete_pipeline.call_args
    assert "crash" in kwargs['error_message']
    assert kwargs['error_step'] == "failing_step"

@pytest.mark.asyncio
async def test_pipeline_async_error_handling():
    pa = PipelineAsync(worker_id="aw1", pipeline_name="async_pipe")
    async def failing_step(data):
        raise ValueError("async crash")
    failing_step.NAME = "async_failing_step"

    pa.tasks_list = [(failing_step, "async_failing_step", "1.0", "")]
    pa.tracker = MagicMock()
    pa.pipeline_id = "ap1"
    pa.continue_on_error = False

    with pytest.raises(TaskError):
        await pa._pipeline_run({})

    pa.tracker.complete_pipeline.assert_called()
    _, kwargs = pa.tracker.complete_pipeline.call_args
    assert "async crash" in kwargs['error_message']
    assert kwargs['error_step'] == pa.task_name

@pytest.mark.asyncio
async def test_pipeline_async_with_report_task_error():
    pa = PipelineAsync(worker_id="aw1")
    pa.send_to_api = True
    pa.continue_on_error = False
    pa.process_id = "aproc1"

    async def dummy_task(data): return data
    pa.tasks_list = [(dummy_task, "name", "v1")]

    with patch.object(pa, '_pipeline_run', side_effect=TaskError("async task error", Codes.TASK_FAILED)):
        with patch.object(pa, 'register_process', return_value={"father": "aproc1", "sons": [{"id": "as1"}]}):
            with patch.object(pa, 'end_process', return_value=True):
                with pytest.raises(ProcessError):
                    await pa.run({})

@pytest.mark.asyncio
async def test_pipeline_async_with_report_api_error():
    pa = PipelineAsync(worker_id="aw1")
    pa.send_to_api = True
    pa.continue_on_error = False
    pa.SHOW_API_ERRORS = True
    with patch.object(pa, 'register_process', side_effect=ApiError("api fail", Codes.API_ERROR)):
        with pytest.raises(ApiError):
            await pa.run({})

def test_pipeline_continue_on_error_with_report():
    p = Pipeline(worker_id="w1")
    p.send_to_api = True
    p.continue_on_error = True
    p.tasks_list = [(lambda x: x, "name", "v1")]

    with patch.object(p, '_pipeline_run', side_effect=TaskError("test error", Codes.TASK_FAILED)):
        with patch.object(p, 'register_process', return_value={"father": "p1", "sons": [{"id": "s1"}]}):
            with patch.object(p, 'end_process', return_value=True):
                result = p.run({})
                assert "error" in result
                assert "test error" in result["error"]["message"]

@pytest.mark.asyncio
async def test_pipeline_async_continue_on_error_with_report():
    pa = PipelineAsync(worker_id="aw1")
    pa.send_to_api = True
    pa.continue_on_error = True

    async def dummy_task(data): return data
    pa.tasks_list = [(dummy_task, "name", "v1")]

    with patch.object(pa, '_pipeline_run', side_effect=TaskError("async error", Codes.TASK_FAILED)):
        with patch.object(pa, 'register_process', return_value={"father": "ap1", "sons": [{"id": "as1"}]}):
            with patch.object(pa, 'end_process', return_value=True):
                result = await pa.run({})
                assert "error" in result
                assert "async error" in result["error"]["message"]
