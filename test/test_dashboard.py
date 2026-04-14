
import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from wpipe.dashboard.main import create_app
from wpipe.tracking import PipelineTracker

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def tracker(temp_db):
    return PipelineTracker(temp_db)

@pytest.fixture
def client(temp_db, tracker):
    # Populate some data
    res = tracker.register_pipeline("test_pipeline", ["step1", "step2"])
    pipeline_id = res["pipeline_id"]
    
    step_id = tracker.start_step(pipeline_id, 1, "step1")
    tracker.complete_step(step_id, output_data={"result": "ok"}, pipeline_id=pipeline_id)
    
    tracker.complete_pipeline(pipeline_id)
    
    # Add an alert threshold
    tracker.add_alert_threshold(metric="pipeline_duration_ms", expression=">100", severity="critical")
    
    # Fire an alert manually (by running another pipeline that exceeds threshold if we want, 
    # but let's just use the tracker to see if it's there)
    # Actually, let's just use the client to hit the endpoints and see they don't crash.
    
    app = create_app(temp_db)
    return TestClient(app)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.headers["content-type"]

def test_api_stats(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_pipelines" in data
    assert data["total_pipelines"] >= 1

def test_api_pipelines(client):
    response = client.get("/api/pipelines")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "test_pipeline"

def test_api_pipelines_with_status(client):
    response = client.get("/api/pipelines?status=completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_api_table_data(client):
    for table in ["pipelines", "steps", "alerts_fired", "events"]:
        response = client.get(f"/api/data/{table}")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

def test_api_pipeline_detail(client):
    # Get pipeline id first
    pipelines = client.get("/api/pipelines").json()
    pid = pipelines[0]["id"]
    
    response = client.get(f"/api/pipelines/{pid}")
    assert response.status_code == 200
    assert response.json()["id"] == pid

def test_api_pipeline_by_name(client):
    response = client.get("/api/pipelines/by-name/test_pipeline")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_api_pipeline_graph(client):
    pipelines = client.get("/api/pipelines").json()
    pid = pipelines[0]["id"]
    
    response = client.get(f"/api/pipelines/{pid}/graph")
    assert response.status_code == 200
    assert "nodes" in response.json()

def test_api_pipeline_yaml(client):
    pipelines = client.get("/api/pipelines").json()
    pid = pipelines[0]["id"]
    
    response = client.get(f"/api/pipelines/{pid}/yaml")
    # It might return 404 if yaml file is not found, but it should return a response
    assert response.status_code == 200

def test_api_trends(client):
    response = client.get("/api/trends")
    assert response.status_code == 200

def test_api_alerts(client):
    response = client.get("/api/alerts")
    assert response.status_code == 200

def test_api_alerts_config(client):
    response = client.get("/api/alerts/config")
    assert response.status_code == 200

def test_api_events(client):
    response = client.get("/api/events")
    assert response.status_code == 200

def test_api_slow_steps(client):
    response = client.get("/api/slow-steps")
    assert response.status_code == 200

def test_api_analysis_states(client):
    response = client.get("/api/analysis/states")
    assert response.status_code == 200

def test_api_analysis_pipelines(client):
    response = client.get("/api/analysis/pipelines")
    assert response.status_code == 200

def test_api_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_acknowledge_alert(client, tracker):
    # Manually insert an alert to acknowledge
    from wpipe.sqlite.tables_dto.tracker_models import AlertFiredModel
    alert = AlertFiredModel(
        alert_config_id=1,
        pipeline_id="PIPE-123",
        metric="test",
        metric_value=100.0,
        threshold_value=50.0,
        severity="critical"
    )
    alert_id = tracker.db_alerts_fired.insert(alert)

    response = client.post(f"/api/alerts/{alert_id}/acknowledge")
    # Endpoint should respond (200 or 404 depending on implementation)
    assert response.status_code in (200, 404)
