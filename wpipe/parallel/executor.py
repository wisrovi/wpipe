"""
Parallel execution engine for WPipe pipelines.

Enables execution of multiple pipeline steps in parallel using:
- ThreadPoolExecutor for I/O-bound tasks
- ProcessPoolExecutor for CPU-bound tasks
- Automatic dependency resolution
"""

import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class ExecutionMode(Enum):
    """Execution mode for parallel steps."""
    IO_BOUND = "io_bound"      # Use ThreadPoolExecutor
    CPU_BOUND = "cpu_bound"    # Use ProcessPoolExecutor
    SEQUENTIAL = "sequential"  # No parallelism


@dataclass
class StepDependency:
    """Represents a step and its dependencies."""
    name: str
    func: Callable
    timeout: Optional[float] = None
    mode: ExecutionMode = ExecutionMode.IO_BOUND
    dependencies: List[str] = field(default_factory=list)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, StepDependency):
            return self.name == other.name
        return self.name == other


class DAGScheduler:
    """Directed Acyclic Graph scheduler for step dependencies."""

    def __init__(self):
        """Initialize DAG scheduler."""
        self.steps: Dict[str, StepDependency] = {}
        self.graph: Dict[str, Set[str]] = {}
        self.in_degree: Dict[str, int] = {}

    def add_step(self, step: StepDependency) -> None:
        """Add step to DAG."""
        self.steps[step.name] = step
        self.graph[step.name] = set(step.dependencies)
        self.in_degree[step.name] = len(step.dependencies)

        # Update graph for dependencies
        for dep in step.dependencies:
            if dep not in self.graph:
                self.graph[dep] = set()

    def topological_sort(self) -> List[List[str]]:
        """
        Get steps in topological order, grouped by execution level.
        
        Returns:
            List of lists, where each inner list contains steps that can
            run in parallel at that level.
        """
        in_degree = self.in_degree.copy()
        queue = [name for name, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            # All items in queue can run in parallel
            result.append(queue[:])
            new_queue = []

            for step in queue:
                # Find all steps that depend on this one
                for other, deps in self.graph.items():
                    if step in deps:
                        in_degree[other] -= 1
                        if in_degree[other] == 0:
                            new_queue.append(other)

            queue = new_queue

        return result

    def get_parallel_groups(self) -> List[List[StepDependency]]:
        """Get groups of steps that can run in parallel."""
        groups = self.topological_sort()
        return [
            [self.steps[name] for name in group]
            for group in groups
        ]


class ContextMerger:
    """Merge contexts from parallel step executions."""

    @staticmethod
    def merge(contexts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge multiple contexts into single context.
        
        Args:
            contexts: Dict mapping step names to their result contexts
            
        Returns:
            Merged context with all results
        """
        merged = {}

        for step_name, context in contexts.items():
            if context:
                merged.update(context)

        return merged


class ParallelExecutor:
    """Executes pipeline steps in parallel with dependency resolution."""

    def __init__(self, max_workers: int = 4):
        """
        Initialize parallel executor.
        
        Args:
            max_workers: Maximum number of worker threads/processes
        """
        self.max_workers = max_workers
        self.scheduler = DAGScheduler()
        self.results: Dict[str, Any] = {}
        self.lock = threading.Lock()

    def add_step(
        self,
        name: str,
        func: Callable,
        mode: ExecutionMode = ExecutionMode.IO_BOUND,
        timeout: Optional[float] = None,
        depends_on: Optional[List[str]] = None,
    ) -> None:
        """
        Add step to executor.
        
        Args:
            name: Step name
            func: Step function
            mode: Execution mode (IO_BOUND or CPU_BOUND)
            timeout: Optional timeout in seconds
            depends_on: List of step names this depends on
        """
        step = StepDependency(
            name=name,
            func=func,
            timeout=timeout,
            mode=mode,
            dependencies=depends_on or [],
        )
        self.scheduler.add_step(step)

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute all steps respecting dependencies.
        
        Args:
            context: Initial pipeline context
            
        Returns:
            Final context with all step results
        """
        parallel_groups = self.scheduler.get_parallel_groups()
        current_context = context.copy()

        for group in parallel_groups:
            # Separate by execution mode
            io_tasks = [s for s in group if s.mode == ExecutionMode.IO_BOUND]
            cpu_tasks = [s for s in group if s.mode == ExecutionMode.CPU_BOUND]
            seq_tasks = [s for s in group if s.mode == ExecutionMode.SEQUENTIAL]

            # Execute sequential tasks first (no parallelism)
            for step in seq_tasks:
                result = self._execute_step(step, current_context)
                if result:
                    current_context.update(result)
                with self.lock:
                    self.results[step.name] = result

            # Execute IO-bound tasks in ThreadPool
            if io_tasks:
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {
                        executor.submit(self._execute_step, step, current_context): step
                        for step in io_tasks
                    }

                    for future in as_completed(futures):
                        step = futures[future]
                        result = future.result()
                        if result:
                            current_context.update(result)
                        with self.lock:
                            self.results[step.name] = result

            # Execute CPU-bound tasks in ProcessPool
            if cpu_tasks:
                with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {
                        executor.submit(self._execute_step_safe, step, current_context): step
                        for step in cpu_tasks
                    }

                    for future in as_completed(futures):
                        step = futures[future]
                        result = future.result()
                        if result:
                            current_context.update(result)
                        with self.lock:
                            self.results[step.name] = result

        return current_context

    def _execute_step(
        self,
        step: StepDependency,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute a single step."""
        try:
            result = step.func(context)
            return result or {}
        except Exception as e:
            print(f"Error in step {step.name}: {e}")
            raise

    def _execute_step_safe(
        self,
        step: StepDependency,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute step safely (for ProcessPool)."""
        # Note: For ProcessPool, we need to handle serialization
        return self._execute_step(step, context)

    def get_results(self) -> Dict[str, Any]:
        """Get results from all executed steps."""
        return self.results.copy()

    def get_execution_time(self) -> float:
        """Get total execution time (stub for now)."""
        return 0.0


class ContextMerger:
    """Merge results from parallel executions."""

    @staticmethod
    def merge(results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple result contexts."""
        merged = {}
        for name, ctx in results.items():
            if ctx:
                merged.update(ctx)
        return merged
