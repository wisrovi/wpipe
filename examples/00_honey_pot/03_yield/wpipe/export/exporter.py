"""
Export and analytics module for pipeline execution data.

Provides functionality to export pipeline logs, metrics, and statistics
to various formats (JSON, CSV) for analysis and reporting.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from wsqlite import WSQLite

from wpipe.sqlite.tables_dto.tracker_models import PipelineModel, SystemMetricsModel


class PipelineExporter:
    """Export pipeline execution data to various formats."""

    def __init__(self, db_path: str):
        """
        Initialize pipeline exporter.

        Args:
            db_path: Path to the tracking database
        """
        self.db_path = db_path

    def export_pipeline_logs(
        self,
        pipeline_id: Optional[str] = None,
        format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Export pipeline execution logs.
        """
        # Forzamos el nombre de tabla 'pipelines' que es el que usa el Tracker
        db = WSQLite(PipelineModel, self.db_path)
        db.table_name = "pipelines"

        if pipeline_id:
            results = db.get_by_field(id=pipeline_id)
        else:
            results = db.get_all()

        results.sort(key=lambda x: x.started_at or "", reverse=True)
        data = [r.model_dump() for r in results]

        if format == "json":
            return self._export_json(data, output_path)
        elif format == "csv":
            return self._export_csv(data, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def export_metrics(
        self,
        pipeline_id: Optional[str] = None,
        format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Export system metrics data.
        """
        db = WSQLite(SystemMetricsModel, self.db_path)
        db.table_name = "system_metrics"

        if pipeline_id:
            results = db.get_by_field(pipeline_id=pipeline_id)
        else:
            results = db.get_all()

        results.sort(key=lambda x: x.recorded_at or "", reverse=True)
        data = [r.model_dump() for r in results]

        if format == "json":
            return self._export_json(data, output_path)
        if format == "csv":
            return self._export_csv(data, output_path)
        raise ValueError(f"Unsupported format: {format}")

    def export_statistics(
        self,
        pipeline_id: Optional[str] = None,
        format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Export pipeline statistics.
        """
        stats = self._calculate_statistics(pipeline_id)

        if format == "json":
            data = json.dumps(stats, indent=2, default=str)
            if output_path:
                Path(output_path).write_text(data)
                return output_path
            return data
        raise ValueError("Statistics export only supports JSON format")

    def _export_json(
        self, data: List[Dict[str, Any]], output_path: Optional[str] = None
    ) -> str:
        """Export data as JSON."""
        json_str = json.dumps(data, indent=2, default=str)
        if output_path:
            Path(output_path).write_text(json_str)
            return output_path
        return json_str

    def _export_csv(
        self, data: List[Dict[str, Any]], output_path: Optional[str] = None
    ) -> str:
        """Export data as CSV."""
        if not data:
            csv_str = ""
            if output_path:
                Path(output_path).write_text(csv_str)
            return csv_str

        keys = data[0].keys()
        csv_lines = [",".join(keys)]
        for row in data:
            values = [str(row[key]).replace(",", ";") for key in keys]
            csv_lines.append(",".join(values))

        csv_str = "\n".join(csv_lines)
        if output_path:
            Path(output_path).write_text(csv_str)
            return output_path
        return csv_str

    def _calculate_statistics(self, pipeline_id: Optional[str]) -> Dict[str, Any]:
        """Calculate pipeline statistics using WSQLite."""
        try:
            db = WSQLite(PipelineModel, self.db_path)
            db.table_name = "pipelines"

            if pipeline_id:
                results = db.get_by_field(id=pipeline_id)
            else:
                results = db.get_all()

            if not results:
                return {
                    "total_executions": 0,
                    "successful_executions": 0,
                    "success_rate_percent": 0.0,
                    "average_execution_time_seconds": 0.0,
                    "exported_at": datetime.now().isoformat(),
                }

            total_executions = len(results)
            durations = [r.total_duration_ms / 1000.0 for r in results if r.total_duration_ms is not None]
            avg_time = sum(durations) / len(durations) if durations else 0.0
            successful = len([r for r in results if r.status == 'completed'])

            return {
                "total_executions": total_executions,
                "successful_executions": successful,
                "success_rate_percent": round((successful / total_executions * 100), 2) if total_executions > 0 else 0,
                "average_execution_time_seconds": round(avg_time, 2),
                "exported_at": datetime.now().isoformat(),
            }
        except OSError as e:
            return {"error": str(e), "total_executions": 0}
