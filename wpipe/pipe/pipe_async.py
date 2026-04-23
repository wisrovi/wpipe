"""
Async Pipeline module for orchestrating asynchronous task execution.

This module provides the PipelineAsync class for managing and executing
a sequence of async tasks, with support for conditional branching,
retry logic, API tracking, and execution history tracking.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from rich.progress import Progress

from wpipe.api_client.api_client import APIClient
from wpipe.exception import Codes, TaskError
from wpipe.tracking import PipelineTracker

from .pipe import Condition, Parallel, SystemMetricsCollector


def _is_async_callable(func: Any) -> bool:
    """
    Check if a callable is async (handles both functions and callable objects).

    Args:
        func: The object to check.

    Returns:
        bool: True if it's an async callable, False otherwise.
    """
    if asyncio.iscoroutinefunction(func):
        return True
    if hasattr(func, "__call__") and asyncio.iscoroutinefunction(func.__call__):
        return True
    return False


class PipelineAsync(APIClient):
    """
    Async Pipeline for orchestrating asynchronous task execution with API tracking support.

    Attributes:
        worker_id (Optional[str]): Unique identifier for the worker.
        worker_name (str): Name of the worker.
        verbose (bool): Whether to enable verbose logging.
        tasks_list (List[Any]): List of steps/tasks to execute.
        pipeline_name (str): Name of the pipeline.
        tracker (Optional[PipelineTracker]): Tracker for execution history.
    """

    # pylint: disable=too-many-instance-attributes
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
        Initialize the Async Pipeline.

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
            self.api_config: Optional[Dict[str, Any]] = api_config
        else:
            self.api_config = None

        self.worker_id: Optional[str] = None
        if worker_id:
            self.set_worker_id(worker_id)

        self.worker_name: str = worker_name or "worker"
        self.verbose: bool = verbose
        self.max_retries: int = max_retries
        self.retry_delay: float = retry_delay
        self.retry_on_exceptions: Tuple[type, ...] = retry_on_exceptions
        self.parent_pipeline_id: Optional[str] = parent_pipeline_id
        self._collect_system_metrics: bool = collect_system_metrics
        self.continue_on_error: bool = continue_on_error
        self.show_progress: bool = show_progress
        self.tracking_db: Optional[str] = tracking_db

        # Initialize tracking if database path provided
        self.tracker: Optional[PipelineTracker] = None
        if tracking_db:
            self.tracker = PipelineTracker(tracking_db, config_dir)

        self.pipeline_name: str = pipeline_name or "Pipeline"
        self.pipeline_id: Optional[str] = None
        self.tasks_list: List[Any] = []
        self._step_order: int = 0

        # Internal queues
        self._pending_events: List[Dict[str, Any]] = []
        self._post_run_tasks: List[Any] = []
        self._checkpoints: List[Dict[str, Any]] = []
        self._error_capture_tasks: List[Any] = []

        self._metrics_collector: Optional[SystemMetricsCollector] = None
        self.progress_rich: Optional[Progress] = None

    def add_event(
        self,
        event_type: str,
        event_name: str,
        message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        steps: Optional[List[Any]] = None,
    ) -> None:
        """
        Add an event or annotation to the pipeline.

        Args:
            event_type: Category of the event.
            event_name: Specific name for the event.
            message: Descriptive message.
            data: Additional metadata.
            tags: List of tags for categorization.
            steps: Optional steps to run after the current execution.
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

    def add_checkpoint(
        self,
        checkpoint_name: str,
        expression: str = "True",
        steps: Optional[List[Any]] = None,
    ) -> None:
        """
        Add a checkpoint to the pipeline.

        Args:
            checkpoint_name: Unique name for the checkpoint.
            expression: Python expression to trigger the checkpoint.
            steps: Steps to run when the checkpoint is reached.
        """
        self._checkpoints.append({
            "name": checkpoint_name,
            "expression": expression,
            "steps": steps or [],
            "fired": False
        })

    def add_error_capture(self, steps: List[Any]) -> None:
        """
        Add steps to be executed when an error occurs.

        Args:
            steps: List of callables or logic blocks for error handling.
        """
        self.continue_on_error = True
        self._error_capture_tasks.extend(steps)

    async def _evaluate_checkpoints(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate and fire checkpoints based on current data.

        Args:
            data: Current pipeline context.

        Returns:
            Dict[str, Any]: Updated pipeline context.
        """
        for cp in self._checkpoints:
            if not cp["fired"]:
                # Use a restricted environment for security
                safe_locals = data
                safe_globals: Dict[str, Any] = {
                    "True": True,
                    "False": False,
                    "None": None,
                    "asyncio": asyncio,
                    "__builtins__": {}
                }
                try:
                    if eval(cp["expression"], safe_globals, safe_locals):  # pylint: disable=eval-used
                        if self.verbose:
                            print(f"\n[ASYNC CHECKPOINT REACHED] {cp['name']}")

                        self.add_event(
                            event_type="checkpoint",
                            event_name=cp["name"],
                            message=f"Checkpoint reached: {cp['name']}"
                        )

                        for step_item in cp["steps"]:
                            data = await self._execute_step(step_item, data)

                        cp["fired"] = True
                except (NameError, SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
                    if self.verbose:
                        print(f"[CHECKPOINT INFO] Milestone '{cp['name']}' skip: {e}")
        return data

    def set_worker_id(self, worker_id: str) -> None:
        """
        Set the worker ID.

        Args:
            worker_id: The worker identifier string.

        Raises:
            TypeError: If worker_id is not a string.
        """
        if not isinstance(worker_id, str):
            raise TypeError(f"worker_id must be a string, got {type(worker_id)}")

        if len(worker_id) > 5:
            self.worker_id = worker_id
        else:
            self.worker_id = None

    async def _task_invoke(
        self, func: Any, name: str, *args: Any, **kwargs: Any
    ) -> Any:
        """
        Invoke an async task, optionally with retry logic.

        Args:
            func: The callable to invoke.
            name: Name of the task.
            *args: Positional arguments for the task.
            **kwargs: Keyword arguments for the task.

        Returns:
            Any: The result of the task execution.

        Raises:
            TaskError: If the task fails after all retries.
        """
        # Retry priority: Decorator > Pipeline
        decorator_meta = getattr(func, "_wpipe_metadata", None)
        max_retries = self.max_retries
        retry_delay = self.retry_delay
        retry_on_exceptions = self.retry_on_exceptions

        if decorator_meta:
            if getattr(decorator_meta, "retry_count", None) is not None:
                max_retries = decorator_meta.retry_count
            if getattr(decorator_meta, "retry_delay", None) is not None:
                retry_delay = decorator_meta.retry_delay

        # Clean internal tracking arguments
        kwargs.pop("parent_step_id", None)
        kwargs.pop("parallel_group", None)

        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                if isinstance(func, PipelineAsync):
                    result = await func.run(*args, **kwargs)
                elif _is_async_callable(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                # Success cleanup
                if args and isinstance(args[0], dict):
                    args[0].pop("error", None)
                return result

            except Exception as e:  # pylint: disable=broad-exception-caught
                last_exception = e
                # Capture error for handlers
                error_details = {
                    "step_name": name,
                    "error_message": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "attempt": attempt + 1
                }

                context = args[0] if args and isinstance(args[0], dict) else {}
                for handler in self._error_capture_tasks:
                    try:
                        if _is_async_callable(handler):
                            await handler(context, error_details)
                        else:
                            handler(context, error_details)
                    except Exception:  # pylint: disable=broad-exception-caught
                        pass

                if attempt < max_retries and isinstance(e, retry_on_exceptions):
                    if self.verbose:
                        print(f"[ASYNC RETRY] {name} failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                    await asyncio.sleep(retry_delay)
                else:
                    raise TaskError(str(e), Codes.TASK_FAILED) from e

        raise last_exception if last_exception else RuntimeError("Task failed")

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
        filtered_input = {
            k: v
            for k, v in (input_data or {}).items()
            if k not in ("progress_rich",) and not callable(v)
        }
        return self.tracker.start_step(
            pipeline_id=self.pipeline_id,
            step_order=self._step_order,
            step_name=name,
            step_version=version,
            step_type=step_type,
            input_data=filtered_input,
            parent_step_id=parent_step_id,
            parallel_group=parallel_group,
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
        filtered_output = None
        if output_data and not error_message:
            filtered_output = {
                k: v
                for k, v in output_data.items()
                if k not in ("progress_rich",) and not callable(v)
            }

        return self.tracker.complete_step(
            step_id=step_id,
            output_data=filtered_output,
            error_message=error_message,
            error_traceback=error_traceback,
            pipeline_id=self.pipeline_id,
        )

    async def _execute_step(self, item: Any, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """
        Execute a single step in the async pipeline.

        Args:
            item: The step to execute (callable, logic block, etc).
            data: Current pipeline context.
            **kwargs: Additional execution parameters.

        Returns:
            Dict[str, Any]: Updated pipeline context.
        """
        parent_step_id = kwargs.get("parent_step_id")
        parallel_group = kwargs.get("parallel_group")

        if isinstance(item, Condition):
            tracked_id = self._start_step_tracking(
                "Condition", "v1.0", "condition", data,
                parent_step_id=parent_step_id,
                parallel_group=parallel_group
            )
            branch = item.branch_true if item.evaluate(data) else (item.branch_false or [])
            for step in branch:
                data = await self._execute_step(step, data, **kwargs)
            self._end_step_tracking(tracked_id, data)
            return data

        if isinstance(item, Parallel):
            return await self._execute_parallel(item, data, parent_step_id, parallel_group, **kwargs)

        return await self._execute_task(item, data, parent_step_id, parallel_group, **kwargs)

    async def _execute_parallel(
        self,
        item: Parallel,
        data: Dict[str, Any],
        parent_step_id: Optional[int],
        parallel_group: Optional[str],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute parallel steps concurrently."""
        tracked_parallel_id = self._start_step_tracking(
            "Parallel Block", "v1.0", "parallel", data,
            parent_step_id=parent_step_id,
            parallel_group=parallel_group
        )
        loop_data = data.copy()
        loop_data.pop("progress_rich", None)
        current_group = f"group_{tracked_parallel_id or 'none'}"

        if self.verbose:
            print(f"\n[PARALLEL ASYNC] Executing {len(item.steps)} steps concurrently")

        error_msg = None
        try:
            tasks = [
                self._execute_step(
                    step,
                    loop_data.copy(),
                    **{**kwargs, "parent_step_id": tracked_parallel_id, "parallel_group": current_group}
                )
                for step in item.steps
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            errors = []
            for res in results:
                if isinstance(res, Exception):
                    errors.append(str(res))
                elif isinstance(res, dict):
                    if "error" in res:
                        errors.append(res["error"])
                    data.update({k: v for k, v in res.items() if k != "progress_rich"})
            if errors:
                error_msg = " | ".join(errors)
                data["error"] = error_msg
        except Exception as e:  # pylint: disable=broad-exception-caught
            error_msg = str(e)
            data["error"] = error_msg
        finally:
            self._end_step_tracking(tracked_parallel_id, data if not error_msg else None, error_msg)
        return data

    async def _execute_task(
        self,
        item: Any,
        data: Dict[str, Any],
        parent_step_id: Optional[int],
        parallel_group: Optional[str],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute a single task step."""
        func = None
        name = "unknown"
        version = "v1.0"

        if isinstance(item, tuple):
            func, name, version = item[0], item[1], item[2]
        elif callable(item):
            func = item
            name = getattr(item, "NAME", getattr(item, "__name__", "task"))
            version = getattr(item, "VERSION", "v1.0")

        if func:
            tracked_step_id = self._start_step_tracking(
                name, version, "task", data,
                parent_step_id=parent_step_id,
                parallel_group=parallel_group
            )
            error_msg = None
            try:
                result = await self._task_invoke(func, name, data, **kwargs)
                if result is None:
                    result = {}
                data.update(result)
                data.pop("error", None)
            except Exception as e:  # pylint: disable=broad-exception-caught
                error_msg = str(e)
                data["error"] = error_msg
                if not self.continue_on_error:
                    self._end_step_tracking(tracked_step_id, None, error_msg)
                    raise
            finally:
                self._end_step_tracking(tracked_step_id, data if not error_msg else None, error_msg)
        return data

    async def _pipeline_run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Internal async pipeline run implementation."""
        data = args[0].copy() if args else {}
        error_message = None

        # Resumption logic
        checkpoint_mgr = kwargs.get("checkpoint_mgr")
        checkpoint_id = kwargs.get("checkpoint_id")
        start_at_step = 0
        if checkpoint_mgr and checkpoint_id and checkpoint_mgr.can_resume(checkpoint_id):
            last = checkpoint_mgr.get_last_checkpoint(checkpoint_id)
            data.update(last["data"] or {})
            start_at_step = last["step_order"] + 1

        if self.tracker:
            reg = self.tracker.register_pipeline(name=self.pipeline_name, pipeline_steps=self.tasks_list, input_data=data)
            self.pipeline_id = reg["pipeline_id"]
            for event in self._pending_events:
                self.tracker.add_event(pipeline_id=self.pipeline_id, **event)
            self._pending_events = []

        total_steps = len(self.tasks_list)
        try:
            data = await self._evaluate_checkpoints(data)
            for i in range(start_at_step, total_steps):
                item = self.tasks_list[i]
                data = await self._execute_step(item, data)

                if "error" not in data:
                    error_message = None
                    if checkpoint_mgr and checkpoint_id:
                        name = getattr(item, "NAME", f"step_{i}")
                        checkpoint_mgr.save_checkpoint(checkpoint_id, i, name, "success", data)
                else:
                    error_message = data["error"]
                    if not self.continue_on_error:
                        break
                data = await self._evaluate_checkpoints(data)
        except Exception as e:  # pylint: disable=broad-exception-caught
            error_message = str(e)
            data["error"] = error_message
        finally:
            if self.tracker and self.pipeline_id:
                self.tracker.complete_pipeline(
                    pipeline_id=self.pipeline_id,
                    output_data=data if not error_message else None,
                    error_message=error_message
                )
                if self.verbose:
                    status = "ERROR" if error_message else "COMPLETED"
                    print(f"\n[ASYNC STATUS] {self.pipeline_id}: {status}")
        return data

    async def run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute the async pipeline.

        Args:
            *args: Positional arguments, typically the initial data dictionary.
            **kwargs: Additional keyword arguments for execution control.

        Returns:
            Dict[str, Any]: The final pipeline data dictionary.
        """
        result = await self._pipeline_run(*args, **kwargs)
        
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

    def set_steps(self, steps: List[Any]) -> None:
        """
        Set the async pipeline steps.

        Args:
            steps: List of steps to be executed.
        """
        self.tasks_list = steps
