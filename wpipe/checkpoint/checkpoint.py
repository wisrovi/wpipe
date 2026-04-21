"""
Checkpoint manager for pipeline resumption after interruptions.

Allows pipelines to be paused and resumed from the last successful step,
storing state in the tracking database.
"""

import json
from typing import Any, Dict, Optional

from wsqlite import WSQLite

from wpipe.sqlite.tables_dto.tracker_models import CheckpointModel
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
        self.db = WSQLite(CheckpointModel, self.db_path)

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
        serializable_data = object_to_dict(data) if data else None
        data_json = json.dumps(serializable_data) if serializable_data else None

        checkpoint = CheckpointModel(
            pipeline_id=pipeline_id,
            step_order=step_order,
            step_name=step_name,
            status=status,
            data=data_json
        )

        # Check if already exists for this pipeline and step
        existing = self.db.get_by_field(pipeline_id=pipeline_id, step_order=step_order)
        if existing:
            checkpoint.id = existing[0].id
            self.db.update(checkpoint.id, checkpoint)
        else:
            self.db.insert(checkpoint)

    def get_last_checkpoint(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the last successful checkpoint for a pipeline.

        Args:
            pipeline_id: Unique pipeline identifier

        Returns:
            Checkpoint data or None if no checkpoint exists
        """
        checkpoints = self.db.get_by_field(pipeline_id=pipeline_id, status='success')
        if not checkpoints:
            return None

        # Sort by step_order descending
        checkpoints.sort(key=lambda x: x.step_order, reverse=True)
        row = checkpoints[0]

        return {
            "step_order": row.step_order,
            "step_name": row.step_name,
            "status": row.status,
            "data": json.loads(row.data) if row.data else None,
            "created_at": row.created_at,
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
        checkpoints = self.db.get_by_field(pipeline_id=pipeline_id)
        for cp in checkpoints:
            self.db.delete(cp.id)

    def get_checkpoint_stats(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get statistics about checkpoints for a pipeline.

        Args:
            pipeline_id: Unique pipeline identifier

        Returns:
            Dictionary with checkpoint statistics
        """
        checkpoints = self.db.get_by_field(pipeline_id=pipeline_id)
        if not checkpoints:
            return {
                "total_checkpoints": 0,
                "successful": 0,
                "failed": 0,
                "last_checkpoint": None,
            }

        successful = sum(1 for cp in checkpoints if cp.status == 'success')
        failed = sum(1 for cp in checkpoints if cp.status == 'failed')
        last_cp = max(cp.created_at for cp in checkpoints) if checkpoints else None

        return {
            "total_checkpoints": len(checkpoints),
            "successful": successful,
            "failed": failed,
            "last_checkpoint": last_cp,
        }
