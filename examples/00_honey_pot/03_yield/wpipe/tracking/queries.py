"""
Data query module for pipeline and event retrieval.
"""

import json
from typing import List, Optional


class QueryManager:
    """Handles data retrieval for the dashboard and API."""

    def __init__(
        self, db_pipelines, db_steps, db_alerts_config, db_alerts_fired, db_events
    ):
        self.db_pipelines = db_pipelines
        self.db_steps = db_steps
        self.db_alerts_config = db_alerts_config
        self.db_alerts_fired = db_alerts_fired
        self.db_events = db_events

    def get_pipelines(
        self, limit: int = 50, offset: int = 0, status: Optional[str] = None
    ) -> List[dict]:
        """Get list of pipelines for the dashboard."""
        try:
            all_pipelines = self.db_pipelines.get_all()
        except Exception:
            return []

        all_pipelines.sort(key=lambda x: x.started_at or "", reverse=True)

        if status:
            all_pipelines = [p for p in all_pipelines if p.status == status]

        paged = all_pipelines[offset : offset + limit]

        result = []
        for p in paged:
            try:
                d = p.model_dump()
                for field in ["input_data", "output_data"]:
                    if d.get(field):
                        try:
                            d[field] = json.loads(d[field])
                        except:
                            pass
                result.append(d)
            except Exception:
                continue
        return result

    def get_pipeline(self, pipeline_id: str) -> Optional[dict]:
        """Get detailed pipeline data including steps."""
        try:
            pipelines = self.db_pipelines.get_by_field(id=pipeline_id)
        except Exception:
            return None

        if not pipelines:
            return None

        try:
            pipeline = pipelines[0].model_dump()
        except Exception:
            return None

        for field in ["input_data", "output_data"]:
            if pipeline.get(field):
                try:
                    pipeline[field] = json.loads(pipeline[field])
                except:
                    pass

        try:
            steps = self.db_steps.get_by_field(pipeline_id=pipeline_id)
            steps.sort(key=lambda x: x.step_order)
        except Exception:
            steps = []

        pipeline["steps"] = []
        for s in steps:
            try:
                sd = s.model_dump()
                for field in ["input_data", "output_data"]:
                    if sd.get(field):
                        try:
                            sd[field] = json.loads(sd[field])
                        except:
                            pass
                pipeline["steps"].append(sd)
            except Exception:
                continue

        return pipeline

    def get_pipeline_executions(
        self, name: str, limit: int = 100, offset: int = 0
    ) -> List[dict]:
        """Get all executions of a pipeline by name."""
        all_p = self.db_pipelines.get_by_field(name=name)
        all_p.sort(key=lambda x: x.started_at or "", reverse=True)
        return [p.model_dump() for p in all_p[offset : offset + limit]]

    def get_fired_alerts(
        self, limit: int = 50, severity: Optional[str] = None
    ) -> List[dict]:
        """Get recent fired alerts."""
        alerts = self.db_alerts_fired.get_all()
        alerts.sort(key=lambda x: x.fired_at or "", reverse=True)
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return [a.model_dump() for a in alerts[:limit]]

    def get_alert_thresholds(self) -> List[dict]:
        """Get alert configurations."""
        return [c.model_dump() for c in self.db_alerts_config.get_all()]

    def get_events(
        self, pipeline_id: Optional[str] = None, limit: int = 50
    ) -> List[dict]:
        """Get pipeline events."""
        events = (
            self.db_events.get_by_field(pipeline_id=pipeline_id)
            if pipeline_id
            else self.db_events.get_all()
        )
        events.sort(key=lambda x: x.created_at or "", reverse=True)
        return [e.model_dump() for e in events[:limit]]
