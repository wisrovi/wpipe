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
    """
    Export pipeline execution data to various formats.

    Attributes:
        db_path (str): Path to the tracking database file.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initializes the pipeline exporter.

        Args:
            db_path (str): Path to the tracking database.
        """
        self.db_path = db_path

    def export_pipeline_logs(
        self,
        pipeline_id: Optional[str] = None,
        export_format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Exports pipeline execution logs.

        Args:
            pipeline_id (Optional[str]): ID of the pipeline to export. If None, exports all.
            export_format (str): Export format ('json' or 'csv'). Defaults to 'json'.
            output_path (Optional[str]): File path to save the export. If None, returns string.

        Returns:
            str: Exported data as a string or the path to the saved file.

        Raises:
            ValueError: If the requested format is not supported.
        """
        # Force the table name to 'pipelines' as used by the Tracker.
        db = WSQLite(PipelineModel, self.db_path)
        db.table_name = "pipelines"

        if pipeline_id:
            results = db.get_by_field(id=pipeline_id)
        else:
            results = db.get_all()

        results.sort(key=lambda x: x.started_at or "", reverse=True)
        data = [r.model_dump() for r in results]

        if export_format == "json":
            return self._export_json(data, output_path)
        if export_format == "csv":
            return self._export_csv(data, output_path)
        raise ValueError(f"Unsupported format: {export_format}")

    def export_metrics(
        self,
        pipeline_id: Optional[str] = None,
        export_format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Exports system metrics data.

        Args:
            pipeline_id (Optional[str]): ID of the pipeline to export metrics for.
            export_format (str): Export format ('json' or 'csv'). Defaults to 'json'.
            output_path (Optional[str]): File path to save the export.

        Returns:
            str: Exported data as a string or the path to the saved file.

        Raises:
            ValueError: If the requested format is not supported.
        """
        db = WSQLite(SystemMetricsModel, self.db_path)
        db.table_name = "system_metrics"

        if pipeline_id:
            results = db.get_by_field(pipeline_id=pipeline_id)
        else:
            results = db.get_all()

        results.sort(key=lambda x: x.recorded_at or "", reverse=True)
        data = [r.model_dump() for r in results]

        if export_format == "json":
            return self._export_json(data, output_path)
        if export_format == "csv":
            return self._export_csv(data, output_path)
        raise ValueError(f"Unsupported format: {export_format}")

    def export_statistics(
        self,
        pipeline_id: Optional[str] = None,
        export_format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Exports calculated pipeline statistics.

        Args:
            pipeline_id (Optional[str]): ID of the pipeline to calculate stats for.
            export_format (str): Export format (only 'json' is supported). Defaults to 'json'.
            output_path (Optional[str]): File path to save the export.

        Returns:
            str: Exported statistics as a string or the path to the saved file.

        Raises:
            ValueError: If the requested format is not supported.
        """
        stats = self._calculate_statistics(pipeline_id)

        if export_format == "json":
            data = json.dumps(stats, indent=2, default=str)
            if output_path:
                Path(output_path).write_text(data, encoding="utf-8")
                return output_path
            return data
        raise ValueError("Statistics export only supports JSON format")

    def _export_json(
        self, data: List[Dict[str, Any]], output_path: Optional[str] = None
    ) -> str:
        """
        Exports data as a JSON string or file.

        Args:
            data (List[Dict[str, Any]]): Data to export.
            output_path (Optional[str]): File path to save the export.

        Returns:
            str: JSON string or the path to the saved file.
        """
        json_str = json.dumps(data, indent=2, default=str)
        if output_path:
            Path(output_path).write_text(json_str, encoding="utf-8")
            return output_path
        return json_str

    def _export_csv(
        self, data: List[Dict[str, Any]], output_path: Optional[str] = None
    ) -> str:
        """
        Exports data as a CSV string or file.

        Args:
            data (List[Dict[str, Any]]): Data to export.
            output_path (Optional[str]): File path to save the export.

        Returns:
            str: CSV string or the path to the saved file.
        """
        if not data:
            csv_str = ""
            if output_path:
                Path(output_path).write_text(csv_str, encoding="utf-8")
            return csv_str

        keys = list(data[0].keys())
        csv_lines = [",".join(keys)]
        for row in data:
            values = [str(row.get(key, "")).replace(",", ";") for key in keys]
            csv_lines.append(",".join(values))

        csv_str = "\n".join(csv_lines)
        if output_path:
            Path(output_path).write_text(csv_str, encoding="utf-8")
            return output_path
        return csv_str

    def _calculate_statistics(self, pipeline_id: Optional[str]) -> Dict[str, Any]:
        """
        Calculates pipeline execution statistics using WSQLite.

        Args:
            pipeline_id (Optional[str]): ID of the pipeline to analyze.

        Returns:
            Dict[str, Any]: Dictionary containing calculated statistics.
        """
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
            durations = [
                r.total_duration_ms / 1000.0
                for r in results
                if r.total_duration_ms is not None
            ]
            avg_time = sum(durations) / len(durations) if durations else 0.0
            successful = len([r for r in results if r.status == 'completed'])

            return {
                "total_executions": total_executions,
                "successful_executions": successful,
                "success_rate_percent": round(
                    (successful / total_executions * 100), 2
                ) if total_executions > 0 else 0,
                "average_execution_time_seconds": round(avg_time, 2),
                "exported_at": datetime.now().isoformat(),
            }
        except OSError as e:
            return {"error": str(e), "total_executions": 0}
