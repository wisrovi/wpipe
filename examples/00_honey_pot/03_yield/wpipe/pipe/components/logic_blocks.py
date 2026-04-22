"""
Logic control blocks for WPipe pipelines.
"""

from typing import Any, List, Optional


class Condition:
    """A conditional branch in the pipeline."""

    def __init__(
        self,
        expression: str,
        branch_true: Optional[List[Any]] = None,
        branch_false: Optional[List[Any]] = None,
    ) -> None:
        self.expression = expression
        self.branch_true = branch_true or []
        self.branch_false = branch_false or []

    def evaluate(self, data: dict) -> bool:
        """Evaluate the condition expression."""
        try:
            return eval(self.expression, {}, data)
        except Exception:
            return False

    def get_branch(self, result: bool) -> List[Any]:
        """Get the steps for the chosen branch."""
        return self.branch_true if result else self.branch_false


class For:
    """A loop block in the pipeline."""

    def __init__(
        self,
        steps: List[Any],
        iterations: Optional[int] = None,
        validation_expression: Optional[str] = None,
    ) -> None:
        if not validation_expression and iterations is None:
            raise ValueError("Either iterations or validation_expression must be provided")
        self.steps = steps
        self.iterations = iterations
        self.validation_expression = validation_expression

    def should_continue(self, data: dict, current_iteration: int) -> bool:
        """Check if the loop should continue."""
        if self.iterations is not None:
            return current_iteration < self.iterations
        if self.validation_expression:
            try:
                return eval(self.validation_expression, {}, data)
            except Exception:
                return False
        return False
