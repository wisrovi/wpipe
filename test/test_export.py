import pytest
import json
from pathlib import Path

from wpipe.tracking.tracker import PipelineTracker
from wpipe.export.exporter import PipelineExporter

@pytest.fixture
def tracker_and_exporter(tmp_path):
    db_path = str(tmp_path / "test_tracker.db")
    config_dir = str(tmp_path / "configs")
    tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
    exporter = PipelineExporter(db_path=db_path)
    
    # Populate data
    reg1 = tracker.register_pipeline("pipe1", [{"type": "task", "name": "step1"}])
    tracker.record_system_metrics(reg1["pipeline_id"], {"cpu_percent": 10.5})
    tracker.complete_pipeline(reg1["pipeline_id"], output_data={"status": "ok"})
    
    reg2 = tracker.register_pipeline("pipe2", [])
    tracker.record_system_metrics(reg2["pipeline_id"], {"cpu_percent": 20.0})
    tracker.complete_pipeline(reg2["pipeline_id"], error_message="Failed")
    
    return tracker, exporter, tmp_path, reg1["pipeline_id"]

def test_export_pipeline_logs(tracker_and_exporter):
    tracker, exporter, tmp_path, p1_id = tracker_and_exporter
    
    # All JSON
    res_json = exporter.export_pipeline_logs(format="json")
    data = json.loads(res_json)
    assert len(data) == 2
    
    # Specific ID JSON
    res_json_id = exporter.export_pipeline_logs(pipeline_id=p1_id, format="json")
    data_id = json.loads(res_json_id)
    assert len(data_id) == 1
    assert data_id[0]["id"] == p1_id
    
    # All CSV
    res_csv = exporter.export_pipeline_logs(format="csv")
    assert "pipe1" in res_csv
    assert "pipe2" in res_csv
    
    # Output to file JSON
    out_json = str(tmp_path / "out.json")
    res_file = exporter.export_pipeline_logs(format="json", output_path=out_json)
    assert res_file == out_json
    assert Path(out_json).exists()
    
    # Output to file CSV
    out_csv = str(tmp_path / "out.csv")
    res_file_csv = exporter.export_pipeline_logs(format="csv", output_path=out_csv)
    assert res_file_csv == out_csv
    assert Path(out_csv).exists()
    
    with pytest.raises(ValueError):
        exporter.export_pipeline_logs(format="xml")

def test_export_metrics(tracker_and_exporter):
    tracker, exporter, tmp_path, p1_id = tracker_and_exporter
    
    # JSON
    res_json = exporter.export_metrics(format="json")
    data = json.loads(res_json)
    assert len(data) == 2
    
    # ID JSON
    res_json_id = exporter.export_metrics(pipeline_id=p1_id, format="json")
    assert len(json.loads(res_json_id)) == 1
    
    # CSV
    res_csv = exporter.export_metrics(format="csv")
    assert "10.5" in res_csv
    
    with pytest.raises(ValueError):
        exporter.export_metrics(format="xml")

def test_export_statistics(tracker_and_exporter):
    tracker, exporter, tmp_path, p1_id = tracker_and_exporter
    
    stats_json = exporter.export_statistics(format="json")
    stats = json.loads(stats_json)
    assert stats["total_executions"] == 2
    assert stats["successful_executions"] == 1
    assert stats["success_rate_percent"] == 50.0
    
    stats_id_json = exporter.export_statistics(pipeline_id=p1_id, format="json")
    stats_id = json.loads(stats_id_json)
    assert stats_id["total_executions"] == 1
    assert stats_id["successful_executions"] == 1
    assert stats_id["success_rate_percent"] == 100.0
    
    out_stats = str(tmp_path / "stats.json")
    res = exporter.export_statistics(format="json", output_path=out_stats)
    assert res == out_stats
    assert Path(out_stats).exists()
    
    with pytest.raises(ValueError):
        exporter.export_statistics(format="csv")

def test_export_empty_data(tmp_path):
    db_path = str(tmp_path / "empty.db")
    # Tracker create tables
    PipelineTracker(db_path=db_path, config_dir=str(tmp_path))
    exporter = PipelineExporter(db_path=db_path)
    
    # Should handle empty gracefully
    res_csv = exporter.export_pipeline_logs(format="csv")
    assert res_csv == ""
    
    out_csv = str(tmp_path / "empty.csv")
    exporter.export_pipeline_logs(format="csv", output_path=out_csv)
    assert Path(out_csv).exists()
    assert Path(out_csv).read_text() == ""
    
    stats_json = exporter.export_statistics(format="json")
    stats = json.loads(stats_json)
    assert stats["total_executions"] == 0
    assert stats["success_rate_percent"] == 0.0

def test_exporter_bad_db(tmp_path):
    exporter = PipelineExporter(db_path="/invalid/dir/db.db")
    with pytest.raises(Exception):
        exporter.export_statistics(format="json")
