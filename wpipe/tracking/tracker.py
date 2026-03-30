"""
wpipe Pipeline Tracker - Professional Execution Tracking System.

Complete tracking system with:
- Unique pipeline IDs (matrícula) with YAML configuration
- Performance metrics with percentiles (p50, p95, p99)
- Alert system with configurable thresholds
- Event/milestone annotations
- Pipeline relationship tracking
- System metrics (CPU, memory, disk)
- Execution comparison
"""

import json
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import yaml


def _safe_json_dumps(obj: Any) -> Optional[str]:
    """Safely serialize object to JSON, handling non-serializable types."""
    if obj is None:
        return None
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):

        def default_handler(o):
            if hasattr(o, "__dict__"):
                return str(o)
            return str(o)

        try:
            return json.dumps(obj, default=default_handler)
        except (TypeError, ValueError):
            return json.dumps({"_raw": str(obj)})


@dataclass
class AlertThreshold:
    """Alert threshold configuration."""

    metric: str  # pipeline_duration_ms, step_duration_ms, error_rate, success_rate
    condition: str  # >, <, >=, <=, ==
    value: float
    severity: str  # info, warning, critical
    message: Optional[str] = None
    enabled: bool = True


class PipelineTracker:
    """
    Professional pipeline tracking system.

    Features:
    - Unique pipeline ID (matrícula) for each execution
    - YAML configuration file generation
    - Complete input/output logging per step
    - Performance metrics with percentiles
    - Alert system with configurable thresholds
    - Event/annotation system
    - Pipeline relationship tracking
    - System metrics collection
    - Execution comparison
    """

    SCHEMA = """
    -- Core tables
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

    -- Performance metrics (aggregated statistics)
    CREATE TABLE IF NOT EXISTS performance_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,  -- 'pipeline' or 'step'
        entity_name TEXT NOT NULL,
        period_start TIMESTAMP NOT NULL,
        period_end TIMESTAMP NOT NULL,
        execution_count INTEGER DEFAULT 0,
        success_count INTEGER DEFAULT 0,
        error_count INTEGER DEFAULT 0,
        avg_duration_ms REAL,
        min_duration_ms REAL,
        max_duration_ms REAL,
        p50_duration_ms REAL,
        p95_duration_ms REAL,
        p99_duration_ms REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Step duration history (for trend charts)
    CREATE TABLE IF NOT EXISTS step_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pipeline_id TEXT NOT NULL,
        step_name TEXT NOT NULL,
        step_version TEXT,
        duration_ms REAL NOT NULL,
        status TEXT NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(id) ON DELETE CASCADE
    );

    -- Alert configurations
    CREATE TABLE IF NOT EXISTS alerts_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        metric TEXT NOT NULL,
        condition TEXT NOT NULL,
        value REAL NOT NULL,
        severity TEXT DEFAULT 'warning',
        message TEXT,
        enabled INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Fired alerts
    CREATE TABLE IF NOT EXISTS alerts_fired (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_config_id INTEGER,
        pipeline_id TEXT,
        step_id INTEGER,
        metric TEXT NOT NULL,
        metric_value REAL NOT NULL,
        threshold_value REAL NOT NULL,
        severity TEXT NOT NULL,
        message TEXT,
        acknowledged INTEGER DEFAULT 0,
        acknowledged_at TIMESTAMP,
        fired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alert_config_id) REFERENCES alerts_config(id) ON DELETE SET NULL,
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(id) ON DELETE SET NULL
    );

    -- Events/annotations
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pipeline_id TEXT,
        step_id INTEGER,
        event_type TEXT NOT NULL,
        event_name TEXT NOT NULL,
        message TEXT,
        data TEXT,
        tags TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(id) ON DELETE CASCADE
    );

    -- Pipeline relationships
    CREATE TABLE IF NOT EXISTS pipeline_relations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_pipeline_id TEXT NOT NULL,
        child_pipeline_id TEXT NOT NULL,
        relation_type TEXT NOT NULL DEFAULT 'triggered',
        metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (parent_pipeline_id) REFERENCES pipelines(id) ON DELETE CASCADE,
        FOREIGN KEY (child_pipeline_id) REFERENCES pipelines(id) ON DELETE CASCADE,
        UNIQUE(parent_pipeline_id, child_pipeline_id, relation_type)
    );

    -- System metrics during execution
    CREATE TABLE IF NOT EXISTS system_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pipeline_id TEXT NOT NULL,
        cpu_percent REAL,
        memory_percent REAL,
        memory_used_mb REAL,
        memory_available_mb REAL,
        disk_io_read_mb REAL,
        disk_io_write_mb REAL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(id) ON DELETE CASCADE
    );

    -- Comparisons between executions
    CREATE TABLE IF NOT EXISTS comparisons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comparison_uuid TEXT UNIQUE,
        pipeline_a_id TEXT NOT NULL,
        pipeline_b_id TEXT NOT NULL,
        comparison_data TEXT,
        duration_diff_ms REAL,
        status_diff TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pipeline_a_id) REFERENCES pipelines(id) ON DELETE CASCADE,
        FOREIGN KEY (pipeline_b_id) REFERENCES pipelines(id) ON DELETE CASCADE
    );

    -- Indexes
    CREATE INDEX IF NOT EXISTS idx_pipelines_status ON pipelines(status);
    CREATE INDEX IF NOT EXISTS idx_pipelines_started ON pipelines(started_at);
    CREATE INDEX IF NOT EXISTS idx_pipelines_name ON pipelines(name);
    CREATE INDEX IF NOT EXISTS idx_steps_pipeline ON steps(pipeline_id);
    CREATE INDEX IF NOT EXISTS idx_step_history_name ON step_history(step_name);
    CREATE INDEX IF NOT EXISTS idx_step_history_recorded ON step_history(recorded_at);
    CREATE INDEX IF NOT EXISTS idx_alerts_fired_fired ON alerts_fired(fired_at);
    CREATE INDEX IF NOT EXISTS idx_events_pipeline ON events(pipeline_id);
    CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
    CREATE INDEX IF NOT EXISTS idx_relations_parent ON pipeline_relations(parent_pipeline_id);
    CREATE INDEX IF NOT EXISTS idx_relations_child ON pipeline_relations(child_pipeline_id);
    CREATE INDEX IF NOT EXISTS idx_system_metrics_pipeline ON system_metrics(pipeline_id);
    """

    def __init__(self, db_path: str, config_dir: Optional[str] = None):
        """
        Initialize the tracker.

        Args:
            db_path: Path to SQLite database.
            config_dir: Directory to store YAML config files.
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
        conn.execute("PRAGMA synchronous = NORMAL")
        return conn

    @contextmanager
    def _transaction(self):
        """Context manager for database transactions."""
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _ensure_tables(self):
        """Create all tables if they don't exist."""
        with self._transaction() as conn:
            conn.executescript(self.SCHEMA)

    def _generate_id(self) -> str:
        """Generate unique pipeline ID (matrícula)."""
        unique = uuid.uuid4().hex[:8].upper()
        return f"PIPE-{unique}"

    def _generate_yaml_config(
        self, pipeline_id: str, name: str, steps: list, metadata: Optional[dict] = None
    ) -> str:
        """Generate YAML configuration file."""
        config = {
            "pipeline": {
                "id": pipeline_id,
                "name": name,
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
            },
            "steps": [
                s
                if isinstance(s, dict)
                else {
                    "name": s[1] if len(s) > 1 else str(s[0]),
                    "version": s[2] if len(s) > 2 else "1.0.0",
                    "type": "task",
                }
                if isinstance(s, (tuple, list))
                else {
                    "name": getattr(s, "name", "condition")
                    if hasattr(s, "name")
                    else str(s),
                    "type": "condition",
                    "expression": getattr(s, "expression", None),
                }
                for s in steps
            ],
            "metadata": metadata or {},
        }

        yaml_content = yaml.dump(config, default_flow_style=False, allow_unicode=True)
        yaml_path = self.config_dir / f"{pipeline_id}.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        return str(yaml_path)

    # ========================================
    # PIPELINE REGISTRATION (MATRÍCULA)
    # ========================================

    def register_pipeline(
        self,
        name: str,
        steps: list,
        input_data: Optional[dict] = None,
        worker_id: Optional[str] = None,
        worker_name: Optional[str] = None,
        metadata: Optional[dict] = None,
        tags: Optional[list] = None,
        parent_pipeline_id: Optional[str] = None,
    ) -> dict:
        """
        Register a new pipeline execution (matrícula).

        Args:
            name: Pipeline name.
            steps: List of step configurations.
            input_data: Initial input data.
            worker_id: Worker identifier.
            worker_name: Worker name.
            metadata: Additional metadata.
            tags: Tags for categorization.
            parent_pipeline_id: Parent pipeline ID for relationships.

        Returns:
            Dict with pipeline_id, yaml_path, and status.
        """
        pipeline_id = self._generate_id()

        yaml_path = self._generate_yaml_config(pipeline_id, name, steps, metadata)

        with self._transaction() as conn:
            conn.execute(
                """INSERT INTO pipelines
                   (id, name, config_yaml, status, input_data, worker_id, worker_name, tags, metadata)
                   VALUES (?, ?, ?, 'running', ?, ?, ?, ?, ?)""",
                (
                    pipeline_id,
                    name,
                    yaml_path,
                    _safe_json_dumps(input_data),
                    worker_id,
                    worker_name,
                    _safe_json_dumps(tags),
                    _safe_json_dumps(metadata),
                ),
            )

            # Record relationship if parent provided
            if parent_pipeline_id:
                conn.execute(
                    """INSERT OR IGNORE INTO pipeline_relations
                       (parent_pipeline_id, child_pipeline_id, relation_type)
                       VALUES (?, ?, 'triggered')""",
                    (parent_pipeline_id, pipeline_id),
                )

            # Record start event
            conn.execute(
                """INSERT INTO events (pipeline_id, event_type, event_name, message)
                   VALUES (?, 'lifecycle', 'pipeline_started', ?)""",
                (pipeline_id, f"Pipeline '{name}' started execution"),
            )

            # Check alerts
            self._check_pipeline_alerts(conn, pipeline_id, name, "started")

        return {
            "pipeline_id": pipeline_id,
            "yaml_path": yaml_path,
            "status": "registered",
        }

    def complete_pipeline(
        self,
        pipeline_id: str,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_step: Optional[str] = None,
    ):
        """Complete pipeline execution and trigger metrics/alerts."""
        status = "error" if error_message else "completed"

        with self._transaction() as conn:
            row = conn.execute(
                "SELECT started_at, name FROM pipelines WHERE id = ?", (pipeline_id,)
            ).fetchone()

            if row and row["started_at"]:
                started = datetime.fromisoformat(row["started_at"])
                duration_ms = (datetime.now() - started).total_seconds() * 1000
            else:
                duration_ms = 0

            conn.execute(
                """UPDATE pipelines
                   SET status = ?, completed_at = ?, total_duration_ms = ?,
                       output_data = ?, error_message = ?, error_step = ?
                   WHERE id = ?""",
                (
                    status,
                    datetime.now().isoformat(),
                    duration_ms,
                    _safe_json_dumps(output_data),
                    error_message,
                    error_step,
                    pipeline_id,
                ),
            )

            # Record completion event
            event_msg = (
                f"Pipeline completed in {duration_ms:.2f}ms"
                if not error_message
                else f"Pipeline failed: {error_message}"
            )
            conn.execute(
                """INSERT INTO events (pipeline_id, event_type, event_name, message)
                   VALUES (?, 'lifecycle', ?, ?)""",
                (pipeline_id, f"pipeline_{status}", event_msg),
            )

            # Check alerts
            self._check_pipeline_alerts(
                conn,
                pipeline_id,
                row["name"] if row else "unknown",
                status,
                duration_ms,
            )

    # ========================================
    # STEP TRACKING
    # ========================================

    def start_step(
        self,
        pipeline_id: str,
        step_order: int,
        step_name: str,
        step_version: Optional[str] = None,
        step_type: str = "task",
        input_data: Optional[dict] = None,
    ) -> int:
        """Start tracking a pipeline step."""
        with self._transaction() as conn:
            cursor = conn.execute(
                """INSERT INTO steps
                   (pipeline_id, step_order, step_name, step_version, step_type, status, started_at, input_data)
                   VALUES (?, ?, ?, ?, ?, 'running', ?, ?)""",
                (
                    pipeline_id,
                    step_order,
                    step_name,
                    step_version,
                    step_type,
                    datetime.now().isoformat(),
                    _safe_json_dumps(input_data),
                ),
            )
            return cursor.lastrowid

    def complete_step(
        self,
        step_id: int,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_traceback: Optional[str] = None,
        pipeline_id: Optional[str] = None,
    ):
        """Complete a step execution."""
        status = "error" if error_message else "completed"

        with self._transaction() as conn:
            row = conn.execute(
                "SELECT started_at, step_name FROM steps WHERE id = ?", (step_id,)
            ).fetchone()

            if row and row["started_at"]:
                started = datetime.fromisoformat(row["started_at"])
                duration_ms = (datetime.now() - started).total_seconds() * 1000
            else:
                duration_ms = 0

            conn.execute(
                """UPDATE steps
                   SET status = ?, completed_at = ?, duration_ms = ?,
                       output_data = ?, error_message = ?, error_traceback = ?
                    WHERE id = ?""",
                (
                    status,
                    datetime.now().isoformat(),
                    duration_ms,
                    _safe_json_dumps(output_data),
                    error_message,
                    error_traceback,
                    step_id,
                ),
            )

            # Add to step history for trends
            if pipeline_id:
                conn.execute(
                    """INSERT INTO step_history (pipeline_id, step_name, duration_ms, status)
                       VALUES (?, ?, ?, ?)""",
                    (
                        pipeline_id,
                        row["step_name"] if row else "unknown",
                        duration_ms,
                        status,
                    ),
                )

                # Check step alerts
                self._check_step_alerts(
                    conn,
                    pipeline_id,
                    row["step_name"] if row else "unknown",
                    duration_ms,
                    status,
                )

    # ========================================
    # ALERTS SYSTEM
    # ========================================

    def add_alert_threshold(
        self,
        name: str,
        metric: str,
        condition: str,
        value: float,
        severity: str = "warning",
        message: Optional[str] = None,
    ) -> int:
        """
        Add an alert threshold configuration.

        Args:
            name: Unique alert name.
            metric: Metric to monitor (pipeline_duration_ms, step_duration_ms, error_rate).
            condition: Comparison operator (>, <, >=, <=, ==).
            value: Threshold value.
            severity: Alert severity (info, warning, critical).
            message: Custom alert message.

        Returns:
            Alert config ID.
        """
        with self._transaction() as conn:
            cursor = conn.execute(
                """INSERT OR REPLACE INTO alerts_config
                   (name, metric, condition, value, severity, message, enabled)
                   VALUES (?, ?, ?, ?, ?, ?, 1)""",
                (name, metric, condition, value, severity, message),
            )
            return cursor.lastrowid

    def get_alert_thresholds(self) -> list:
        """Get all alert threshold configurations."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM alerts_config ORDER BY name").fetchall()
            return [dict(row) for row in rows]

    def disable_alert(self, alert_id: int):
        """Disable an alert."""
        with self._transaction() as conn:
            conn.execute(
                "UPDATE alerts_config SET enabled = 0 WHERE id = ?", (alert_id,)
            )

    def enable_alert(self, alert_id: int):
        """Enable an alert."""
        with self._transaction() as conn:
            conn.execute(
                "UPDATE alerts_config SET enabled = 1 WHERE id = ?", (alert_id,)
            )

    def _check_pipeline_alerts(
        self,
        conn,
        pipeline_id: str,
        pipeline_name: str,
        status: str,
        duration_ms: float = 0,
    ):
        """Check and fire pipeline-level alerts."""
        alerts = conn.execute(
            "SELECT * FROM alerts_config WHERE enabled = 1"
        ).fetchall()

        for alert in alerts:
            alert = dict(alert)
            metric_value = None

            if alert["metric"] == "pipeline_duration_ms" and duration_ms > 0:
                metric_value = duration_ms
            elif alert["metric"] == "error_rate" and status == "error":
                # Calculate current error rate
                total = conn.execute(
                    "SELECT COUNT(*) as cnt FROM pipelines"
                ).fetchone()["cnt"]
                errors = conn.execute(
                    "SELECT COUNT(*) as cnt FROM pipelines WHERE status = 'error'"
                ).fetchone()["cnt"]
                metric_value = (errors / total * 100) if total > 0 else 0

            if metric_value is not None and self._evaluate_condition(
                metric_value, alert["condition"], alert["value"]
            ):
                self._fire_alert(conn, alert, pipeline_id, None, metric_value)

    def _check_step_alerts(
        self, conn, pipeline_id: str, step_name: str, duration_ms: float, status: str
    ):
        """Check and fire step-level alerts."""
        alerts = conn.execute(
            "SELECT * FROM alerts_config WHERE enabled = 1"
        ).fetchall()

        for alert in alerts:
            alert = dict(alert)

            if alert["metric"] == "step_duration_ms" and duration_ms > 0:
                if self._evaluate_condition(
                    duration_ms, alert["condition"], alert["value"]
                ):
                    self._fire_alert(
                        conn,
                        alert,
                        pipeline_id,
                        None,
                        duration_ms,
                        message=f"Step '{step_name}' took {duration_ms:.0f}ms",
                    )

    def _evaluate_condition(
        self, value: float, condition: str, threshold: float
    ) -> bool:
        """Evaluate a condition."""
        if condition == ">":
            return value > threshold
        elif condition == "<":
            return value < threshold
        elif condition == ">=":
            return value >= threshold
        elif condition == "<=":
            return value <= threshold
        elif condition == "==":
            return value == threshold
        return False

    def _fire_alert(
        self,
        conn,
        alert: dict,
        pipeline_id: str,
        step_id: Optional[int],
        metric_value: float,
        message: Optional[str] = None,
    ):
        """Fire an alert."""
        alert_message = (
            message or alert.get("message") or f"Alert: {alert['name']} triggered"
        )

        conn.execute(
            """INSERT INTO alerts_fired
               (alert_config_id, pipeline_id, step_id, metric, metric_value,
                threshold_value, severity, message)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                alert["id"],
                pipeline_id,
                step_id,
                alert["metric"],
                metric_value,
                alert["value"],
                alert["severity"],
                alert_message,
            ),
        )

        # Also create an event
        conn.execute(
            """INSERT INTO events (pipeline_id, event_type, event_name, message)
               VALUES (?, 'alert', ?, ?)""",
            (pipeline_id, f"alert_{alert['severity']}", alert_message),
        )

    def get_fired_alerts(self, limit: int = 50, severity: Optional[str] = None) -> list:
        """Get fired alerts."""
        with self._get_connection() as conn:
            if severity:
                rows = conn.execute(
                    """SELECT af.*, ac.name as alert_name
                       FROM alerts_fired af
                       LEFT JOIN alerts_config ac ON af.alert_config_id = ac.id
                       WHERE af.severity = ?
                       ORDER BY af.fired_at DESC LIMIT ?""",
                    (severity, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT af.*, ac.name as alert_name
                       FROM alerts_fired af
                       LEFT JOIN alerts_config ac ON af.alert_config_id = ac.id
                       ORDER BY af.fired_at DESC LIMIT ?""",
                    (limit,),
                ).fetchall()
            return [dict(row) for row in rows]

    def acknowledge_alert(self, alert_id: int):
        """Acknowledge an alert."""
        with self._transaction() as conn:
            conn.execute(
                "UPDATE alerts_fired SET acknowledged = 1, acknowledged_at = ? WHERE id = ?",
                (datetime.now().isoformat(), alert_id),
            )

    # ========================================
    # EVENTS/ANNOTATIONS
    # ========================================

    def add_event(
        self,
        pipeline_id: str,
        event_type: str,
        event_name: str,
        message: Optional[str] = None,
        data: Optional[dict] = None,
        tags: Optional[list] = None,
        created_by: Optional[str] = None,
    ) -> int:
        """
        Add an event/annotation.

        Args:
            pipeline_id: Pipeline ID.
            event_type: Event type (milestone, annotation, warning, error, custom).
            event_name: Event name.
            message: Event message.
            data: Additional data.
            tags: Tags for categorization.
            created_by: Who created the event.

        Returns:
            Event ID.
        """
        with self._transaction() as conn:
            cursor = conn.execute(
                """INSERT INTO events
                   (pipeline_id, event_type, event_name, message, data, tags, created_by)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    pipeline_id,
                    event_type,
                    event_name,
                    message,
                    _safe_json_dumps(data),
                    _safe_json_dumps(tags),
                    created_by,
                ),
            )
            return cursor.lastrowid

    def get_events(
        self,
        pipeline_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> list:
        """Get events with optional filters."""
        with self._get_connection() as conn:
            query = "SELECT * FROM events WHERE 1=1"
            params = []

            if pipeline_id:
                query += " AND pipeline_id = ?"
                params.append(pipeline_id)
            if event_type:
                query += " AND event_type = ?"
                params.append(event_type)

            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    # ========================================
    # PIPELINE RELATIONSHIPS
    # ========================================

    def link_pipelines(
        self,
        parent_id: str,
        child_id: str,
        relation_type: str = "triggered",
        metadata: Optional[dict] = None,
    ) -> int:
        """Create a relationship between pipelines."""
        with self._transaction() as conn:
            cursor = conn.execute(
                """INSERT OR IGNORE INTO pipeline_relations
                   (parent_pipeline_id, child_pipeline_id, relation_type, metadata)
                   VALUES (?, ?, ?, ?)""",
                (
                    parent_id,
                    child_id,
                    relation_type,
                    _safe_json_dumps(metadata),
                ),
            )
            return cursor.lastrowid

    def get_pipeline_relations(self, pipeline_id: str) -> dict:
        """Get all relations for a pipeline (parents and children)."""
        with self._get_connection() as conn:
            parents = conn.execute(
                """SELECT pr.*, p.name as parent_name, p.status as parent_status
                   FROM pipeline_relations pr
                   JOIN pipelines p ON pr.parent_pipeline_id = p.id
                   WHERE pr.child_pipeline_id = ?""",
                (pipeline_id,),
            ).fetchall()

            children = conn.execute(
                """SELECT pr.*, p.name as child_name, p.status as child_status
                   FROM pipeline_relations pr
                   JOIN pipelines p ON pr.child_pipeline_id = p.id
                   WHERE pr.parent_pipeline_id = ?""",
                (pipeline_id,),
            ).fetchall()

            return {
                "parents": [dict(row) for row in parents],
                "children": [dict(row) for row in children],
            }

    # ========================================
    # SYSTEM METRICS
    # ========================================

    def record_system_metrics(self, pipeline_id: str, metrics: dict):
        """
        Record system metrics during pipeline execution.

        Args:
            pipeline_id: Pipeline ID.
            metrics: Dict with cpu_percent, memory_percent, memory_used_mb, etc.
        """
        with self._transaction() as conn:
            conn.execute(
                """INSERT INTO system_metrics
                   (pipeline_id, cpu_percent, memory_percent, memory_used_mb,
                    memory_available_mb, disk_io_read_mb, disk_io_write_mb)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    pipeline_id,
                    metrics.get("cpu_percent"),
                    metrics.get("memory_percent"),
                    metrics.get("memory_used_mb"),
                    metrics.get("memory_available_mb"),
                    metrics.get("disk_io_read_mb"),
                    metrics.get("disk_io_write_mb"),
                ),
            )

    def get_system_metrics(self, pipeline_id: str) -> list:
        """Get system metrics for a pipeline."""
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM system_metrics WHERE pipeline_id = ? ORDER BY recorded_at",
                (pipeline_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    # ========================================
    # COMPARISONS
    # ========================================

    def compare_pipelines(self, pipeline_a_id: str, pipeline_b_id: str) -> dict:
        """
        Compare two pipeline executions.

        Args:
            pipeline_a_id: First pipeline ID.
            pipeline_b_id: Second pipeline ID.

        Returns:
            Comparison data dict.
        """
        with self._get_connection() as conn:
            pipe_a = conn.execute(
                "SELECT * FROM pipelines WHERE id = ?", (pipeline_a_id,)
            ).fetchone()
            pipe_b = conn.execute(
                "SELECT * FROM pipelines WHERE id = ?", (pipeline_b_id,)
            ).fetchone()

            if not pipe_a or not pipe_b:
                return {"error": "Pipeline not found"}

            pipe_a, pipe_b = dict(pipe_a), dict(pipe_b)

            # Get steps
            steps_a = {
                row["step_name"]: dict(row)
                for row in conn.execute(
                    "SELECT * FROM steps WHERE pipeline_id = ?", (pipeline_a_id,)
                ).fetchall()
            }
            steps_b = {
                row["step_name"]: dict(row)
                for row in conn.execute(
                    "SELECT * FROM steps WHERE pipeline_id = ?", (pipeline_b_id,)
                ).fetchall()
            }

            # Build comparison
            comparison = {
                "pipeline_a": {
                    "id": pipeline_a_id,
                    "name": pipe_a["name"],
                    "status": pipe_a["status"],
                    "duration_ms": pipe_a["total_duration_ms"],
                },
                "pipeline_b": {
                    "id": pipeline_b_id,
                    "name": pipe_b["name"],
                    "status": pipe_b["status"],
                    "duration_ms": pipe_b["total_duration_ms"],
                },
                "duration_diff_ms": (pipe_b["total_duration_ms"] or 0)
                - (pipe_a["total_duration_ms"] or 0),
                "duration_diff_percent": self._calc_percent_diff(
                    pipe_a["total_duration_ms"], pipe_b["total_duration_ms"]
                ),
                "status_changed": pipe_a["status"] != pipe_b["status"],
                "steps_comparison": [],
            }

            # Compare steps
            all_step_names = set(list(steps_a.keys()) + list(steps_b.keys()))
            for step_name in sorted(all_step_names):
                step_a = steps_a.get(step_name)
                step_b = steps_b.get(step_name)

                step_comp = {
                    "step_name": step_name,
                    "in_a": step_a is not None,
                    "in_b": step_b is not None,
                }

                if step_a and step_b:
                    step_comp["duration_a"] = step_a.get("duration_ms")
                    step_comp["duration_b"] = step_b.get("duration_ms")
                    step_comp["duration_diff_ms"] = (step_b.get("duration_ms") or 0) - (
                        step_a.get("duration_ms") or 0
                    )
                    step_comp["status_a"] = step_a.get("status")
                    step_comp["status_b"] = step_b.get("status")
                    step_comp["status_changed"] = step_a.get("status") != step_b.get(
                        "status"
                    )

                comparison["steps_comparison"].append(step_comp)

            # Store comparison
            comparison_id = str(uuid.uuid4())[:8]
            with self._transaction() as conn:
                conn.execute(
                    """INSERT INTO comparisons
                       (comparison_uuid, pipeline_a_id, pipeline_b_id, comparison_data,
                        duration_diff_ms, status_diff)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        comparison_id,
                        pipeline_a_id,
                        pipeline_b_id,
                        _safe_json_dumps(comparison),
                        comparison["duration_diff_ms"],
                        f"{pipe_a['status']} -> {pipe_b['status']}"
                        if comparison["status_changed"]
                        else None,
                    ),
                )

            comparison["comparison_id"] = comparison_id
            return comparison

    def _calc_percent_diff(
        self, a: Optional[float], b: Optional[float]
    ) -> Optional[float]:
        """Calculate percentage difference."""
        if not a or not b:
            return None
        return round(((b - a) / a) * 100, 2)

    def get_comparison(self, comparison_id: str) -> Optional[dict]:
        """Get a stored comparison."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM comparisons WHERE comparison_uuid = ?", (comparison_id,)
            ).fetchone()
            if row:
                result = dict(row)
                if result.get("comparison_data"):
                    result["comparison_data"] = json.loads(result["comparison_data"])
                return result
            return None

    def get_comparisons(self, limit: int = 20) -> list:
        """Get recent comparisons."""
        with self._get_connection() as conn:
            rows = conn.execute(
                """SELECT c.*,
                          pa.name as pipeline_a_name, pb.name as pipeline_b_name
                   FROM comparisons c
                   JOIN pipelines pa ON c.pipeline_a_id = pa.id
                   JOIN pipelines pb ON c.pipeline_b_id = pb.id
                   ORDER BY c.created_at DESC LIMIT ?""",
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]

    # ========================================
    # PERFORMANCE STATISTICS
    # ========================================

    def calculate_performance_stats(self, period_hours: int = 24):
        """Calculate and store performance statistics for the given period."""
        period_end = datetime.now()
        period_start = period_end - timedelta(hours=period_hours)

        with self._transaction() as conn:
            # Pipeline stats
            pipelines = conn.execute(
                """SELECT name, total_duration_ms, status
                   FROM pipelines
                   WHERE started_at BETWEEN ? AND ? AND status != 'running'""",
                (period_start.isoformat(), period_end.isoformat()),
            ).fetchall()

            # Group by pipeline name
            pipeline_groups = {}
            for p in pipelines:
                p = dict(p)
                if p["name"] not in pipeline_groups:
                    pipeline_groups[p["name"]] = []
                if p["total_duration_ms"]:
                    pipeline_groups[p["name"]].append(p)

            for name, p_list in pipeline_groups.items():
                if not p_list:
                    continue

                durations = [
                    p["total_duration_ms"] for p in p_list if p["total_duration_ms"]
                ]
                success = sum(1 for p in p_list if p["status"] == "completed")
                errors = sum(1 for p in p_list if p["status"] == "error")

                if durations:
                    durations_sorted = sorted(durations)
                    stats = {
                        "execution_count": len(p_list),
                        "success_count": success,
                        "error_count": errors,
                        "avg_duration_ms": sum(durations) / len(durations),
                        "min_duration_ms": min(durations),
                        "max_duration_ms": max(durations),
                        "p50_duration_ms": self._percentile(durations_sorted, 50),
                        "p95_duration_ms": self._percentile(durations_sorted, 95),
                        "p99_duration_ms": self._percentile(durations_sorted, 99),
                    }

                    conn.execute(
                        """INSERT INTO performance_stats
                           (entity_type, entity_name, period_start, period_end,
                            execution_count, success_count, error_count,
                            avg_duration_ms, min_duration_ms, max_duration_ms,
                            p50_duration_ms, p95_duration_ms, p99_duration_ms)
                           VALUES ('pipeline', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            name,
                            period_start.isoformat(),
                            period_end.isoformat(),
                            *stats.values(),
                        ),
                    )

            # Step stats
            steps = conn.execute(
                """SELECT step_name, duration_ms, status
                   FROM step_history
                   WHERE recorded_at BETWEEN ? AND ? AND status != 'running'""",
                (period_start.isoformat(), period_end.isoformat()),
            ).fetchall()

            step_groups = {}
            for s in steps:
                s = dict(s)
                if s["step_name"] not in step_groups:
                    step_groups[s["step_name"]] = []
                step_groups[s["step_name"]].append(s)

            for name, s_list in step_groups.items():
                if not s_list:
                    continue

                durations = [s["duration_ms"] for s in s_list if s["duration_ms"]]
                success = sum(1 for s in s_list if s["status"] == "completed")
                errors = sum(1 for s in s_list if s["status"] == "error")

                if durations:
                    durations_sorted = sorted(durations)
                    stats = {
                        "execution_count": len(s_list),
                        "success_count": success,
                        "error_count": errors,
                        "avg_duration_ms": sum(durations) / len(durations),
                        "min_duration_ms": min(durations),
                        "max_duration_ms": max(durations),
                        "p50_duration_ms": self._percentile(durations_sorted, 50),
                        "p95_duration_ms": self._percentile(durations_sorted, 95),
                        "p99_duration_ms": self._percentile(durations_sorted, 99),
                    }

                    conn.execute(
                        """INSERT INTO performance_stats
                           (entity_type, entity_name, period_start, period_end,
                            execution_count, success_count, error_count,
                            avg_duration_ms, min_duration_ms, max_duration_ms,
                            p50_duration_ms, p95_duration_ms, p99_duration_ms)
                           VALUES ('step', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            name,
                            period_start.isoformat(),
                            period_end.isoformat(),
                            *stats.values(),
                        ),
                    )

    def _percentile(self, sorted_list: list, percentile: float) -> float:
        """Calculate percentile from sorted list."""
        if not sorted_list:
            return 0
        k = (len(sorted_list) - 1) * (percentile / 100)
        f = int(k)
        c = f + 1 if f + 1 < len(sorted_list) else f
        d = k - f
        return sorted_list[f] + d * (sorted_list[c] - sorted_list[f])

    def get_performance_stats(
        self, entity_type: Optional[str] = None, limit: int = 100
    ) -> list:
        """Get performance statistics."""
        with self._get_connection() as conn:
            if entity_type:
                rows = conn.execute(
                    """SELECT * FROM performance_stats
                       WHERE entity_type = ?
                       ORDER BY period_end DESC LIMIT ?""",
                    (entity_type, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT * FROM performance_stats
                       ORDER BY period_end DESC LIMIT ?""",
                    (limit,),
                ).fetchall()
            return [dict(row) for row in rows]

    # ========================================
    # QUERIES
    # ========================================

    def get_pipeline(self, pipeline_id: str) -> Optional[dict]:
        """Get pipeline with all steps."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM pipelines WHERE id = ?", (pipeline_id,)
            ).fetchone()
            if not row:
                return None

            pipeline = dict(row)
            for field in ["input_data", "output_data", "tags", "metadata"]:
                if pipeline.get(field):
                    try:
                        pipeline[field] = json.loads(pipeline[field])
                    except:
                        pass

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
                        except:
                            pass
                pipeline["steps"].append(step_dict)

            return pipeline

    def get_pipelines(
        self, limit: int = 50, offset: int = 0, status: Optional[str] = None
    ) -> list:
        """Get list of pipelines."""
        with self._get_connection() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM pipelines WHERE status = ? ORDER BY started_at DESC LIMIT ? OFFSET ?",
                    (status, limit, offset),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM pipelines ORDER BY started_at DESC LIMIT ? OFFSET ?",
                    (limit, offset),
                ).fetchall()

            result = []
            for row in rows:
                pipeline = dict(row)
                for field in ["input_data", "output_data", "tags", "metadata"]:
                    if pipeline.get(field):
                        try:
                            pipeline[field] = json.loads(pipeline[field])
                        except:
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

        steps_list = pipeline.get("steps", [])

        for i, step in enumerate(steps_list):
            output_data = step.get("output_data")
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

            if step["step_type"] == "condition" and output_data:
                if isinstance(output_data, dict):
                    node["expression"] = output_data.get("expression")
                    node["branch_taken"] = output_data.get("branch_taken")
                    node["true_branch_ids"] = output_data.get("true_branch_ids", [])
                    node["false_branch_ids"] = output_data.get("false_branch_ids", [])
                    node["skipped_branch_ids"] = output_data.get(
                        "skipped_branch_ids", []
                    )
                    input_data = step.get("input_data")
                    if input_data and isinstance(input_data, dict):
                        node["true_branch_names"] = input_data.get("true_branch", [])
                        node["false_branch_names"] = input_data.get("false_branch", [])

            nodes.append(node)

            if i > 0:
                prev_step = steps_list[i - 1]
                if prev_step["step_type"] != "condition":
                    edges.append(
                        {
                            "from": f"step_{prev_step['id']}",
                            "to": f"step_{step['id']}",
                        }
                    )
                else:
                    edges.append(
                        {
                            "from": f"step_{prev_step['id']}",
                            "to": f"step_{step['id']}",
                            "label": "taken"
                            if step["step_type"] != "skipped"
                            else "skipped",
                            "style": "solid"
                            if step["step_type"] != "skipped"
                            else "dashed",
                        }
                    )

        name_to_id = {node["name"]: node["id"] for node in nodes}

        for node in nodes:
            if node["type"] == "condition":
                taken_names = (
                    node.get("true_branch_names", [])
                    if node.get("branch_taken") == "true"
                    else node.get("false_branch_names", [])
                )
                skipped_names = (
                    node.get("false_branch_names", [])
                    if node.get("branch_taken") == "true"
                    else node.get("true_branch_names", [])
                )

                cond_id = node["id"]

                for name in taken_names:
                    if name in name_to_id:
                        edges.append(
                            {
                                "from": cond_id,
                                "to": name_to_id[name],
                                "label": "✓",
                                "style": "solid",
                                "color": "#10b981",
                            }
                        )

                for name in skipped_names:
                    if name in name_to_id:
                        edges.append(
                            {
                                "from": cond_id,
                                "to": name_to_id[name],
                                "label": "✗",
                                "style": "dashed",
                                "color": "#6b7280",
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

            unack_alerts = conn.execute(
                "SELECT COUNT(*) as cnt FROM alerts_fired WHERE acknowledged = 0"
            ).fetchone()["cnt"]

            success_rate = ((completed / total) * 100) if total > 0 else 0
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
                "unacknowledged_alerts": unack_alerts,
            }

    def get_trend_data(
        self, days: int = 7, pipeline_name: Optional[str] = None
    ) -> dict:
        """Get trend data for charts."""
        with self._get_connection() as conn:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()

            query = """
                SELECT DATE(started_at) as date,
                       COUNT(*) as count,
                       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as success,
                       SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors,
                       AVG(total_duration_ms) as avg_duration
                FROM pipelines
                WHERE started_at >= ?
            """
            params = [start_date]

            if pipeline_name:
                query += " AND name = ?"
                params.append(pipeline_name)

            query += " GROUP BY DATE(started_at) ORDER BY date"

            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def get_step_trend_data(self, step_name: str, days: int = 7) -> list:
        """Get trend data for a specific step."""
        with self._get_connection() as conn:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()

            rows = conn.execute(
                """SELECT DATE(recorded_at) as date,
                          AVG(duration_ms) as avg_duration,
                          MIN(duration_ms) as min_duration,
                          MAX(duration_ms) as max_duration,
                          COUNT(*) as count
                   FROM step_history
                   WHERE step_name = ? AND recorded_at >= ?
                   GROUP BY DATE(recorded_at)
                   ORDER BY date""",
                (step_name, start_date),
            ).fetchall()
            return [dict(row) for row in rows]

    def get_top_slow_steps(self, limit: int = 10) -> list:
        """Get top slowest steps by average duration."""
        with self._get_connection() as conn:
            rows = conn.execute(
                """SELECT step_name,
                          COUNT(*) as execution_count,
                          AVG(duration_ms) as avg_duration_ms,
                          MAX(duration_ms) as max_duration_ms
                   FROM step_history
                   WHERE status = 'completed'
                   GROUP BY step_name
                   ORDER BY avg_duration_ms DESC
                   LIMIT ?""",
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]

    def delete_pipeline(self, pipeline_id: str):
        """Delete a pipeline and all related data."""
        with self._transaction() as conn:
            conn.execute(
                "DELETE FROM system_metrics WHERE pipeline_id = ?", (pipeline_id,)
            )
            conn.execute("DELETE FROM events WHERE pipeline_id = ?", (pipeline_id,))
            conn.execute(
                "DELETE FROM step_history WHERE pipeline_id = ?", (pipeline_id,)
            )
            conn.execute(
                "DELETE FROM alerts_fired WHERE pipeline_id = ?", (pipeline_id,)
            )
            conn.execute("DELETE FROM steps WHERE pipeline_id = ?", (pipeline_id,))
            conn.execute("DELETE FROM pipelines WHERE id = ?", (pipeline_id,))

        yaml_path = self.config_dir / f"{pipeline_id}.yaml"
        if yaml_path.exists():
            yaml_path.unlink()

    def clear_old_data(self, days: int = 30):
        """Clear old pipelines and related data."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        with self._transaction() as conn:
            # Get old pipeline IDs
            old_ids = [
                row["id"]
                for row in conn.execute(
                    "SELECT id FROM pipelines WHERE started_at < ?", (cutoff,)
                ).fetchall()
            ]

            for pid in old_ids:
                conn.execute("DELETE FROM system_metrics WHERE pipeline_id = ?", (pid,))
                conn.execute("DELETE FROM events WHERE pipeline_id = ?", (pid,))
                conn.execute("DELETE FROM step_history WHERE pipeline_id = ?", (pid,))
                conn.execute("DELETE FROM alerts_fired WHERE pipeline_id = ?", (pid,))
                conn.execute(
                    "DELETE FROM pipeline_relations WHERE parent_pipeline_id = ? OR child_pipeline_id = ?",
                    (pid, pid),
                )
                conn.execute("DELETE FROM steps WHERE pipeline_id = ?", (pid,))
                conn.execute("DELETE FROM pipelines WHERE id = ?", (pid,))

                yaml_path = self.config_dir / f"{pid}.yaml"
                if yaml_path.exists():
                    yaml_path.unlink()

    def get_states_analysis(self) -> dict:
        """Get analysis of states used across all pipelines."""
        with self._get_connection() as conn:
            most_used = conn.execute("""
                SELECT step_name, COUNT(*) as count, 
                       AVG(duration_ms) as avg_duration,
                       SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as error_count
                FROM steps 
                GROUP BY step_name 
                ORDER BY count DESC
                LIMIT 20
            """).fetchall()

            slowest = conn.execute("""
                SELECT step_name, AVG(duration_ms) as avg_duration,
                       COUNT(*) as count, MAX(duration_ms) as max_duration
                FROM steps 
                WHERE status = 'completed' AND duration_ms IS NOT NULL
                GROUP BY step_name
                ORDER BY avg_duration DESC
                LIMIT 15
            """).fetchall()

            most_errors = conn.execute("""
                SELECT step_name, COUNT(*) as error_count,
                       COUNT(*) as total_count,
                       AVG(duration_ms) as avg_duration
                FROM steps 
                WHERE status = 'error'
                GROUP BY step_name
                ORDER BY error_count DESC
                LIMIT 15
            """).fetchall()

            unique_states = conn.execute(
                "SELECT COUNT(DISTINCT step_name) as cnt FROM steps"
            ).fetchone()["cnt"]

            return {
                "unique_states": unique_states,
                "most_used": [dict(r) for r in most_used],
                "slowest": [dict(r) for r in slowest],
                "most_errors": [dict(r) for r in most_errors],
            }

    def get_pipelines_analysis(self) -> dict:
        """Get analysis of pipelines."""
        with self._get_connection() as conn:
            unique = conn.execute("""
                SELECT name, COUNT(*) as run_count,
                       AVG(total_duration_ms) as avg_duration,
                       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                       SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors
                FROM pipelines 
                GROUP BY name
                ORDER BY run_count DESC
            """).fetchall()

            slowest = conn.execute("""
                SELECT name, AVG(total_duration_ms) as avg_duration,
                       COUNT(*) as run_count
                FROM pipelines 
                WHERE status = 'completed' AND total_duration_ms IS NOT NULL
                GROUP BY name
                ORDER BY avg_duration DESC
                LIMIT 10
            """).fetchall()

            error_pipelines = conn.execute("""
                SELECT name, COUNT(*) as error_count
                FROM pipelines 
                WHERE status = 'error'
                GROUP BY name
                ORDER BY error_count DESC
                LIMIT 10
            """).fetchall()

            unique_count = conn.execute(
                "SELECT COUNT(DISTINCT name) as cnt FROM pipelines"
            ).fetchone()["cnt"]

            return {
                "unique_count": unique_count,
                "unique_pipelines": [dict(r) for r in unique],
                "slowest": [dict(r) for r in slowest],
                "most_errors": [dict(r) for r in error_pipelines],
            }

    def get_table_data(
        self,
        table: str,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        """Get data from any table with pagination and filtering."""
        valid_tables = ["pipelines", "steps", "alerts_fired", "events"]
        if table not in valid_tables:
            return {"items": [], "total": 0, "page": page, "page_size": page_size}

        with self._get_connection() as conn:
            offset = (page - 1) * page_size

            where = ""
            params = []
            if search and table == "pipelines":
                where = "WHERE (name LIKE ? OR id LIKE ?)"
                params = [f"%{search}%", f"%{search}%"]
            elif search and table == "steps":
                where = "WHERE step_name LIKE ?"
                params = [f"%{search}%"]
            elif status and table == "pipelines":
                where = "WHERE status = ?"
                params = [status]

            total = conn.execute(
                f"SELECT COUNT(*) as cnt FROM {table} {where}", params
            ).fetchone()["cnt"]
            rows = conn.execute(
                f"SELECT * FROM {table} {where} ORDER BY rowid DESC LIMIT ? OFFSET ?",
                params + [page_size, offset],
            ).fetchall()

            items = []
            for row in rows:
                item = dict(row)
                for k, v in item.items():
                    if isinstance(v, str) and len(v) > 200:
                        item[k] = v[:200] + "..."
                items.append(item)

            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size,
            }
