
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
import json
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from wpipe.pipe.pipe_async import PipelineAsync, _is_async_callable
from wpipe.dashboard.main import create_app, get_dashboard_html
from wpipe.parallel.executor import ParallelExecutor, ExecutionMode, StepDependency, DAGScheduler
from wpipe.pipe.pipe import Pipeline, Condition, For, TaskError, ApiError, Codes

# Module-level functions for multiprocessing compatibility
def _io_step(c): return {"io": True}
def _cpu_step(c): return {"cpu": True}

# --- Tests for wpipe/pipe/pipe_async.py ---

@pytest.mark.asyncio
async def test_pipe_async_coverage():
    # Test _is_async_callable
    assert _is_async_callable(lambda: None) is False
    async def async_fn(): pass
    assert _is_async_callable(async_fn) is True
    
    class AsyncCallable:
        async def __call__(self): pass
    assert _is_async_callable(AsyncCallable()) is True

    # Initialize PipelineAsync with mocked tracker to avoid DB issues
    with patch('wpipe.pipe.pipe_async.PipelineTracker') as MockTracker, \
         patch.object(PipelineAsync, 'register_process', return_value={"sons": [], "father": "dad"}), \
         patch.object(PipelineAsync, 'update_task', return_value={}), \
         patch.object(PipelineAsync, 'end_process', return_value=True):
         
        pipe = PipelineAsync(
            worker_id="123456",
            api_config={"base_url": "http://api", "token": "tok"},
            verbose=True
        )
        pipe.tracker = MockTracker.return_value
        pipe.SHOW_API_ERRORS = True
        PipelineAsync.SHOW_API_ERRORS = True # Also set on class
        
        # Line 138: _api_task_update exception
        with patch.object(pipe, 'update_task', side_effect=Exception("API Fail")):
            pipe.send_to_api = True
            with pytest.raises(ApiError):
                pipe._api_task_update({"status": "start"})
        pipe.send_to_api = False
                
        # Lines 149-150, 168, 172-173: _api_process_update exceptions
        pipe.send_to_api = True
        with patch.object(PipelineAsync, 'register_process', side_effect=Exception("API Fail")):
            with pytest.raises(ApiError):
                pipe._api_process_update({}, start=True)

        with patch.object(PipelineAsync, 'end_process', return_value=False):
            with pytest.raises(ApiError):
                pipe._api_process_update({}, start=False)
        pipe.send_to_api = False

        # _task_invoke_with_report error traceback (lines 189-207)
        async def fail_task(data):
            raise ValueError("Task Failed")
        
        pipe.task_id = "task1"
        with patch.object(pipe, 'update_task'):
            with pytest.raises(TaskError) as excinfo:
                await pipe._task_invoke_with_report(fail_task, {})
            assert "Task Failed" in str(excinfo.value)

        # _pipeline_run_with_report (lines 211-219, 233-236)
        with patch.object(pipe, '_pipeline_run', side_effect=TaskError("TE", Codes.TASK_FAILED)):
            pipe.continue_on_error = True
            res = await pipe._pipeline_run_with_report({})
            assert "error" in res

        with patch.object(pipe, '_pipeline_run', side_effect=ApiError("AE", Codes.API_ERROR)):
            with pytest.raises(ApiError):
                await pipe._pipeline_run_with_report({})

        # set_steps (lines 243-247, 251)
        def dummy_task(data): return {}
        pipe.set_steps([(dummy_task, "name", "v1")])
        assert len(pipe.tasks_list) == 1
        
        cond = Condition("True", [(dummy_task, "name", "v1")], [])
        pipe.set_steps([cond])
        assert isinstance(pipe.tasks_list[0], Condition)
        
        with pytest.raises(ValueError):
            pipe.set_steps(["invalid"])

        # _run_branch Condition errors (lines 269-317)
        pipe.pipeline_id = "pipe1"
        pipe.tracker.start_step.return_value = None
        bad_cond = Condition("1/0", [], [])
        data, ids = await pipe._run_branch([bad_cond], {})
        # ids may contain None from mocked tracker.start_step, filter to check no real ids
        assert [i for i in ids if i] == []

        # Condition success branch
        good_cond = Condition("True", [(dummy_task, "task_true", "v1")], [])
        with patch.object(pipe, '_task_invoke', AsyncMock(return_value={})):
            data, ids = await pipe._run_branch([good_cond], {})
            assert len(ids) >= 1

        # _execute_with_retry (lines 364-365, 385)
        pipe.max_retries = 1
        pipe.retry_delay = 0.01
        count = 0
        async def retry_task(data):
            nonlocal count
            count += 1
            if count == 1: raise ValueError("Retry me")
            return {"ok": True}
        
        res = await pipe._execute_with_retry(retry_task, "retry", {})
        assert res == {"ok": True}
        assert count == 2

        # _task_invoke (lines 405, 437, 441)
        with pytest.raises(TaskError):
            await pipe._task_invoke(fail_task, "fail", {})

        # PipelineAsync worker registration
        with patch.object(pipe, 'register_worker', return_value={"id": "new_id"}):
            pipe.tasks_list = [(lambda d: {}, "name", "v1", "id")]
            res = pipe.worker_register("test", "1.0")
            assert res["id"] == "new_id"

        # _execute_with_retry failure (all retries failed)
        pipe.max_retries = 1
        pipe.retry_delay = 0
        async def fail_retry(data): raise ValueError("Always Fail")
        with pytest.raises(ValueError):
            await pipe._execute_with_retry(fail_retry, "fail", {})

        # run with initial error (lines 945)
        with pytest.raises(TaskError):
            await pipe.run({"error": "Init fail"})

        # set_steps normalize_step (lines 243-247)
        pipe.set_steps([(lambda d: {}, "s1", "v1")])
        assert len(pipe.tasks_list[0]) == 4
        
        # ParallelExecutor more coverage
        exec = ParallelExecutor(max_workers=2)
        exec.add_step("io", _io_step, mode=ExecutionMode.SEQUENTIAL)
        exec.add_step("cpu", _cpu_step, mode=ExecutionMode.SEQUENTIAL)
        res = exec.execute({})
        assert res["io"] is True and res["cpu"] is True
        assert len(exec.get_results()) == 2
        assert exec.get_execution_time() == 0.0
        
        # Full mock run of PipelineAsync
        async def step1(d): return {"s1": True}
        async def step2(d): return {"s2": True}
        pipe.set_steps([(step1, "s1", "v1"), (step2, "s2", "v1")])
        res = await pipe._pipeline_run({"input": 1})
        assert res["s1"] is True and res["s2"] is True
        
        # PipelineAsync continue_on_error
        pipe.continue_on_error = True
        async def fail_step(d): raise ValueError("Oops")
        pipe.set_steps([(fail_step, "fail", "v1")])
        res = await pipe._pipeline_run({})
        assert "error" in res
        
        # PipelineAsync nested pipeline
        nested = PipelineAsync(worker_id="nest")
        nested.set_steps([(step1, "n1", "v1")])
        pipe.set_steps([(nested.run, "nested", "v1")])
        with patch.object(nested, 'register_process', return_value={"sons": [], "father": "f"}):
            with patch.object(nested, 'end_process', return_value=True):
                res = await pipe._pipeline_run({})
                assert res["s1"] is True

def test_dashboard_coverage():
    app = create_app(db_path=":memory:")
    client = TestClient(app)
    
    # Lines 67->70: Static files (covered if static dir exists, we can mock it)
    
    # API endpoints
    with patch('wpipe.dashboard.main.PipelineTracker') as MockTracker:
        tracker = MockTracker.return_value
        tracker.get_stats.return_value = {"stats": "ok"}
        tracker.get_pipelines.return_value = []
        tracker.get_table_data.return_value = []
        tracker.get_pipeline.return_value = {"config_yaml": "nonexistent.yaml"}
        tracker.get_pipeline_executions.return_value = []
        tracker.get_pipeline_graph.return_value = {}
        tracker.get_trend_data.return_value = []
        tracker.get_fired_alerts.return_value = []
        tracker.get_alert_thresholds.return_value = {}
        tracker.get_events.return_value = []
        tracker.get_top_slow_steps.return_value = []
        tracker.get_states_analysis.return_value = {}
        tracker.get_pipelines_analysis.return_value = {}
        
        assert client.get("/api/stats").status_code == 200
        assert client.get("/api/pipelines").status_code == 200
        assert client.get("/api/data/pipelines").status_code == 200
        assert client.get("/api/pipelines/1").status_code == 200
        assert client.get("/api/pipelines/by-name/test").status_code == 200
        assert client.get("/api/pipelines/1/graph").status_code == 200
        assert client.get("/api/pipelines/1/yaml").status_code == 200
        assert client.get("/api/trends").status_code == 200
        assert client.get("/api/alerts").status_code == 200
        assert client.get("/api/alerts/config").status_code == 200
        assert client.get("/api/events").status_code == 200
        assert client.get("/api/slow-steps").status_code == 200
        assert client.get("/api/analysis/states").status_code == 200
        assert client.get("/api/analysis/pipelines").status_code == 200
        assert client.post("/api/alerts/1/acknowledge").status_code == 200
        assert client.get("/api/health").status_code == 200

    # Line 126-132: get_pipeline_yaml logic
    with patch('wpipe.dashboard.main.PipelineTracker') as MockTracker:
        tracker = MockTracker.return_value
        tracker.get_pipeline.return_value = {"config_yaml": "exists.yaml"}
        with patch('wpipe.dashboard.main.Path.exists', return_value=True):
            with patch('wpipe.dashboard.main.Path.read_text', return_value="yaml content"):
                assert client.get("/api/pipelines/1/yaml").json() == "yaml content"

    # Line 187-189: get_dashboard_html fallback
    with patch('wpipe.dashboard.main.jinja_env.get_template', side_effect=Exception("Template Fail")):
        html = get_dashboard_html(":memory:")
        assert "Dashboard Error" in html

# --- Tests for wpipe/parallel/executor.py ---

def test_parallel_executor_coverage():
    # Lines 36, 39-41: StepDependency hash and eq
    s1 = StepDependency("s1", lambda x: x)
    s2 = StepDependency("s1", lambda x: x)
    s3 = StepDependency("s3", lambda x: x)
    assert hash(s1) == hash(s2)
    assert s1 == s2
    assert s1 != s3
    assert s1 == "s1"

    # Line 62: DAGScheduler.add_step dependency not in graph
    dag = DAGScheduler()
    dag.add_step(StepDependency("b", lambda x: x, dependencies=["a"]))
    assert "a" in dag.graph

    # ParallelExecutor.execute sequential (lines 194->154, 197-200)
    exec = ParallelExecutor(max_workers=2)
    def task_seq(ctx): return {"seq": True}
    exec.add_step("s1", task_seq, mode=ExecutionMode.SEQUENTIAL)
    res = exec.execute({})
    assert res["seq"] is True

    # Exception in _execute_step (lines 213-215, 224, 228, 232)
    def fail_task(ctx): raise ValueError("Fail")
    exec = ParallelExecutor()
    exec.add_step("fail", fail_task, mode=ExecutionMode.IO_BOUND)
    with pytest.raises(ValueError):
        exec.execute({})
        
    # _execute_step_safe (lines 241-245)
    res = exec._execute_step_safe(StepDependency("safe", lambda x: {"ok": True}), {})
    assert res["ok"] is True

# --- Tests for wpipe/pipe/pipe.py ---

def test_pipe_coverage():
    with patch('wpipe.pipe.pipe.PipelineTracker') as MockTracker, \
         patch.object(Pipeline, 'register_process', return_value={"sons": [], "father": "dad"}), \
         patch.object(Pipeline, 'update_task', return_value={}), \
         patch.object(Pipeline, 'end_process', return_value=True):
         
        pipe = Pipeline(
            worker_id="123456",
            api_config={"base_url": "http://api", "token": "tok"},
            verbose=True
        )
        pipe.tracker = MockTracker.return_value
        pipe.SHOW_API_ERRORS = True
        
        # Retry logic branches
        pipe.max_retries = 1
        pipe.retry_delay = 0
        count = 0
        def retry_task(data):
            nonlocal count
            count += 1
            if count == 1: raise ValueError("Retry")
            return {"ok": True}
        
        res = pipe._execute_with_retry(retry_task, "retry", {})
        assert res["ok"] is True
        assert count == 2

        # API reporting branches
        with patch.object(Pipeline, 'update_task', side_effect=Exception("API")):
            pipe.send_to_api = True
            with pytest.raises(ApiError):
                pipe._api_task_update({"status": "start"})
        pipe.send_to_api = False

        # For loop coverage
        def loop_task(data):
            data["count"] = data.get("count", 0) + 1
            return data
            
        for_loop = For(iterations=2, steps=[(loop_task, "loop", "v1")])
        pipe.set_steps([for_loop])
        res = pipe._pipeline_run({"count": 0})
        assert res["count"] == 2

        # For with validation_expression
        for_loop2 = For(validation_expression="count < 5", steps=[(loop_task, "loop2", "v1")])
        res = pipe._execute_step(for_loop2, {"count": 0})
        assert res["count"] == 5

        # Condition branch false
        cond = Condition("False", [], [(loop_task, "false_task", "v1")])
        pipe.set_steps([cond])
        res = pipe._pipeline_run({"count": 0})
        assert res["count"] == 1

        # add_state and steps property
        pipe.add_state("test_state", lambda d: {"state_run": True})
        assert len(pipe.steps) >= 1
        assert pipe.steps[-1].name == "test_state"
        
        # Checkpoint logic (mocking checkpoint_mgr)
        mock_cp_mgr = MagicMock()
        mock_cp_mgr.can_resume.return_value = True
        mock_cp_mgr.get_last_checkpoint.return_value = {"step_order": 0, "data": {"restarted": True}}
        pipe.set_steps([(lambda d: {"done": True}, "done_task", "v1")])
        res = pipe._pipeline_run({"initial": True}, checkpoint_mgr=mock_cp_mgr, checkpoint_id="cp1")
        assert res.get("restarted") is True

        # Alert hooks
        pipe.tracker.complete_step.return_value = [(lambda d: {"hooked": True}, "hook", "v1")]
        pipe.set_steps([(lambda d: {"step": 1}, "s1", "v1")])
        res = pipe._pipeline_run({})
        assert res.get("hooked") is True

def test_start_dashboard_coverage():
    from wpipe.dashboard.main import start_dashboard
    with patch('uvicorn.run'):
        with patch('webbrowser.open'):
            # This is hard to test fully because of the thread, but we can hit the lines
            start_dashboard(open_browser=True, port=9999)

