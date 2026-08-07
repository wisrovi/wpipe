"""
Step decorators for pipeline definitions.

Provides @wpipe.step() decorator for inline step definitions.
"""

import inspect
from dataclasses import dataclass, field
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Optional, cast

if TYPE_CHECKING:
    from wpipe.pipeline import Pipeline

# Global registry for decorated steps
_STEP_REGISTRY: dict[str, "DecoratedStep"] = {}


@dataclass
class StepMetadata:
    """Metadata for a decorated step.

    Attributes:
        name: The name of the step.
        func: The function to execute.
        version: The version of the step.
        timeout: Execution timeout in seconds.
        depends_on: List of step names this step depends on.
        retry_count: Number of retries on failure.
        retry_delay: Delay between retries in seconds.
        retry_on_exceptions: Tuple of exceptions that trigger a retry.
        parallel: Whether the step can run in parallel.
        description: Description of the step's purpose.
        tags: List of tags for categorization.
    """

    name: str
    func: Callable
    version: str = "v1.0"
    timeout: Optional[float] = None
    depends_on: list[str] = field(default_factory=list)
    retry_count: Optional[int] = None
    retry_delay: Optional[float] = None
    retry_on_exceptions: Optional[tuple[type, ...]] = None
    parallel: bool = False
    description: str = ""
    tags: list[str] = field(default_factory=list)


class DecoratedStep:
    """Represents a decorated step.

    Attributes:
        metadata: The metadata associated with the step.
        parallel: Whether the step can run in parallel.
        name: The name of the step (compatibility attribute).
        version: The version of the step (compatibility attribute).
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        version: str = "v1.0",
        timeout: Optional[float] = None,
        depends_on: Optional[list[str]] = None,
        retry_count: Optional[int] = None,
        retry_delay: Optional[float] = None,
        retry_on_exceptions: Optional[tuple[type, ...]] = None,
        parallel: bool = False,
        description: str = "",
        tags: Optional[list[str]] = None,
    ):
        """Initialize decorated step.

        Args:
            func: Function to be wrapped as a step.
            name: Step name (defaults to function name).
            version: Step version.
            timeout: Execution timeout.
            depends_on: Dependencies list.
            retry_count: Max retry attempts.
            retry_delay: Seconds between retries.
            retry_on_exceptions: Exceptions to catch for retrying.
            parallel: Parallel execution flag.
            description: Step description.
            tags: Category tags.
        """
        self.metadata = StepMetadata(
            name=name or func.__name__,
            func=func,
            version=version,
            timeout=timeout,
            depends_on=depends_on or [],
            retry_count=retry_count,
            retry_delay=retry_delay,
            retry_on_exceptions=retry_on_exceptions,
            description=description,
            tags=tags or [],
        )
        self.parallel = parallel
        # Compatibility with @state attributes
        self.NAME = self.metadata.name  # pylint: disable=invalid-name
        self.VERSION = self.metadata.version  # pylint: disable=invalid-name

    def __call__(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute decorated step.

        Args:
            context: The pipeline context.

        Returns:
            The modified context.
        """
        return cast(dict[str, Any], self.metadata.func(context))

    def get_name(self) -> str:
        """Get step name.

        Returns:
            The step name.
        """
        return self.metadata.name

    def get_dependencies(self) -> list[str]:
        """Get step dependencies.

        Returns:
            List of dependency names.
        """
        return self.metadata.depends_on

    def get_timeout(self) -> Optional[float]:
        """Get step timeout.

        Returns:
            The timeout in seconds or None.
        """
        return self.metadata.timeout

    def get_metadata(self) -> StepMetadata:
        """Get all metadata.

        Returns:
            The StepMetadata object.
        """
        return self.metadata


def step(
    name: Optional[Any] = None,
    version: str = "v1.0",
    timeout: Optional[float] = None,
    depends_on: Optional[list[str]] = None,
    retry_count: Optional[int] = None,
    retry_delay: Optional[float] = None,
    retry_on_exceptions: Optional[tuple[type, ...]] = None,
    parallel: bool = False,
    description: str = "",
    tags: Optional[list[str]] = None,
) -> Callable:
    """Decorator to mark a function or class as a pipeline step.

    Supports both @step and @step(name="...") syntax.
    """

    def decorator(func: Callable) -> Callable:
        # Determine step name
        actual_name = name if isinstance(name, str) else func.__name__

        # Create decorated step
        decorated = DecoratedStep(
            func=func,
            name=actual_name,
            version=version,
            timeout=timeout,
            depends_on=depends_on,
            retry_count=retry_count,
            retry_delay=retry_delay,
            retry_on_exceptions=retry_on_exceptions,
            parallel=parallel,
            description=description,
            tags=tags,
        )

        # Register in global registry
        _STEP_REGISTRY[actual_name] = decorated

        # Preserve original function/class but add metadata
        if inspect.isclass(func):
            # For classes, we return the class itself
            # We add attributes to the original class for metadata detection
            setattr(func, "_wpipe_step", decorated)  # noqa: B010
            setattr(func, "_wpipe_metadata", decorated.get_metadata())  # noqa: B010
            setattr(func, "NAME", decorated.NAME)  # noqa: B010
            setattr(func, "VERSION", decorated.VERSION)  # noqa: B010
            return func

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        setattr(wrapper, "_wpipe_step", decorated)  # noqa: B010
        setattr(wrapper, "_wpipe_metadata", decorated.get_metadata())  # noqa: B010

        # Mirror attributes for @state compatibility
        setattr(wrapper, "NAME", decorated.NAME)  # noqa: B010
        setattr(wrapper, "VERSION", decorated.VERSION)  # noqa: B010

        return wrapper

    # If used as @step without parentheses
    if callable(name) and not isinstance(name, str):
        func = name
        # We must re-assign name to None so that actual_name uses func.__name__
        name = None
        return decorator(func)

    return decorator


class StepRegistry:
    """Registry for managing decorated steps.

    Attributes:
        steps: Dictionary mapping step names to DecoratedStep objects.
    """

    def __init__(self) -> None:
        """Initialize registry."""
        self.steps: dict[str, DecoratedStep] = {}

    def register(self, decorated_step: DecoratedStep) -> None:
        """Register a decorated step.

        Args:
            decorated_step: The step to register.
        """
        self.steps[decorated_step.get_name()] = decorated_step

    def register_func(
        self,
        func: Callable,
        name: Optional[str] = None,
        **metadata: Any,
    ) -> None:
        """Register a function as a step.

        Args:
            func: Function to register.
            name: Step name.
            **metadata: Additional metadata.
        """
        decorated = DecoratedStep(
            func=func,
            name=name or func.__name__,
            **metadata,
        )
        self.register(decorated)

    def get(self, name: str) -> Optional[DecoratedStep]:
        """Get step by name.

        Args:
            name: The name of the step.

        Returns:
            The DecoratedStep object or None if not found.
        """
        return self.steps.get(name)

    def get_all(self) -> dict[str, DecoratedStep]:
        """Get all registered steps.

        Returns:
            A copy of the steps dictionary.
        """
        return self.steps.copy()

    def clear(self) -> None:
        """Clear all registered steps."""
        self.steps.clear()

    @staticmethod
    def get_global_registry() -> dict[str, "DecoratedStep"]:
        """Get global step registry.

        Returns:
            A copy of the global step registry.
        """
        return _STEP_REGISTRY.copy()

    @classmethod
    def from_global(cls) -> "StepRegistry":
        """Create registry from global registry.

        Returns:
            A StepRegistry instance populated with global steps.
        """
        registry = cls()
        registry.steps = _STEP_REGISTRY.copy()
        return registry


class AutoRegister:
    """Utility to auto-register decorated steps into a pipeline.

    Example:
        @wpipe.step(timeout=30)
        def fetch_data(context):
            return {"data": [...]}

        @wpipe.step(depends_on=["fetch_data"])
        def process_data(context):
            return {"result": [...]}

        pipeline = Pipeline()
        AutoRegister.register_all(pipeline)
    """

    @staticmethod
    def register_all(
        pipeline: "Pipeline", registry: Optional[StepRegistry] = None
    ) -> None:
        """Auto-register all decorated steps to pipeline.

        Args:
            pipeline: Target pipeline.
            registry: Optional custom registry (uses global by default).
        """
        if registry is None:
            steps = _STEP_REGISTRY
        else:
            steps = registry.get_all()

        for name, decorated_step in steps.items():
            metadata = decorated_step.get_metadata()
            pipeline.add_state(
                name=name,
                state=decorated_step.metadata.func,
                depends_on=metadata.depends_on,
                timeout=metadata.timeout,
            )

    @staticmethod
    def register_by_tag(
        pipeline: "Pipeline",
        tag: str,
        registry: Optional[StepRegistry] = None,
    ) -> None:
        """Register steps with specific tag.

        Args:
            pipeline: Target pipeline.
            tag: Tag to filter by.
            registry: Optional custom registry.
        """
        if registry is None:
            steps = _STEP_REGISTRY
        else:
            steps = registry.get_all()

        for name, decorated_step in steps.items():
            metadata = decorated_step.get_metadata()
            if tag in metadata.tags:
                pipeline.add_state(
                    name=name,
                    state=decorated_step.metadata.func,
                    depends_on=metadata.depends_on,
                    timeout=metadata.timeout,
                )


def get_step_registry() -> StepRegistry:
    """Get the global step registry.

    Returns:
        The StepRegistry from the global scope.
    """
    return StepRegistry.from_global()


def clear_registry() -> None:
    """Clear the global step registry."""
    _STEP_REGISTRY.clear()
