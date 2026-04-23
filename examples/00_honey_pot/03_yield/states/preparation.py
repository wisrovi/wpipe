"""
Module for the preparation phase of the car.
"""

from typing import Dict, Any
from wpipe.decorators import step
from wpipe.parallel import ExecutionMode, ParallelExecutor


@step(name="open_car", version="v1.1", tags=["preparation"])
def open_car(context: Any) -> Dict[str, Any]:
    """Open the car doors.

    Args:
        context (Any): Pipeline context.

    Returns:
        Dict[str, Any]: Empty result.
    """
    _ = context
    return {}


@step(
    name="inflate_tires_prep",
    version="v1.1",
    depends_on=["open_car"],
    parallel=True,
)
def inflate_tires_prep(context: Any) -> Dict[str, Any]:
    """Inflate tires as part of preparation.

    Args:
        context (Any): Pipeline context.

    Returns:
        Dict[str, Any]: Tire status.
    """
    _ = context
    return {"tires": "OK"}


@step(
    name="clean_windshield",
    version="v1.1",
    depends_on=["open_car"],
    parallel=True,
)
def clean_windshield(context: Any) -> Dict[str, Any]:
    """Clean the windshield.

    Args:
        context (Any): Pipeline context.

    Returns:
        Dict[str, Any]: Windshield status.
    """
    _ = context
    return {"windshield": "Clean"}


@step(
    name="start_motor",
    version="v1.1",
    depends_on=["inflate_tires_prep", "clean_windshield"],
)
def start_motor(context: Any) -> Dict[str, Any]:
    """Start the car motor.

    Args:
        context (Any): Pipeline context.

    Returns:
        Dict[str, Any]: Motor status.
    """
    _ = context
    return {"motor": "ON"}


@step(name="preparation_phase", version="v1.1")
def preparation_phase(data: Any) -> Dict[str, Any]:
    """Encapsulate a parallel execution within a pipeline step.

    Args:
        data (Any): Input data for preparation.

    Returns:
        Dict[str, Any]: Combined results of the preparation steps.
    """
    executor = ParallelExecutor(max_workers=4)

    executor.add_step("open_car", open_car)
    executor.add_step(
        "inflate_tires_prep", inflate_tires_prep, mode=ExecutionMode.IO_BOUND
    )
    executor.add_step(
        "clean_windshield", clean_windshield, mode=ExecutionMode.IO_BOUND
    )
    executor.add_step("start_motor", start_motor)

    result = executor.execute(data)
    return result
