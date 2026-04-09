"""
Pipeline module for orchestrating task execution.

This module provides the Pipeline class for managing and executing
a sequence of tasks, with support for conditional branching,
retry logic, API tracking, and execution history tracking.
"""

import json
import os
import time
import traceback
from typing import Any, Callable, Optional

from rich.errors import LiveError
from rich.progress import Progress
from tqdm import tqdm

from wpipe.api_client.api_client import APIClient
from wpipe.exception import ApiError, Codes, ProcessError, TaskError
from wpipe.exception.api_error import logger
from wpipe.tracking import PipelineTracker


def get_system_metrics() -> dict:
    """Get current system metrics."""
    try:
        import psutil

        process = psutil.Process(os.getpid())
        memory = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()

        return {
            "cpu_percent": process.cpu_percent(),
            "memory_percent": memory.percent,
            "memory_used_mb": memory.used / 1024 / 1024,
            "memory_available_mb": memory.available / 1024 / 1024,
            "disk_io_read_mb": (disk_io.read_bytes / 1024 / 1024) if disk_io else 0,
            "disk_io_write_mb": (disk_io.write_bytes / 1024 / 1024) if disk_io else 0,
        }
    except ImportError:
        return {}


class SystemMetricsCollector:
    """Collects system metrics during pipeline execution."""

    def __init__(
        self, tracker: PipelineTracker, pipeline_id: str, interval_seconds: float = 5.0
    ):
        self.tracker = tracker
        self.pipeline_id = pipeline_id
        self.interval = interval_seconds
        self._running = False
        self._thread = None

    def start(self):
        """Start collecting metrics."""
        import threading

        self._running = True
        self._thread = threading.Thread(target=self._collect_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop collecting metrics."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _collect_loop(self):
        """Collection loop."""
        while self._running:
            try:
                metrics = get_system_metrics()
                if metrics:
                    self.tracker.record_system_metrics(self.pipeline_id, metrics)
            except Exception:
                pass
            time.sleep(self.interval)


class Condition:
    """Represents a conditional branch in the pipeline."""

    def __init__(
        self,
        expression: str,
        branch_true: list,
        branch_false: Optional[list] = None,
    ) -> None:
        """
        Initialize a Condition.

        Args:
            expression: The condition expression to evaluate.
            branch_true: Steps to execute if condition is True.
            branch_false: Steps to execute if condition is False.
        """
        self.expression = expression
        self.branch_true = branch_true
        self.branch_false = branch_false or []

    def evaluate(self, data: dict) -> bool:
        """
        Evaluate the condition expression against data.

        Args:
            data: Dictionary containing data for evaluation.

        Returns:
            True if condition is met, False otherwise.
        """
        safe_globals = {"True": True, "False": False, "None": None}
        safe_locals = data.copy()
        try:
            return eval(self.expression, safe_globals, safe_locals)
        except Exception as e:
            raise ValueError(
                f"Invalid condition expression: {self.expression}. Error: {e}"
            ) from e

    def get_branch(self, data: dict) -> list:
        """
        Get the appropriate branch based on evaluation.

        Args:
            data: Dictionary containing data for evaluation.

        Returns:
            List of steps to execute.
        """
        if self.evaluate(data):
            return self.branch_true
        if self.branch_false:
            return self.branch_false
        return []


class For:
    """Represents a loop in the pipeline (conditional or count-based)."""

    def __init__(
        self,
        validation_expression: Optional[str] = None,
        steps: Optional[list] = None,
        iterations: Optional[int] = None,
    ) -> None:
        if not validation_expression and iterations is None:
            raise ValueError(
                "Must provide either 'validation_expression' or 'iterations'"
            )
        self.validation_expression = validation_expression
        self.iterations = iterations
        self.steps = steps or []

    def _evaluate_condition(self, data: dict) -> bool:
        if not self.validation_expression:
            return True
        safe_globals = {"True": True, "False": False, "None": None, "len": len}
        safe_locals = data.copy()
        try:
            return eval(self.validation_expression, safe_globals, safe_locals)
        except Exception as e:
            raise ValueError(
                f"Invalid loop expression: {self.validation_expression}. Error: {e}"
            ) from e


class ProgressManager:
    """Singleton manager for Rich Progress bars."""

    _instance = None

    def __new__(cls):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.progress = Progress()
        return cls._instance

    def __enter__(self):
        """Enter context manager."""
        self.progress.__enter__()
        return self.progress

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.progress.__exit__(exc_type, exc_val, exc_tb)


class Pipeline(APIClient):
    """Pipeline for orchestrating task execution with API tracking support."""

    worker_id: Optional[str] = None
    worker_name: str = "worker"
    verbose: bool = False
    task_id: Optional[str] = None

    process_id: Optional[str] = None
    send_to_api: bool = False
    api_config: Optional[dict] = None
    tasks_list: list = []

    SHOW_API_ERRORS = False

    task_name: str = "Processing pipeline tasks"
    progress_rich: Optional[Progress] = None

    max_retries: int = 0
    retry_delay: float = 1.0
    retry_on_exceptions: tuple = (Exception,)

    # Tracking
    tracker: Optional[PipelineTracker] = None
    pipeline_name: str = "Pipeline"
    pipeline_id: Optional[str] = None
    _step_order: int = 0
    _step_ids: dict = {}
    _metrics_collector: Optional[SystemMetricsCollector] = None
    parent_pipeline_id: Optional[str] = None

    def __init__(
        self,
        worker_id: Optional[str] = None,
        worker_name: Optional[str] = None,
        api_config: Optional[dict] = None,
        verbose: bool = False,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        retry_on_exceptions: tuple = (Exception,),
        tracking_db: Optional[str] = None,
        pipeline_name: Optional[str] = None,
        config_dir: Optional[str] = None,
        parent_pipeline_id: Optional[str] = None,
        collect_system_metrics: bool = False,
        continue_on_error: bool = True,
    ) -> None:
        """
        Initialize the Pipeline.

        Args:
            worker_id: Unique identifier for this worker.
            worker_name: Human-readable name for the worker.
            api_config: Configuration for API tracking.
            verbose: Enable verbose output.
            max_retries: Maximum retry attempts for failed tasks.
            retry_delay: Delay between retries in seconds.
            retry_on_exceptions: Tuple of exception types to retry on.
            tracking_db: Path to SQLite database for execution tracking.
            pipeline_name: Name for the pipeline (used in tracking).
            config_dir: Directory to store YAML configuration files.
            parent_pipeline_id: Parent pipeline ID for relationship tracking.
            collect_system_metrics: Enable system metrics collection during execution.
            continue_on_error: Continue pipeline execution after errors (captures error in result).
        """
        if api_config:
            super().__init__(
                base_url=api_config.get("base_url"),
                token=api_config.get("token"),
            )
            self.api_config = api_config

        if worker_id:
            self.set_worker_id(worker_id)

        if worker_name:
            self.worker_name = worker_name

        self.verbose = verbose
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_on_exceptions = retry_on_exceptions
        self.parent_pipeline_id = parent_pipeline_id
        self._collect_system_metrics = collect_system_metrics
        self.continue_on_error = continue_on_error

        # Initialize tracking if database path provided
        if tracking_db:
            self.tracker = PipelineTracker(tracking_db, config_dir)

        self.pipeline_name = pipeline_name or "Pipeline"

    def add_event(
        self,
        event_type: str,
        event_name: str,
        message: Optional[str] = None,
        data: Optional[dict] = None,
        tags: Optional[list] = None,
    ):
        """Add an event/annotation to the current pipeline."""
        if self.tracker and self.pipeline_id:
            self.tracker.add_event(
                pipeline_id=self.pipeline_id,
                event_type=event_type,
                event_name=event_name,
                message=message,
                data=data,
                tags=tags,
            )

    def link_to_pipeline(self, other_pipeline_id: str, relation_type: str = "related"):
        """Create a relationship to another pipeline."""
        if self.tracker and self.pipeline_id:
            self.tracker.link_pipelines(
                parent_id=self.pipeline_id,
                child_id=other_pipeline_id,
                relation_type=relation_type,
            )

    def set_worker_id(self, worker_id: str) -> None:
        """
        Set the worker ID.

        Args:
            worker_id: The worker ID to set.

        Raises:
            TypeError: If worker_id is not a string.
            ValueError: If worker_id is too short (must be > 5 chars).
        """
        if not isinstance(worker_id, str):
            raise TypeError(f"worker_id must be a string, got {type(worker_id)}")

        if len(worker_id) > 5:
            if self.api_config and not self.worker_id:
                self.send_to_api = True
                print("[INFO] worker_id defined correct")
            self.worker_id = worker_id
        else:
            self.worker_id = None

    def worker_register(self, name: str, version: str) -> Optional[dict]:
        """
        Register the worker with the API.

        Args:
            name: Worker name.
            version: Worker version.

        Returns:
            Worker registration data if successful, None otherwise.
        """
        data = {
            "name": name,
            "version": version,
            "tasks": [
                {
                    "name": name,
                    "version": version,
                }
                for func, step_name, step_version, _step_id in self.tasks_list
            ],
        }

        if self.api_config:
            worker_data = self.register_worker(data)

            if worker_data and "id" in worker_data:
                self.set_worker_id(worker_data.get("id"))
                return worker_data
        return None

    def _api_task_update(self, msg: dict) -> None:
        """Update task status via API."""
        if self.send_to_api:
            try:
                task_updated = self.update_task(msg)
                if self.verbose:
                    print(f"[task] [ERROR] '{self.task_name}': {task_updated}")
            except Exception as exc:  # noqa: BLE001
                print("Problem update task")
                if self.SHOW_API_ERRORS:
                    raise ApiError("Problem update task", Codes.UPDATE_TASK) from exc

    def _api_process_update(self, msg: dict, start: bool = False) -> None:
        """Update process status via API."""
        if self.send_to_api:
            try:
                if start:
                    process_registered = self.register_process(msg)

                    self.tasks_list = [
                        (rta[0], rta[1], rta[2], son["id"])
                        for son, rta in zip(process_registered["sons"], self.tasks_list)
                    ]

                    self.process_id = process_registered["father"]

                    if self.verbose:
                        print(
                            "\t",
                            f"[INFO] [START] pipeline: new process ({self.process_id})",
                        )
                else:
                    status = self.end_process(msg)

                    if not status:
                        if self.verbose:
                            print("\t", f"[INFO] [END] pipeline: {status}")
                        if self.SHOW_API_ERRORS:
                            raise ApiError("API problem", Codes.UPDATE_PROCESS_OK)
            except Exception as exc:  # noqa: BLE001
                print("Problem update Process")
                if self.SHOW_API_ERRORS:
                    raise ApiError(
                        "Problem update Process", Codes.UPDATE_PROCESS_ERROR
                    ) from exc

    def _task_invoke_with_report(
        self, func: Callable, *args: Any, **kwargs: Any
    ) -> dict:
        """
        Invoke a task with API reporting.

        Args:
            func: Function to invoke.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Result dictionary from the function.
        """
        self._api_task_update({"task_id": self.task_id, "status": "start"})

        result = {}
        try:
            if isinstance(func, Pipeline):
                result = func.run(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            self._api_task_update({"task_id": self.task_id, "status": "success"})
        except Exception as e:
            errors_tb = traceback.extract_tb(e.__traceback__)

            errors_list = []
            for error_traceback in errors_tb:
                errors_list.append(
                    {
                        "file": error_traceback.filename,
                        "line": error_traceback.lineno,
                        "method": error_traceback.name,
                    }
                )

            error_info = {
                "task_name": self.task_name,
                "error_traceback": errors_list,
                "error_message": str(e),
                "task_id": self.task_id,
            }

            result["error"] = error_info["error_message"]

            self._api_task_update(
                {
                    "task_id": self.task_id,
                    "status": "error",
                    "details": json.dumps(error_info),
                }
            )

            if self.verbose:
                for error in errors_list:
                    logger.error(error)

            raise TaskError(error_info, Codes.TASK_FAILED) from e

        return result

    def _pipeline_run_with_report(self, *args: Any, **kwargs: Any) -> dict:
        """
        Run the pipeline with API reporting.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Result dictionary from the pipeline.
        """
        worker_id = self.worker_id

        if self.verbose:
            print("\n", "\t", "*" * 50)
            print("\n", f"\t [WORKER] {self.worker_id}")
            print("\n\t", "*" * 50)

        self._api_process_update({"id": worker_id}, start=True)

        result = {}
        try:
            result = self._pipeline_run(*args, **kwargs)

            self._api_process_update({"id": self.process_id, "details": ""})
        except TaskError as te:
            error = {
                "message": str(te),
                "error_code": te.error_code,
                "process_name": self.process_id,
                "worker_id": self.worker_id,
                "worker_name": self.worker_name or "worker",
                "task_name": self.task_name,
                "task_id": self.task_id,
            }

            self._api_process_update(
                {"id": self.process_id, "details": json.dumps(error)}
            )

            if self.continue_on_error:
                result["error"] = error
                return result

            raise ProcessError(str(te), Codes.TASK_FAILED) from te
        except ApiError as ae:
            raise ApiError(str(ae), Codes.API_ERROR) from ae

        return result

    def set_steps(self, steps: list) -> None:
        """
        Set the pipeline steps.

        Args:
            steps: List of steps (tuples or Conditions).

        Raises:
            ValueError: If step format is invalid.
        """
        new_list = []

        def normalize_step(step: tuple) -> tuple:
            """Normalize a step tuple to 4 elements."""
            if isinstance(step, tuple) and len(step) == 3 and callable(step[0]):
                return (step[0], step[1], step[2], "")
            return step

        for item in steps:
            if isinstance(item, Condition):
                normalized_true = [normalize_step(s) for s in item.branch_true]
                normalized_false = [
                    normalize_step(s) for s in (item.branch_false or [])
                ]
                condition = Condition(
                    expression=item.expression,
                    branch_true=normalized_true,
                    branch_false=normalized_false,
                )
                new_list.append(condition)
            elif isinstance(item, For):
                normalized_steps = [normalize_step(s) for s in item.steps]
                new_list.append(
                    For(
                        validation_expression=item.validation_expression,
                        iterations=item.iterations,
                        steps=normalized_steps,
                    )
                )
            elif callable(item):
                name = getattr(item, "NAME", None) or getattr(
                    item, "__name__", "unknown"
                )
                version = getattr(item, "VERSION", "v1.0") or "v1.0"
                new_list.append((item, name, version, ""))
            elif not (
                isinstance(item, tuple)
                and len(item) == 3
                and callable(item[0])
                and isinstance(item[1], str)
            ):
                raise ValueError(
                    "Each element must be a tuple (function, name, version), "
                    "a Condition object, a For object, or a callable (e.g., @state decorated function)."
                )
            else:
                new_list.append((item[0], item[1], item[2], ""))

        self.tasks_list = new_list

    def add_state(
        self,
        name: str,
        func: Callable = None,
        version: str = "",
        state: Callable = None,
        depends_on=None,
        timeout=None,
        **kwargs,
    ) -> None:
        """
        Add a single step to the pipeline (Phase 2 compatibility method).

        This is a convenience wrapper around set_steps() for adding steps
        one at a time. Maintains backward compatibility with Phase 2 code.

        Args:
            name: Step name identifier.
            func: Callable function for the step (alternative: use 'state' parameter).
            version: Optional version string (default: "").
            state: Alternative parameter name for the function (for compatibility).
            depends_on: Optional list of dependencies (note: currently ignored).
            timeout: Optional timeout (note: currently ignored).
            **kwargs: Additional keyword arguments (for future compatibility).
        """
        # Support both 'func' and 'state' parameter names
        step_func = func or state
        if step_func is None:
            raise ValueError("Either 'func' or 'state' parameter must be provided")

        current_steps = list(self.tasks_list) if hasattr(self, "tasks_list") else []

        # Convert 4-tuple elements to 3-tuple (strip the 4th empty string added by set_steps)
        current_steps = [
            (s[0], s[1], s[2]) if len(s) == 4 else s for s in current_steps
        ]

        # Convert to 3-tuple format (function, name, version)
        new_step = (step_func, name, version)
        current_steps.append(new_step)
        self.set_steps(current_steps)

    @property
    def steps(self):
        """Property to access steps for Phase 2 compatibility."""

        # Create step objects for compatibility
        class Step:
            def __init__(self, func, name, version=""):
                self.func = func
                self.name = name
                self.version = version

            def run(self, context):
                return self.func(context)

        result = []
        for item in self.tasks_list:
            if isinstance(item, tuple) and len(item) >= 2:
                result.append(Step(item[0], item[1], item[2] if len(item) > 2 else ""))
        return result

    def _execute_with_retry(
        self, func: Callable, name: str, *args: Any, **kwargs: Any
    ) -> Any:
        """
        Execute a function with retry logic.

        Args:
            func: Function to execute.
            name: Function name for logging.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Result from function execution.

        Raises:
            Exception: The last exception if all retries fail.
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                if isinstance(func, Pipeline):
                    return func.run(*args, **kwargs)
                return func(*args, **kwargs)
            except self.retry_on_exceptions as e:
                last_exception = e
                if attempt < self.max_retries:
                    if self.verbose:
                        print(
                            f"[RETRY] {name} failed "
                            f"(attempt {attempt + 1}/{self.max_retries + 1}): {e}"
                        )
                        print(
                            f"[RETRY] Waiting {self.retry_delay}s "
                            "before next attempt..."
                        )
                    time.sleep(self.retry_delay)
                else:
                    if self.verbose:
                        print(
                            f"[RETRY] {name} failed "
                            f"after {self.max_retries + 1} attempts"
                        )

        raise last_exception

    def _task_invoke(self, func: Callable, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Invoke a task, optionally with retry logic.

        Args:
            func: Function to invoke.
            name: Function name.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Result from function.

        Raises:
            TaskError: If the task raises an exception.
        """
        try:
            if self.send_to_api:
                return self._task_invoke_with_report(func, *args, **kwargs)

            if self.max_retries > 0:
                return self._execute_with_retry(func, name, *args, **kwargs)

            if isinstance(func, Pipeline):
                return func.run(*args, **kwargs)
            return func(*args, **kwargs)
        except (TaskError, ApiError):
            raise
        except Exception as e:
            raise TaskError(str(e), Codes.TASK_FAILED) from e

    def _execute_for_inline(self, item: "For", data: dict) -> dict:
        loop_data = data.copy()
        loop_data.pop("progress_rich", None)

        iteration = 0
        while True:
            if item.validation_expression:
                if not item._evaluate_condition(loop_data):
                    break

            if item.iterations is not None and iteration >= item.iterations:
                break

            for step in item.steps:
                if isinstance(step, For):
                    loop_data = self._execute_for_inline(step, loop_data)
                elif isinstance(step, tuple) and len(step) >= 3:
                    func, step_name, step_version, _ = step
                    try:
                        result = func(loop_data)
                        if isinstance(result, dict):
                            loop_data.update(result)
                    except Exception as e:
                        loop_data["error"] = str(e)
                        break

                    if "error" in loop_data:
                        break
                else:
                    continue

            if "error" in loop_data:
                break

            iteration += 1
            loop_data["_loop_iteration"] = iteration

        return loop_data

    def _run_branch(self, steps: list, data: dict, **kwargs: Any) -> tuple[dict, list]:
        """
        Execute a branch of steps.

        Args:
            steps: List of steps to execute.
            data: Initial data dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            Tuple of (updated data dictionary, list of executed step IDs).
        """
        executed_step_ids = []

        for item in steps:
            if isinstance(item, Condition):
                cond_name = getattr(item, "name", "condition") or "condition"
                cond_expr = getattr(item, "expression", "unknown")
                true_branch = item.branch_true or []
                false_branch = item.branch_false or []

                branch_taken = "true" if item.evaluate(data) else "false"
                branch_executed = (
                    true_branch if branch_taken == "true" else false_branch
                )
                branch_skipped = false_branch if branch_taken == "true" else true_branch

                true_branch_ids = []
                false_branch_ids = []
                skipped_branch_ids = []
                cond_step_id = None

                if self.tracker and self.pipeline_id:
                    self._step_order += 1
                    cond_step_id = self.tracker.start_step(
                        pipeline_id=self.pipeline_id,
                        step_order=self._step_order,
                        step_name=cond_name,
                        step_version="1.0.0",
                        step_type="condition",
                        input_data={
                            "expression": cond_expr,
                            "true_branch": [
                                s[1] if isinstance(s, tuple) else str(s)
                                for s in true_branch
                                if not isinstance(s, Condition)
                            ],
                            "false_branch": [
                                s[1] if isinstance(s, tuple) else str(s)
                                for s in false_branch
                                if not isinstance(s, Condition)
                            ],
                        },
                    )

                data, branch_ids = self._run_branch(branch_executed, data, **kwargs)

                if branch_taken == "true":
                    true_branch_ids = branch_ids
                    false_branch_ids = []
                    skipped_branch_names = [
                        self._get_step_name(s)
                        for s in branch_skipped
                        if not isinstance(s, Condition)
                    ]
                else:
                    false_branch_ids = branch_ids
                    true_branch_ids = []
                    skipped_branch_names = [
                        self._get_step_name(s)
                        for s in branch_skipped
                        if not isinstance(s, Condition)
                    ]

                executed_step_ids.append(cond_step_id)
                executed_step_ids.extend(branch_ids)

                if cond_step_id and self.tracker:
                    self.tracker.complete_step(
                        cond_step_id,
                        output_data={
                            "branch_taken": branch_taken,
                            "expression": cond_expr,
                            "true_branch_ids": true_branch_ids,
                            "false_branch_ids": false_branch_ids,
                            "skipped_branch_names": skipped_branch_names,
                        },
                    )

            elif callable(item):
                func, name, version = item
                step_id = None
                self.task_name = name
                self.task_id = step_id

                # Start step tracking
                tracked_step_id = self._start_step_tracking(name, version, "task", data)

                data["progress_rich"] = self.progress_rich
                error_msg = None
                error_trace = None
                try:
                    result = self._task_invoke(func, name, *(data,), **kwargs)

                    assert isinstance(result, dict), (
                        f"[ERROR] The result of state ({self.task_name}) must be a dict"
                    )

                    data.update(result)
                except Exception as e:
                    error_msg = str(e)
                    error_trace = traceback.format_exc()
                    raise
                finally:
                    self._end_step_tracking(
                        tracked_step_id, data, error_msg, error_trace
                    )

                if tracked_step_id:
                    executed_step_ids.append(tracked_step_id)

                if "error" in data:
                    break
            else:
                try:
                    func, name, version, step_id = item
                except ValueError:
                    try:
                        func, name, version = item
                        step_id = None
                    except ValueError:
                        raise ValueError(
                            f"Invalid step format: {item}. Expected (func, name, version) or (func, name, version, step_id)"
                        )
                self.task_name = name
                self.task_id = step_id

                # Start step tracking
                tracked_step_id = self._start_step_tracking(name, version, "task", data)

                data["progress_rich"] = self.progress_rich
                error_msg = None
                error_trace = None
                try:
                    result = self._task_invoke(func, name, *(data,), **kwargs)

                    assert isinstance(result, dict), (
                        f"[ERROR] The result of state ({self.task_name}) must be a dict"
                    )

                    data.update(result)
                except Exception as e:
                    error_msg = str(e)
                    error_trace = traceback.format_exc()
                    raise
                finally:
                    self._end_step_tracking(
                        tracked_step_id, data, error_msg, error_trace
                    )

                if tracked_step_id:
                    executed_step_ids.append(tracked_step_id)

                if "error" in data:
                    break

        return data, executed_step_ids

    def _get_step_name(self, step) -> Optional[str]:
        """Get step name from step tuple or callable."""
        if isinstance(step, tuple) and len(step) >= 2:
            return step[1] if isinstance(step[1], str) else None
        elif callable(step):
            return step.__name__ if hasattr(step, "__name__") else None
        return None

    def _start_step_tracking(
        self,
        name: str,
        version: Optional[str] = None,
        step_type: str = "task",
        input_data: Optional[dict] = None,
    ) -> Optional[int]:
        """Start tracking a step execution."""
        if not self.tracker or not self.pipeline_id:
            return None

        self._step_order += 1

        # Filter out internal keys from input data
        filtered_input = {
            k: v
            for k, v in (input_data or {}).items()
            if k not in ("progress_rich",) and not callable(v)
        }

        step_id = self.tracker.start_step(
            pipeline_id=self.pipeline_id,
            step_order=self._step_order,
            step_name=name,
            step_version=version,
            step_type=step_type,
            input_data=filtered_input,
        )
        return step_id

    def _end_step_tracking(
        self,
        step_id: Optional[int],
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_traceback: Optional[str] = None,
    ):
        """End tracking a step execution."""
        if not self.tracker or not step_id:
            return

        # Filter out internal keys from output data
        filtered_output = None
        if output_data:
            filtered_output = {
                k: v
                for k, v in output_data.items()
                if k not in ("progress_rich", "error") and not callable(v)
            }

        self.tracker.complete_step(
            step_id=step_id,
            output_data=filtered_output,
            error_message=error_message,
            error_traceback=error_traceback,
        )

    def _pipeline_run(self, *args: Any, **kwargs: Any) -> dict:
        """
        Internal pipeline run implementation.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Result dictionary from pipeline execution.
        """
        result_data = {}
        data = {}
        error_message = None
        error_step = None
        metrics_collector = None

        # Register pipeline with tracking system (matrícula)
        if self.tracker:
            registration = self.tracker.register_pipeline(
                name=self.pipeline_name,
                steps=self.tasks_list,
                input_data=args[0] if args else None,
                worker_id=self.worker_id,
                worker_name=self.worker_name,
                parent_pipeline_id=self.parent_pipeline_id,
            )
            self.pipeline_id = registration["pipeline_id"]
            self._step_order = 0
            self._step_ids = {}

            if self.verbose:
                print(f"\n[MATRÍCULA] Pipeline registered: {self.pipeline_id}")
                print(f"[MATRÍCULA] Config YAML: {registration['yaml_path']}")
                if self.parent_pipeline_id:
                    print(f"[MATRÍCULA] Parent pipeline: {self.parent_pipeline_id}")

            # Start system metrics collection
            if self._collect_system_metrics:
                metrics_collector = SystemMetricsCollector(
                    self.tracker, self.pipeline_id
                )
                metrics_collector.start()
                if self.verbose:
                    print("[METRICS] System metrics collection started")

        total_steps = len(self.tasks_list)

        def progress_bar_generator(size: int):
            """Generate progress bar updates."""
            try:
                advance_id = 0
                progress_manager = ProgressManager()

                with progress_manager as progress_rich_instance:
                    self.progress_rich = progress_rich_instance

                    task = progress_rich_instance.add_task(
                        f"[cyan][{self.worker_name}]{self.task_name}",
                        total=size,
                    )
                    while not progress_rich_instance.finished:
                        yield advance_id, progress_rich_instance

                        advance_id += 1
                        progress_rich_instance.update(task, advance=1)
            except LiveError:
                for advance_id in tqdm(
                    range(size),
                    desc=f"{self.task_name}",
                    unit="steps",
                ):
                    yield advance_id, None

        try:
            for advance_id, progress in progress_bar_generator(size=total_steps):
                if advance_id >= len(self.tasks_list):
                    break

                item = self.tasks_list[advance_id]

                if isinstance(item, Condition):
                    if self.verbose:
                        print(f"\n[CONDITION] Evaluating: {item.expression}")
                    data, _ = self._run_branch([item], data, **kwargs)
                elif isinstance(item, For):
                    loop_data = data.copy()
                    loop_data.pop("progress_rich", None)
                    loop_data.update(args[0] if args else {})

                    iteration = 0
                    while True:
                        if item.validation_expression:
                            if not item._evaluate_condition(loop_data):
                                break

                        if item.iterations is not None and iteration >= item.iterations:
                            break

                        for step in item.steps:
                            if isinstance(step, For):
                                loop_data = self._execute_for_inline(step, loop_data)
                            elif isinstance(step, tuple) and len(step) >= 3:
                                func, step_name, step_version, _ = step
                                try:
                                    result = func(loop_data)
                                    if isinstance(result, dict):
                                        loop_data.update(result)
                                except Exception as e:
                                    loop_data["error"] = str(e)
                                    break

                                if "error" in loop_data:
                                    break
                            elif callable(step):
                                try:
                                    result = step(loop_data)
                                    if isinstance(result, dict):
                                        loop_data.update(result)
                                except Exception as e:
                                    loop_data["error"] = str(e)
                                    break

                                if "error" in loop_data:
                                    break
                            else:
                                continue

                        if "error" in loop_data:
                            break

                        iteration += 1
                        loop_data["_loop_iteration"] = iteration

                    data.update(loop_data)
                    data.pop("progress_rich", None)
                else:
                    func, name, version, step_id = item

                    self.task_name = name
                    self.task_id = step_id
                    self.progress_rich = progress

                    data.update(args[0] if args else {})
                    data["progress_rich"] = progress

                    # Start step tracking
                    tracked_step_id = self._start_step_tracking(
                        name, version, "task", data
                    )

                    step_error = None
                    step_error_traceback = None
                    try:
                        result_data = self._task_invoke(func, name, *(data,), **kwargs)

                        assert isinstance(result_data, dict), (
                            f"[ERROR] The result of state ({self.task_name}) must be a dict"
                        )

                        data.update(result_data)
                    except Exception as e:
                        step_error = str(e)
                        step_error_traceback = traceback.format_exc()
                        if self.continue_on_error:
                            data["error"] = step_error
                            data["_step_error"] = step_error
                            data["_step_error_traceback"] = step_error_traceback
                            continue
                        raise
                    finally:
                        # Complete step tracking with output
                        self._end_step_tracking(
                            tracked_step_id,
                            data if not step_error else None,
                            step_error,
                            step_error_traceback,
                        )

                    if self.verbose:
                        print()

                    if "error" in data:
                        error_message = data.get("error")
                        error_step = name
                        if not self.continue_on_error:
                            break
        except Exception as e:
            error_message = str(e)
            error_step = self.task_name
            if not self.continue_on_error:
                raise
            if self.verbose:
                print(f"\n[ERROR] {error_step}: {error_message}")
                print(
                    "[CONTINUING] Pipeline will continue due to continue_on_error=True"
                )
        finally:
            # Stop metrics collection
            if metrics_collector:
                metrics_collector.stop()
                if self.verbose:
                    print("[METRICS] System metrics collection stopped")

            # Complete pipeline tracking
            if self.tracker and self.pipeline_id:
                try:
                    self.tracker.complete_pipeline(
                        pipeline_id=self.pipeline_id,
                        output_data=data if not error_message else None,
                        error_message=error_message,
                        error_step=error_step,
                    )

                    if self.verbose:
                        status = "ERROR" if error_message else "COMPLETED"
                        print(f"\n[MATRÍCULA] Pipeline {self.pipeline_id}: {status}")
                except Exception:
                    pass  # Don't fail pipeline due to tracking errors

        if "error" in data and not self.continue_on_error:
            raise TaskError(
                f"[{self.task_name}] Fail the pipeline:{data['error']}",
                Codes.TASK_FAILED,
            )

        data.pop("progress_rich", None)

        return data

    def run(self, *args: Any, **kwargs: Any) -> dict:
        """
        Execute the pipeline.

        Args:
            *args: Initial data dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            Result dictionary from pipeline execution.

        Raises:
            TaskError: If a task fails.
        """
        if "error" in (args[0] if args else {}):
            raise TaskError(
                f"[{self.task_name}] Initial data contains error",
                Codes.TASK_FAILED,
            )

        return self._pipeline_run_with_report(*args, **kwargs)
