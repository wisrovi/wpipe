"""
Alert system for pipeline and step monitoring.
"""

import re
import uuid
from typing import Optional

from wpipe.sqlite.tables_dto.tracker_models import AlertConfigModel, AlertFiredModel


class AlertManager:
    """Handles alert threshold configuration and firing logic."""

    def __init__(self, db_alerts_config, db_alerts_fired, alert_hooks):
        self.db_alerts_config = db_alerts_config
        self.db_alerts_fired = db_alerts_fired
        self._alert_hooks = alert_hooks

    def add_alert_threshold(
        self,
        metric: str,
        expression: str,
        name: Optional[str] = None,
        severity: str = "warning",
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

    def evaluate_condition(self, condition: str, actual: float, threshold: float) -> bool:
        """Evaluate if a metric value triggers a condition."""
        ops = {
            ">": actual > threshold,
            "<": actual < threshold,
            ">=": actual >= threshold,
            "<=": actual <= threshold,
            "==": actual == threshold,
        }
        return ops.get(condition, False)

    def check_step_alerts(self, pipeline_id: str, step_name: str, duration_ms: float) -> list:
        """Check and fire step-level alerts."""
        fired_hooks = []
        # Import local constants to avoid circular imports if needed
        configs = self.db_alerts_config.get_by_field(metric="step_duration_ms", enabled=1)

        for config in configs:
            if self.evaluate_condition(config.condition, duration_ms, config.value):
                fire_model = AlertFiredModel(
                    alert_config_id=config.id or 0,
                    pipeline_id=pipeline_id,
                    metric="step_duration_ms",
                    metric_value=duration_ms,
                    threshold_value=config.value,
                    severity=config.severity,
                    message=config.message or f"Step {step_name} exceeded threshold",
                )
                self.db_alerts_fired.insert(fire_model)
                if config.name in self._alert_hooks:
                    fired_hooks.extend(self._alert_hooks[config.name])
        return fired_hooks

    def check_pipeline_alerts(self, pipeline_id: str, pipeline_name: str, status: str, duration_ms: float, db_pipelines) -> list:
        """Check and fire pipeline-level alerts."""
        fired_hooks = []
        configs = self.db_alerts_config.get_by_field(enabled=1)

        for config in configs:
            metric_value = None
            if config.metric == "pipeline_duration_ms" and duration_ms > 0:
                metric_value = duration_ms
            elif config.metric == "error_rate" and status == "error":
                all_p = db_pipelines.get_all()
                errors = len([p for p in all_p if p.status == "error"])
                metric_value = (errors / len(all_p) * 100) if all_p else 0

            if metric_value is not None and self.evaluate_condition(config.condition, metric_value, config.value):
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
