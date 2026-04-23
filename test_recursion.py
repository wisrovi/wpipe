"""
Module to test pipeline recursion and complex orchestrations.

This script defines various mock steps and classes to build a complex
pipeline using WPipe, including conditional branches and parallel execution.
"""

import logging
import traceback
from typing import Any, Dict
from wpipe import Pipeline, step, Condition, Parallel, For

# Configure logger
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

# Mock steps
@step(name="check_requirements")
def check_requirements(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if the necessary requirements are met.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

@step(name="clean_folder")
def clean_folder(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean the temporary folder.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

@step(name="reset_part_model")
def reset_part_model(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reset the part detection model.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

@step(name="reset_damage_search")
def reset_damage_search(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reset the damage search state.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

@step(name="open_video_capture")
def open_video_capture(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Open the video capture device.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

@step(name="create_batch_frames")
def create_batch_frames(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a batch of frames for processing.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary with processing status.
    """
    data["process_completed"] = 0
    return data

@step(name="filter_by_car")
def filter_by_car(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter frames to detect cars.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

# Mock classes for steps that are classes
@step(name="DamageDetector")
class DamageDetector:
    """
    Step class to detect damage in frames.
    """
    def __init__(self) -> None:
        """Initialize the DamageDetector."""

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute damage detection.

        Args:
            data: The pipeline data dictionary.

        Returns:
            The updated data dictionary.
        """
        return data

@step(name="PartSegmentator")
class PartSegmentator:
    """
    Step class to segment parts in frames.
    """
    def __init__(self) -> None:
        """Initialize the PartSegmentator."""

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute part segmentation.

        Args:
            data: The pipeline data dictionary.

        Returns:
            The updated data dictionary.
        """
        return data

@step(name="get_angle")
def get_angle(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the angle of the detected object.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

@step(name="DamageSegmentator")
class DamageSegmentator:
    """
    Step class to segment damage areas.
    """
    def __init__(self) -> None:
        """Initialize the DamageSegmentator."""

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute damage segmentation.

        Args:
            data: The pipeline data dictionary.

        Returns:
            The updated data dictionary.
        """
        return data

@step(name="DamageClasification")
class DamageClasification:
    """
    Step class to classify detected damage.
    """
    def __init__(self) -> None:
        """Initialize the DamageClasification."""

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute damage classification.

        Args:
            data: The pipeline data dictionary.

        Returns:
            The updated data dictionary.
        """
        return data

@step(name="DamageSecondClasification")
class DamageSecondClasification:
    """
    Step class for secondary damage classification.
    """
    def __init__(self) -> None:
        """Initialize the DamageSecondClasification."""

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute secondary damage classification.

        Args:
            data: The pipeline data dictionary.

        Returns:
            The updated data dictionary.
        """
        return data

@step(name="add_watermark")
def add_watermark(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a watermark to the processed video.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

@step(name="save_video_report")
def save_video_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save the final video report.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    return data

@step(name="damage_tracker")
def damage_tracker(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Track damages across frames.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    logger.info("[main] damage_tracker...")
    return data

@step(name="parts_tracker")
def parts_tracker(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Track parts across frames.

    Args:
        data: The pipeline data dictionary.

    Returns:
        The updated data dictionary.
    """
    logger.info("[main] parts_tracker...")
    return data

def build_and_run_pipeline() -> None:
    """
    Build and execute the test pipeline.
    """
    # Build the pipeline
    pipeline_instance: Pipeline = Pipeline(pipeline_name="test_pipeline")
    pipeline_instance.set_steps([
        check_requirements,
        clean_folder,
        reset_part_model,
        reset_damage_search,
        open_video_capture,
        For(
            validation_expression="process_completed == 0",
            steps=[
                create_batch_frames,
                Condition(
                    expression="active_background_extractor == 1",
                    branch_true=[filter_by_car],
                    branch_false=[],
                ),
                Parallel(
                    steps=[
                        DamageDetector(),  # Damage detector only
                        PartSegmentator(),  # Runs on thread B
                        get_angle,          # Runs on thread C
                    ],
                    max_workers=2,
                ),
                Parallel(
                    steps=[
                        DamageSegmentator(),      # Runs on thread A
                        DamageClasification(),    # Runs on thread B
                        DamageSecondClasification(),  # Runs on thread C
                    ],
                    max_workers=3,
                ),
                add_watermark,
                save_video_report,
            ],
        ),
        Condition(
            expression="tracker_external == 1",
            branch_true=[
                (
                    lambda context: logger.info("[main] damage_tracker..."),
                    "damage_tracker",
                    "v1.0",
                ),
                (
                    lambda context: logger.info("[main] parts_tracker..."),
                    "parts_tracker",
                    "v1.0",
                ),
            ],
            branch_false=[],
        ),
    ])

    # Run the pipeline
    try:
        initial_data: Dict[str, Any] = {}
        result: Dict[str, Any] = pipeline_instance.run(initial_data)
        print("Pipeline executed successfully")
        print("Result:", result)
    except Exception as err: # pylint: disable=broad-exception-caught
        print("Pipeline execution failed with error:", err)
        traceback.print_exc()

if __name__ == "__main__":
    build_and_run_pipeline()
