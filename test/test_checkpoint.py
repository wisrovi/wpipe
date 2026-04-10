"""
Unit tests for checkpoint functionality.
"""

import os
import tempfile
import unittest
from pathlib import Path

from wpipe.checkpoint import CheckpointManager


class TestCheckpointManager(unittest.TestCase):
    """Test CheckpointManager functionality."""

    def setUp(self):
        """Create temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_checkpoint.db")
        self.manager = CheckpointManager(self.db_path)
        self.pipeline_id = "test_pipeline_001"

    def tearDown(self):
        """Clean up temporary files."""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_checkpoint_manager_initialization(self):
        """Test CheckpointManager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertEqual(self.manager.db_path, self.db_path)

    def test_save_checkpoint(self):
        """Test saving a checkpoint."""
        data = {"key": "value", "number": 42}

        self.manager.save_checkpoint(
            pipeline_id=self.pipeline_id,
            step_order=1,
            step_name="test_step",
            status="success",
            data=data,
        )

        checkpoint = self.manager.get_last_checkpoint(self.pipeline_id)
        self.assertIsNotNone(checkpoint)
        self.assertEqual(checkpoint["step_name"], "test_step")
        self.assertEqual(checkpoint["status"], "success")

    def test_can_resume(self):
        """Test can_resume functionality."""
        self.assertFalse(self.manager.can_resume(self.pipeline_id))

        self.manager.save_checkpoint(
            pipeline_id=self.pipeline_id,
            step_order=1,
            step_name="step_1",
            status="success",
            data={},
        )

        self.assertTrue(self.manager.can_resume(self.pipeline_id))

    def test_get_checkpoint_stats(self):
        """Test checkpoint statistics."""
        self.manager.save_checkpoint(
            pipeline_id=self.pipeline_id,
            step_order=1,
            step_name="step_1",
            status="success",
            data={},
        )

        self.manager.save_checkpoint(
            pipeline_id=self.pipeline_id,
            step_order=2,
            step_name="step_2",
            status="success",
            data={},
        )

        stats = self.manager.get_checkpoint_stats(self.pipeline_id)

        self.assertEqual(stats["total_checkpoints"], 2)
        self.assertEqual(stats["successful"], 2)
        self.assertEqual(stats["failed"], 0)

    def test_clear_checkpoints(self):
        """Test clearing checkpoints."""
        self.manager.save_checkpoint(
            pipeline_id=self.pipeline_id,
            step_order=1,
            step_name="step_1",
            status="success",
            data={},
        )

        self.assertTrue(self.manager.can_resume(self.pipeline_id))

        self.manager.clear_checkpoints(self.pipeline_id)

        self.assertFalse(self.manager.can_resume(self.pipeline_id))


if __name__ == "__main__":
    unittest.main()
