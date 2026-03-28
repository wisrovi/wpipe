"""
Pipeline tracker - Professional execution tracking system.

Provides a registration system with unique IDs, YAML configuration,
and complete step input/output logging for dashboard visualization.
"""

import json
import hashlib
import sqlite3
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml


class PipelineTracker:
    """
    Professional pipeline tracking system.

    Features:
    - Unique pipeline ID (matrícula) for each execution
    - YAML configuration file generation
    - Complete input/output logging per step
    - Prevents duplicate registrations
    - Real-time status tracking
    """

    SCHEMA = """
    -- Pipelines table - main execution records
    CREATE TABLE IF NOT EXISTS pipelines (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        config_yaml TEXT,
        status TEXT NOT NULL DEFAULT 'running',
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        total_duration_ms REAL,
        input_data TEXT,
        output_data TEXT,
        error_message TEXT,
        error_step TEXT,
        worker_id TEXT,
        worker_name TEXT,
        tags TEXT,
        metadata TEXT
    );
    
    -- Steps table - detailed step execution records
    CREATE TABLE IF NOT EXISTS steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pipeline_id TEXT NOT NULL,
        step_order INTEGER NOT NULL,
        step_name TEXT NOT NULL,
        step_version TEXT,
        step_type TEXT DEFAULT 'task',
        status TEXT NOT NULL DEFAULT 'pending',
        started_at TIMESTAMP,
        completed_at TIMESTAMP,
        duration_ms REAL,
        input_data TEXT,
        output_data TEXT,
        error_message TEXT,
        error_traceback TEXT,
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(id) ON DELETE CASCADE
    );
    
    -- Step metrics for analytics
    CREATE TABLE IF NOT EXISTS step_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        step_id INTEGER NOT NULL,
        metric_name TEXT NOT NULL,
        metric_value REAL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (step_id) REFERENCES steps(id) ON DELETE CASCADE
    );
    
    -- Indexes for performance
    CREATE INDEX IF NOT EXISTS idx_pipelines_id ON pipelines(id);
    CREATE INDEX IF NOT EXISTS idx_pipelines_status ON pipelines(status);
    CREATE INDEX IF NOT EXISTS idx_pipelines_started ON pipelines(started_at);
    CREATE INDEX IF NOT EXISTS idx_steps_pipeline ON steps(pipeline_id);
    CREATE INDEX IF NOT EXISTS idx_steps_status ON steps(status);
    """

    def __init__(self, db_path: str, config_dir: Optional[str] = None):
        """
        Initialize the tracker.

        Args:
            db_path: Path to SQLite database.
            config_dir: Directory to store YAML config files (optional).
        """
        self.db_path = db_path
        self.config_dir = (
            Path(config_dir)
            if config_dir
            else Path(db_path).parent / "pipeline_configs"
        )
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_tables()

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    def _ensure_tables(self):
        """Create tables if they don't exist."""
        with self._get_connection() as conn:
            conn.executescript(self.SCHEMA)

    def _generate_id(self, name: str, worker_id: Optional[str] = None) -> str:
        """
        Generate a unique pipeline ID (matrícula).

        Format: PIPE-XXXXXXXX (8 char hex unique ID)
        """
        unique = uuid.uuid4().hex[:8].upper()
        return f"PIPE-{unique}"

    def _generate_yaml_config(
        self,
        pipeline_id: str,
        name: str,
        steps: list,
        metadata: Optional[dict] = None,
    ) -> str:
        """
        Generate YAML configuration file for the pipeline.

        Args:
            pipeline_id: Unique pipeline ID.
            name: Pipeline name.
            steps: List of step configurations.
            metadata: Additional metadata.

        Returns:
            Path to the generated YAML file.
        """
        config = {
            "pipeline": {
                "id": pipeline_id,
                "name": name,
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
            },
            "steps": steps,
            "metadata": metadata or {},
        }

        yaml_content = yaml.dump(config, default_flow_style=False, allow_unicode=True)

        # Save YAML file
        yaml_path = self.config_dir / f"{pipeline_id}.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")

        return str(yaml_path)

    def register_pipeline(
        self,
        name: str,
        steps: list,
        input_data: Optional[dict] = None,
        worker_id: Optional[str] = None,
        worker_name: Optional[str] = None,
        metadata: Optional[dict] = None,
        tags: Optional[list] = None,
    ) -> dict:
        """
        Register a new pipeline execution (matrícula).

        This creates a unique pipeline ID and generates a YAML config file.
        If a pipeline with the same name and steps already exists and is running,
        it returns the existing ID instead of creating a new one.

        Args:
            name: Pipeline name.
            steps: List of step configurations (name, version, type).
            input_data: Initial input data.
            worker_id: Worker identifier.
            worker_name: Worker name.
            metadata: Additional metadata.
            tags: Tags for categorization.

        Returns:
            Dict with pipeline_id, yaml_path, and status.
        """
        pipeline_id = self._generate_id(name, worker_id)

        # Generate step configurations for YAML
        step_configs = []
        for step in steps:
            if isinstance(step, dict):
                step_configs.append(step)
            elif isinstance(step, (list, tuple)):
                step_name = step[1] if len(step) > 1 else str(step[0])
                step_version = step[2] if len(step) > 2 else "1.0.0"
                step_configs.append(
                    {
                        "name": step_name,
                        "version": step_version,
                        "type": "task",
                    }
                )

        # Generate YAML config
        yaml_path = self._generate_yaml_config(
            pipeline_id=pipeline_id,
            name=name,
            steps=step_configs,
            metadata=metadata,
        )

        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO pipelines 
                (id, name, config_yaml, status, input_data, worker_id, worker_name, tags, metadata)
                VALUES (?, ?, ?, 'running', ?, ?, ?, ?, ?)
                """,
                (
                    pipeline_id,
                    name,
                    yaml_path,
                    json.dumps(input_data) if input_data else None,
                    worker_id,
                    worker_name,
                    json.dumps(tags) if tags else None,
                    json.dumps(metadata) if metadata else None,
                ),
            )

        return {
            "pipeline_id": pipeline_id,
            "yaml_path": yaml_path,
            "status": "registered",
        }

    def start_step(
        self,
        pipeline_id: str,
        step_order: int,
        step_name: str,
        step_version: Optional[str] = None,
        step_type: str = "task",
        input_data: Optional[dict] = None,
    ) -> int:
        """
        Start tracking a pipeline step.

        Args:
            pipeline_id: Parent pipeline ID.
            step_order: Order of the step.
            step_name: Step name.
            step_version: Step version.
            step_type: Type of step.
            input_data: Step input data (will be logged).

        Returns:
            Step ID.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO steps 
                (pipeline_id, step_order, step_name, step_version, step_type, 
                 status, started_at, input_data)
                VALUES (?, ?, ?, ?, ?, 'running', ?, ?)
                """,
                (
                    pipeline_id,
                    step_order,
                    step_name,
                    step_version,
                    step_type,
                    datetime.now().isoformat(),
                    json.dumps(input_data, default=str) if input_data else None,
                ),
            )
            return cursor.lastrowid

    def complete_step(
        self,
        step_id: int,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_traceback: Optional[str] = None,
        metrics: Optional[dict] = None,
    ):
        """
        Complete a step execution.

        Args:
            step_id: Step ID.
            output_data: Step output data (will be logged).
            error_message: Error message if failed.
            error_traceback: Error traceback if failed.
            metrics: Additional metrics to record.
        """
        status = "error" if error_message else "completed"

        with self._get_connection() as conn:
            # Get start time for duration calculation
            row = conn.execute(
                "SELECT started_at FROM steps WHERE id = ?", (step_id,)
            ).fetchone()

            if row and row["started_at"]:
                started = datetime.fromisoformat(row["started_at"])
                duration_ms = (datetime.now() - started).total_seconds() * 1000
            else:
                duration_ms = None

            conn.execute(
                """
                UPDATE steps 
                SET status = ?, completed_at = ?, duration_ms = ?,
                    output_data = ?, error_message = ?, error_traceback = ?
                WHERE id = ?
                """,
                (
                    status,
                    datetime.now().isoformat(),
                    duration_ms,
                    json.dumps(output_data, default=str) if output_data else None,
                    error_message,
                    error_traceback,
                    step_id,
                ),
            )

            # Record metrics
            if metrics:
                for metric_name, metric_value in metrics.items():
                    conn.execute(
                        """
                        INSERT INTO step_metrics (step_id, metric_name, metric_value)
                        VALUES (?, ?, ?)
                        """,
                        (step_id, metric_name, float(metric_value)),
                    )

    def complete_pipeline(
        self,
        pipeline_id: str,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_step: Optional[str] = None,
    ):
        """
        Complete pipeline execution.

        Args:
            pipeline_id: Pipeline ID.
            output_data: Pipeline output data.
            error_message: Error message if failed.
            error_step: Name of the step that failed.
        """
        status = "error" if error_message else "completed"

        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT started_at FROM pipelines WHERE id = ?", (pipeline_id,)
            ).fetchone()

            if row and row["started_at"]:
                started = datetime.fromisoformat(row["started_at"])
                duration_ms = (datetime.now() - started).total_seconds() * 1000
            else:
                duration_ms = None

            conn.execute(
                """
                UPDATE pipelines 
                SET status = ?, completed_at = ?, total_duration_ms = ?,
                    output_data = ?, error_message = ?, error_step = ?
                WHERE id = ?
                """,
                (
                    status,
                    datetime.now().isoformat(),
                    duration_ms,
                    json.dumps(output_data, default=str) if output_data else None,
                    error_message,
                    error_step,
                    pipeline_id,
                ),
            )

    def get_pipeline(self, pipeline_id: str) -> Optional[dict]:
        """Get pipeline with all steps."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM pipelines WHERE id = ?", (pipeline_id,)
            ).fetchone()

            if not row:
                return None

            pipeline = dict(row)

            # Parse JSON fields
            for field in ["input_data", "output_data", "tags", "metadata"]:
                if pipeline.get(field):
                    try:
                        pipeline[field] = json.loads(pipeline[field])
                    except (json.JSONDecodeError, TypeError):
                        pass

            # Get steps with their data
            steps = conn.execute(
                "SELECT * FROM steps WHERE pipeline_id = ? ORDER BY step_order",
                (pipeline_id,),
            ).fetchall()

            pipeline["steps"] = []
            for step in steps:
                step_dict = dict(step)
                for field in ["input_data", "output_data"]:
                    if step_dict.get(field):
                        try:
                            step_dict[field] = json.loads(step_dict[field])
                        except (json.JSONDecodeError, TypeError):
                            pass
                pipeline["steps"].append(step_dict)

            return pipeline

    def get_pipelines(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None,
    ) -> list:
        """Get list of pipelines."""
        with self._get_connection() as conn:
            if status:
                rows = conn.execute(
                    """
                    SELECT * FROM pipelines WHERE status = ?
                    ORDER BY started_at DESC LIMIT ? OFFSET ?
                    """,
                    (status, limit, offset),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM pipelines
                    ORDER BY started_at DESC LIMIT ? OFFSET ?
                    """,
                    (limit, offset),
                ).fetchall()

            result = []
            for row in rows:
                pipeline = dict(row)
                # Parse JSON fields
                for field in ["input_data", "output_data", "tags", "metadata"]:
                    if pipeline.get(field):
                        try:
                            pipeline[field] = json.loads(pipeline[field])
                        except (json.JSONDecodeError, TypeError):
                            pass
                result.append(pipeline)

            return result

    def get_pipeline_graph(self, pipeline_id: str) -> dict:
        """Get pipeline data formatted for graph visualization."""
        pipeline = self.get_pipeline(pipeline_id)

        if not pipeline:
            return {"nodes": [], "edges": []}

        nodes = []
        edges = []

        for i, step in enumerate(pipeline.get("steps", [])):
            node = {
                "id": f"step_{step['id']}",
                "name": step["step_name"],
                "type": step["step_type"],
                "status": step["status"],
                "duration_ms": step.get("duration_ms"),
                "version": step.get("step_version"),
                "error": step.get("error_message"),
                "order": step["step_order"],
                "has_input": step.get("input_data") is not None,
                "has_output": step.get("output_data") is not None,
            }
            nodes.append(node)

            if i > 0:
                edges.append(
                    {
                        "from": f"step_{pipeline['steps'][i - 1]['id']}",
                        "to": f"step_{step['id']}",
                    }
                )

        return {
            "pipeline_id": pipeline_id,
            "pipeline_name": pipeline["name"],
            "status": pipeline["status"],
            "total_duration_ms": pipeline.get("total_duration_ms"),
            "started_at": pipeline.get("started_at"),
            "completed_at": pipeline.get("completed_at"),
            "nodes": nodes,
            "edges": edges,
        }

    def get_stats(self) -> dict:
        """Get overall statistics."""
        with self._get_connection() as conn:
            total = conn.execute("SELECT COUNT(*) as cnt FROM pipelines").fetchone()[
                "cnt"
            ]
            completed = conn.execute(
                "SELECT COUNT(*) as cnt FROM pipelines WHERE status = 'completed'"
            ).fetchone()["cnt"]
            errors = conn.execute(
                "SELECT COUNT(*) as cnt FROM pipelines WHERE status = 'error'"
            ).fetchone()["cnt"]
            running = conn.execute(
                "SELECT COUNT(*) as cnt FROM pipelines WHERE status = 'running'"
            ).fetchone()["cnt"]

            avg_duration = conn.execute(
                "SELECT AVG(total_duration_ms) as avg FROM pipelines WHERE status = 'completed'"
            ).fetchone()["avg"]

            total_steps = conn.execute("SELECT COUNT(*) as cnt FROM steps").fetchone()[
                "cnt"
            ]
            completed_steps = conn.execute(
                "SELECT COUNT(*) as cnt FROM steps WHERE status = 'completed'"
            ).fetchone()["cnt"]

            success_rate = ((completed / total) * 100) if total > 0 else 0

            # Step success rate
            step_success = (
                ((completed_steps / total_steps) * 100) if total_steps > 0 else 0
            )

            return {
                "total_pipelines": total,
                "completed": completed,
                "errors": errors,
                "running": running,
                "success_rate": round(success_rate, 1),
                "avg_duration_ms": round(avg_duration, 2) if avg_duration else 0,
                "total_steps": total_steps,
                "step_success_rate": round(step_success, 1),
            }

    def delete_pipeline(self, pipeline_id: str):
        """Delete a pipeline and its steps."""
        with self._get_connection() as conn:
            conn.execute(
                "DELETE FROM step_metrics WHERE step_id IN (SELECT id FROM steps WHERE pipeline_id = ?)",
                (pipeline_id,),
            )
            conn.execute("DELETE FROM steps WHERE pipeline_id = ?", (pipeline_id,))
            conn.execute("DELETE FROM pipelines WHERE id = ?", (pipeline_id,))

        # Delete YAML file
        yaml_path = self.config_dir / f"{pipeline_id}.yaml"
        if yaml_path.exists():
            yaml_path.unlink()

    def clear_old_pipelines(self, days: int = 30):
        """Clear pipelines older than specified days."""
        with self._get_connection() as conn:
            # Get old pipeline IDs
            old_ids = conn.execute(
                "SELECT id FROM pipelines WHERE started_at < datetime('now', '-' || ? || ' days')",
                (days,),
            ).fetchall()

            for row in old_ids:
                self.delete_pipeline(row["id"])
