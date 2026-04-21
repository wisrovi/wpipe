import pytest
import asyncio
from wpipe import PipelineAsync, Condition, Parallel

async def add_one_async(data: dict):
    return {"counter": data.get("counter", 0) + 1}
add_one_async.NAME = "add_one_async"
add_one_async.VERSION = "v1.0"

async def multiply_two_async(data: dict):
    return {"counter": data.get("counter", 0) * 2}
multiply_two_async.NAME = "multiply_two_async"
multiply_two_async.VERSION = "v1.0"

async def error_step_async(data: dict):
    raise ValueError("Simulated async error")
error_step_async.NAME = "error_step_async"
error_step_async.VERSION = "v1.0"
error_step_async.retry_count = 2
error_step_async.retry_delay = 0

@pytest.mark.asyncio
async def test_pipeline_async_basic(tmp_path):
    p = PipelineAsync(
        pipeline_name="test_async_basic",
        tracking_db=str(tmp_path / "test_async_pipe.db"),
        show_progress=False
    )
    p.set_steps([add_one_async, multiply_two_async])
    res = await p.run({"counter": 2})
    assert res["counter"] == 6

@pytest.mark.asyncio
async def test_pipeline_async_components(tmp_path):
    p = PipelineAsync(
        pipeline_name="test_async_components",
        tracking_db=str(tmp_path / "test_async_comp.db"),
        show_progress=False
    )
    
    steps = [
        add_one_async,
        Condition(
            expression="counter > 0",
            branch_true=[multiply_two_async],
            branch_false=[add_one_async]
        ),
        Parallel(
            steps=[add_one_async, add_one_async]
        )
    ]
    p.set_steps(steps)
    res = await p.run({"counter": 0})
    
    assert "counter" in res

@pytest.mark.asyncio
async def test_pipeline_async_errors(tmp_path):
    p = PipelineAsync(pipeline_name="test_async_err", show_progress=False)
    p.set_steps([error_step_async])
    res = await p.run({})
    assert "error" in res
    assert "Simulated async error" in res["error"]
