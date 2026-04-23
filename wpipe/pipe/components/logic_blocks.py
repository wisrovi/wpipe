"""
Logic control blocks for WPipe pipelines.

This module provides classes for managing conditional branching, loops,
and parallel execution within a pipeline execution flow.
"""

from typing import Any, Dict, List, Optional, Union


def _serialize_step(step: Any) -> Union[Dict[str, Any], str]:
    """
    Serialize a pipeline step for representation.

    Args:
        step: The pipeline step to serialize.

    Returns:
        Union[Dict[str, Any], str]: Serialized step representation.
    """
    if hasattr(step, "to_dict"):
        return step.to_dict()
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
        branch_true: List[Any],
        branch_false: Optional[List[Any]] = None,
    ) -> None:
        """
        Initialize the Condition block.

        Args:
            expression: A Python expression string to evaluate against the data.
            branch_true: Steps to run if the condition evaluates to True.
            branch_false: Steps to run if the condition evaluates to False.
        """
        self.expression: str = expression
        self.branch_true: List[Any] = branch_true or []
        self.branch_false: List[Any] = branch_false or []

    def to_dict(self) -> Dict[str, Any]:
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

    def evaluate(self, data: Dict[str, Any]) -> bool:
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
        safe_globals: Dict[str, Any] = {
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

    def get_branch(self, data: Dict[str, Any]) -> List[Any]:
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
    """

    def __init__(
        self,
        steps: List[Any],
        iterations: Optional[int] = None,
        validation_expression: Optional[str] = None,
    ) -> None:
        """
        Initialize the For loop block.

        Args:
            steps: Steps to execute in each loop.
            iterations: Optional fixed number of iterations.
            validation_expression: Optional expression to evaluate for continuation.

        Raises:
            ValueError: If neither iterations nor validation_expression is provided.
        """
        if not validation_expression and iterations is None:
            raise ValueError("Either iterations or validation_expression must be provided")
        self.steps: List[Any] = steps or []
        self.iterations: Optional[int] = iterations
        self.validation_expression: Optional[str] = validation_expression

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the block to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Serialized representation of the loop block.
        """
        return {
            "type": "for",
            "iterations": self.iterations,
            "expression": self.validation_expression,
            "steps": [_serialize_step(s) for s in self.steps],
        }

    def should_continue(self, data: Dict[str, Any], current_iteration: int) -> bool:
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
                safe_globals: Dict[str, Any] = {
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


class Parallel:
    """
    Represents a parallel execution block in the pipeline.

    Attributes:
        steps (List[Any]): List of steps to execute in parallel.
        max_workers (Optional[int]): Maximum number of worker threads/processes.
        use_processes (bool): Whether to use ProcessPoolExecutor instead of ThreadPoolExecutor.
    """

    def __init__(
        self,
        steps: List[Any],
        max_workers: Optional[int] = None,
        use_processes: bool = False,
    ) -> None:
        """
        Initialize a Parallel block.

        Args:
            steps: List of steps to execute in parallel.
            max_workers: Maximum number of worker threads/processes.
            use_processes: Whether to use ProcessPoolExecutor.
        """
        self.steps: List[Any] = steps or []
        self.max_workers: Optional[int] = max_workers
        self.use_processes: bool = use_processes

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the block to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Serialized representation of the parallel block.
        """
        return {
            "type": "parallel",
            "max_workers": self.max_workers,
            "use_processes": self.use_processes,
            "steps": [_serialize_step(s) for s in self.steps],
        }
