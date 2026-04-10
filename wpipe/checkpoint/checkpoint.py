"""
Checkpoint manager for pipeline resumption after interruptions.

Allows pipelines to be paused and resumed from the last successful step,
storing state in the tracking database.
"""

import json
import sqlite3
from typing import Any, Dict, Optional

from wpipe.util.transform import object_to_dict


class CheckpointManager:
    """Manages pipeline checkpoints for resume functionality."""

    def __init__(self, db_path: str):
        """
        Initialize checkpoint manager.

        Args:
            db_path: Path to the tracking database
        """
        self.db_path = db_path
        self._ensure_checkpoint_table()

    def _ensure_checkpoint_table(self) -> None:
        """Create checkpoint table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pipeline_id TEXT NOT NULL,
                    step_order INTEGER NOT NULL,
                    step_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(pipeline_id, step_order)
                )
            """)
            conn.commit()

    def save_checkpoint(
        self,
        pipeline_id: str,
        step_order: int,
        step_name: str,
        status: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Save a checkpoint at a specific step.

        Args:
            pipeline_id: Unique pipeline identifier
            step_order: Order of the step in the pipeline
            step_name: Name of the step
            status: Status ('pending', 'running', 'success', 'failed')
            data: Step output data to save
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            serializable_data = object_to_dict(data) if data else None
            data_json = json.dumps(serializable_data) if serializable_data else None
            cursor.execute("""
                INSERT OR REPLACE INTO checkpoints 
                (pipeline_id, step_order, step_name, status, data)
                VALUES (?, ?, ?, ?, ?)
            """, (pipeline_id, step_order, step_name, status, data_json))
            conn.commit()

    def get_last_checkpoint(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the last successful checkpoint for a pipeline.

        Args:
            pipeline_id: Unique pipeline identifier

        Returns:
            Checkpoint data or None if no checkpoint exists
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT step_order, step_name, status, data, created_at
                FROM checkpoints
                WHERE pipeline_id = ? AND status = 'success'
                ORDER BY step_order DESC
                LIMIT 1
            """, (pipeline_id,))
            row = cursor.fetchone()

        if not row:
            return None

        return {
            "step_order": row[0],
            "step_name": row[1],
            "status": row[2],
            "data": json.loads(row[3]) if row[3] else None,
            "created_at": row[4],
        }

    def can_resume(self, pipeline_id: str) -> bool:
        """
        Check if a pipeline can be resumed from a checkpoint.

        Args:
            pipeline_id: Unique pipeline identifier

        Returns:
            True if a checkpoint exists, False otherwise
        """
        checkpoint = self.get_last_checkpoint(pipeline_id)
        return checkpoint is not None

    def clear_checkpoints(self, pipeline_id: str) -> None:
        """
        Clear all checkpoints for a pipeline.

        Args:
            pipeline_id: Unique pipeline identifier
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM checkpoints WHERE pipeline_id = ?",
                (pipeline_id,)
            )
            conn.commit()

    def get_checkpoint_stats(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get statistics about checkpoints for a pipeline.

        Args:
            pipeline_id: Unique pipeline identifier

        Returns:
            Dictionary with checkpoint statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    MAX(created_at) as last_checkpoint
                FROM checkpoints
                WHERE pipeline_id = ?
            """, (pipeline_id,))
            row = cursor.fetchone()

        return {
            "total_checkpoints": row[0] or 0,
            "successful": row[1] or 0,
            "failed": row[2] or 0,
            "last_checkpoint": row[3],
        }
