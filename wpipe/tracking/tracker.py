"""
wpipe Pipeline Tracker - Professional Execution Tracking System using WSQLite.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Any, Optional

from wsqlite import WSQLite

from wpipe.sqlite.tables_dto.tracker_models import (
    AlertConfigModel,
    AlertFiredModel,
    ComparisonModel,
    EventModel,
    PerformanceStatsModel,
    PipelineModel,
    PipelineRelationModel,
    StepHistoryModel,
    StepModel,
    SystemMetricsModel,
)

from .alerts import AlertManager
from .analysis import AnalysisManager
from .queries import QueryManager


def _safe_json_dumps(data: Any) -> str:
    """Safe JSON dump that handles non-serializable objects."""
    try:
        return json.dumps(data)
    except (TypeError, OverflowError):
        return json.dumps(str(data))


class Metric:
    """Constants for alert metrics."""

    PIPELINE_DURATION = "pipeline_duration_ms"
    STEP_DURATION = "step_duration_ms"
    ERROR_RATE = "error_rate"


class Severity:
    """Constants for alert severity levels."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class PipelineTracker:
    """
    Unified Pipeline Tracker.

    Orchestrates registration, step tracking, alerts, and dashboard queries.
    """

    def __init__(self, db_path: str, config_dir: Optional[str] = None):
        self.db_path = db_path
        self.config_dir = os.path.abspath(config_dir or "pipeline_configs")

        # Table instances
        self.db_pipelines = WSQLite(PipelineModel, db_path)
        self.db_steps = WSQLite(StepModel, db_path)
        self.db_step_history = WSQLite(StepHistoryModel, db_path)
        self.db_performance_stats = WSQLite(PerformanceStatsModel, db_path)
        self.db_alerts_config = WSQLite(AlertConfigModel, db_path)
        self.db_alerts_fired = WSQLite(AlertFiredModel, db_path)
        self.db_events = WSQLite(EventModel, db_path)
        self.db_pipeline_relations = WSQLite(PipelineRelationModel, db_path)
        self.db_system_metrics = WSQLite(SystemMetricsModel, db_path)
        self.db_comparisons = WSQLite(ComparisonModel, db_path)

        self._alert_hooks = {}

        # Specialized Managers
        self.alerts = AlertManager(
            self.db_alerts_config, self.db_alerts_fired, self._alert_hooks
        )
        self.queries = QueryManager(
            self.db_pipelines,
            self.db_steps,
            self.db_alerts_config,
            self.db_alerts_fired,
            self.db_events,
        )
        self.analysis = AnalysisManager(
            self.db_pipelines, self.db_steps, self.db_step_history, self.db_alerts_fired
        )

    # ========================================
    # DELEGATED METHODS (Backward Compatibility)
    # ========================================

    def add_alert_threshold(self, *args, **kwargs):
        return self.alerts.add_alert_threshold(*args, **kwargs)

    def get_pipelines(self, *args, **kwargs):
        return self.queries.get_pipelines(*args, **kwargs)

    def get_pipeline(self, *args, **kwargs):
        return self.queries.get_pipeline(*args, **kwargs)

    def get_stats(self, *args, **kwargs):
        return self.analysis.get_stats(*args, **kwargs)

    def get_trend_data(self, *args, **kwargs):
        return self.analysis.get_trend_data(*args, **kwargs)

    def get_top_slow_steps(self, *args, **kwargs):
        return self.analysis.get_top_slow_steps(*args, **kwargs)

    def get_events(self, *args, **kwargs):
        return self.queries.get_events(*args, **kwargs)

    def get_fired_alerts(self, *args, **kwargs):
        return self.queries.get_fired_alerts(*args, **kwargs)

    def get_alert_thresholds(self, *args, **kwargs):
        return self.queries.get_alert_thresholds(*args, **kwargs)

    def get_states_analysis(self, *args, **kwargs):
        return self.analysis.get_states_analysis(*args, **kwargs)

    def get_pipelines_analysis(self, *args, **kwargs):
        return self.analysis.get_pipelines_analysis(*args, **kwargs)

    def get_table_data(self, *args, **kwargs):
        return self.analysis.get_table_data(*args, **kwargs)

    def get_pipeline_executions(self, *args, **kwargs):
        return self.queries.get_pipeline_executions(*args, **kwargs)

    # ========================================
    # CORE TRACKING LOGIC
    # ========================================

    def register_pipeline(self, name: str, steps: list, **kwargs) -> dict:
        pipeline_id = f"PIPE-{uuid.uuid4().hex[:8].upper()}"
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        safe_name = os.path.basename(os.path.normpath(name))
        yaml_path = os.path.join(self.config_dir, f"{safe_name}.yaml")
        if not os.path.exists(yaml_path):
            import yaml

            config = {
                "name": name,
                "registered_at": datetime.now().isoformat(),
                "step_count": len(steps),
                "steps": [str(s) for s in steps],
            }
            with open(yaml_path, "w") as f:
                yaml.dump(config, f)

        model = PipelineModel(
            id=pipeline_id,
            name=name,
            worker_id=kwargs.get("worker_id"),
            worker_name=kwargs.get("worker_name"),
            input_data=(
                _safe_json_dumps(kwargs.get("input_data"))
                if kwargs.get("input_data")
                else None
            ),
            parent_pipeline_id=kwargs.get("parent_pipeline_id"),
            yaml_path=yaml_path,
        )
        self.db_pipelines.insert(model)
        if kwargs.get("parent_pipeline_id"):
            self.link_pipelines(kwargs.get("parent_pipeline_id"), pipeline_id)
        return {"pipeline_id": pipeline_id, "yaml_path": yaml_path}

    def complete_pipeline(
        self,
        pipeline_id: str,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_step: Optional[str] = None,
    ) -> list:
        pipelines = self.db_pipelines.get_by_field(id=pipeline_id)
        if not pipelines:
            return []
        model = pipelines[0]
        started = datetime.fromisoformat(model.started_at)
        duration_ms = (datetime.now() - started).total_seconds() * 1000
        model.status = "error" if error_message else "completed"
        model.completed_at = datetime.now().isoformat()
        model.total_duration_ms = duration_ms
        model.output_data = _safe_json_dumps(output_data) if output_data else None
        model.error_message = error_message
        model.error_step = error_step
        self.db_pipelines.update(pipeline_id, model)
        return self.alerts.check_pipeline_alerts(
            pipeline_id, model.name, model.status, duration_ms, self.db_pipelines
        )

    def start_step(
        self, pipeline_id: str, step_order: int, step_name: str, **kwargs
    ) -> int:
        model = StepModel(
            pipeline_id=pipeline_id,
            step_order=step_order,
            step_name=step_name,
            step_version=kwargs.get("step_version"),
            step_type=kwargs.get("step_type", "task"),
            input_data=(
                _safe_json_dumps(kwargs.get("input_data"))
                if kwargs.get("input_data")
                else None
            ),
        )
        return self.db_steps.insert(model)

    def complete_step(
        self,
        step_id: int,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_traceback: Optional[str] = None,
        pipeline_id: Optional[str] = None,
    ) -> list:
        steps = self.db_steps.get_by_field(id=step_id)
        if not steps:
            return []
        model = steps[0]
        started = datetime.fromisoformat(model.started_at)
        duration_ms = (datetime.now() - started).total_seconds() * 1000
        model.status = "error" if error_message else "completed"
        model.completed_at = datetime.now().isoformat()
        model.duration_ms = duration_ms
        model.output_data = _safe_json_dumps(output_data) if output_data else None
        model.error_message = error_message
        model.error_traceback = error_traceback
        self.db_steps.update(step_id, model)

        history = StepHistoryModel(
            pipeline_id=pipeline_id or model.pipeline_id,
            step_name=model.step_name,
            duration_ms=duration_ms,
            status=model.status,
        )
        self.db_step_history.insert(history)
        return self.alerts.check_step_alerts(
            pipeline_id or model.pipeline_id, model.step_name, duration_ms
        )

    def link_pipelines(
        self, parent_id: str, child_id: str, relation_type: str = "triggered"
    ):
        model = PipelineRelationModel(
            parent_pipeline_id=parent_id,
            child_pipeline_id=child_id,
            relation_type=relation_type,
        )
        self.db_pipeline_relations.insert(model)

    def add_event(self, pipeline_id: str, event_type: str, event_name: str, **kwargs):
        model = EventModel(
            pipeline_id=pipeline_id,
            step_id=kwargs.get("step_id"),
            event_type=event_type,
            event_name=event_name,
            message=kwargs.get("message"),
            data=json.dumps(kwargs.get("data")) if kwargs.get("data") else None,
            tags=json.dumps(kwargs.get("tags")) if kwargs.get("tags") else None,
        )
        self.db_events.insert(model)

    def record_system_metrics(self, pipeline_id: str, metrics: dict):
        model = SystemMetricsModel(
            pipeline_id=pipeline_id,
            cpu_percent=metrics.get("cpu_percent"),
            memory_percent=metrics.get("memory_percent"),
            memory_used_mb=metrics.get("memory_used_mb"),
            memory_available_mb=metrics.get("memory_available_mb"),
            disk_io_read_mb=metrics.get("disk_io_read_mb"),
            disk_io_write_mb=metrics.get("disk_io_write_mb"),
        )
        self.db_system_metrics.insert(model)

    def acknowledge_alert(self, alert_id: int):
        alerts = self.db_alerts_fired.get_by_field(id=alert_id)
        if alerts:
            self.db_alerts_fired.update(alert_id, alerts[0])
        return {"status": "success"}

    def get_pipeline_graph(self, pipeline_id: str) -> dict:
        """Get pipeline data formatted for graph visualization with full metadata."""
        pipeline = self.get_pipeline(pipeline_id)
        if not pipeline:
            return {"nodes": [], "edges": []}

        nodes = []
        edges = []
        steps_list = pipeline.get("steps", [])

        for i, step in enumerate(steps_list):
            # Parseamos datos de entrada/salida para extraer info de bifurcación
            output_data = step.get("output_data") or {}
            input_data = step.get("input_data") or {}

            node = {
                "id": f"step_{step['id']}",
                "name": step["step_name"],
                "type": step["step_type"],
                "status": step["status"],
                "duration_ms": step.get("duration_ms"),
                "version": step.get("step_version"),
                "error": step.get("error_message"),
                "order": step["step_order"],
                "branch_taken": (
                    output_data.get("branch_taken")
                    if isinstance(output_data, dict)
                    else None
                ),
                "expression": (
                    output_data.get("expression")
                    if isinstance(output_data, dict)
                    else None
                ),
                "has_input": step.get("input_data") is not None,
                "has_output": step.get("output_data") is not None,
            }
            nodes.append(node)

            # Lógica de conexión de bordes
            if i > 0:
                prev_step = steps_list[i - 1]
                # Si el anterior no es una condición, conexión simple
                if prev_step["step_type"] != "condition":
                    edges.append(
                        {
                            "from": f"step_{prev_step['id']}",
                            "to": f"step_{step['id']}",
                            "label": "next",
                        }
                    )
                else:
                    # Si el anterior fue una condición, marcamos si este paso fue tomado o saltado
                    is_skipped = (
                        step["status"] == "skipped" or step["step_type"] == "skipped"
                    )
                    edges.append(
                        {
                            "from": f"step_{prev_step['id']}",
                            "to": f"step_{step['id']}",
                            "label": "taken" if not is_skipped else "skipped",
                            "style": "solid" if not is_skipped else "dashed",
                            "color": "#10b981" if not is_skipped else "#6b7280",
                        }
                    )

        return {
            "pipeline_id": pipeline_id,
            "pipeline_name": pipeline["name"],
            "status": pipeline["status"],
            "total_duration_ms": pipeline.get("total_duration_ms"),
            "nodes": nodes,
            "edges": edges,
        }

    def delete_pipeline(self, pipeline_id: str):
        self.db_pipelines.delete(pipeline_id)
        for s in self.db_steps.get_by_field(pipeline_id=pipeline_id):
            self.db_steps.delete(s.id)
        for e in self.db_events.get_by_field(pipeline_id=pipeline_id):
            self.db_events.delete(e.id)
