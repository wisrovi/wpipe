"""
Pipeline module for orchestrating task execution.

This module provides the Pipeline class for managing and executing
a sequence of tasks, with support for conditional branching,
retry logic, and API tracking.
"""

import json
import time
import traceback
from typing import Any, Callable, Optional

from rich.errors import LiveError
from rich.progress import Progress
from tqdm import tqdm

from wpipe.api_client.api_client import APIClient
from wpipe.exception import ApiError, Codes, ProcessError, TaskError
from wpipe.exception.api_error import logger


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

    def __init__(
        self,
        worker_id: Optional[str] = None,
        worker_name: Optional[str] = None,
        api_config: Optional[dict] = None,
        verbose: bool = False,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        retry_on_exceptions: tuple = (Exception,),
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
            elif not (
                isinstance(item, tuple)
                and len(item) == 3
                and callable(item[0])
                and isinstance(item[1], str)
            ):
                raise ValueError(
                    "Each element must be a tuple (function, name, version) "
                    "or a Condition object."
                )
            else:
                new_list.append((item[0], item[1], item[2], ""))

        self.tasks_list = new_list

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
            if self.max_retries > 0:
                return self._execute_with_retry(func, name, *args, **kwargs)

            if isinstance(func, Pipeline):
                return func.run(*args, **kwargs)
            return func(*args, **kwargs)
        except (TaskError, ApiError):
            raise
        except Exception as e:
            raise TaskError(str(e), Codes.TASK_FAILED) from e

    def _run_branch(self, steps: list, data: dict, **kwargs: Any) -> dict:
        """
        Execute a branch of steps.

        Args:
            steps: List of steps to execute.
            data: Initial data dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            Updated data dictionary.
        """
        for item in steps:
            if isinstance(item, Condition):
                branch = item.get_branch(data)
                data = self._run_branch(branch, data, **kwargs)
            else:
                func, name, _, step_id = item
                self.task_name = name
                self.task_id = step_id

                data["progress_rich"] = self.progress_rich
                result = self._task_invoke(func, name, *(data,), **kwargs)

                assert isinstance(result, dict), (
                    f"[ERROR] The result of state ({self.task_name}) must be a dict"
                )

                data.update(result)

                if "error" in data:
                    break

        return data

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
        total_steps = sum(
            1
            for item in self.tasks_list
            if not isinstance(item, Condition) or item.branch_true
        )

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

        for advance_id, progress in progress_bar_generator(size=total_steps):
            if advance_id >= len(self.tasks_list):
                return data

            item = self.tasks_list[advance_id]

            if isinstance(item, Condition):
                if self.verbose:
                    print(f"\n[CONDITION] Evaluating: {item.expression}")
                data = self._run_branch([item], data, **kwargs)
            else:
                func, name, _, step_id = item

                self.task_name = name
                self.task_id = step_id
                self.progress_rich = progress

                data.update(args[0] if args else {})
                data["progress_rich"] = progress

                result_data = self._task_invoke(func, name, *(data,), **kwargs)

                assert isinstance(result_data, dict), (
                    f"[ERROR] The result of state ({self.task_name}) must be a dict"
                )

                data.update(result_data)

                if self.verbose:
                    print()

                if "error" in data:
                    break

        if "error" in data:
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
