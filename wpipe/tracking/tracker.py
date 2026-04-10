"""
wpipe Pipeline Tracker - Professional Execution Tracking System using WSQLite.
"""

import json
import math
import os
import re
import uuid
from datetime import datetime, timedelta
from typing import Any, List, Optional, Union

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
    """Professional tracker using WSQLite and Pydantic models for all 10 tables."""

    def __init__(self, db_path: str, config_dir: Optional[str] = None):
        """
        Initialize the tracker.
        """
        self.db_path = db_path
        self.config_dir = os.path.abspath(config_dir or "pipeline_configs")

        # Initialize WSQLite instances for all 10 tables
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

        self._alert_hooks = {}  # Memory registry for alert hooks

    # ========================================
    # PIPELINE TRACKING
    # ========================================

    def register_pipeline(
        self,
        name: str,
        steps: list,
        input_data: Optional[dict] = None,
        worker_id: Optional[str] = None,
        worker_name: Optional[str] = None,
        parent_pipeline_id: Optional[str] = None,
    ) -> dict:
        """Register a new pipeline execution."""
        pipeline_id = f"PIPE-{uuid.uuid4().hex[:8].upper()}"

        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        yaml_path = os.path.join(self.config_dir, f"{name}.yaml")

        if not os.path.exists(yaml_path):
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
            worker_id=worker_id,
            worker_name=worker_name,
            input_data=_safe_json_dumps(input_data) if input_data else None,
            parent_pipeline_id=parent_pipeline_id,
            yaml_path=yaml_path,
        )
        self.db_pipelines.insert(model)

        if parent_pipeline_id:
            self.link_pipelines(parent_pipeline_id, pipeline_id, "triggered")

        return {"pipeline_id": pipeline_id, "yaml_path": yaml_path}

    def complete_pipeline(
        self,
        pipeline_id: str,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_step: Optional[str] = None,
    ) -> list:
        """Complete a pipeline execution and return fired hooks."""
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

        return self._check_pipeline_alerts(
            pipeline_id, model.name, model.status, duration_ms
        )

    # ========================================
    # QUERIES (Dashboard API)
    # ========================================

    def get_pipelines(self, limit: int = 50, offset: int = 0, status: Optional[str] = None) -> List[dict]:
        """Get list of pipelines for the dashboard."""
        all_pipelines = self.db_pipelines.get_all()
        all_pipelines.sort(key=lambda x: x.started_at or "", reverse=True)
        
        if status:
            all_pipelines = [p for p in all_pipelines if p.status == status]
            
        paged = all_pipelines[offset : offset + limit]
        
        result = []
        for p in paged:
            d = p.model_dump()
            for field in ["input_data", "output_data"]:
                if d.get(field):
                    try: d[field] = json.loads(d[field])
                    except: pass
            result.append(d)
        return result

    def get_pipeline(self, pipeline_id: str) -> Optional[dict]:
        """Get detailed pipeline data including steps."""
        pipelines = self.db_pipelines.get_by_field(id=pipeline_id)
        if not pipelines:
            return None
            
        pipeline = pipelines[0].model_dump()
        for field in ["input_data", "output_data"]:
            if pipeline.get(field):
                try: pipeline[field] = json.loads(pipeline[field])
                except: pass
                
        steps = self.db_steps.get_by_field(pipeline_id=pipeline_id)
        steps.sort(key=lambda x: x.step_order)
        
        pipeline["steps"] = []
        for s in steps:
            sd = s.model_dump()
            for field in ["input_data", "output_data"]:
                if sd.get(field):
                    try: sd[field] = json.loads(sd[field])
                    except: pass
            pipeline["steps"].append(sd)
            
        return pipeline

    def get_pipeline_executions(self, name: str, limit: int = 100, offset: int = 0) -> List[dict]:
        """Get all executions of a pipeline by name."""
        all_p = self.db_pipelines.get_by_field(name=name)
        all_p.sort(key=lambda x: x.started_at or "", reverse=True)
        return [p.model_dump() for p in all_p[offset : offset + limit]]

    def get_stats(self) -> dict:
        """Get overall statistics for dashboard summary cards."""
        all_p = self.db_pipelines.get_all()
        total = len(all_p)
        completed = len([p for p in all_p if p.status == "completed"])
        errors = len([p for p in all_p if p.status == "error"])
        running = len([p for p in all_p if p.status == "running"])
        
        durations = [p.total_duration_ms for p in all_p if p.status == "completed" and p.total_duration_ms]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        all_steps = self.db_steps.get_all()
        total_steps = len(all_steps)
        completed_steps = len([s for s in all_steps if s.status == "completed"])
        
        fired = self.db_alerts_fired.get_all()
        unack = len([a for a in fired if getattr(a, 'acknowledged', 0) == 0])
        
        return {
            "total_pipelines": total,
            "completed": completed,
            "errors": errors,
            "running": running,
            "success_rate": round((completed / total * 100), 1) if total > 0 else 0,
            "avg_duration_ms": round(avg_duration, 2),
            "total_steps": total_steps,
            "step_success_rate": round((completed_steps / total_steps * 100), 1) if total_steps > 0 else 0,
            "unacknowledged_alerts": unack,
        }

    def get_fired_alerts(self, limit: int = 50, severity: Optional[str] = None) -> List[dict]:
        """Get recent fired alerts."""
        alerts = self.db_alerts_fired.get_all()
        alerts.sort(key=lambda x: x.fired_at or "", reverse=True)
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return [a.model_dump() for a in alerts[:limit]]

    def get_alert_thresholds(self) -> List[dict]:
        """Get alert configurations."""
        return [c.model_dump() for c in self.db_alerts_config.get_all()]

    def get_events(self, pipeline_id: Optional[str] = None, limit: int = 50) -> List[dict]:
        """Get pipeline events."""
        events = self.db_events.get_by_field(pipeline_id=pipeline_id) if pipeline_id else self.db_events.get_all()
        events.sort(key=lambda x: x.created_at or "", reverse=True)
        return [e.model_dump() for e in events[:limit]]

    def get_trend_data(self, days: int = 7, pipeline_name: Optional[str] = None) -> List[dict]:
        """Get aggregated daily data for trend charts."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        all_p = self.db_pipelines.get_all()
        filtered = [p for p in all_p if p.started_at and p.started_at >= cutoff]
        if pipeline_name:
            filtered = [p for p in filtered if p.name == pipeline_name]
            
        daily = {}
        for p in filtered:
            date = p.started_at.split("T")[0]
            if date not in daily:
                daily[date] = {"date": date, "count": 0, "success": 0, "errors": 0, "durations": []}
            daily[date]["count"] += 1
            if p.status == "completed":
                daily[date]["success"] += 1
                if p.total_duration_ms: daily[date]["durations"].append(p.total_duration_ms)
            elif p.status == "error":
                daily[date]["errors"] += 1
                
        result = []
        for date in sorted(daily.keys()):
            day = daily[date]
            day["avg_duration"] = sum(day["durations"]) / len(day["durations"]) if day["durations"] else 0
            del day["durations"]
            result.append(day)
        return result

    def get_top_slow_steps(self, limit: int = 10) -> List[dict]:
        """Identify slowest steps across all executions."""
        all_history = self.db_step_history.get_all()
        stats = {}
        for h in all_history:
            if h.status != "completed": continue
            if h.step_name not in stats:
                stats[h.step_name] = {"step_name": h.step_name, "count": 0, "total_ms": 0, "max_ms": 0}
            stats[h.step_name]["count"] += 1
            stats[h.step_name]["total_ms"] += h.duration_ms
            stats[h.step_name]["max_ms"] = max(stats[h.step_name]["max_ms"], h.duration_ms)
            
        slow_steps = []
        for name, s in stats.items():
            s["avg_duration_ms"] = s["total_ms"] / s["count"]
            slow_steps.append(s)
        slow_steps.sort(key=lambda x: x["avg_duration_ms"], reverse=True)
        return slow_steps[:limit]

    def get_states_analysis(self) -> dict:
        """Get comprehensive analysis of all states/steps."""
        all_steps = self.db_steps.get_all()
        if not all_steps:
            return {"total_states": 0, "total_executions": 0, "total_errors": 0, "most_used": [], "slowest": [], "most_errors": []}

        stats = {}
        for s in all_steps:
            name = s.step_name
            if name not in stats:
                stats[name] = {"state_name": name, "execution_count": 0, "total_ms": 0, "error_count": 0}
            stats[name]["execution_count"] += 1
            if s.status == "error": stats[name]["error_count"] += 1
            if s.duration_ms: stats[name]["total_ms"] += s.duration_ms

        most_used = sorted(stats.values(), key=lambda x: x["execution_count"], reverse=True)[:20]
        for item in most_used: item["avg_duration_ms"] = item["total_ms"] / item["execution_count"]

        slowest = sorted([s for s in stats.values() if s["execution_count"] > s["error_count"]], 
                         key=lambda x: (x["total_ms"] / (x["execution_count"] - x["error_count"])), reverse=True)[:15]
        for item in slowest: item["avg_duration_ms"] = item["total_ms"] / (item["execution_count"] - item["error_count"])

        most_errors = sorted([s for s in stats.values() if s["error_count"] > 0], 
                             key=lambda x: x["error_count"] / x["execution_count"], reverse=True)[:15]
        for item in most_errors: item["error_rate"] = item["error_count"] / item["execution_count"]

        return {
            "total_states": len(stats),
            "total_executions": len(all_steps),
            "total_errors": len([s for s in all_steps if s.status == "error"]),
            "most_used": most_used,
            "slowest": slowest,
            "most_errors": most_errors,
        }

    def get_pipelines_analysis(self) -> dict:
        """Get comprehensive analysis of all pipelines."""
        all_p = self.db_pipelines.get_all()
        if not all_p:
            return {"total_pipelines": 0, "total_runs": 0, "avg_duration_ms": 0, "total_errors": 0, "slowest": [], "most_errors": [], "recent": []}

        stats = {}
        for p in all_p:
            if p.name not in stats:
                stats[p.name] = {"name": p.name, "execution_count": 0, "total_ms": 0, "error_count": 0}
            stats[p.name]["execution_count"] += 1
            if p.status == "error": stats[p.name]["error_count"] += 1
            if p.total_duration_ms: stats[p.name]["total_ms"] += p.total_duration_ms

        slowest = sorted([s for s in stats.values() if s["execution_count"] > s["error_count"]], 
                         key=lambda x: (x["total_ms"] / (x["execution_count"] - x["error_count"])), reverse=True)[:10]
        for item in slowest: item["avg_duration_ms"] = item["total_ms"] / (item["execution_count"] - item["error_count"])

        most_errors = sorted([s for s in stats.values() if s["error_count"] > 0], 
                             key=lambda x: x["error_count"] / x["execution_count"], reverse=True)[:10]
        for item in most_errors: item["error_rate"] = item["error_count"] / item["execution_count"]

        all_p.sort(key=lambda x: x.started_at or "", reverse=True)
        recent = [p.model_dump() for p in all_p[:10]]

        durations = [p.total_duration_ms for p in all_p if p.status == "completed" and p.total_duration_ms]
        avg_dur = sum(durations) / len(durations) if durations else 0

        return {
            "total_pipelines": len(set(p.name for p in all_p)),
            "total_runs": len(all_p),
            "avg_duration_ms": avg_dur,
            "total_errors": len([p for p in all_p if p.status == "error"]),
            "slowest": slowest,
            "most_errors": most_errors,
            "recent": recent,
        }

    def get_table_data(self, table: str, page: int = 1, page_size: int = 20, search: Optional[str] = None, status: Optional[str] = None) -> dict:
        """Generic paginated data retriever for any table."""
        db_map = {"pipelines": self.db_pipelines, "steps": self.db_steps, "alerts_fired": self.db_alerts_fired, "events": self.db_events}
        if table not in db_map: return {"items": [], "total": 0}
        
        items = db_map[table].get_all()
        if status: items = [i for i in items if getattr(i, 'status', None) == status]
        if search:
            search = search.lower()
            items = [i for i in items if search in str(i.model_dump()).lower()]
            
        total = len(items)
        offset = (page - 1) * page_size
        paged = items[offset : offset + page_size]
        
        return {
            "items": [i.model_dump() for i in paged],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size) if page_size > 0 else 1
        }

    # ========================================
    # ALERTS SYSTEM
    # ========================================

    def add_alert_threshold(
        self,
        metric: str,
        expression: str,
        name: Optional[str] = None,
        severity: str = Severity.WARNING,
        message: Optional[str] = None,
        steps: Optional[list] = None,
    ) -> int:
        """Add an alert threshold configuration."""
        match = re.match(r"([><=!]+)\s*(\d+(\.\d+)?)", expression)
        if not match:
            raise ValueError(f"Invalid alert expression: {expression}")

        condition = match.group(1)
        value = float(match.group(2))

        if not name:
            name = f"alert_{metric}_{condition}{value}_{uuid.uuid4().hex[:4]}"

        if steps:
            self._alert_hooks[name] = steps

        model = AlertConfigModel(
            name=name,
            metric=metric,
            condition=condition,
            value=value,
            severity=severity,
            message=message,
        )
        return self.db_alerts_config.insert(model)

    # ========================================
    # STEP TRACKING
    # ========================================

    def start_step(self, pipeline_id: str, step_order: int, step_name: str, step_version: Optional[str] = None, step_type: str = "task", input_data: Optional[dict] = None) -> int:
        """Start tracking a step."""
        model = StepModel(
            pipeline_id=pipeline_id,
            step_order=step_order,
            step_name=step_name,
            step_version=step_version,
            step_type=step_type,
            input_data=_safe_json_dumps(input_data) if input_data else None,
        )
        return self.db_steps.insert(model)

    def complete_step(self, step_id: int, output_data: Optional[dict] = None, error_message: Optional[str] = None, error_traceback: Optional[str] = None, pipeline_id: Optional[str] = None) -> list:
        """Complete a step execution and record in history."""
        steps = self.db_steps.get_by_field(id=step_id)
        if not steps: return []

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

        return self._check_step_alerts(
            pipeline_id or model.pipeline_id, model.step_name, duration_ms, model.status
        )

    # ========================================
    # INTERNAL LOGIC
    # ========================================

    def _evaluate_condition(self, condition: str, actual: float, threshold: float) -> bool:
        ops = {">": actual > threshold, "<": actual < threshold, ">=": actual >= threshold, "<=": actual <= threshold, "==": actual == threshold}
        return ops.get(condition, False)

    def _check_step_alerts(self, pipeline_id: str, step_name: str, duration_ms: float, status: str) -> list:
        fired_hooks = []
        configs = self.db_alerts_config.get_by_field(metric=Metric.STEP_DURATION, enabled=1)

        for config in configs:
            if self._evaluate_condition(config.condition, duration_ms, config.value):
                fire_model = AlertFiredModel(
                    alert_config_id=config.id or 0,
                    pipeline_id=pipeline_id,
                    metric=Metric.STEP_DURATION,
                    metric_value=duration_ms,
                    threshold_value=config.value,
                    severity=config.severity,
                    message=config.message or f"Step {step_name} exceeded threshold",
                )
                self.db_alerts_fired.insert(fire_model)
                if config.name in self._alert_hooks:
                    fired_hooks.extend(self._alert_hooks[config.name])
        return fired_hooks

    def _check_pipeline_alerts(self, pipeline_id: str, pipeline_name: str, status: str, duration_ms: float = 0) -> list:
        fired_hooks = []
        configs = self.db_alerts_config.get_by_field(enabled=1)

        for config in configs:
            metric_value = None
            if config.metric == Metric.PIPELINE_DURATION and duration_ms > 0:
                metric_value = duration_ms
            elif config.metric == Metric.ERROR_RATE and status == "error":
                all_p = self.db_pipelines.get_all()
                errors = len([p for p in all_p if p.status == "error"])
                metric_value = (errors / len(all_p) * 100) if all_p else 0

            if metric_value is not None and self._evaluate_condition(config.condition, metric_value, config.value):
                fire_model = AlertFiredModel(
                    alert_config_id=config.id or 0,
                    pipeline_id=pipeline_id,
                    metric=config.metric,
                    metric_value=metric_value,
                    threshold_value=config.value,
                    severity=config.severity,
                    message=config.message or f"Pipeline {pipeline_name} alert",
                )
                self.db_alerts_fired.insert(fire_model)
                if config.name in self._alert_hooks:
                    fired_hooks.extend(self._alert_hooks[config.name])
        return fired_hooks

    def link_pipelines(self, parent_id: str, child_id: str, relation_type: str = "triggered"):
        model = PipelineRelationModel(parent_pipeline_id=parent_id, child_pipeline_id=child_id, relation_type=relation_type)
        self.db_pipeline_relations.insert(model)

    def add_event(self, pipeline_id: str, event_type: str, event_name: str, message: Optional[str] = None, data: Optional[dict] = None, tags: Optional[list] = None, step_id: Optional[int] = None):
        model = EventModel(pipeline_id=pipeline_id, step_id=step_id, event_type=event_type, event_name=event_name, message=message, data=json.dumps(data) if data else None, tags=json.dumps(tags) if tags else None)
        self.db_events.insert(model)

    def record_system_metrics(self, pipeline_id: str, metrics: dict):
        model = SystemMetricsModel(pipeline_id=pipeline_id, cpu_percent=metrics.get("cpu_percent"), memory_percent=metrics.get("memory_percent"), memory_used_mb=metrics.get("memory_used_mb"), memory_available_mb=metrics.get("memory_available_mb"), disk_io_read_mb=metrics.get("disk_io_read_mb"), disk_io_write_mb=metrics.get("disk_io_write_mb"))
        self.db_system_metrics.insert(model)

    def acknowledge_alert(self, alert_id: int):
        alerts = self.db_alerts_fired.get_by_field(id=alert_id)
        if alerts:
            alert = alerts[0]
            self.db_alerts_fired.update(alert_id, alert)
        return {"status": "success"}

    def get_pipeline_graph(self, pipeline_id: str) -> dict:
        pipeline = self.get_pipeline(pipeline_id)
        if not pipeline: return {"nodes": [], "edges": []}
        nodes, edges = [], []
        steps = pipeline.get("steps", [])
        for i, step in enumerate(steps):
            nodes.append({"id": f"step_{step['id']}", "name": step["step_name"], "type": step["step_type"], "status": step["status"], "duration_ms": step.get("duration_ms")})
            if i > 0:
                edges.append({"from": f"step_{steps[i-1]['id']}", "to": f"step_{step['id']}"})
        return {"pipeline_id": pipeline_id, "nodes": nodes, "edges": edges}

    def delete_pipeline(self, pipeline_id: str):
        self.db_pipelines.delete(pipeline_id)
        # WSQLite no soporta cascada automática en el wrapper, borramos dependencias manualmente
        for s in self.db_steps.get_by_field(pipeline_id=pipeline_id): self.db_steps.delete(s.id)
        for e in self.db_events.get_by_field(pipeline_id=pipeline_id): self.db_events.delete(e.id)

    def _percentile(self, data: list, percentile: int) -> float:
        if not data: return 0
        data_sorted = sorted(data)
        index = (len(data_sorted) - 1) * percentile / 100
        lower = math.floor(index); upper = math.ceil(index)
        if lower == upper: return data_sorted[int(index)]
        return data_sorted[int(lower)] * (upper - index) + data_sorted[int(upper)] * (index - lower)
