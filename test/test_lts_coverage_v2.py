import os
import sqlite3
import pytest
import json
import time
from datetime import datetime, timedelta
from wpipe import PipelineTracker, PipelineExporter, Condition, Pipeline, PipelineAsync
from wpipe.tracking.analysis import AnalysisManager
from wpipe.tracking.queries import QueryManager
from wpipe.type_hinting.validators import TypeValidator
from wpipe.sqlite.Sqlite import WSQLite
from wpipe.exception import TaskError

@pytest.fixture
def lts_db_v2():
    import tempfile
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    tracker = PipelineTracker(db_path)
    # Important: Register a pipeline to force the 'pipelines' table creation in disk
    tracker.register_pipeline("init_v2", [])
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)

# --- SQLite & CRUD Tests ---

def test_sqlite_advanced_crud(lts_db_v2):
    """Test advanced operations in WSQLite class."""
    tracker = PipelineTracker(lts_db_v2)
    db = tracker.db_pipelines 
    assert db.table_name == "pipelines"
    all_p = db.get_all()
    assert len(all_p) >= 1

# --- Analysis & Queries Tests ---

def test_analysis_comprehensive_stats(lts_db_v2):
    """Test real statistical methods in AnalysisManager."""
    tracker = PipelineTracker(lts_db_v2)
    
    # Fill data
    reg = tracker.register_pipeline("analysis_test", [])
    tracker.complete_pipeline(reg["pipeline_id"])
    
    analysis = tracker.analysis
    # Use real method names
    stats = analysis.get_stats()
    assert stats["total_pipelines"] >= 1
    
    trends = analysis.get_trend_data(days=1)
    assert len(trends) >= 1
    
    p_analysis = analysis.get_pipelines_analysis()
    assert p_analysis["total_runs"] >= 1
    
    s_analysis = analysis.get_states_analysis()
    assert "total_states" in s_analysis

def test_queries_advanced(lts_db_v2):
    """Test QueryManager methods."""
    tracker = PipelineTracker(lts_db_v2)
    reg = tracker.register_pipeline("query_test", [])
    tracker.add_event(reg["pipeline_id"], "custom", "test_event")
    
    events = tracker.queries.get_events(limit=5)
    assert len(events) >= 1
    
    # Verify we can get by status
    pipes = tracker.queries.get_pipelines(status="completed")
    assert isinstance(pipes, list)

# --- Type Hinting Tests ---

def test_type_validators_robust():
    """Test runtime type validation logic."""
    validator = TypeValidator()
    assert validator.validate({"a": 1}, dict) == {"a": 1}
    with pytest.raises(TypeError):
        validator.validate("string", int)

# --- Exporter Robustness ---

def test_exporter_robustness_v2(lts_db_v2):
    """Test exporter with real data and schema confirmation."""
    tracker = PipelineTracker(lts_db_v2)
    # Ensure there is at least one completed execution
    reg = tracker.register_pipeline("export_target", [])
    tracker.complete_pipeline(reg["pipeline_id"])

    # Wait to ensure SQLite disk sync
    time.sleep(0.2)

    exporter = PipelineExporter(lts_db_v2)
    stats = json.loads(exporter.export_statistics())
    assert stats["total_executions"] >= 1

    logs = exporter.export_pipeline_logs(format="json")
    assert "export_target" in logs

# --- Pipeline Edge Cases ---

def test_pipeline_sequential_robust():
    """Test sequential pipeline execution."""
    pipe = Pipeline(pipeline_name="Seq_Test")
    pipe.set_steps([(lambda d: {"res": "ok"}, "step1", "v1")])
    res = pipe.run({})
    assert res["res"] == "ok"

@pytest.mark.asyncio
async def test_async_condition_advanced():
    """Test conditions in async pipeline."""
    async def step_ok(d): return {"status": "ok"}
    cond = Condition("x == 1", [(step_ok, "ok", "v1")])
    pipe = PipelineAsync(pipeline_name="Async_Cond")
    pipe.set_steps([cond])
    res = await pipe.run({"x": 1})
    assert res["status"] == "ok"
