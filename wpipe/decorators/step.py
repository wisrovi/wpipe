"""
Step decorators for pipeline definitions.

Provides @wpipe.step() decorator for inline step definitions.
"""

from typing import Callable, Optional, List, Any, Dict
from functools import wraps
from dataclasses import dataclass, field


# Global registry for decorated steps
_STEP_REGISTRY: Dict[str, 'DecoratedStep'] = {}


@dataclass
class StepMetadata:
    """Metadata for a decorated step."""
    name: str
    func: Callable
    version: str = "v1.0"
    timeout: Optional[float] = None
    depends_on: List[str] = field(default_factory=list)
    retry_count: int = 0
    parallel: bool = False
    description: str = ""
    tags: List[str] = field(default_factory=list)


class DecoratedStep:
    """Represents a decorated step."""
    
    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        version: str = "v1.0",
        timeout: Optional[float] = None,
        depends_on: Optional[List[str]] = None,
        retry_count: int = 0,
        parallel: bool = False,
        description: str = "",
        tags: Optional[List[str]] = None,
    ):
        """Initialize decorated step."""
        self.metadata = StepMetadata(
            name=name or func.__name__,
            func=func,
            version=version,
            timeout=timeout,
            depends_on=depends_on or [],
            retry_count=retry_count,
            description=description,
            tags=tags or [],
        )
        self.parallel = parallel
        self.NAME = self.metadata.name
        self.VERSION = self.metadata.version
    
    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute decorated step."""
        return self.metadata.func(context)
    
    def get_name(self) -> str:
        """Get step name."""
        return self.metadata.name
    
    def get_dependencies(self) -> List[str]:
        """Get step dependencies."""
        return self.metadata.depends_on
    
    def get_timeout(self) -> Optional[float]:
        """Get step timeout."""
        return self.metadata.timeout
    
    def get_metadata(self) -> StepMetadata:
        """Get all metadata."""
        return self.metadata


def step(
    name: Optional[str] = None,
    version: str = "v1.0",
    timeout: Optional[float] = None,
    depends_on: Optional[List[str]] = None,
    retry_count: int = 0,
    parallel: bool = False,
    description: str = "",
    tags: Optional[List[str]] = None,
):
    """
    Decorator to mark a function as a pipeline step.
    
    Args:
        name: Step name (defaults to function name)
        version: Step version (defaults to "v1.0")
        timeout: Timeout in seconds
        depends_on: List of step names this depends on
        retry_count: Number of retries on failure
        parallel: Whether this step can run in parallel
        description: Step description
        tags: List of tags for step
        
    Returns:
        Decorated function
        
    Example:
        @wpipe.step(timeout=30, depends_on=["fetch_data"])
        def process_data(context):
            return {"result": "..."}
    """
    def decorator(func: Callable) -> Callable:
        step_name = name or func.__name__
        
        # Create decorated step
        decorated = DecoratedStep(
            func=func,
            name=step_name,
            version=version,
            timeout=timeout,
            depends_on=depends_on,
            retry_count=retry_count,
            parallel=parallel,
            description=description,
            tags=tags,
        )
        
        # Register in global registry
        _STEP_REGISTRY[step_name] = decorated
        
        # Preserve original function but add metadata
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper._wpipe_step = decorated
        wrapper._wpipe_metadata = decorated.get_metadata()
        
        # Mirror attributes for @state compatibility
        wrapper.NAME = decorated.NAME
        wrapper.VERSION = decorated.VERSION
        
        return wrapper
    
    return decorator


class StepRegistry:
    """Registry for managing decorated steps."""
    
    def __init__(self):
        """Initialize registry."""
        self.steps: Dict[str, DecoratedStep] = {}
    
    def register(self, decorated_step: DecoratedStep) -> None:
        """Register a decorated step."""
        self.steps[decorated_step.get_name()] = decorated_step
    
    def register_func(
        self,
        func: Callable,
        name: Optional[str] = None,
        **metadata,
    ) -> None:
        """
        Register a function as a step.
        
        Args:
            func: Function to register
            name: Step name
            **metadata: Additional metadata
        """
        decorated = DecoratedStep(
            func=func,
            name=name or func.__name__,
            **metadata,
        )
        self.register(decorated)
    
    def get(self, name: str) -> Optional[DecoratedStep]:
        """Get step by name."""
        return self.steps.get(name)
    
    def get_all(self) -> Dict[str, DecoratedStep]:
        """Get all registered steps."""
        return self.steps.copy()
    
    def clear(self) -> None:
        """Clear all registered steps."""
        self.steps.clear()
    
    def get_global_registry() -> Dict[str, DecoratedStep]:
        """Get global step registry."""
        return _STEP_REGISTRY.copy()
    
    @staticmethod
    def from_global() -> 'StepRegistry':
        """Create registry from global registry."""
        registry = StepRegistry()
        registry.steps = _STEP_REGISTRY.copy()
        return registry


class AutoRegister:
    """
    Utility to auto-register decorated steps into a pipeline.
    
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
    def register_all(pipeline: 'Pipeline', registry: Optional[StepRegistry] = None) -> None:
        """
        Auto-register all decorated steps to pipeline.
        
        Args:
            pipeline: Target pipeline
            registry: Optional custom registry (uses global by default)
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
        pipeline: 'Pipeline',
        tag: str,
        registry: Optional[StepRegistry] = None,
    ) -> None:
        """
        Register steps with specific tag.
        
        Args:
            pipeline: Target pipeline
            tag: Tag to filter by
            registry: Optional custom registry
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
    """Get the global step registry."""
    return StepRegistry.from_global()


def clear_registry() -> None:
    """Clear the global step registry."""
    _STEP_REGISTRY.clear()
