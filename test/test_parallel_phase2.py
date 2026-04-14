"""
Tests for Phase 2 parallelism features.
"""

import time

import pytest

from wpipe.parallel import DAGScheduler, ExecutionMode, ParallelExecutor, StepDependency


class TestDAGScheduler:
    """Test dependency resolution."""

    def test_linear_dependencies(self):
        """Test linear dependency chain."""
        scheduler = DAGScheduler()

        scheduler.add_step(StepDependency("step_1", lambda c: c, dependencies=[]))
        scheduler.add_step(
            StepDependency("step_2", lambda c: c, dependencies=["step_1"])
        )
        scheduler.add_step(
            StepDependency("step_3", lambda c: c, dependencies=["step_2"])
        )

        groups = scheduler.topological_sort()

        assert len(groups) == 3
        assert groups[0] == ["step_1"]
        assert groups[1] == ["step_2"]
        assert groups[2] == ["step_3"]

    def test_parallel_dependencies(self):
        """Test parallel execution branches."""
        scheduler = DAGScheduler()

        scheduler.add_step(StepDependency("step_1", lambda c: c, dependencies=[]))
        scheduler.add_step(
            StepDependency("step_2", lambda c: c, dependencies=["step_1"])
        )
        scheduler.add_step(
            StepDependency("step_3", lambda c: c, dependencies=["step_1"])
        )
        scheduler.add_step(
            StepDependency("step_4", lambda c: c, dependencies=["step_2", "step_3"])
        )

        groups = scheduler.topological_sort()

        assert len(groups) == 3
        assert groups[0] == ["step_1"]
        assert set(groups[1]) == {"step_2", "step_3"}
        assert groups[2] == ["step_4"]

    def test_diamond_dependency(self):
        """Test diamond dependency pattern."""
        scheduler = DAGScheduler()

        scheduler.add_step(StepDependency("A", lambda c: c, dependencies=[]))
        scheduler.add_step(StepDependency("B", lambda c: c, dependencies=["A"]))
        scheduler.add_step(StepDependency("C", lambda c: c, dependencies=["A"]))
        scheduler.add_step(StepDependency("D", lambda c: c, dependencies=["B", "C"]))

        groups = scheduler.topological_sort()

        assert len(groups) == 3
        assert groups[0] == ["A"]
        assert set(groups[1]) == {"B", "C"}
        assert groups[2] == ["D"]


class TestParallelExecutor:
    """Test parallel execution."""

    def test_sequential_execution(self):
        """Test sequential step execution."""

        def step_1(c):
            return {"value": 1}

        def step_2(c):
            v = c.get("value", 0)
            return {"value": v + 1}

        def step_3(c):
            v = c.get("value", 0)
            return {"value": v + 1}

        executor = ParallelExecutor()
        executor.add_step("step_1", step_1)
        executor.add_step("step_2", step_2, depends_on=["step_1"])
        executor.add_step("step_3", step_3, depends_on=["step_2"])

        result = executor.execute({})

        assert result["value"] == 3

    def test_parallel_execution_speedup(self):
        """Test that parallel execution is faster."""
        executor = ParallelExecutor(max_workers=3)

        def slow_task_1(c):
            time.sleep(0.5)
            return {"task_1": "done"}

        def slow_task_2(c):
            time.sleep(0.5)
            return {"task_2": "done"}

        def slow_task_3(c):
            time.sleep(0.5)
            return {"task_3": "done"}

        def merge(c):
            return {"merged": True}

        executor.add_step("task_1", slow_task_1, mode=ExecutionMode.IO_BOUND)
        executor.add_step("task_2", slow_task_2, mode=ExecutionMode.IO_BOUND)
        executor.add_step("task_3", slow_task_3, mode=ExecutionMode.IO_BOUND)
        executor.add_step("merge", merge, depends_on=["task_1", "task_2", "task_3"])

        start = time.time()
        result = executor.execute({})
        elapsed = time.time() - start

        # Should complete in ~1s (parallel) instead of ~2s (sequential)
        assert elapsed < 1.5
        assert result["merged"] == True

    def test_context_passing(self):
        """Test context passing between steps."""

        def step_1(c):
            return {"value": 10}

        def step_2(c):
            return {"multiplied": c.get("value", 1) * 2}

        def step_3(c):
            return {"added": c.get("multiplied", 0) + 5}

        executor = ParallelExecutor()
        executor.add_step("step_1", step_1)
        executor.add_step("step_2", step_2, depends_on=["step_1"])
        executor.add_step("step_3", step_3, depends_on=["step_2"])

        result = executor.execute({})

        assert result["value"] == 10
        assert result["multiplied"] == 20
        assert result["added"] == 25

    def test_execution_modes(self):
        """Test different execution modes."""

        def io_task(c):
            return {"io": "done"}

        def seq_task(c):
            return {"seq": "done"}

        executor = ParallelExecutor()

        # Note: ProcessPool requires top-level functions for pickling
        # We test IO_BOUND and SEQUENTIAL in this test
        executor.add_step("io_task", io_task, mode=ExecutionMode.IO_BOUND)
        executor.add_step("seq_task", seq_task, mode=ExecutionMode.SEQUENTIAL)

        result = executor.execute({})

        assert result["io"] == "done"
        assert result["seq"] == "done"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
