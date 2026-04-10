"""
Tests for Phase 1 checkpoint functionality.

Tests CheckpointManager and checkpoint workflows.
"""

import sqlite3
import tempfile
from pathlib import Path

import pytest

from wpipe import CheckpointManager


class TestCheckpointManager:
    """Test CheckpointManager class."""

    @pytest.fixture
    def db_path(self):
        """Create temporary database."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
            yield f.name
        Path(f.name).unlink(missing_ok=True)

    @pytest.fixture
    def checkpoint_mgr(self, db_path):
        """Create CheckpointManager instance."""
        return CheckpointManager(db_path)

    def test_initialization(self, checkpoint_mgr):
        """Test manager initialization."""
        assert checkpoint_mgr is not None
        assert checkpoint_mgr.db_path is not None

    def test_table_creation(self, db_path):
        """Test checkpoint table creation."""
        checkpoint_mgr = CheckpointManager(db_path)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='checkpoints'"
            )
            table = cursor.fetchone()

        assert table is not None

    def test_save_checkpoint(self, checkpoint_mgr):
        """Test saving a checkpoint."""
        checkpoint_mgr.save_checkpoint(
            pipeline_id="test_pipeline",
            step_order=0,
            step_name="step_1",
            status="success",
            data={"result": "test_data"},
        )

        with sqlite3.connect(checkpoint_mgr.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM checkpoints")
            count = cursor.fetchone()[0]

        assert count == 1

    def test_get_last_checkpoint(self, checkpoint_mgr):
        """Test retrieving last checkpoint."""
        # Save multiple checkpoints
        for i in range(3):
            checkpoint_mgr.save_checkpoint(
                pipeline_id="test_pipeline",
                step_order=i,
                step_name=f"step_{i}",
                status="success",
                data={"step": i},
            )

        last = checkpoint_mgr.get_last_checkpoint("test_pipeline")

        assert last is not None
        assert last["step_order"] == 2
        assert last["step_name"] == "step_2"
        assert last["status"] == "success"

    def test_can_resume(self, checkpoint_mgr):
        """Test resume detection."""
        assert not checkpoint_mgr.can_resume("non_existent")

        checkpoint_mgr.save_checkpoint(
            pipeline_id="resumable", step_order=0, step_name="step_1", status="success"
        )

        assert checkpoint_mgr.can_resume("resumable")

    def test_clear_checkpoints(self, checkpoint_mgr):
        """Test clearing checkpoints."""
        # Save some checkpoints
        for i in range(3):
            checkpoint_mgr.save_checkpoint(
                pipeline_id="test",
                step_order=i,
                step_name=f"step_{i}",
                status="success",
            )

        assert checkpoint_mgr.can_resume("test")

        checkpoint_mgr.clear_checkpoints("test")

        assert not checkpoint_mgr.can_resume("test")

    def test_get_checkpoint_stats(self, checkpoint_mgr):
        """Test getting checkpoint statistics."""
        # Save checkpoints with different statuses
        checkpoint_mgr.save_checkpoint("test", 0, "step_1", "success")
        checkpoint_mgr.save_checkpoint("test", 1, "step_2", "success")
        checkpoint_mgr.save_checkpoint("test", 2, "step_3", "failed")

        stats = checkpoint_mgr.get_checkpoint_stats("test")

        assert stats["total_checkpoints"] == 3
        assert stats["successful"] == 2
        assert stats["failed"] == 1

    def test_data_persistence(self, checkpoint_mgr):
        """Test that data is persisted correctly."""
        test_data = {"key": "value", "number": 42, "list": [1, 2, 3]}

        checkpoint_mgr.save_checkpoint(
            pipeline_id="test",
            step_order=0,
            step_name="step_1",
            status="success",
            data=test_data,
        )

        last = checkpoint_mgr.get_last_checkpoint("test")

        assert last["data"] == test_data

    def test_checkpoint_update(self, checkpoint_mgr):
        """Test updating checkpoint (unique constraint)."""
        # Save initial checkpoint
        checkpoint_mgr.save_checkpoint(
            pipeline_id="test",
            step_order=0,
            step_name="step_1",
            status="success",
            data={"version": 1},
        )

        # Update same checkpoint
        checkpoint_mgr.save_checkpoint(
            pipeline_id="test",
            step_order=0,
            step_name="step_1",
            status="success",
            data={"version": 2},
        )

        # Should still have only one checkpoint
        stats = checkpoint_mgr.get_checkpoint_stats("test")
        assert stats["total_checkpoints"] == 1

        # Data should be updated
        last = checkpoint_mgr.get_last_checkpoint("test")
        assert last["data"]["version"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
