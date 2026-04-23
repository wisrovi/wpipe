"""
Asynchronous logic control blocks for WPipe pipelines.

This module provides asynchronous versions of conditional branching and loops
for use within async pipeline execution flows.
"""

from typing import Any, Dict, List, Optional


class ConditionAsync:
    """
    An asynchronous conditional branch in the pipeline.

    Attributes:
        expression (str): A string expression to be evaluated.
        branch_true (List[Any]): A list of steps to execute if the expression is true.
        branch_false (List[Any]): A list of steps to execute if the expression is false.
    """

    def __init__(
        self,
        expression: str,
        branch_true: Optional[List[Any]] = None,
        branch_false: Optional[List[Any]] = None,
    ) -> None:
        """
        Initialize the ConditionAsync block.

        Args:
            expression: A Python expression string to evaluate against the data.
            branch_true: Steps to run if the condition evaluates to True.
            branch_false: Steps to run if the condition evaluates to False.
        """
        self.expression: str = expression
        self.branch_true: List[Any] = branch_true or []
        self.branch_false: List[Any] = branch_false or []

    def evaluate(self, data: Dict[str, Any]) -> bool:
        """
        Evaluate the condition expression using the provided data as context.

        Args:
            data: The current pipeline data dictionary.

        Returns:
            bool: The result of the expression evaluation.
        """
        try:
            # We use a restricted environment for eval to improve security.
            safe_locals = data
            safe_globals: Dict[str, Any] = {"__builtins__": {}}
            return bool(eval(self.expression, safe_globals, safe_locals))  # pylint: disable=eval-used
        except (NameError, SyntaxError, TypeError, ValueError, ZeroDivisionError):
            return False


class ForAsync:
    """
    An asynchronous loop block in the pipeline.

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
        Initialize the ForAsync loop block.

        Args:
            steps: Steps to execute in each loop.
            iterations: Optional fixed number of iterations.
            validation_expression: Optional expression to evaluate for continuation.

        Raises:
            ValueError: If neither iterations nor validation_expression is provided.
        """
        if not validation_expression and iterations is None:
            raise ValueError("Either iterations or validation_expression must be provided")
        self.steps: List[Any] = steps
        self.iterations: Optional[int] = iterations
        self.validation_expression: Optional[str] = validation_expression

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
                safe_locals = data
                safe_globals: Dict[str, Any] = {"__builtins__": {}}
                return bool(eval(self.validation_expression, safe_globals, safe_locals))  # pylint: disable=eval-used
            except (NameError, SyntaxError, TypeError, ValueError, ZeroDivisionError):
                return False
        return False
