import asyncio
import pytest
from wpipe.pipe.components.constants import Codes
from wpipe.pipe.components.logic_blocks import Condition, For
from wpipe.pipe.components.logic_blocks_async import ConditionAsync, ForAsync
from wpipe.pipe.components.reporting import ReportingMixin
from wpipe.api_client import APIClient
from unittest.mock import MagicMock

# 1. Tests para Constantes
def test_constants():
    assert Codes.TASK_RUNNING == 100
    assert Codes.PROCESS_FINISHED == 3

# 2. Tests para Logic Blocks (Sync)
def test_condition_logic():
    cond = Condition("x > 10", branch_true=["true_step"], branch_false=["false_step"])
    assert cond.evaluate({"x": 15}) is True
    assert cond.evaluate({"x": 5}) is False
    assert cond.evaluate({"y": 1}) is False # Missing key
    assert cond.get_branch(True) == ["true_step"]
    assert cond.get_branch(False) == ["false_step"]

def test_for_logic():
    loop = For(steps=["step1"], iterations=3)
    assert loop.should_continue({}, 0) is True
    assert loop.should_continue({}, 3) is False
    
    expr_loop = For(steps=["step1"], validation_expression="go")
    assert expr_loop.should_continue({"go": True}, 0) is True
    assert expr_loop.should_continue({"go": False}, 0) is False
    assert expr_loop.should_continue({}, 0) is False
    
    with pytest.raises(ValueError):
        For(steps=[])

# 3. Tests para Logic Blocks (Async)
def test_condition_async_logic():
    cond = ConditionAsync("x == 1")
    assert cond.evaluate({"x": 1}) is True
    assert cond.evaluate({"x": 2}) is False

def test_for_async_logic():
    loop = ForAsync(steps=[], iterations=2)
    assert loop.should_continue({}, 0) is True
    assert loop.should_continue({}, 2) is False

# 4. Tests para Reporting Mixin
def test_reporting_mixin():
    mixin = ReportingMixin()
    mock_api = MagicMock()
    
    # Task update
    mixin._api_task_update(mock_api, {"id": 1})
    mock_api.update_task.assert_called_once()
    
    # Process update
    mixin._api_process_update(mock_api, {"id": 2})
    mock_api.update_process.assert_called_once()
    
    # Error handling (should not raise)
    mock_api.update_task.side_effect = Exception("API Down")
    mixin._api_task_update(mock_api, {"id": 1}, verbose=True)
    
    # Traceback formatting
    try:
        raise ValueError("test")
    except Exception as e:
        tb = mixin._format_error_traceback(e)
        assert any("ValueError: test" in line for line in tb)
