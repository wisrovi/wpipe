"""
Unit tests for export functionality.
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
from wpipe.export import PipelineExporter


class TestPipelineExporter(unittest.TestCase):
    """Test PipelineExporter functionality."""
    
    def setUp(self):
        """Create temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_export.db")
        self.exporter = PipelineExporter(self.db_path)
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_exporter_initialization(self):
        """Test PipelineExporter initialization."""
        self.assertIsNotNone(self.exporter)
        self.assertEqual(self.exporter.db_path, self.db_path)
    
    def test_export_statistics(self):
        """Test exporting statistics."""
        stats_str = self.exporter.export_statistics(format="json")
        
        # Should return valid JSON
        stats = json.loads(stats_str)
        self.assertIn("total_executions", stats)
        self.assertIn("successful_executions", stats)
        self.assertIn("success_rate_percent", stats)
        self.assertIn("average_execution_time_seconds", stats)
    
    def test_export_to_file(self):
        """Test exporting to file."""
        output_path = os.path.join(self.temp_dir, "stats.json")
        
        result = self.exporter.export_statistics(
            format="json",
            output_path=output_path
        )
        
        # Should return the path
        self.assertEqual(result, output_path)
        
        # File should exist
        self.assertTrue(os.path.exists(output_path))
        
        # File should contain valid JSON
        with open(output_path) as f:
            data = json.load(f)
            self.assertIn("total_executions", data)
    
    def test_export_format_validation(self):
        """Test invalid export format raises error."""
        with self.assertRaises(ValueError):
            self.exporter.export_statistics(format="invalid")


if __name__ == "__main__":
    unittest.main()
