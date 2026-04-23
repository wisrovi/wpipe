"""
Pipeline module for orchestrating task execution.

This module provides the Pipeline class for managing and executing
a sequence of tasks, with support for conditional branching,
retry logic, API tracking, and execution history tracking.
"""

import inspect
import json
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from wpipe.api_client.api_client import APIClient
from wpipe.exception import ApiError, Codes, ProcessError, TaskError
from wpipe.exception.api_error import logger
from wpipe.tracking import PipelineTracker
from wpipe.util.utils import clean_for_json

from .components.logic_blocks import Condition, For, Parallel
from .components.metrics import SystemMetricsCollector
from .components.progress import ProgressManager


class Pipeline(APIClient):
    """
    Pipeline for orchestrating task execution with API tracking support.

    Attributes:
        worker_id (Optional[str]): Unique identifier for the worker.
        worker_name (str): Name of the worker.
        verbose (bool): Whether to enable verbose logging.
        tasks_list (List[Any]): List of steps/tasks to execute.
        pipeline_name (str): Name of the pipeline.
        tracker (Optional[PipelineTracker]): Tracker for execution history.
    """

    # pylint: disable=too-many-instance-attributes
    worker_id: Optional[str] = None
    worker_name: str = "worker"
    verbose: bool = False
    task_id: Optional[str] = None

    process_id: Optional[str] = None
    send_to_api: bool = False
    api_config: Optional[Dict[str, Any]] = None
    tasks_list: List[Any] = []

    SHOW_API_ERRORS = False

    task_name: str = "Processing pipeline tasks"
    progress_rich: Optional["Progress"] = None

    max_retries: int = 0
    retry_delay: float = 1.0
    retry_on_exceptions: Tuple[type, ...] = (Exception,)
    show_progress: bool = True

    # Tracking
    _tracker: Optional[Any] = None
    
    @property
    def tracker(self) -> Any:
        if self._tracker is None and getattr(self, "tracking_db", None):
            from wpipe.tracking import PipelineTracker
            self._tracker = PipelineTracker(self.tracking_db)
        return self._tracker
        
    @tracker.setter
    def tracker(self, value: Any) -> None:
        self._tracker = value
    pipeline_name: str = "Pipeline"
    pipeline_id: Optional[str] = None
    _step_order: int = 0
    _step_ids: Dict[str, Any] = {}
    _metrics_collector: Optional[SystemMetricsCollector] = None
    parent_pipeline_id: Optional[str] = None

    def __init__(
        self,
        worker_id: Optional[str] = None,
        worker_name: Optional[str] = None,
        api_config: Optional[Dict[str, Any]] = None,
        verbose: bool = False,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        retry_on_exceptions: Tuple[type, ...] = (Exception,),
        tracking_db: Optional[str] = None,
        pipeline_name: Optional[str] = None,
        config_dir: Optional[str] = None,
        parent_pipeline_id: Optional[str] = None,
        collect_system_metrics: bool = False,
        continue_on_error: bool = False,
        show_progress: bool = True,
    ) -> None:
        """
        Initialize the Pipeline.

        Args:
            worker_id: Unique identifier for the worker.
            worker_name: Human-readable name for the worker.
            api_config: Configuration for API tracking.
            verbose: Enable detailed output.
            max_retries: Default number of retries for failed tasks.
            retry_delay: Delay between retries in seconds.
            retry_on_exceptions: Exceptions that trigger a retry.
            tracking_db: Path to the SQLite database for tracking.
            pipeline_name: Name of this pipeline instance.
            config_dir: Directory containing configuration files.
            parent_pipeline_id: ID of the parent pipeline if nested.
            collect_system_metrics: Whether to collect resource usage.
            continue_on_error: Whether to proceed if a step fails.
            show_progress: Whether to show a progress bar.
        """
        # pylint: disable=too-many-arguments
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
        self.show_progress = show_progress
        self.tracking_db = tracking_db

        # Internal queues for events and post-run tasks
        self._pending_events: List[Dict[str, Any]] = []
        self._post_run_tasks: List[Any] = []
        self._checkpoints: List[Dict[str, Any]] = []
        self._error_capture_tasks: List[Any] = []

        # Initialize tracking if database path provided
        if tracking_db:
            self.tracker = PipelineTracker(tracking_db, config_dir)

        self.pipeline_name = pipeline_name or "Pipeline"

    def add_event(
        self,
        event_type: str,
        event_name: str,
        message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        steps: Optional[List[Any]] = None,
    ) -> "Pipeline":
        """
        Add an event/annotation to the pipeline.

        Args:
            event_type: Category of the event.
            event_name: Name of the event.
            message: Descriptive message.
            data: Additional metadata.
            tags: Categorization tags.
            steps: Steps to run after the current execution.

        Returns:
            Pipeline: Current pipeline instance for chaining.
        """
        event_info = {
            "event_type": event_type,
            "event_name": event_name,
            "message": message,
            "data": data,
            "tags": tags,
        }

        if self.tracker and self.pipeline_id:
            self.tracker.add_event(pipeline_id=self.pipeline_id, **event_info)
        else:
            self._pending_events.append(event_info)

        if steps:
            self._post_run_tasks.extend(steps)

        return self

    def add_checkpoint(
        self,
        checkpoint_name: str,
        expression: str = "True",
        steps: Optional[List[Any]] = None,
    ) -> "Pipeline":
        """
        Add a checkpoint that triggers when expression is True.

        Args:
            checkpoint_name: Name of the checkpoint.
            expression: Python expression to evaluate against context data.
            steps: List of steps to execute when this checkpoint is reached.

        Returns:
            Pipeline: Current pipeline instance for chaining.
        """
        self._checkpoints.append(
            {
                "name": checkpoint_name,
                "expression": expression,
                "steps": steps or [],
                "fired": False,
            }
        )
        return self

    def _evaluate_checkpoints(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate and fire checkpoints based on current data."""
        for cp in self._checkpoints:
            if not cp["fired"]:
                safe_globals: Dict[str, Any] = {
                    "True": True,
                    "False": False,
                    "None": None,
                    "__builtins__": {}
                }
                try:
                    if eval(cp["expression"], safe_globals, data):  # pylint: disable=eval-used
                        if self.verbose:
                            print(f"\n[CHECKPOINT REACHED] {cp['name']}")

                        # Register event with simple retry for SQLite stability
                        max_db_tries = 3
                        for db_try in range(max_db_tries):
                            try:
                                self.add_event(
                                    event_type="checkpoint",
                                    event_name=cp["name"],
                                    message=f"Checkpoint reached: {cp['name']}",
                                )
                                break
                            except Exception:  # pylint: disable=broad-exception-caught
                                if db_try == max_db_tries - 1:
                                    raise
                                time.sleep(0.05)

                        # Execute associated steps
                        for step_item in cp["steps"]:
                            data = self._execute_step(step_item, data)

                        cp["fired"] = True
                except (NameError, SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
                    if self.verbose:
                        print(f"[CHECKPOINT INFO] Milestone '{cp['name']}' skip/busy: {e}")
        return data

    def add_error_capture(self, steps: List[Any]) -> "Pipeline":
        """
        Add steps to execute when an error occurs in the pipeline.

        Args:
            steps: List of steps for error handling.

        Returns:
            Pipeline: Current pipeline instance for chaining.
        """
        self.continue_on_error = True
        self._error_capture_tasks.extend(steps)
        return self

    def _execute_error_capture(self, data: Dict[str, Any], error_info: Dict[str, Any]) -> Dict[str, Any]:
        """Execute error capture steps safely."""
        if not self._error_capture_tasks:
            return data

        if self.verbose:
            print(f"\n[ERROR CAPTURE] Processing error in state '{error_info['step_name']}'...")

        for task in self._error_capture_tasks:
            try:
                func = task[0] if isinstance(task, tuple) else task
                name = (
                    task[1]
                    if isinstance(task, tuple)
                    else (
                        getattr(func, "NAME", None)
                        or getattr(func, "__name__", "error_handler")
                    )
                )

                sig = inspect.signature(func)
                if len(sig.parameters) >= 2:
                    data = self._task_invoke(func, name, data, error_info)
                else:
                    data = self._task_invoke(func, name, data)
            except Exception as e:  # pylint: disable=broad-exception-caught
                if self.verbose:
                    print(f"[ERROR CAPTURE FAILED] {e}")

        return data

    def _execute_post_run_tasks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute post-run tasks safely."""
        if not self._post_run_tasks:
            return data

        if self.verbose:
            print("\n[HOOKS] Executing post-run tasks...")

        for task in self._post_run_tasks:
            try:
                data = self._execute_step(task, data)
            except Exception as e:  # pylint: disable=broad-exception-caught
                if self.verbose:
                    print(f"[HOOK ERROR] Task failed: {e}")

        return data

    def link_to_pipeline(self, other_pipeline_id: str, relation_type: str = "related") -> None:
        """Create a relationship to another pipeline."""
        if self.tracker and self.pipeline_id:
            self.tracker.link_pipelines(
                parent_id=self.pipeline_id,
                child_id=other_pipeline_id,
                relation_type=relation_type,
            )

    def set_worker_id(self, worker_id: str) -> "Pipeline":
        """Set the worker ID."""
        if not isinstance(worker_id, str):
            raise TypeError(f"worker_id must be a string, got {type(worker_id)}")

        if len(worker_id) > 5:
            if self.api_config and not self.worker_id:
                self.send_to_api = True
                if self.verbose:
                    print("[INFO] worker_id defined correctly")
            self.worker_id = worker_id
        else:
            self.worker_id = None

        return self

    def worker_register(self, name: str, version: str) -> Optional[Dict[str, Any]]:
        """Register the worker with the API."""
        data = {
            "name": name,
            "version": version,
            "tasks": [
                {
                    "name": getattr(s[0], "NAME", s[1]),
                    "version": getattr(s[0], "VERSION", s[2]),
                }
                for s in self.tasks_list if isinstance(s, tuple)
            ],
        }

        if self.api_config:
            worker_data = self.register_worker(data)
            if worker_data and "id" in worker_data:
                self.set_worker_id(worker_data.get("id"))
                return worker_data
        return None

    def _api_task_update(self, msg: Dict[str, Any]) -> None:
        """Update task status via API."""
        if self.send_to_api:
            try:
                task_updated = self.update_task(msg)
                if self.verbose:
                    print(f"[task] Status update: {task_updated}")
            except Exception as exc:
                if self.SHOW_API_ERRORS:
                    raise ApiError("Problem updating task", Codes.UPDATE_TASK) from exc
                print("Problem updating task")

    def _api_process_update(self, msg: Dict[str, Any], start: bool = False) -> None:
        """Update process status via API."""
        if self.send_to_api:
            try:
                if start:
                    process_registered = self.register_process(msg)
                    updated_tasks = []
                    for son, rta in zip(process_registered.get("sons", []), self.tasks_list):
                        if isinstance(rta, tuple):
                            updated_tasks.append((rta[0], rta[1], rta[2], son.get("id")))
                        else:
                            updated_tasks.append(rta)
                    self.tasks_list = updated_tasks
                    self.process_id = process_registered.get("father")

                    if self.verbose:
                        print(f"[INFO] [START] pipeline: new process ({self.process_id})")
                else:
                    status = self.end_process(msg)
                    if not status:
                        if self.SHOW_API_ERRORS:
                            raise ApiError("API problem ending process", Codes.UPDATE_PROCESS_OK)
                        if self.verbose:
                            print(f"[INFO] [END] pipeline update problem: {status}")
            except Exception as exc:
                if self.SHOW_API_ERRORS:
                    raise ApiError("Problem updating Process", Codes.UPDATE_PROCESS_ERROR) from exc
                print("Problem updating Process")

    def _task_invoke_with_report(self, func: Callable, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Invoke a task with API reporting."""
        self._api_task_update({"task_id": self.task_id, "status": "start"})

        result: Dict[str, Any] = {}
        try:
            if isinstance(func, Pipeline):
                result = func.run(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            self._api_task_update({"task_id": self.task_id, "status": "success"})
        except Exception as e:
            errors_tb = traceback.extract_tb(e.__traceback__)
            errors_list = [
                {"file": tb.filename, "line": tb.lineno, "method": tb.name}
                for tb in errors_tb
            ]

            error_info = {
                "task_name": self.task_name,
                "error_traceback": errors_list,
                "error_message": str(e),
                "task_id": self.task_id,
            }

            result["error"] = error_info["error_message"]
            self._api_task_update({
                "task_id": self.task_id,
                "status": "error",
                "details": json.dumps(error_info),
            })

            if self.verbose:
                for error in errors_list:
                    logger.error(error)

            raise TaskError(error_info, Codes.TASK_FAILED) from e

        return result

    def _pipeline_run_with_report(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Run the pipeline with API reporting."""
        worker_id = self.worker_id
        self._api_process_update({"id": worker_id}, start=True)

        result: Dict[str, Any] = {}
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
            safe_error = clean_for_json(error)
            self._api_process_update({"id": self.process_id, "details": json.dumps(safe_error)})

            if self.continue_on_error:
                result["error"] = error
                return result
            raise ProcessError(str(te), Codes.TASK_FAILED) from te
        except ApiError as ae:
            raise ApiError(str(ae), Codes.API_ERROR) from ae

        return result

    def set_steps(self, steps: List[Any]) -> "Pipeline":
        """Set the pipeline steps."""
        new_list = []

        def normalize_step(step: Any) -> Any:
            """Normalize a step tuple to 4 elements (func, name, version, metadata)."""
            if isinstance(step, tuple):
                if len(step) == 3 and callable(step[0]):
                    if isinstance(step[2], dict):
                        return (step[0], step[1], "v1.0", step[2])
                    return (step[0], step[1], step[2], {})
                if len(step) == 2 and callable(step[0]):
                    return (step[0], step[1], "v1.0", {})
                if len(step) == 4 and callable(step[0]):
                    return step
            return step

        for item in steps:
            if isinstance(item, Condition):
                normalized_true = [normalize_step(s) for s in item.branch_true]
                normalized_false = [normalize_step(s) for s in item.branch_false]
                new_list.append(Condition(
                    expression=item.expression,
                    branch_true=normalized_true,
                    branch_false=normalized_false,
                ))
            elif isinstance(item, For):
                normalized_steps = [normalize_step(s) for s in item.steps]
                new_list.append(For(
                    validation_expression=item.validation_expression,
                    iterations=item.iterations,
                    steps=normalized_steps,
                ))
            elif isinstance(item, Parallel):
                normalized_steps = [normalize_step(s) for s in item.steps]
                new_list.append(Parallel(
                    steps=normalized_steps,
                    max_workers=item.max_workers,
                    use_processes=item.use_processes,
                ))
            elif isinstance(item, Pipeline):
                new_list.append((item, item.pipeline_name or "SubPipeline", "v1.0", {}))
            elif callable(item):
                name = getattr(item, "NAME", getattr(item, "__name__", "unknown"))
                version = getattr(item, "VERSION", "v1.0")
                meta = getattr(item, "_wpipe_metadata", {})
                new_list.append((item, name, version, meta))
            elif (isinstance(item, tuple) and len(item) >= 2 and callable(item[0])):
                new_list.append(normalize_step(item))
            else:
                raise ValueError("Invalid step type in tasks list")

        self.tasks_list = new_list
        return self

    def add_state(
        self,
        name: str,
        func: Optional[Callable] = None,
        version: str = "v1.0",
        state: Optional[Callable] = None,
        depends_on: Optional[List[str]] = None,
        timeout: Optional[float] = None,
        retry_count: Optional[int] = None,
        retry_delay: Optional[float] = None,
        retry_on_exceptions: Optional[Tuple[type, ...]] = None,
        **kwargs: Any,
    ) -> "Pipeline":
        """Add a single step to the pipeline."""
        # pylint: disable=unused-argument
        step_func = func or state
        if step_func is None:
            raise ValueError("Either 'func' or 'state' parameter must be provided")

        meta = {
            "depends_on": depends_on,
            "timeout": timeout,
            "retry_count": retry_count,
            "retry_delay": retry_delay,
            "retry_on_exceptions": retry_on_exceptions,
        }

        decorator_meta = getattr(step_func, "_wpipe_metadata", None)
        if decorator_meta:
            for key, val in meta.items():
                if val is None:
                    meta[key] = getattr(decorator_meta, key, None)

        current_steps = list(self.tasks_list)
        current_steps.append((step_func, name, version, meta))
        self.set_steps(current_steps)
        return self

    @property
    def steps(self) -> List["Step"]:
        """
        Provides access to the pipeline steps as Step objects for compatibility.

        This property iterates through the internal `tasks_list` and creates
        `Step` objects, which encapsulate a callable function, its name,
        and version. This is useful for external tools or introspective
        operations that need to work with pipeline steps abstractly.

        Returns:
            List[Step]: A list of Step objects, each representing a task or logic block.
        """
        class Step:
            """
            Represents a single executable step within a pipeline.

            Attributes:
                func (Callable): The callable function or method to execute.
                name (str): The name of the step.
                version (str): The version of the step.
            """
            func: Callable
            name: str
            version: str

            def __init__(self, func: Callable, name: str, version: str = "") -> None:
                """
                Initializes a Step object.

                Args:
                    func: The callable function or method to be executed as part of the step.
                    name: A human-readable name for the step.
                    version: The version identifier for this step's implementation.
                """
                self.func = func
                self.name = name
                self.version = version

            def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
                """
                Executes the step function with the provided data context.

                The `data` dictionary contains the current state and context
                of the pipeline execution. The function is expected to return
                an updated `data` dictionary.

                Args:
                    data: The current pipeline data context (input dictionary).

                Returns:
                    Dict[str, Any]: The updated pipeline data context after execution.
                                    If the original function returns a non-dict type,
                                    it will be wrapped in a dictionary with a 'result' key.
                """
                # The original code passed 'context' and expected Dict[str, Any] return.
                # Renamed to 'data' for consistency with the rest of the Pipeline class.
                result = self.func(data)
                if not isinstance(result, dict):
                    # Wrap non-dict return values to maintain Dict[str, Any] consistency.
                    return {"result": result}
                return result


        result: List["Step"] = []
        for item in self.tasks_list:
            if isinstance(item, tuple) and len(item) >= 2:
                # Ensure function, name, and version are correctly extracted from the tuple
                func: Callable = item[0]
                name: str = item[1]
                version: str = item[2] if len(item) > 2 else ""
                result.append(Step(func, name, version))
        return result

    def _task_invoke(self, func: Callable, name: str, *args: Any, **kwargs: Any) -> Any:
        """Invoke a task with retry logic and timeout."""
        step_meta = kwargs.pop("__step_meta__", {})
        decorator_meta = getattr(func, "_wpipe_metadata", None)

        max_retries = self.max_retries
        retry_delay = self.retry_delay
        retry_on_exceptions = self.retry_on_exceptions
        timeout = None

        # Apply settings: Step Meta > Decorator > Pipeline Default
        if decorator_meta:
            max_retries = getattr(decorator_meta, "retry_count", max_retries) or max_retries
            retry_delay = getattr(decorator_meta, "retry_delay", retry_delay) or retry_delay
            retry_on_exceptions = getattr(decorator_meta, "retry_on_exceptions", retry_on_exceptions) or retry_on_exceptions
            timeout = getattr(decorator_meta, "timeout", None)

        if step_meta:
            max_retries = getattr(step_meta, "retry_count", None) or max_retries
            retry_delay = getattr(step_meta, "retry_delay", None) or retry_delay
            retry_on_exceptions = getattr(step_meta, "retry_on_exceptions", None) or retry_on_exceptions
            timeout = getattr(step_meta, "timeout", timeout)

        kwargs.pop("parent_step_id", None)
        kwargs.pop("parallel_group", None)

        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                def _run():
                    if self.send_to_api:
                        return self._task_invoke_with_report(func, *args, **kwargs)
                    if isinstance(func, Pipeline):
                        return func.run(*args, **kwargs)
                    return func(*args, **kwargs)

                if timeout:
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(_run)
                        result = future.result(timeout=timeout)
                else:
                    result = _run()

                if args and isinstance(args[0], dict):
                    args[0].pop("error", None)
                return result

            except (TaskError, ApiError):
                raise
            except Exception as e:  # pylint: disable=broad-exception-caught
                last_exception = e
                tb_list = traceback.extract_tb(e.__traceback__)
                
                # Find the most relevant frame (user code instead of library code)
                # We look for the last frame that doesn't contain 'site-packages' or 'wpipe'
                relevant_frame = tb_list[-1]
                for frame in reversed(tb_list):
                    if "site-packages" not in frame.filename and "wpipe/pipe" not in frame.filename:
                        relevant_frame = frame
                        break
                
                error_details = {
                    "step_name": name,
                    "error_message": str(e),
                    "error_traceback": traceback.format_exc(),
                    "file_path": relevant_frame.filename,
                    "line_number": relevant_frame.lineno,
                    "method": relevant_frame.name,
                    "timestamp": datetime.now().isoformat(),
                    "attempt": attempt + 1,
                }

                context = args[0] if args and isinstance(args[0], dict) else {}
                self._execute_error_capture(context, error_details)

                if attempt < max_retries and isinstance(e, retry_on_exceptions):
                    if self.verbose:
                        print(f"[RETRY] {name} failed (attempt {attempt + 1}): {e}")
                    time.sleep(retry_delay)
                else:
                    raise TaskError(str(e), Codes.TASK_FAILED) from e

        raise last_exception if last_exception else TaskError("Unknown error", Codes.TASK_FAILED)

    @staticmethod
    def _run_parallel_step(pipeline_instance: "Pipeline", step_item: Any, step_data: Dict[str, Any], pipe_kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Helper static method to run a step in parallel."""
        try:
            return pipeline_instance._execute_step(step_item, step_data, **pipe_kwargs)
        except Exception as e:  # pylint: disable=broad-exception-caught
            return {"error": f"Parallel execution error: {str(e)}"}

    def _execute_step(self, item: Any, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """Execute a single step."""
        # Clean kwargs to prevent collision with named arguments
        kwargs = {k: v for k, v in kwargs.items() if k not in ("parent_step_id", "parallel_group")}
        parent_step_id = kwargs.get("parent_step_id")
        parallel_group = kwargs.get("parallel_group")

        if isinstance(item, Condition):
            if self.verbose:
                print(f"[CONDITION] Evaluating: {item.expression}")
            data, _ = self._run_branch([item], data, **kwargs)
            return data

        if isinstance(item, For):
            loop_data = data.copy()
            loop_data.pop("progress_rich", None)
            iteration = 0
            while item.should_continue(loop_data, iteration):
                loop_data["_loop_iteration"] = iteration
                for step_in_loop in item.steps:
                    loop_data = self._execute_step(step_in_loop, loop_data, **kwargs)
                    if "error" in loop_data:
                        print(f"  [ERROR] Loop broken at iteration {iteration} due to: {loop_data['error']}")
                        break
                if "error" in loop_data:
                    break
                iteration += 1
            data.update(loop_data)
            return data

        if isinstance(item, Parallel):
            return self._execute_parallel(item, data, parent_step_id, parallel_group, **kwargs)

        return self._execute_task_step(item, data, parent_step_id, parallel_group, **kwargs)

    def _execute_parallel(
        self,
        item: Parallel,
        data: Dict[str, Any],
        parent_step_id: Optional[int],
        parallel_group: Optional[str],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute steps in parallel."""
        # pylint: disable=too-many-locals
        tracked_id = self._start_step_tracking(
            "Parallel Block", "v1.0", "parallel", data,
            parent_step_id=parent_step_id,
            parallel_group=parallel_group,
        )
        loop_data = data.copy()
        loop_data.pop("progress_rich", None)
        max_workers = item.max_workers or max(1, len(item.steps))
        is_multiprocess = item.use_processes
        ExecutorClass = ProcessPoolExecutor if is_multiprocess else ThreadPoolExecutor

        if self.verbose:
            mode = "PROCESSES" if is_multiprocess else "THREADS"
            print(f"[PARALLEL] Executing {len(item.steps)} steps using {mode} (workers={max_workers})")

        try:
            current_group = f"group_{tracked_id or 'none'}"
            clean_self = self
            if is_multiprocess:
                import copy as cp  # pylint: disable=import-outside-toplevel
                clean_self = cp.copy(self)
                clean_self.tracker = None
                clean_self._metrics_collector = None

            with ExecutorClass(max_workers=max_workers) as executor:
                initial_keys = set(loop_data.keys())
                futures = {}
                for step in item.steps:
                    if is_multiprocess:
                        fut = executor.submit(self._run_parallel_step, clean_self, step, loop_data.copy(), {
                            **kwargs, "parent_step_id": tracked_id, "parallel_group": current_group,
                        })
                    else:
                        def _thread_worker(s, d):
                            # Ensure we don't pass duplicate arguments to _execute_step
                            worker_kwargs = {k: v for k, v in kwargs.items() if k not in ("parent_step_id", "parallel_group")}
                            return self._execute_step(s, d, 
                                                   parent_step_id=tracked_id, 
                                                   parallel_group=current_group, 
                                                   **worker_kwargs)
                        fut = executor.submit(_thread_worker, step, loop_data.copy())
                    futures[fut] = step

                errors = []
                for future in as_completed(futures):
                    try:
                        res = future.result()
                        if res and "error" in res:
                            errors.append(res["error"])
                        elif isinstance(res, dict):
                            delta = {k: v for k, v in res.items() if k not in initial_keys and k != "progress_rich"}
                            data.update(delta or {k: v for k, v in res.items() if k != "progress_rich"})
                    except Exception as e:  # pylint: disable=broad-exception-caught
                        errors.append(str(e))

            if errors:
                data["error"] = " | ".join(errors)
        except Exception as e:  # pylint: disable=broad-exception-caught
            data["error"] = f"Executor failure: {str(e)}"
        finally:
            self._end_step_tracking(tracked_id, data if "error" not in data else None, data.get("error"))
        return data

    def _execute_task_step(
        self,
        item: Any,
        data: Dict[str, Any],
        parent_step_id: Optional[int],
        parallel_group: Optional[str],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute a single task step."""
        func, name, version, step_id, step_meta = None, "unknown", "v1.0", None, {}
        if isinstance(item, tuple):
            if len(item) < 2:
                return data
            func, name, version = item[0], item[1], item[2] if len(item) > 2 else "v1.0"
            if len(item) >= 4:
                if isinstance(item[3], dict):
                    step_meta = item[3]
                else:
                    step_id = item[3]
        elif callable(item):
            func = item
            # Look for step name in priorities: NAME attribute > __name__ > class name
            name = getattr(item, "NAME", getattr(item, "__name__", item.__class__.__name__))
            if name == "task" or name == "function":
                # Fallback to a more descriptive name if possible
                name = item.__class__.__name__
            
            version = getattr(item, "VERSION", "v1.0")
            step_meta = getattr(item, "_wpipe_metadata", {})

        if func:
            self.task_name = name
            self.task_id = step_id
            tracked_id = self._start_step_tracking(name, version, "task", data,
                                                   parent_step_id=parent_step_id,
                                                   parallel_group=parallel_group)
            data["progress_rich"] = data.get("progress_rich") or self.progress_rich
            try:
                result_data = self._task_invoke(func, name, data, __step_meta__=step_meta, **kwargs)
                data.update(result_data or {})
                data.pop("error", None)
            except Exception as e:  # pylint: disable=broad-exception-caught
                if not self.continue_on_error:
                    raise
                data["error"] = str(e)
            finally:
                hooks = self._end_step_tracking(tracked_id, data if "error" not in data else None, data.get("error"))
                data = self._handle_alert_hooks(hooks, data)
        return data

    def _run_branch(self, steps: List[Any], data: Dict[str, Any], **kwargs: Any) -> Tuple[Dict[str, Any], List[int]]:
        """Execute a branch of steps."""
        executed_ids: List[int] = []
        for item in steps:
            if isinstance(item, Condition):
                cond_name = getattr(item, "name", "condition")
                cond_expr = item.expression
                try:
                    res = item.evaluate(data)
                    branch = item.branch_true if res else item.branch_false
                    taken = "true" if res else "false"
                    err = None
                except Exception as e:  # pylint: disable=broad-exception-caught
                    branch, taken, err = item.branch_false, "false", str(e)

                cond_id = self._start_step_tracking(cond_name, "1.0.0", "condition", {"expression": cond_expr})
                data, b_ids = self._run_branch(branch, data, **kwargs)
                if cond_id:
                    executed_ids.append(cond_id)
                    executed_ids.extend(b_ids)
                    hooks = self._end_step_tracking(cond_id, {"branch_taken": taken, "expression": cond_expr}, err)
                    data = self._handle_alert_hooks(hooks, data)
            else:
                data = self._execute_step(item, data, **kwargs)
                if "error" in data:
                    break
        return data, executed_ids

    def _start_step_tracking(
        self,
        name: str,
        version: Optional[str] = None,
        step_type: str = "task",
        input_data: Optional[Dict[str, Any]] = None,
        parent_step_id: Optional[int] = None,
        parallel_group: Optional[str] = None,
    ) -> Optional[int]:
        """Start tracking a pipeline step."""
        if not self.tracker or not self.pipeline_id:
            return None
        self._step_order += 1
        filtered_input = {k: v for k, v in (input_data or {}).items() if k != "progress_rich" and not callable(v)}
        return self.tracker.start_step(
            pipeline_id=self.pipeline_id, step_order=self._step_order, step_name=name,
            step_version=version, step_type=step_type, input_data=filtered_input,
            parent_step_id=parent_step_id, parallel_group=parallel_group,
        )

    def _end_step_tracking(
        self,
        step_id: Optional[int],
        output_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        error_traceback: Optional[str] = None,
    ) -> List[Any]:
        """End tracking a pipeline step."""
        if not self.tracker or not step_id:
            return []
        filtered_out = {k: v for k, v in (output_data or {}).items()
                        if k not in ("progress_rich", "error") and not callable(v)}
        return self.tracker.complete_step(
            step_id=step_id, output_data=filtered_out, error_message=error_message,
            error_traceback=error_traceback, pipeline_id=self.pipeline_id,
        )

    def _handle_alert_hooks(self, hooks: List[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute alert hooks."""
        if not hooks:
            return data
        if self.verbose:
            print(f"[ALERTS] Firing {len(hooks)} alert hooks...")
        for hook in hooks:
            try:
                data = self._execute_step(hook, data)
            except Exception as e:  # pylint: disable=broad-exception-caught
                if self.verbose:
                    print(f"[ALERT HOOK ERROR] Hook failed: {e}")
        return data

    def _initialize_pipeline_run_context(
        self,
        initial_data: Dict[str, Any],
        checkpoint_mgr: Any,
        checkpoint_id: Optional[str],
        **kwargs: Any,
    ) -> Tuple[Dict[str, Any], Optional[SystemMetricsCollector], int]:
        """
        Initializes the context for a pipeline run.

        This includes setting the start time, handling checkpoint resumption,
        registering the pipeline with the tracker, and initializing system
        metrics collection if enabled.

        Args:
            initial_data: The initial data dictionary passed to the pipeline.
            checkpoint_mgr: The checkpoint manager instance, if used.
            checkpoint_id: The ID of the checkpoint to resume from, if any.
            **kwargs: Additional keyword arguments, potentially containing pipeline configuration.

        Returns:
            Tuple[Dict[str, Any], Optional[SystemMetricsCollector], int]:
                A tuple containing the prepared data dictionary, the
                SystemMetricsCollector instance (or None if not enabled),
                and the step index to start from.
        """
        data = initial_data.copy()
        pipeline_start = datetime.now()
        data["_pipeline_start_time"] = pipeline_start.isoformat()

        start_at_step = 0
        if checkpoint_mgr and checkpoint_id and checkpoint_mgr.can_resume(checkpoint_id):
            last = checkpoint_mgr.get_last_checkpoint(checkpoint_id)
            data.update(last["data"] or {})
            start_at_step = last["step_order"] + 1
            if self.verbose:
                print(f"[CHECKPOINT] Resuming '{checkpoint_id}' from step {start_at_step}")

        metrics_collector: Optional[SystemMetricsCollector] = None
        if self.tracker:
            reg = self.tracker.register_pipeline(
                name=self.pipeline_name,
                pipeline_steps=self.tasks_list,
                input_data=data,
                worker_id=self.worker_id,
                worker_name=self.worker_name,
                parent_pipeline_id=self.parent_pipeline_id,
            )
            self.pipeline_id = reg["pipeline_id"]
            self._step_order = start_at_step
            if self.verbose:
                print(f"[PIPELINE STATUS] Registered: {self.pipeline_id}")
            for event in self._pending_events:
                self.tracker.add_event(pipeline_id=self.pipeline_id, **event)
            self._pending_events = []
            if self._collect_system_metrics:
                metrics_collector = SystemMetricsCollector(self.tracker, self.pipeline_id)
                metrics_collector.start()

        return data, metrics_collector, start_at_step

    def _setup_progress_bar_manager(self, total_steps: int) -> Tuple[Callable[[int], Any], int]:
        """
        Sets up and returns a progress bar generator.

        Configures the progress bar based on the `show_progress` attribute,
        utilizing `ProgressManager` for rich output or `tqdm` as a fallback.

        Args:
            total_steps: The total number of steps in the pipeline.

        Returns:
            Tuple[Callable[[int], Any], int]: A tuple containing:
                - A generator function that yields step index and progress object.
                - The total number of steps.
        """
        def progress_bar_gen(size: int):
            from tqdm import tqdm
            try:
                from rich.errors import LiveError
            except ImportError:
                class LiveError(Exception): pass

            if not self.show_progress:
                for i in range(size):
                    yield i, None
                return
            try:
                with ProgressManager() as progress:
                    self.progress_rich = progress
                    task = progress.add_task(f"[cyan]{self.pipeline_name}", total=size)
                    for i in range(size):
                        yield i, progress
                        progress.update(task, advance=1)
            except (LiveError, ImportError):
                # Fallback to tqdm if rich is not available or fails
                for i in tqdm(range(size), desc=self.pipeline_name):
                    yield i, None

        return progress_bar_gen, total_steps

    def _execute_all_pipeline_steps(
        self,
        data: Dict[str, Any],
        start_at_step: int,
        progress_bar_gen: Callable[[int], Any],
        total_steps: int,
        checkpoint_mgr: Any,
        checkpoint_id: Optional[str],
        step_kwargs: Dict[str, Any],
    ) -> Tuple[Dict[str, Any], Optional[str], Optional[str]]:
        """
        Executes all steps of the pipeline sequentially.

        This method iterates through the pipeline tasks, executes each step,
        handles errors according to `continue_on_error` setting, evaluates checkpoints,
        and saves checkpoints if a manager is provided.

        Args:
            data: The current pipeline data dictionary.
            start_at_step: The index of the first step to execute.
            progress_bar_gen: The generator function for the progress bar.
            total_steps: The total number of steps in the pipeline.
            checkpoint_mgr: The checkpoint manager instance, if used.
            checkpoint_id: The ID of the checkpoint to resume from, if any.
            step_kwargs: Additional keyword arguments for step execution.

        Returns:
            Tuple[Dict[str, Any], Optional[str], Optional[str]]:
                A tuple containing the updated data dictionary, the error message (if any),
                and the name of the step where the error occurred (if any).
        """
        error_msg: Optional[str] = None
        error_step: Optional[str] = None

        try:
            data = self._evaluate_checkpoints(data)
            for idx, progress in progress_bar_gen(size=total_steps):
                if idx < start_at_step:
                    continue
                item = self.tasks_list[idx]
                data["progress_rich"] = progress
                data = self._execute_step(item, data, **step_kwargs)

                if "error" in data:
                    error_msg, error_step = data["error"], getattr(item, "NAME", str(item))
                    if not self.continue_on_error:
                        break
                else:
                    error_msg, error_step = None, None

                data = self._evaluate_checkpoints(data)
                if checkpoint_mgr and checkpoint_id and "error" not in data:
                    # Safely get step name for checkpoint
                    name = getattr(item, "NAME", getattr(item, "__name__", f"step_{idx}"))
                    # Filter out progress_rich and errors from data for checkpoint
                    cp_data = {k: v for k, v in data.items() if k != "progress_rich" and k != "error"}
                    checkpoint_mgr.save_checkpoint(checkpoint_id, idx, name, "success", cp_data)
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Catching broader exceptions here as _execute_step should handle TaskError/ApiError
            error_msg, error_step = str(e), self.task_name
            if not self.continue_on_error:
                raise
        return data, error_msg, error_step

    def _finalize_pipeline_execution(
        self,
        data: Dict[str, Any],
        metrics_collector: Optional[SystemMetricsCollector],
        error_msg: Optional[str],
        error_step: Optional[str],
    ) -> None:
        """
        Finalizes the pipeline execution.

        This includes running post-run tasks, stopping system metrics collection,
        completing the pipeline tracking, and clearing checkpoints if the pipeline
        completed successfully without errors.

        Args:
            data: The current data dictionary.
            metrics_collector: The system metrics collector instance.
            error_msg: The error message, if an error occurred.
            error_step: The name of the step where the error occurred.
        """
        data = self._execute_post_run_tasks(data)
        if metrics_collector:
            metrics_collector.stop()
        self._complete_tracking(data, error_msg, error_step)
        # Clear checkpoints only if pipeline completed successfully and a checkpoint manager was used.
        if not error_msg and self.tracker and hasattr(self, 'checkpoint_mgr') and self.checkpoint_mgr and hasattr(self, 'checkpoint_id') and self.checkpoint_id:
            self.checkpoint_mgr.clear_checkpoints(self.checkpoint_id)

    def _pipeline_run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Internal pipeline run implementation orchestrated by reporting wrappers.

        This method orchestrates the execution of the pipeline by calling
        several helper methods to manage context initialization, progress
        bar setup, step execution, and finalization. It aims to improve
        readability and maintainability by breaking down the complex logic.

        Args:
            *args: Positional arguments. The first argument is expected to be the initial data dictionary.
            **kwargs: Keyword arguments, potentially including checkpoint manager and ID.

        Returns:
            Dict[str, Any]: The final data dictionary after pipeline execution.
        """
        # pylint: disable=too-many-locals,too-many-branches,too-many-statements

        # Initialize context (data, tracker, metrics, start_at_step)
        initial_data = args[0].copy() if args else {}
        checkpoint_mgr = kwargs.pop("checkpoint_mgr", None)
        checkpoint_id = kwargs.pop("checkpoint_id", None)
        # Assign checkpoint_mgr and checkpoint_id to self for _finalize_pipeline_execution
        self.checkpoint_mgr = checkpoint_mgr
        self.checkpoint_id = checkpoint_id
        data, metrics_collector, start_at_step = self._initialize_pipeline_run_context(
            initial_data, checkpoint_mgr, checkpoint_id, **kwargs
        )

        # Setup progress bar
        total_steps = len(self.tasks_list)
        progress_bar_gen, total_steps = self._setup_progress_bar_manager(total_steps)

        # Prepare arguments for step execution
        step_kwargs = {k: v for k, v in kwargs.items() if k not in ("checkpoint_mgr", "checkpoint_id")}

        # Execute steps
        error_msg, error_step = None, None
        try:
            data, error_msg, error_step = self._execute_all_pipeline_steps(
                data, start_at_step, progress_bar_gen, total_steps,
                checkpoint_mgr, checkpoint_id, step_kwargs
            )
        finally:
            # Finalize execution (post-run tasks, stop metrics, complete tracking)
            self._finalize_pipeline_execution(data, metrics_collector, error_msg, error_step)

        data.pop("progress_rich", None) # Clean up progress_rich from data
        return data

    def _complete_tracking(self, data: Dict[str, Any], error_msg: Optional[str], error_step: Optional[str]) -> None:
        """Finalize tracking for the pipeline."""
        if self.tracker and self.pipeline_id:
            try:
                output = data.copy() if not error_msg else {}
                output["pipeline_start_time"] = data.get("_pipeline_start_time")
                output["pipeline_end_time"] = datetime.now().isoformat()
                start = datetime.fromisoformat(output["pipeline_start_time"]) if output.get("pipeline_start_time") else None
                if start:
                    output["pipeline_elapsed_time_ms"] = (datetime.now() - start).total_seconds() * 1000

                hooks = self.tracker.complete_pipeline(
                    pipeline_id=self.pipeline_id, output_data=output,
                    error_message=error_msg, error_step=error_step,
                )
                self._handle_alert_hooks(hooks, data)
            except Exception as e:  # pylint: disable=broad-exception-caught
                if self.verbose:
                    print(f"[WARNING] Tracker completion failed: {e}")
            if self.verbose:
                print(f"[PIPELINE STATUS] {self.pipeline_id}: {'ERROR' if error_msg else 'COMPLETED'}")

    def run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Execute the pipeline."""
        if "error" in (args[0] if args else {}):
            raise TaskError(f"[{self.task_name}] Initial data contains error", Codes.TASK_FAILED)
        result = self._pipeline_run_with_report(*args, **kwargs)
        
        # Release database locks after execution
        if self.tracking_db:
            try:
                from wpipe import _db_connections, _db_lock
                with _db_lock:
                    if self.tracking_db in _db_connections:
                        _db_connections[self.tracking_db].commit()
            except Exception:
                pass
        return result
