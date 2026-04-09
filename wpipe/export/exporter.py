"""
Export and analytics module for pipeline execution data.

Provides functionality to export pipeline logs, metrics, and statistics
to various formats (JSON, CSV) for analysis and reporting.
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import sqlite3
from pathlib import Path


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

        Args:
            pipeline_id: Optional pipeline ID to filter by
            format: Export format ('json' or 'csv')
            output_path: Path to save export file

        Returns:
            Exported data as string or file path
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM executions"
            if pipeline_id:
                query += f" WHERE pipeline_id = '{pipeline_id}'"
            query += " ORDER BY created_at DESC"

            cursor.execute(query)
            rows = cursor.fetchall()

        if format == "json":
            return self._export_json(rows, output_path)
        elif format == "csv":
            return self._export_csv(rows, output_path)
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

        Args:
            pipeline_id: Optional pipeline ID to filter by
            format: Export format ('json' or 'csv')
            output_path: Path to save export file

        Returns:
            Exported data as string or file path
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM system_metrics"
            if pipeline_id:
                query += f" WHERE pipeline_id = '{pipeline_id}'"
            query += " ORDER BY created_at DESC"

            cursor.execute(query)
            rows = cursor.fetchall()

        if format == "json":
            return self._export_json(rows, output_path)
        elif format == "csv":
            return self._export_csv(rows, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def export_statistics(
        self,
        pipeline_id: Optional[str] = None,
        format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Export pipeline statistics and summary.

        Args:
            pipeline_id: Optional pipeline ID to filter by
            format: Export format ('json' or 'csv')
            output_path: Path to save export file

        Returns:
            Exported data as string or file path
        """
        stats = self._calculate_statistics(pipeline_id)

        if format == "json":
            data = json.dumps(stats, indent=2, default=str)
            if output_path:
                Path(output_path).write_text(data)
                return output_path
            return data
        else:
            raise ValueError("Statistics export only supports JSON format")

    def _export_json(
        self, rows: List[sqlite3.Row], output_path: Optional[str] = None
    ) -> str:
        """Export data as JSON."""
        data = [dict(row) for row in rows]
        json_str = json.dumps(data, indent=2, default=str)

        if output_path:
            Path(output_path).write_text(json_str)
            return output_path

        return json_str

    def _export_csv(
        self, rows: List[sqlite3.Row], output_path: Optional[str] = None
    ) -> str:
        """Export data as CSV."""
        if not rows:
            csv_str = ""
            if output_path:
                Path(output_path).write_text(csv_str)
                return output_path
            return csv_str

        keys = rows[0].keys()
        csv_lines = [",".join(keys)]

        for row in rows:
            values = [str(row[key]).replace(",", ";") for key in keys]
            csv_lines.append(",".join(values))

        csv_str = "\n".join(csv_lines)

        if output_path:
            Path(output_path).write_text(csv_str)
            return output_path

        return csv_str

    def _calculate_statistics(self, pipeline_id: Optional[str]) -> Dict[str, Any]:
        """Calculate pipeline statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            try:
                # Check if table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='executions'")
                if not cursor.fetchone():
                    # Table doesn't exist, return empty stats
                    return {
                        "total_executions": 0,
                        "successful_executions": 0,
                        "success_rate_percent": 0.0,
                        "average_execution_time_seconds": 0.0,
                        "exported_at": datetime.now().isoformat(),
                    }
                
                # Total executions
                exec_query = "SELECT COUNT(*) FROM executions"
                if pipeline_id:
                    exec_query += f" WHERE pipeline_id = '{pipeline_id}'"
                cursor.execute(exec_query)
                total_executions = cursor.fetchone()[0]

                # Average execution time
                time_query = "SELECT AVG(execution_time) FROM executions WHERE execution_time IS NOT NULL"
                if pipeline_id:
                    time_query += f" AND pipeline_id = '{pipeline_id}'"
                cursor.execute(time_query)
                avg_time = cursor.fetchone()[0] or 0

                # Success rate
                success_query = "SELECT COUNT(*) FROM executions WHERE status = 'completed'"
                if pipeline_id:
                    success_query += f" AND pipeline_id = '{pipeline_id}'"
                cursor.execute(success_query)
                successful = cursor.fetchone()[0]

                success_rate = (successful / total_executions * 100) if total_executions > 0 else 0

            except sqlite3.OperationalError:
                # Table doesn't exist or other error
                return {
                    "total_executions": 0,
                    "successful_executions": 0,
                    "success_rate_percent": 0.0,
                    "average_execution_time_seconds": 0.0,
                    "exported_at": datetime.now().isoformat(),
                }

        return {
            "total_executions": total_executions,
            "successful_executions": successful,
            "success_rate_percent": round(success_rate, 2),
            "average_execution_time_seconds": round(avg_time, 2),
            "exported_at": datetime.now().isoformat(),
        }
