"""
wpipe Pipeline Tracker - Professional Execution Tracking System using WSQLite.
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import yaml
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
from wpipe.util.transform import object_to_dict

from .alerts import AlertManager
from .analysis import AnalysisManager
from .queries import QueryManager


def _safe_json_dumps(data: Any) -> str:
    """
    Safe JSON dump that handles non-serializable objects and circular references.

    Args:
        data: The data to serialize.

    Returns:
        A JSON string representation of the data.
    """
    try:
        # First convert everything to a clean dict/list structure
        clean_data = object_to_dict(data)
        return json.dumps(clean_data)
    except (TypeError, OverflowError, ValueError):
        try:
            # Fallback for exotic types not covered
            return json.dumps(str(data))
        except (TypeError, ValueError, OverflowError):
            return '"<Unserializable Data>"'


class Metric:
    """Constants for alert metrics and utility for recording numeric data."""

    PIPELINE_DURATION = "pipeline_duration_ms"
    STEP_DURATION = "step_duration_ms"
    ERROR_RATE = "error_rate"

    # Reference to the active tracker for static recording
    _active_tracker: Optional["PipelineTracker"] = None

    @staticmethod
    def record(name: str, value: float, unit: Optional[str] = None) -> None:
        """
        Record a numeric metric in the current pipeline execution.

        Args:
            name: Name of the metric.
            value: Numeric value.
            unit: Optional unit of measurement (e.g., 'L/100km').
        """
        if Metric._active_tracker and Metric._active_tracker.pipeline_id:
            Metric._active_tracker.add_event(
                pipeline_id=Metric._active_tracker.pipeline_id,
                event_type="metric",
                event_name=name,
                message=f"Metric '{name}' recorded: {value} {unit or ''}",
                data={"value": value, "unit": unit}
            )
        else:
            # Fallback for when no tracker is active
            print(f"[METRIC] {name}: {value} {unit or ''}")


class Severity:
    """Constants for alert severity levels."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


# --- PROFESSIONAL TABLE NAMING FOR LTS ---
# pylint: disable=invalid-name
class pipelines(PipelineModel):
    """Pipeline table model."""


class steps(StepModel):
    """Steps table model."""


class step_history(StepHistoryModel):
    """Step history table model."""


class performance_stats(PerformanceStatsModel):
    """Performance stats table model."""


class alerts_config(AlertConfigModel):
    """Alerts configuration table model."""


class alerts_fired(AlertFiredModel):
    """Alerts fired table model."""


class events(EventModel):
    """Events table model."""


class pipeline_relations(PipelineRelationModel):
    """Pipeline relations table model."""


class system_metrics(SystemMetricsModel):
    """System metrics table model."""


class comparisons(ComparisonModel):
    """Comparisons table model."""
# pylint: enable=invalid-name


class PipelineTracker:
    """
    Unified Pipeline Tracker.

    Orchestrates registration, step tracking, alerts, and dashboard queries.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, db_path: str, config_dir: Optional[str] = None):
        """
        Initialize the PipelineTracker.

        Args:
            db_path: Path to the SQLite database.
            config_dir: Directory to store pipeline configurations.
        """
        self.db_path = db_path
        self.config_dir = os.path.abspath(config_dir or "pipeline_configs")
        self.pipeline_id: Optional[str] = None

        # Table instances with professional names
        self.db_pipelines = WSQLite(pipelines, db_path)
        self.db_steps = WSQLite(steps, db_path)
        self.db_step_history = WSQLite(step_history, db_path)
        self.db_performance_stats = WSQLite(performance_stats, db_path)
        self.db_alerts_config = WSQLite(alerts_config, db_path)
        self.db_alerts_fired = WSQLite(alerts_fired, db_path)
        self.db_events = WSQLite(events, db_path)
        self.db_pipeline_relations = WSQLite(pipeline_relations, db_path)
        self.db_system_metrics = WSQLite(system_metrics, db_path)
        self.db_comparisons = WSQLite(comparisons, db_path)

        self._ensure_schema_up_to_date()

        self._alert_hooks: Dict[str, List[str]] = {}

        # specialized Managers
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

        # Set this tracker as the active one for Metric.record utility
        Metric._active_tracker = self

    # ========================================
    # DELEGATED METHODS (Backward Compatibility)
    # ========================================

    def add_alert_threshold(self, *args, **kwargs) -> int:
        """Delegate to alerts manager."""
        return self.alerts.add_alert_threshold(*args, **kwargs)

    def get_pipelines(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Delegate to queries manager."""
        return self.queries.get_pipelines(*args, **kwargs)

    def get_pipeline(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        """Delegate to queries manager."""
        return self.queries.get_pipeline(*args, **kwargs)

    def get_stats(self, *args, **kwargs) -> Dict[str, Any]:
        """Delegate to analysis manager."""
        return self.analysis.get_stats(*args, **kwargs)

    def get_trend_data(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Delegate to analysis manager."""
        return self.analysis.get_trend_data(*args, **kwargs)

    def get_top_slow_steps(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Delegate to analysis manager."""
        return self.analysis.get_top_slow_steps(*args, **kwargs)

    def get_events(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Delegate to queries manager."""
        return self.queries.get_events(*args, **kwargs)

    def get_fired_alerts(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Delegate to queries manager."""
        return self.queries.get_fired_alerts(*args, **kwargs)

    def get_alert_thresholds(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Delegate to queries manager."""
        return self.queries.get_alert_thresholds(*args, **kwargs)

    def get_states_analysis(self, *args, **kwargs) -> Dict[str, Any]:
        """Delegate to analysis manager."""
        return self.analysis.get_states_analysis(*args, **kwargs)

    def get_pipelines_analysis(self, *args, **kwargs) -> Dict[str, Any]:
        """Delegate to analysis manager."""
        return self.analysis.get_pipelines_analysis(*args, **kwargs)

    def get_table_data(self, *args, **kwargs) -> Dict[str, Any]:
        """Delegate to analysis manager."""
        return self.analysis.get_table_data(*args, **kwargs)

    def get_pipeline_executions(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Delegate to queries manager."""
        return self.queries.get_pipeline_executions(*args, **kwargs)

    # ========================================
    # CORE TRACKING LOGIC
    # ========================================

    def register_pipeline(self, name: str, pipeline_steps: List[Any], **kwargs) -> Dict[str, Any]:
        """
        Register a pipeline and its steps.

        Args:
            name: Pipeline name.
            pipeline_steps: List of pipeline steps.
            **kwargs: Additional metadata (worker_id, worker_name, input_data, parent_pipeline_id).

        Returns:
            Dictionary with pipeline_id and yaml_path.
        """
        pipeline_id = f"PIPE-{uuid.uuid4().hex[:8].upper()}"
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        safe_name = os.path.basename(os.path.normpath(name))
        yaml_path = os.path.join(self.config_dir, f"{safe_name}.yaml")
        if not os.path.exists(yaml_path):
            def _serialize_step(s):
                if hasattr(s, "to_dict"):
                    return s.to_dict()
                if isinstance(s, tuple):
                    return {
                        "type": "task",
                        "name": s[1] if len(s) > 1 else "unknown",
                        "version": s[2] if len(s) > 2 else "v1.0",
                        "func": str(s[0])
                    }
                return str(s)

            config = {
                "name": name,
                "registered_at": datetime.now().isoformat(),
                "step_count": len(pipeline_steps),
                "steps": [_serialize_step(s) for s in pipeline_steps],
            }
            with open(yaml_path, "w", encoding="utf-8") as f:
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
            self.link_pipelines(str(kwargs.get("parent_pipeline_id")), pipeline_id)
        return {"pipeline_id": pipeline_id, "yaml_path": yaml_path}

    def complete_pipeline(
        self,
        pipeline_id: str,
        output_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        error_step: Optional[str] = None,
    ) -> List[str]:
        """
        Mark a pipeline as completed or failed.

        Args:
            pipeline_id: Unique pipeline identifier.
            output_data: Optional execution results.
            error_message: Optional error message if failed.
            error_step: Optional step name where failure occurred.

        Returns:
            List of fired alert hooks.
        """
        pipeline_records = self.db_pipelines.get_by_field(id=pipeline_id)
        if not pipeline_records:
            return []
        model = pipeline_records[0]
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
        """
        Mark a step as started.

        Args:
            pipeline_id: Unique pipeline identifier.
            step_order: Execution order.
            step_name: Name of the step.
            **kwargs: Additional metadata (step_version, step_type, parent_step_id, parallel_group, input_data).

        Returns:
            The ID of the inserted step record.
        """
        model = StepModel(
            pipeline_id=pipeline_id,
            step_order=step_order,
            step_name=step_name,
            step_version=kwargs.get("step_version"),
            step_type=kwargs.get("step_type", "task"),
            parent_step_id=kwargs.get("parent_step_id"),
            parallel_group=kwargs.get("parallel_group"),
            status="running",
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
        output_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        error_traceback: Optional[str] = None,
        pipeline_id: Optional[str] = None,
    ) -> List[str]:
        """
        Mark a step as completed or failed.

        Args:
            step_id: Unique step identifier.
            output_data: Optional step results.
            error_message: Optional error message.
            error_traceback: Optional error traceback.
            pipeline_id: Optional pipeline ID.

        Returns:
            List of fired alert hooks.
        """
        step_records = self.db_steps.get_by_field(id=step_id)
        if not step_records:
            return []
        model = step_records[0]
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
    ) -> None:
        """
        Link two pipelines with a relationship.

        Args:
            parent_id: Parent pipeline ID.
            child_id: Child pipeline ID.
            relation_type: Type of relationship.
        """
        model = PipelineRelationModel(
            parent_pipeline_id=parent_id,
            child_pipeline_id=child_id,
            relation_type=relation_type,
        )
        self.db_pipeline_relations.insert(model)

    def add_event(self, pipeline_id: str, event_type: str, event_name: str, **kwargs) -> None:
        """
        Record an event.

        Args:
            pipeline_id: Unique pipeline identifier.
            event_type: Type of event.
            event_name: Name of the event.
            **kwargs: Additional metadata (step_id, message, data, tags).
        """
        model = EventModel(
            pipeline_id=pipeline_id,
            step_id=kwargs.get("step_id"),
            event_type=event_type,
            event_name=event_name,
            message=kwargs.get("message"),
            data=_safe_json_dumps(kwargs.get("data")) if kwargs.get("data") else None,
            tags=_safe_json_dumps(kwargs.get("tags")) if kwargs.get("tags") else None,
        )
        self.db_events.insert(model)

    def record_system_metrics(self, pipeline_id: str, metrics: Dict[str, Any]) -> None:
        """
        Record system metrics.

        Args:
            pipeline_id: Unique pipeline identifier.
            metrics: Dictionary of system metrics.
        """
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

    def acknowledge_alert(self, alert_id: int) -> Dict[str, str]:
        """
        Acknowledge a fired alert.

        Args:
            alert_id: Unique alert identifier.

        Returns:
            Status dictionary.
        """
        alert_records = self.db_alerts_fired.get_by_field(id=alert_id)
        if alert_records:
            self.db_alerts_fired.update(alert_id, alert_records[0])
        return {"status": "success"}

    def get_pipeline_graph(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get pipeline data formatted for graph visualization with full metadata.

        Args:
            pipeline_id: Unique pipeline identifier.

        Returns:
            Dictionary with nodes and edges for visualization.
        """
        pipeline = self.get_pipeline(pipeline_id)
        if not pipeline:
            return {"nodes": [], "edges": []}

        nodes = []
        edges = []
        steps_list = pipeline.get("steps", [])

        for i, step in enumerate(steps_list):
            output_data = step.get("output_data") or {}

            step_id = step.get("id")
            if not step_id or step_id == "None" or step_id == "":
                step_id = step.get("step_order")
            node = {
                "id": f"step_{step_id}",
                "name": step["step_name"],
                "type": step["step_type"],
                "status": step["status"],
                "duration_ms": step.get("duration_ms"),
                "version": step.get("step_version"),
                "error": step.get("error_message"),
                "order": step["step_order"],
                "parent_step_id": step.get("parent_step_id"),
                "parallel_group": step.get("parallel_group"),
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

            # --- Edge connection logic ---
            parent_id = step.get("parent_step_id")
            step_order = step.get("step_order")

            if parent_id:
                edges.append({
                    "from": f"step_{parent_id}" if parent_id else f"step_{step_order}",
                    "to": f"step_{step_id}",
                    "label": "parallel",
                    "style": "dashed" if step["status"] == "skipped" else "solid"
                })
            elif i > 0:
                j = i - 1
                found_prev = None
                while j >= 0:
                    cand = steps_list[j]
                    if not cand.get("parent_step_id"):
                        found_prev = cand
                        break
                    j -= 1

                if found_prev:
                    prev_id = found_prev.get("id") or found_prev.get("step_order")
                    prev_order = found_prev.get("step_order")
                    is_skipped = step["status"] == "skipped" or step["step_type"] == "skipped"
                    edges.append({
                        "from": f"step_{prev_id}" if prev_id else f"step_{prev_order}",
                        "to": f"step_{step_id}",
                        "label": (
                            "next" if found_prev["step_type"] != "condition"
                            else ("taken" if not is_skipped else "skipped")
                        ),
                        "style": "solid" if not is_skipped else "dashed",
                        "color": (
                            "#10b981" if (found_prev["step_type"] == "condition" and not is_skipped)
                            else None
                        )
                    })

        return {
            "pipeline_id": pipeline_id,
            "pipeline_name": pipeline["name"],
            "status": pipeline["status"],
            "total_duration_ms": pipeline.get("total_duration_ms"),
            "nodes": nodes,
            "edges": edges,
        }

    def delete_pipeline(self, pipeline_id: str) -> None:
        """
        Delete all data related to a pipeline.

        Args:
            pipeline_id: Unique pipeline identifier.
        """
        self.db_pipelines.delete(pipeline_id)
        for s in self.db_steps.get_by_field(pipeline_id=pipeline_id):
            self.db_steps.delete(s.id)
        for e in self.db_events.get_by_field(pipeline_id=pipeline_id):
            self.db_events.delete(e.id)

    def _ensure_schema_up_to_date(self) -> None:
        """Ensure the database schema is up to date with the latest models."""
        try:
            # Force a small operation to ensure tables exist
            try:
                self.db_steps.get_all()
            except (AttributeError, RuntimeError, ValueError):
                pass

            if not os.path.exists(self.db_path):
                return

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check for parent_step_id and parallel_group in common table names
            for table in ["steps", "stepmodel"]:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [info[1] for info in cursor.fetchall()]

                if columns:  # If table exists
                    modified = False
                    if "parent_step_id" not in columns:
                        cursor.execute(f"ALTER TABLE {table} ADD COLUMN parent_step_id INTEGER")
                        modified = True
                    if "parallel_group" not in columns:
                        cursor.execute(f"ALTER TABLE {table} ADD COLUMN parallel_group TEXT")
                        modified = True

                    if modified:
                        conn.commit()
            conn.close()
        except (sqlite3.Error, AttributeError, RuntimeError, ValueError):
            # We don't want to crash the whole app if migration fails
            pass
