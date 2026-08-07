"""
Logic control blocks for WPipe pipelines.

This module provides classes for managing conditional branching, loops,
and parallel execution within a pipeline execution flow.
"""

from typing import Any, Callable, Optional, Union, cast


def merge_parallel_results(
    data: dict[str, Any],
    res: dict[str, Any],
    base: dict[str, Any],
    merge_policy: Union[str, Callable[[Any, Any], Any]] = "accumulate",
) -> dict[str, Any]:
    """
    Merge a parallel step result into the pipeline context.

    Only keys that actually changed relative to the worker's input snapshot
    (``base``) are merged. This makes updates to pre-existing variables
    persist without clobbering keys the worker never touched.

    Args:
        data: Global pipeline context to merge into (mutated in place).
        res: Result returned by the parallel step.
        base: The snapshot the worker received as input.
        merge_policy: How to resolve concurrent writes to the same key:
            - ``"accumulate"`` (default): numbers are summed, lists extended,
              dicts merged; otherwise the last write wins.
            - ``"last_wins"``: the last write (in step declaration order) wins.
            - ``callable(current, new) -> merged``: custom resolution.

    Returns:
        The updated context.
    """
    for key, value in res.items():
        if key == "progress_rich":
            continue
        # Skip keys the worker did not rebind (unchanged snapshot references).
        if key in base and base[key] is value:
            continue

        if key not in data:
            data[key] = value
            continue

        current = data[key]
        if merge_policy == "accumulate":
            if isinstance(current, bool) or isinstance(value, bool):
                data[key] = value
            elif isinstance(current, (int, float)) and isinstance(value, (int, float)):
                data[key] = current + value
            elif isinstance(current, list) and isinstance(value, list):
                data[key] = current + value
            elif isinstance(current, dict) and isinstance(value, dict):
                data[key] = {**current, **value}
            else:
                data[key] = value
        elif merge_policy == "last_wins":
            data[key] = value
        elif callable(merge_policy):
            data[key] = merge_policy(current, value)
        else:
            raise ValueError(f"Unknown merge_policy: {merge_policy!r}")
    return data


def _serialize_step(step: Any) -> Union[dict[str, Any], str]:
    """
    Serialize a pipeline step for representation.

    Args:
        step: The pipeline step to serialize.

    Returns:
        Union[Dict[str, Any], str]: Serialized step representation.
    """
    if hasattr(step, "to_dict"):
        return cast(Union[dict[str, Any], str], step.to_dict())
    if isinstance(step, tuple):
        return {
            "type": "task",
            "name": step[1] if len(step) > 1 else "unknown",
            "version": step[2] if len(step) > 2 else "v1.0",
            "meta": step[3] if len(step) > 3 else {},
        }
    return str(step)


class Condition:
    """
    A conditional branch in the pipeline.

    Attributes:
        expression (str): A string expression to be evaluated.
        branch_true (List[Any]): A list of steps to execute if the expression is true.
        branch_false (List[Any]): A list of steps to execute if the expression is false.
    """

    def __init__(
        self,
        expression: str,
        branch_true: list[Any],
        branch_false: Optional[list[Any]] = None,
    ) -> None:
        """
        Initialize the Condition block.

        Args:
            expression: A Python expression string to evaluate against the data.
            branch_true: Steps to run if the condition evaluates to True.
            branch_false: Steps to run if the condition evaluates to False.
        """
        self.expression: str = expression
        self.branch_true: list[Any] = branch_true or []
        self.branch_false: list[Any] = branch_false or []

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the block to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Serialized representation of the condition block.
        """
        return {
            "type": "condition",
            "expression": self.expression,
            "branch_true": [_serialize_step(s) for s in self.branch_true],
            "branch_false": [_serialize_step(s) for s in self.branch_false],
        }

    def evaluate(self, data: dict[str, Any]) -> bool:
        """
        Evaluate the condition expression using the provided data as context.

        Args:
            data: The current pipeline data dictionary.

        Returns:
            bool: The result of the expression evaluation.

        Raises:
            ValueError: If the expression is invalid or cannot be evaluated.
        """
        # We use a restricted environment for eval to improve security.
        safe_locals = data.copy()
        safe_globals: dict[str, Any] = {
            "True": True,
            "False": False,
            "None": None,
            "__builtins__": {}
        }
        try:
            return bool(eval(self.expression, safe_globals, safe_locals))  # pylint: disable=eval-used
        except (NameError, SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
            raise ValueError(
                f"Invalid condition expression: {self.expression}. Error: {e}"
            ) from e

    def get_branch(self, data: dict[str, Any]) -> list[Any]:
        """
        Get the steps for the chosen branch based on the evaluation result.

        Args:
            data: The current pipeline data dictionary.

        Returns:
            List[Any]: The list of steps to be executed.
        """
        if self.evaluate(data):
            return self.branch_true
        return self.branch_false


class For:
    """
    A loop block in the pipeline.

    Attributes:
        steps (List[Any]): The steps to be executed in each iteration.
        iterations (Optional[int]): Fixed number of iterations.
        validation_expression (Optional[str]): Condition to check before each iteration.
        merge_policy (Union[str, Callable]): How to resolve concurrent writes to the
            same context key when merging the last iteration's result back (see ``merge_parallel_results``).
    """

    def __init__(
        self,
        steps: list[Any],
        iterations: Optional[int] = None,
        validation_expression: Optional[str] = None,
        merge_policy: Union[str, Callable[[Any, Any], Any]] = "last_wins",
    ) -> None:
        """
        Initialize the For loop block.

        Args:
            steps: Steps to execute in each loop.
            iterations: Optional fixed number of iterations.
            validation_expression: Optional expression to evaluate for continuation.
            merge_policy: "last_wins" (default), "accumulate" or a custom callable.
        """
        if not validation_expression and iterations is None:
            raise ValueError("Either iterations or validation_expression must be provided")
        self.steps: list[Any] = steps or []
        self.iterations: Optional[int] = iterations
        self.validation_expression: Optional[str] = validation_expression
        self.merge_policy: Union[str, Callable[[Any, Any], Any]] = merge_policy

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the block to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Serialized representation of the loop block.
        """
        return {
            "type": "for",
            "iterations": self.iterations,
            "expression": self.validation_expression,
            "merge_policy": getattr(self.merge_policy, "__name__", self.merge_policy),
            "steps": [_serialize_step(s) for s in self.steps],
        }

    def should_continue(self, data: dict[str, Any], current_iteration: int) -> bool:
        """
        Check if the loop should continue its execution.

        Args:
            data: The current pipeline data dictionary.
            current_iteration: The index of the current iteration.

        Returns:
            bool: True if the loop should continue, False otherwise.
        """
        if self.iterations is not None:
            return current_iteration < self.iterations

        if self.validation_expression:
            try:
                safe_locals = data.copy()
                safe_globals: dict[str, Any] = {
                    "True": True,
                    "False": False,
                    "None": None,
                    "__builtins__": {}
                }
                return bool(eval(self.validation_expression, safe_globals, safe_locals))  # pylint: disable=eval-used
            except (NameError, SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
                raise ValueError(
                    f"Invalid loop expression: {self.validation_expression}. Error: {e}"
                ) from e
        return False


class Background:
    """
    A background task that executes without blocking the pipeline.

    The step runs in a separate thread and the pipeline continues immediately
    without waiting for completion. The return value is ignored.

    Attributes:
        step: The step to execute in background (callable or tuple).
        capture_error: If True and step fails, run error capture handlers.
    """

    def __init__(self, step: Any, capture_error: bool = False) -> None:
        """
        Initialize a Background block.

        Args:
            step: The step to execute in background (function, class, or tuple).
            capture_error: Whether to run error handlers if the step fails.
        """
        self.step = step
        self.capture_error: bool = capture_error

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the block to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Serialized representation of the background block.
        """
        return {
            "type": "background",
            "capture_error": self.capture_error,
            "step": _serialize_step(self.step),
        }


class Parallel:
    """
    Represents a parallel execution block in the pipeline.

    Attributes:
        steps (List[Any]): List of steps to execute in parallel.
        max_workers (Optional[int]): Maximum number of worker threads/processes.
        use_processes (bool): Whether to use ProcessPoolExecutor instead of ThreadPoolExecutor.
        merge_policy (Union[str, Callable]): How to resolve concurrent writes to the
            same context key (see ``merge_parallel_results``).
    """

    def __init__(
        self,
        steps: list[Any],
        max_workers: Optional[int] = None,
        use_processes: bool = False,
        merge_policy: Union[str, Callable[[Any, Any], Any]] = "accumulate",
    ) -> None:
        """
        Initialize a Parallel block.

        Args:
            steps: List of steps to execute in parallel.
            max_workers: Maximum number of worker threads/processes.
            use_processes: Whether to use ProcessPoolExecutor.
            merge_policy: "accumulate" (default), "last_wins" or a custom callable.
        """
        self.steps: list[Any] = steps or []
        self.max_workers: Optional[int] = max_workers
        self.use_processes: bool = use_processes
        self.merge_policy: Union[str, Callable[[Any, Any], Any]] = merge_policy

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the block to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Serialized representation of the parallel block.
        """
        return {
            "type": "parallel",
            "max_workers": self.max_workers,
            "use_processes": self.use_processes,
            "merge_policy": getattr(self.merge_policy, "__name__", self.merge_policy),
            "steps": [_serialize_step(s) for s in self.steps],
        }
