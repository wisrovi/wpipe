import pytest
from datetime import datetime, timedelta
import time
from wpipe.tracking.tracker import PipelineTracker, Metric, Severity
from wpipe.tracking.alerts import AlertManager
from wpipe.tracking.analysis import AnalysisManager
from wpipe.tracking.queries import QueryManager

@pytest.fixture
def tracker(tmp_path):
    db_path = str(tmp_path / "test_tracking.db")
    config_dir = str(tmp_path / "configs")
    return PipelineTracker(db_path=db_path, config_dir=config_dir)

def test_tracker_pipeline_registration_and_completion(tracker):
    # Register pipeline
    steps = [
        {"type": "task", "name": "step1"},
        (lambda x: x, "step2", "v1", {}),
        "step3_string"
    ]
    reg = tracker.register_pipeline("TestPipe", steps, input_data={"start": True}, parent_pipeline_id="parent_123")
    pipe_id = reg["pipeline_id"]
    
    # Check queries
    pipes = tracker.get_pipelines()
    assert len(pipes) == 1
    
    pipe_info = tracker.get_pipeline(pipe_id)
    assert pipe_info["name"] == "TestPipe"
    
    # Complete pipeline
    tracker.complete_pipeline(pipe_id, output_data={"end": True})
    
    # Test error completion
    reg2 = tracker.register_pipeline("TestPipeError", [], worker_id="w1", worker_name="worker1")
    tracker.complete_pipeline(reg2["pipeline_id"], error_message="Failed", error_step="step_x")
    
    pipe_info_err = tracker.get_pipeline(reg2["pipeline_id"])
    assert pipe_info_err["status"] == "error"

def test_tracker_steps_and_events(tracker):
    reg = tracker.register_pipeline("StepPipe", [])
    pipe_id = reg["pipeline_id"]
    
    # Start step
    step_id = tracker.start_step(pipe_id, 1, "MyStep", step_version="v2", input_data={"i": 1})
    assert step_id is not None
    
    # Complete step successfully
    tracker.complete_step(step_id, output_data={"o": 2})
    
    # Error step
    step2_id = tracker.start_step(pipe_id, 2, "ErrorStep")
    tracker.complete_step(step2_id, error_message="step fail", error_traceback="trace")
    
    # Events
    tracker.add_event(pipe_id, "info", "test_event", step_id=step_id, message="msg", data={"d": 1}, tags=["a"])
    events = tracker.get_events(pipe_id)
    assert len(events) == 1
    assert events[0]["event_name"] == "test_event"

def test_tracker_alerts(tracker):
    def my_hook(data):
        pass
    
    # Add alert
    tracker.add_alert_threshold(Metric.STEP_DURATION, ">0", Severity.WARNING, steps=[my_hook])
    thresholds = tracker.get_alert_thresholds()
    assert len(thresholds) == 1
    
    # Trigger alert
    reg = tracker.register_pipeline("AlertPipe", [])
    pipe_id = reg["pipeline_id"]
    
    step_id = tracker.start_step(pipe_id, 1, "SlowStep")
    time.sleep(0.01) # Sleep to ensure duration > 0
    tracker.complete_step(step_id)
    
    fired = tracker.get_fired_alerts()
    if fired:
        tracker.acknowledge_alert(fired[0]["id"])
    
    # Trigger pipeline alert
    tracker.add_alert_threshold(Metric.PIPELINE_DURATION, ">0", Severity.CRITICAL, steps=[my_hook])
    tracker.complete_pipeline(pipe_id)

def test_tracker_analysis_and_queries(tracker):
    reg = tracker.register_pipeline("AnalysisPipe", [])
    pipe_id = reg["pipeline_id"]
    
    step_id = tracker.start_step(pipe_id, 1, "AnaStep")
    tracker.complete_step(step_id, output_data={"x": 1})
    tracker.complete_pipeline(pipe_id)
    
    stats = tracker.get_stats()
    
    trends = tracker.get_trend_data(days=1)
    
    slow_steps = tracker.get_top_slow_steps(limit=5)
    
    states_ana = tracker.get_states_analysis()
    
    pipe_ana = tracker.get_pipelines_analysis()
    
    executions = tracker.get_pipeline_executions(limit=10)

def test_tracker_graph_and_metrics(tracker):
    reg = tracker.register_pipeline("GraphPipe", [])
    pipe_id = reg["pipeline_id"]
    
    tracker.record_system_metrics(pipe_id, {"cpu_percent": 50})
    
    step1_id = tracker.start_step(pipe_id, 1, "S1", step_type="condition")
    tracker.complete_step(step1_id, output_data={"branch_taken": True})
    
    step2_id = tracker.start_step(pipe_id, 2, "S2", parent_step_id=step1_id)
    tracker.complete_step(step2_id, output_data={"x": 1})
    
    graph = tracker.get_pipeline_graph(pipe_id)
    assert graph["pipeline_id"] == pipe_id
    assert len(graph["nodes"]) == 2
    assert len(graph["edges"]) == 1

def test_tracker_delete(tracker):
    reg = tracker.register_pipeline("DeletePipe", [])
    pipe_id = reg["pipeline_id"]
    tracker.delete_pipeline(pipe_id)
    assert tracker.get_pipeline(pipe_id) is None

def test_safe_json_dumps_complex():
    from wpipe.tracking.tracker import _safe_json_dumps
    class Unserializable:
        pass
        
    res = _safe_json_dumps({"u": Unserializable()})
    assert res == '{"u": {}}'
