"""
Comprehensive tests for the PipelineAsync class.
"""

import asyncio
import os
import pytest
from wsqlite import WSQLite

from wpipe.exception import TaskError
from wpipe.pipe.pipe import Condition
from wpipe.pipe.pipe_async import PipelineAsync
from wpipe.sqlite.tables_dto.tracker_models import PipelineModel


@pytest.mark.asyncio
class TestPipelineAsyncCore:
    """Test core PipelineAsync functionality."""

    async def test_pipeline_async_initialization(self):
        """Test PipelineAsync initialization."""
        pipeline = PipelineAsync(
            worker_id="worker_async",
            worker_name="async_worker",
            verbose=True
        )
        assert pipeline.worker_id == "worker_async"
        assert pipeline.worker_name == "async_worker"
        assert pipeline.verbose is True

    async def test_pipeline_async_run_basic(self):
        """Test basic async pipeline execution."""
        async def step1(data):
            await asyncio.sleep(0.01)
            return {"s1": True}
            
        async def step2(data):
            return {"s2": data.get("x", 0) * 2}
            
        pipeline = PipelineAsync()
        pipeline.set_steps([
            (step1, "Step1", "1.0"),
            (step2, "Step2", "1.0")
        ])
        
        result = await pipeline.run({"x": 10})
        assert result["s1"] is True
        assert result["s2"] == 20


@pytest.mark.asyncio
class TestPipelineAsyncControlFlow:
    """Test Condition blocks in async pipeline."""

    async def test_async_condition_block(self):
        """Test Condition execution paths in async pipeline."""
        pipeline = PipelineAsync()
        
        async def true_step(data): return {"branch": "true"}
        async def false_step(data): return {"branch": "false"}
        
        cond = Condition(
            expression="x > 10",
            branch_true=[(true_step, "TrueStep", "1.0")],
            branch_false=[(false_step, "FalseStep", "1.0")]
        )
        
        pipeline.set_steps([cond])
        
        # Test true branch
        result_true = await pipeline.run({"x": 15})
        assert result_true["branch"] == "true"
        
        # Test false branch
        result_false = await pipeline.run({"x": 5})
        assert result_false["branch"] == "false"


@pytest.mark.asyncio
class TestPipelineAsyncTracking:
    """Test async pipeline tracking."""

    async def test_async_tracking_integration(self, db_file, temp_dir):
        """Test that async pipeline execution is recorded."""
        pipeline = PipelineAsync(
            tracking_db=db_file,
            config_dir=temp_dir,
            pipeline_name="AsyncTracked"
        )
        
        async def step1(data): return {"s1": True}
        
        pipeline.set_steps([(step1, "Step1", "1.0")])
        await pipeline.run({})
        
        assert os.path.exists(db_file)
        
        # Verify using WSQLite (no sqlite3 import)
        inspector = WSQLite(PipelineModel, db_file)
        results = inspector.get_by_field(name="AsyncTracked")
        
        assert len(results) >= 1
        assert results[0].name == "AsyncTracked"
        assert results[0].status == "completed"


@pytest.mark.asyncio
class TestPipelineAsyncAdvanced:
    """Test advanced async features."""

    async def test_async_retry_logic(self):
        """Test retry logic in async pipeline."""
        attempts = 0
        
        async def flaky_step(data):
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise ValueError("Fail")
            return {"success": True}
            
        pipeline = PipelineAsync(max_retries=3, retry_delay=0.01)
        pipeline.set_steps([(flaky_step, "Flaky", "1.0")])
        
        result = await pipeline.run({})
        assert result["success"] is True
        assert attempts == 3

    async def test_async_continue_on_error_false(self):
        """Test continue_on_error=False in async pipeline."""
        async def failing_step(data):
            raise ValueError("Boom")
            
        pipeline = PipelineAsync(continue_on_error=False)
        pipeline.set_steps([(failing_step, "Fail", "1.0")])
        
        from wpipe.exception import ProcessError
        with pytest.raises(ProcessError):
            await pipeline.run({})

    async def test_nested_async_pipelines(self):
        """Test nested async pipelines."""
        child = PipelineAsync()
        async def child_step(data): return {"child": True}
        child.set_steps([(child_step, "ChildStep", "1.0")])

        parent = PipelineAsync()
        parent.set_steps([(child.run, "ChildPipe", "1.0")])

        result = await parent.run({})
        assert result["child"] is True

    async def test_sync_step_in_async_pipeline(self):
        """Test that async pipeline can run sync steps."""
        def sync_step(data):
            return {"sync": True}
            
        pipeline = PipelineAsync()
        pipeline.set_steps([(sync_step, "SyncStep", "1.0")])
        
        result = await pipeline.run({})
        assert result["sync"] is True
