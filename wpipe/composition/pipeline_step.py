"""
Pipeline composition for nested pipelines.

Allows using a Pipeline as a step within another Pipeline.
"""

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class PipelineAsStep:
    """
    Wrapper that treats a Pipeline as a single step.

    This allows nesting pipelines: a Pipeline object can be added
    to another Pipeline and executed as a single step unit.
    """

    name: str
    pipeline: "Pipeline"
    timeout: Optional[float] = None
    depends_on: Optional[List[str]] = None

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute nested pipeline.

        Args:
            context: Parent pipeline context

        Returns:
            Results from nested pipeline
        """
        # Run the nested pipeline with parent context
        result = self.pipeline.run(context)

        # Return only new/modified keys
        return {k: v for k, v in result.items() if k not in context}

    def get_dependencies(self) -> List[str]:
        """
        Get step dependencies.

        Returns:
            List of step names this step depends on.
        """
        return self.depends_on or []

    def get_timeout(self) -> Optional[float]:
        """
        Get step timeout.

        Returns:
            Timeout in seconds or None.
        """
        return self.timeout


class CompositionHelper:
    """Helper utilities for pipeline composition."""

    @staticmethod
    def merge_contexts(
        parent: Dict[str, Any],
        child: Dict[str, Any],
        conflict_resolution: str = "child_wins",
    ) -> Dict[str, Any]:
        """
        Merge child context into parent context.

        Args:
            parent: Parent pipeline context
            child: Child pipeline context
            conflict_resolution: How to handle conflicts
                - "child_wins": Child values override parent
                - "parent_wins": Parent values override child
                - "merge_list": Merge lists instead of replacing

        Returns:
            Merged context
        """
        merged = parent.copy()

        for key, value in child.items():
            if key in parent:
                if conflict_resolution == "child_wins":
                    merged[key] = value
                elif conflict_resolution == "parent_wins":
                    pass  # Keep parent value
                elif conflict_resolution == "merge_list":
                    if isinstance(parent[key], list) and isinstance(value, list):
                        merged[key] = parent[key] + value
                    else:
                        merged[key] = value
            else:
                merged[key] = value

        return merged

    @staticmethod
    def extract_context_subset(context: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
        """
        Extract subset of context for child pipeline.

        Args:
            context: Full context
            keys: Keys to extract

        Returns:
            Subset context
        """
        return {k: context.get(k) for k in keys if k in context}

    @staticmethod
    def validate_context_compatibility(
        parent_schema: Dict[str, type], child_schema: Dict[str, type]
    ) -> bool:
        """
        Validate that child pipeline context is compatible with parent.

        Args:
            parent_schema: Parent context schema
            child_schema: Child context schema

        Returns:
            True if compatible

        Raises:
            TypeError: If incompatible
        """
        for key, child_type in child_schema.items():
            if key in parent_schema:
                parent_type = parent_schema[key]
                if parent_type != child_type:
                    raise TypeError(
                        f"Type mismatch for key '{key}': "
                        f"expected {parent_type}, got {child_type}"
                    )

        return True


class NestedPipelineStep:
    """
    Advanced wrapper for nested pipelines with advanced features.

    Features:
    - Context transformation
    - Result filtering
    - Error handling
    - Performance tracking
    """

    def __init__(
        self,
        name: str,
        pipeline: "Pipeline",
        context_filter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        result_filter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        timeout: Optional[float] = None,
    ):
        """
        Initialize nested pipeline step.

        Args:
            name: Step name
            pipeline: Pipeline to nest
            context_filter: Function to transform context before passing
            result_filter: Function to transform results
            timeout: Step timeout
        """
        self.name = name
        self.pipeline = pipeline
        self.context_filter = context_filter
        self.result_filter = result_filter
        self.timeout = timeout
        self.execution_time = 0.0

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute nested pipeline with filtering.

        Args:
            context: Parent pipeline context.

        Returns:
            Dictionary with the results of the execution.
        """
        # Filter context if needed
        child_context = context
        if self.context_filter:
            child_context = self.context_filter(context)

        # Run pipeline
        start = time.time()
        result = self.pipeline.run(child_context)
        self.execution_time = time.time() - start

        # Filter result if needed
        if self.result_filter:
            result = self.result_filter(result)

        return result

    def get_execution_time(self) -> float:
        """
        Get last execution time.

        Returns:
            Execution time in seconds.
        """
        return self.execution_time
