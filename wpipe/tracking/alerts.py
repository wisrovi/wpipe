"""
Alert system for pipeline and step monitoring.
"""

import re
import uuid
from typing import Any, Dict, List, Optional

from wpipe.sqlite.tables_dto.tracker_models import AlertConfigModel, AlertFiredModel


class AlertManager:
    """Handles alert threshold configuration and firing logic."""

    def __init__(
        self,
        db_alerts_config: Any,
        db_alerts_fired: Any,
        alert_hooks: Dict[str, List[str]],
    ):
        """
        Initialize the AlertManager.

        Args:
            db_alerts_config: Database accessor for alert configurations.
            db_alerts_fired: Database accessor for fired alerts.
            alert_hooks: Dictionary mapping alert names to step names.
        """
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
        steps: Optional[List[str]] = None,
    ) -> int:
        """
        Add an alert threshold configuration.

        Args:
            metric: The metric to monitor.
            expression: The comparison expression (e.g., "> 100").
            name: Optional name for the alert.
            severity: Alert severity level.
            message: Custom alert message.
            steps: Optional list of steps associated with this alert.

        Returns:
            The ID of the inserted alert configuration.

        Raises:
            ValueError: If the expression is invalid.
        """
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

    def evaluate_condition(
        self, condition: str, actual: float, threshold: float
    ) -> bool:
        """
        Evaluate if a metric value triggers a condition.

        Args:
            condition: Comparison operator (>, <, >=, <=, ==).
            actual: The actual metric value.
            threshold: The threshold value.

        Returns:
            True if the condition is met, False otherwise.
        """
        ops = {
            ">": actual > threshold,
            "<": actual < threshold,
            ">=": actual >= threshold,
            "<=": actual <= threshold,
            "==": actual == threshold,
        }
        return ops.get(condition, False)

    def check_step_alerts(
        self, pipeline_id: str, step_name: str, duration_ms: float
    ) -> List[str]:
        """
        Check and fire step-level alerts.

        Args:
            pipeline_id: Unique identifier for the pipeline.
            step_name: Name of the step being checked.
            duration_ms: Execution duration in milliseconds.

        Returns:
            List of fired hooks (step names).
        """
        fired_hooks: List[str] = []
        # Import local constants to avoid circular imports if needed
        configs = self.db_alerts_config.get_by_field(
            metric="step_duration_ms", enabled=1
        )

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

    def check_pipeline_alerts(
        self,
        pipeline_id: str,
        pipeline_name: str,
        status: str,
        duration_ms: float,
        db_pipelines: Any,
    ) -> List[str]:
        """
        Check and fire pipeline-level alerts.

        Args:
            pipeline_id: Unique identifier for the pipeline.
            pipeline_name: Name of the pipeline.
            status: Execution status.
            duration_ms: Execution duration in milliseconds.
            db_pipelines: Database accessor for pipeline history.

        Returns:
            List of fired hooks (step names).
        """
        fired_hooks: List[str] = []
        configs = self.db_alerts_config.get_by_field(enabled=1)

        for config in configs:
            metric_value = None
            if config.metric == "pipeline_duration_ms" and duration_ms > 0:
                metric_value = duration_ms
            elif config.metric == "error_rate" and status == "error":
                all_p = db_pipelines.get_all()
                errors = len([p for p in all_p if p.status == "error"])
                metric_value = (errors / len(all_p) * 100) if all_p else 0

            if metric_value is not None and self.evaluate_condition(
                config.condition, metric_value, config.value
            ):
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
