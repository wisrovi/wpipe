"""
Comprehensive tests to significantly increase coverage.
"""

import asyncio
import os
import tempfile
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch

from wpipe import (
    Pipeline, PipelineAsync, Condition, For, 
    PipelineExporter, ResourceMonitor, PipelineTracker
)
from wpipe.tracking.analysis import AnalysisManager
from wpipe.sqlite import SQLite

@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    if os.path.exists(db_path):
        os.unlink(db_path)

# --- PipelineAsync Tests ---

@pytest.mark.asyncio
async def test_async_pipeline_full_flow():
    """Test PipelineAsync with various step types."""
    async def async_step(data):
        await asyncio.sleep(0.01)
        return {"async": True}
    
    def sync_step(data):
        return {"sync": True}
    
    p = PipelineAsync()
    p.set_steps([
        (async_step, "Async", "1.0"),
        (sync_step, "Sync", "1.0")
    ])
    
    # Using run() which should handle both
    result = await p.run({})
    # If PipelineAsync.run is implemented correctly, it returns merged results
    assert isinstance(result, dict)

@pytest.mark.asyncio
async def test_async_pipeline_with_nesting():
    """Test async pipeline with nested conditions and loops."""
    async def task(data):
        return {"done": True}
        
    cond = Condition("x > 0", [(task, "T", "1.0")])
    
    p = PipelineAsync()
    p.set_steps([cond])
    
    result = await p.run({"x": 10})
    assert isinstance(result, dict)

# --- SQLite Additional Tests ---

def test_sqlite_export_import(temp_db, tmp_path):
    """Test SQLite dataframe export/import."""
    db = SQLite(temp_db)
    db.write(input_data={"a": 1})
    
    df = db.export_to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    
    # Test date range query
    records = db.get_records_by_date_range(
        (datetime.now() - timedelta(days=1)).isoformat(),
        (datetime.now() + timedelta(days=1)).isoformat()
    )
    assert len(records) >= 1

from datetime import datetime, timedelta
