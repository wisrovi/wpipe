"""
Data query module for pipeline and event retrieval.
"""

import json
from typing import Any, Dict, List, Optional


class QueryManager:
    """Handles data retrieval for the dashboard and API."""

    def __init__(
        self,
        db_pipelines: Any,
        db_steps: Any,
        db_alerts_config: Any,
        db_alerts_fired: Any,
        db_events: Any,
    ):
        """
        Initialize the QueryManager with database accessors.

        Args:
            db_pipelines: Database accessor for pipeline history.
            db_steps: Database accessor for step history.
            db_alerts_config: Database accessor for alert configurations.
            db_alerts_fired: Database accessor for fired alerts.
            db_events: Database accessor for pipeline events.
        """
        self.db_pipelines = db_pipelines
        self.db_steps = db_steps
        self.db_alerts_config = db_alerts_config
        self.db_alerts_fired = db_alerts_fired
        self.db_events = db_events

    @staticmethod
    def _parse_json_fields(data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """
        Parse JSON strings in specified fields of a dictionary.

        Args:
            data: The dictionary containing the fields.
            fields: List of field names to parse.

        Returns:
            The dictionary with parsed JSON fields.
        """
        for field in fields:
            value = data.get(field)
            if isinstance(value, str) and value:
                try:
                    data[field] = json.loads(value)
                except json.JSONDecodeError:
                    pass
        return data

    def get_pipelines(
        self, limit: int = 50, offset: int = 0, status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get list of pipelines for the dashboard.

        Args:
            limit: Maximum number of pipelines to return.
            offset: Number of pipelines to skip.
            status: Filter by pipeline status.

        Returns:
            A list of pipeline data dictionaries.
        """
        try:
            all_pipelines = self.db_pipelines.get_all()
        except (AttributeError, RuntimeError, ValueError):
            return []

        all_pipelines.sort(key=lambda x: x.started_at or "", reverse=True)

        if status:
            all_pipelines = [p for p in all_pipelines if p.status == status]

        paged = all_pipelines[offset : offset + limit]

        result = []
        for p in paged:
            try:
                d = p.model_dump()
                self._parse_json_fields(d, ["input_data", "output_data"])
                result.append(d)
            except (AttributeError, TypeError):
                continue
        return result

    def get_pipeline(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed pipeline data including steps.

        Args:
            pipeline_id: Unique identifier for the pipeline.

        Returns:
            Dictionary with pipeline and steps data, or None if not found.
        """
        try:
            pipelines = self.db_pipelines.get_by_field(id=pipeline_id)
        except (AttributeError, RuntimeError, ValueError):
            return None

        if not pipelines:
            return None

        try:
            pipeline = pipelines[0].model_dump()
        except (AttributeError, IndexError):
            return None

        self._parse_json_fields(pipeline, ["input_data", "output_data"])

        try:
            steps = self.db_steps.get_by_field(pipeline_id=pipeline_id)
            steps.sort(key=lambda x: x.step_order)
        except (AttributeError, RuntimeError, ValueError):
            steps = []

        pipeline["steps"] = []
        for s in steps:
            try:
                sd = s.model_dump()
                self._parse_json_fields(sd, ["input_data", "output_data"])
                pipeline["steps"].append(sd)
            except (AttributeError, TypeError):
                continue

        return pipeline

    def get_pipeline_executions(
        self, name: str, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get all executions of a pipeline by name.

        Args:
            name: Name of the pipeline.
            limit: Maximum number of executions to return.
            offset: Number of executions to skip.

        Returns:
            A list of pipeline execution data dictionaries.
        """
        try:
            all_p = self.db_pipelines.get_by_field(name=name)
            all_p.sort(key=lambda x: x.started_at or "", reverse=True)
            return [p.model_dump() for p in all_p[offset : offset + limit]]
        except (AttributeError, RuntimeError, ValueError):
            return []

    def get_fired_alerts(
        self, limit: int = 50, severity: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recent fired alerts.

        Args:
            limit: Maximum number of alerts to return.
            severity: Filter by alert severity.

        Returns:
            A list of fired alert data dictionaries.
        """
        try:
            alerts = self.db_alerts_fired.get_all()
            alerts.sort(key=lambda x: x.fired_at or "", reverse=True)
            if severity:
                alerts = [a for a in alerts if a.severity == severity]
            return [a.model_dump() for a in alerts[:limit]]
        except (AttributeError, RuntimeError, ValueError):
            return []

    def get_alert_thresholds(self) -> List[Dict[str, Any]]:
        """
        Get alert configurations.

        Returns:
            A list of alert configuration dictionaries.
        """
        try:
            return [c.model_dump() for c in self.db_alerts_config.get_all()]
        except (AttributeError, RuntimeError, ValueError):
            return []

    def get_events(
        self, pipeline_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get pipeline events.

        Args:
            pipeline_id: Optional filter by pipeline ID.
            limit: Maximum number of events to return.

        Returns:
            A list of event data dictionaries.
        """
        try:
            events = (
                self.db_events.get_by_field(pipeline_id=pipeline_id)
                if pipeline_id
                else self.db_events.get_all()
            )
            events.sort(key=lambda x: x.created_at or "", reverse=True)
            return [e.model_dump() for e in events[:limit]]
        except (AttributeError, RuntimeError, ValueError):
            return []
