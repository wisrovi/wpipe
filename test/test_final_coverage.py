"""
Final attempt at increasing coverage with correct API signatures.
"""

import pytest
import os
import tempfile
from wpipe.tracking import PipelineTracker

def test_tracker_register_correct():
    """Test tracker register with correct signature."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    
    try:
        tracker = PipelineTracker(db_path)
        # Signature: name, steps, **kwargs
        reg = tracker.register_pipeline("test_name", steps=[])
        assert reg is not None
        assert "pipeline_id" in reg
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)
