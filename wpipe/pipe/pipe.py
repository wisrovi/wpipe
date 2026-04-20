"""
Pipeline module for orchestrating task execution.

This module provides the Pipeline class for managing and executing
a sequence of tasks, with support for conditional branching,
retry logic, API tracking, and execution history tracking.
"""

import inspect
import json
import os
import threading
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from datetime import datetime
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
            "cpu_percent": process.cpu_percent(interval=0),
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
        self, tracker: PipelineTracker, pipeline_id: str, interval_seconds: float = 0.5
    ):
        self.tracker = tracker
        self.pipeline_id = pipeline_id
        self.interval = interval_seconds
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        """Start collecting metrics."""
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._collect_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop collecting metrics."""
        self._stop_event.set()
        # No bloqueamos esperando al hilo, es daemon y cerrará solo
        pass

    def _collect_loop(self):
        """Collection loop."""
        while not self._stop_event.is_set():
            try:
                metrics = get_system_metrics()
                if metrics:
                    self.tracker.record_system_metrics(self.pipeline_id, metrics)
            except Exception:
                pass
            # Wait for interval or until stop event is set
            self._stop_event.wait(self.interval)


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

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        def _ser(s):
            if hasattr(s, "to_dict"): return s.to_dict()
            if isinstance(s, tuple):
                return {
                    "type": "task",
                    "name": s[1] if len(s) > 1 else "unknown",
                    "version": s[2] if len(s) > 2 else "v1.0",
                    "meta": s[3] if len(s) > 3 else {}
                }
            return str(s)

        return {
            "type": "condition",
            "expression": self.expression,
            "branch_true": [_ser(s) for s in self.branch_true],
            "branch_false": [_ser(s) for s in self.branch_false],
        }

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

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        def _ser(s):
            if hasattr(s, "to_dict"): return s.to_dict()
            if isinstance(s, tuple):
                return {
                    "type": "task",
                    "name": s[1] if len(s) > 1 else "unknown",
                    "version": s[2] if len(s) > 2 else "v1.0",
                    "meta": s[3] if len(s) > 3 else {}
                }
            return str(s)

        return {
            "type": "for",
            "iterations": self.iterations,
            "expression": self.validation_expression,
            "steps": [_ser(s) for s in self.steps],
        }

    def _evaluate_condition(self, data: dict) -> bool:
        if not self.validation_expression:
            return True
        safe_globals = {"__builtins__": {}}
        safe_locals = data.copy()
        try:
            return eval(self.validation_expression, safe_globals, safe_locals)
        except Exception as e:
            raise ValueError(
                f"Invalid loop expression: {self.validation_expression}. Error: {e}"
            ) from e


class Parallel:
    """Represents a parallel execution block in the pipeline."""

    def __init__(
        self,
        steps: list,
        max_workers: Optional[int] = None,
        use_processes: bool = False,
    ) -> None:
        """
        Initialize a Parallel block.

        Args:
            steps: List of steps to execute in parallel.
            max_workers: Maximum number of worker threads.
            use_processes: Whether to use ProcessPoolExecutor (multiprocessing) instead of ThreadPoolExecutor.
        """
        self.steps = steps or []
        self.max_workers = max_workers
        self.use_processes = use_processes

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        def _ser(s):
            if hasattr(s, "to_dict"): return s.to_dict()
            if isinstance(s, tuple):
                return {
                    "type": "task",
                    "name": s[1] if len(s) > 1 else "unknown",
                    "version": s[2] if len(s) > 2 else "v1.0",
                    "meta": s[3] if len(s) > 3 else {}
                }
            return str(s)

        return {
            "type": "parallel",
            "max_workers": self.max_workers,
            "use_processes": self.use_processes,
            "steps": [_ser(s) for s in self.steps],
        }


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
        show_progress: bool = True,
    ) -> None:
        """
        Initialize the Pipeline.
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
        self.show_progress = show_progress

        # Internal queues for events and post-run tasks
        self._pending_events = []
        self._post_run_tasks = []
        self._checkpoints = []
        self._error_capture_tasks = []

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
        steps: Optional[list] = None,
    ):
        """
        Add an event/annotation to the pipeline.
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

    def add_checkpoint(self, checkpoint_name: str, expression: str = "True", steps: Optional[list] = None):
        """
        Add a checkpoint to the pipeline that triggers when expression is True.
        Args:
            checkpoint_name: Name of the checkpoint.
            expression: Python expression to evaluate against context data.
            steps: List of steps to execute when this checkpoint is reached.
        """
        self._checkpoints.append({
            "name": checkpoint_name,
            "expression": expression,
            "steps": steps or [],
            "fired": False
        })

    def _evaluate_checkpoints(self, data: dict):
        """Evaluate and fire checkpoints based on current data."""
        for cp in self._checkpoints:
            if not cp["fired"]:
                safe_globals = {"True": True, "False": False, "None": None}
                try:
                    if eval(cp["expression"], safe_globals, data):
                        if self.verbose:
                            print(f"\n[CHECKPOINT REACHED] {cp['name']}")

                        # Registrar el evento con reintento simple para evitar bloqueos de SQLite
                        max_db_tries = 3
                        for db_try in range(max_db_tries):
                            try:
                                self.add_event(
                                    event_type="checkpoint",
                                    event_name=cp["name"],
                                    message=f"Checkpoint reached: {cp['name']}"
                                )
                                break
                            except Exception:
                                if db_try == max_db_tries - 1: raise
                                time.sleep(0.05)

                        # Ejecutar pasos asociados
                        for step_item in cp["steps"]:
                            data = self._execute_step(step_item, data)

                        cp["fired"] = True
                except Exception as e:
                    if self.verbose:
                        print(f"[CHECKPOINT INFO] Milestone '{cp['name']}' not registered yet or busy: {e}")
        return data

    def add_error_capture(self, steps: list):
        """
        Add steps to execute when an error occurs in the pipeline.
        
        The steps will receive (context_data, error_info).
        """
        self._error_capture_tasks.extend(steps)

    def _execute_error_capture(self, data: dict, error_info: dict):
        """Execute error capture steps safely."""
        if not self._error_capture_tasks:
            return data

        if self.verbose:
            print(f"\n[ERROR CAPTURE] Processing error in state '{error_info['step_name']}'...")

        for task in self._error_capture_tasks:
            try:
                # Detectamos si la función acepta 2 argumentos (data, error_info)
                func = task[0] if isinstance(task, tuple) else task
                name = task[1] if isinstance(task, tuple) else (getattr(func, "NAME", None) or getattr(func, "__name__", "error_handler"))

                sig = inspect.signature(func)
                if len(sig.parameters) >= 2:
                    data = self._task_invoke(func, name, data, error_info)
                else:
                    data = self._task_invoke(func, name, data)
            except Exception as e:
                if self.verbose:
                    print(f"[ERROR CAPTURE FAILED] {e}")

        return data

    def _execute_post_run_tasks(self, data: dict):
        """Execute post-run tasks safely."""
        if not self._post_run_tasks:
            return data

        if self.verbose:
            print("\n[HOOKS] Executing post-run tasks...")

        for task in self._post_run_tasks:
            try:
                data = self._execute_step(task, data)
            except Exception as e:
                if self.verbose:
                    print(f"[HOOK ERROR] Task failed: {e}")

        return data

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
        """
        new_list = []

        def normalize_step(step: tuple) -> tuple:
            """Normalize a step tuple to 4 elements (func, name, version, metadata)."""
            if isinstance(step, tuple):
                if len(step) == 3 and callable(step[0]):
                    # Check if the third element is a dict (metadata) or a string (version)
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
            elif isinstance(item, Parallel):
                normalized_steps = [normalize_step(s) for s in item.steps]
                new_list.append(
                    Parallel(
                        steps=normalized_steps,
                        max_workers=item.max_workers,
                        use_processes=item.use_processes,
                    )
                )
            elif callable(item):
                name = getattr(item, "NAME", None) or getattr(
                    item, "__name__", "unknown"
                )
                version = getattr(item, "VERSION", "v1.0") or "v1.0"
                # Extraer metadatos del decorador @step si existen
                meta = getattr(item, "_wpipe_metadata", {})
                new_list.append((item, name, version, meta))
            elif not (
                isinstance(item, tuple)
                and len(item) >= 2
                and callable(item[0])
                and isinstance(item[1], str)
            ):
                raise ValueError(
                    "Each element must be a tuple (function, name, version), "
                    "a Condition object, a For object, or a callable (e.g., @step decorated function)."
                )
            else:
                s = normalize_step(item)
                new_list.append(s)

        self.tasks_list = new_list

    def add_state(
        self,
        name: str,
        func: Optional[Callable] = None,
        version: str = "v1.0",
        state: Optional[Callable] = None,
        depends_on=None,
        timeout=None,
        retry_count=None,
        retry_delay=None,
        retry_on_exceptions=None,
        **kwargs,
    ) -> None:
        """
        Add a single step to the pipeline.
        """
        step_func = func or state
        if step_func is None:
            raise ValueError("Either 'func' or 'state' parameter must be provided")

        meta = {
            "depends_on": depends_on,
            "timeout": timeout,
            "retry_count": retry_count,
            "retry_delay": retry_delay,
            "retry_on_exceptions": retry_on_exceptions
        }

        # Merge with decorator metadata if exists
        decorator_meta = getattr(step_func, "_wpipe_metadata", None)
        if decorator_meta:
            # We prioritize direct parameters of add_state
            for key, val in meta.items():
                if val is None:
                    meta[key] = getattr(decorator_meta, key, None)

        current_steps = list(self.tasks_list) if hasattr(self, "tasks_list") else []
        new_step = (step_func, name, version, meta)
        current_steps.append(new_step)
        self.set_steps(current_steps)

    @property
    def steps(self):
        """Property to access steps for Phase 2 compatibility."""

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
                            f"[RETRY] {name} failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}"
                        )
                    time.sleep(self.retry_delay)
        raise last_exception

    def _task_invoke(self, func: Callable, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Invoke a task, optionally with retry logic.
        """
        # Obtener metadatos específicos del paso si se pasaron desde _execute_step
        step_meta = kwargs.pop("__step_meta__", {})

        # Obtener metadatos si existen en el objeto función (del decorador @step)
        decorator_meta = getattr(func, "_wpipe_metadata", None)

        # Determinar configuraciones de reintento (Prioridad: Explícito > Decorador > Pipeline)
        max_retries = self.max_retries
        retry_delay = self.retry_delay
        retry_on_exceptions = self.retry_on_exceptions

        # 1. Aplicar desde decorador
        if decorator_meta:
            if getattr(decorator_meta, "retry_count", None) is not None:
                max_retries = decorator_meta.retry_count
            if getattr(decorator_meta, "retry_delay", None) is not None:
                retry_delay = decorator_meta.retry_delay
            if getattr(decorator_meta, "retry_on_exceptions", None) is not None:
                retry_on_exceptions = decorator_meta.retry_on_exceptions

        # 2. Aplicar desde metadatos explícitos (add_state o similar) - Manda sobre el decorador
        if step_meta:
            def _get_val(meta, key):
                if isinstance(meta, dict):
                    return meta.get(key)
                return getattr(meta, key, None)

            if _get_val(step_meta, "retry_count") is not None:
                max_retries = _get_val(step_meta, "retry_count")
            if _get_val(step_meta, "retry_delay") is not None:
                retry_delay = _get_val(step_meta, "retry_delay")
            if _get_val(step_meta, "retry_on_exceptions") is not None:
                retry_on_exceptions = _get_val(step_meta, "retry_on_exceptions")

        # 3. Limpiar argumentos internos de tracking para no pasarlos a la función del usuario
        # que podría no aceptarlos (unexpected keyword argument)
        kwargs.pop("parent_step_id", None)
        kwargs.pop("parallel_group", None)

        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                if self.send_to_api:
                    result = self._task_invoke_with_report(func, *args, **kwargs)
                elif isinstance(func, Pipeline):
                    result = func.run(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                # SI TIENE ÉXITO: Limpiamos cualquier rastro de error anterior en este paso
                if args and isinstance(args[0], dict):
                    args[0].pop("error", None)

                return result

            except (TaskError, ApiError):
                raise
            except Exception as e:
                last_exception = e

                # Extraer info detallada del error para el capturador
                tb = traceback.extract_tb(e.__traceback__)
                last_trace = tb[-1] if tb else None
                error_details = {
                    "step_name": name,
                    "error_message": str(e),
                    "error_traceback": traceback.format_exc(),
                    "file_path": last_trace.filename if last_trace else "unknown",
                    "line_number": last_trace.lineno if last_trace else 0,
                    "method": last_trace.name if last_trace else "unknown",
                    "timestamp": datetime.now().isoformat(),
                    "attempt": attempt + 1,
                    "max_retries": max_retries
                }

                # Ejecutar capturadores de error en CADA fallo
                # Usamos el primer argumento de args como contexto (data)
                context = args[0] if args and isinstance(args[0], dict) else {}
                self._execute_error_capture(context, error_details)

                if attempt < max_retries and isinstance(e, retry_on_exceptions):
                    if self.verbose:
                        print(f"[RETRY] {name} failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                    time.sleep(retry_delay)
                else:
                    raise TaskError(str(e), Codes.TASK_FAILED) from e

        raise last_exception if last_exception else TaskError("Unknown error", Codes.TASK_FAILED)

    @staticmethod
    def _run_parallel_step(pipeline_instance, step_item, step_data, pipe_kwargs):
        """Helper static method to run a step in parallel, avoiding pickling issues."""
        try:
            # Re-importar si es necesario en un proceso nuevo
            return pipeline_instance._execute_step(step_item, step_data, **pipe_kwargs)
        except Exception as e:
            return {"error": f"Parallel execution error: {str(e)}"}

    def _execute_step(self, item: Any, data: dict, **kwargs: Any) -> dict:
        """
        Execute a single step and handle alert hooks.
        """
        parent_step_id = kwargs.get("parent_step_id")
        parallel_group = kwargs.get("parallel_group")

        if isinstance(item, Condition):
            if self.verbose:
                print(f"\n[CONDITION] Evaluating: {item.expression}")
            data, _ = self._run_branch([item], data, **kwargs)
            return data

        if isinstance(item, For):
            loop_data = data.copy()
            loop_data.pop("progress_rich", None)
            iteration = 0
            while True:
                loop_data["_loop_iteration"] = iteration
                if item.validation_expression:
                    if not item._evaluate_condition(loop_data):
                        break
                if item.iterations is not None and iteration >= item.iterations:
                    break
                for step in item.steps:
                    loop_data = self._execute_step(step, loop_data, **kwargs)
                    if "error" in loop_data:
                        break
                if "error" in loop_data:
                    break
                iteration += 1
            data.update(loop_data)
            return data

        if isinstance(item, Parallel):
            # Tracking del bloque Parallel como un nodo padre
            tracked_parallel_id = self._start_step_tracking(
                "Parallel Block", "v1.0", "parallel", data,
                parent_step_id=parent_step_id,
                parallel_group=parallel_group
            )

            # Limpiamos el contexto de objetos no serializables
            loop_data = data.copy()
            loop_data.pop("progress_rich", None)

            max_workers = item.max_workers or max(1, len(item.steps))
            results = []
            errors = []

            # Decidimos el ejecutor de forma explícita
            is_multiprocess = getattr(item, 'use_processes', False)
            ExecutorClass = ProcessPoolExecutor if is_multiprocess else ThreadPoolExecutor

            if self.verbose:
                mode = "PROCESSES" if is_multiprocess else "THREADS"
                print(f"\n[DEBUG] item.use_processes value: {getattr(item, 'use_processes', 'NOT_FOUND')}")
                print(f"[PARALLEL] Executing {len(item.steps)} steps using {mode} (workers={max_workers})")

            try:
                # El group ID para que el dashboard sepa que van juntos
                current_group = f"group_{tracked_parallel_id or 'none'}"

                with ExecutorClass(max_workers=max_workers) as executor:
                    if is_multiprocess:
                        # Para procesos usamos el método estático
                        futures = {
                            executor.submit(self._run_parallel_step, self, step, loop_data.copy(), {**kwargs, "parent_step_id": tracked_parallel_id, "parallel_group": current_group}): step
                            for step in item.steps
                        }
                    else:
                        # Para hilos, usamos una función local que captura self pero no requiere pickling
                        def _thread_worker(s, d):
                            return self._execute_step(s, d, **{**kwargs, "parent_step_id": tracked_parallel_id, "parallel_group": current_group})

                        futures = {
                            executor.submit(_thread_worker, step, loop_data.copy()): step
                            for step in item.steps
                        }

                    for future in as_completed(futures):
                        try:
                            res = future.result()
                            if res and "error" in res:
                                errors.append(res["error"])
                            elif res:
                                results.append(res)
                        except Exception as e:
                            errors.append(f"Execution error: {str(e)}")
            except Exception as e:
                data["error"] = f"Executor failure: {str(e)}"
                # Completar tracking con error
                self._end_step_tracking(tracked_parallel_id, None, data["error"])
                return data

            # Combinamos los resultados de todos los hilos/procesos
            for res in results:
                if isinstance(res, dict):
                    data.update({k: v for k, v in res.items() if k != "progress_rich"})

            if errors:
                data["error"] = " | ".join(errors)

            # Finalizar tracking del bloque parallel
            self._end_step_tracking(tracked_parallel_id, data if not errors else None, data.get("error"))

            return data

        func = None
        name = "unknown"
        version = "v1.0"
        step_id = None
        step_meta = {}

        if isinstance(item, tuple):
            if len(item) >= 3:
                func = item[0]
                name = item[1]
                version = item[2]
                if len(item) >= 4:
                    if isinstance(item[3], dict):
                        step_meta = item[3]
                    else:
                        step_id = item[3]
            else:
                return data
        elif callable(item):
            func = item
            name = getattr(item, "NAME", None) or getattr(item, "__name__", "task")
            version = getattr(item, "VERSION", "v1.0") or "v1.0"
            step_meta = getattr(item, "_wpipe_metadata", {})

        if func:
            self.task_name = name
            self.task_id = step_id
            tracked_step_id = self._start_step_tracking(
                name, version, "task", data,
                parent_step_id=parent_step_id,
                parallel_group=parallel_group
            )
            data["progress_rich"] = data.get("progress_rich") or self.progress_rich

            step_error = None
            step_error_trace = None
            try:
                # Pasar metadatos específicos del paso a _task_invoke
                current_kwargs = kwargs.copy()
                current_kwargs["__step_meta__"] = step_meta

                result_data = self._task_invoke(func, name, *(data,), **current_kwargs)
                if result_data is None:
                    result_data = {}

                if not isinstance(result_data, dict):
                    raise TaskError(
                        f"[ERROR] Result of '{name}' must be dict or None, got {type(result_data).__name__}",
                        Codes.TASK_FAILED
                    )

                data.update(result_data)
            except Exception as e:
                # El error ya fue procesado por _task_invoke (incluyendo capturadores)
                if self.continue_on_error:
                    data["error"] = str(e)
                else:
                    raise
            finally:
                alert_hooks = self._end_step_tracking(
                    tracked_step_id,
                    data if not step_error else None,
                    step_error,
                    step_error_trace,
                )
                data = self._handle_alert_hooks(alert_hooks, data)

            if self.verbose and not isinstance(item, (For, Condition)):
                print()

        return data

    def _run_branch(self, steps: list, data: dict, **kwargs: Any) -> tuple[dict, list]:
        """
        Execute a branch of steps.
        """
        executed_step_ids = []
        for item in steps:
            if isinstance(item, Condition):
                cond_name = getattr(item, "name", "condition") or "condition"
                cond_expr = getattr(item, "expression", "unknown")
                branch_taken = "true"
                error_message = None
                try:
                    branch_taken = "true" if item.evaluate(data) else "false"
                except Exception as e:
                    error_message = str(e)
                    branch_taken = "false"

                branch_executed = (
                    item.branch_true
                    if branch_taken == "true"
                    else (item.branch_false or [])
                )
                cond_step_id = None
                if self.tracker and self.pipeline_id:
                    self._step_order += 1
                    cond_step_id = self.tracker.start_step(
                        pipeline_id=self.pipeline_id,
                        step_order=self._step_order,
                        step_name=cond_name,
                        step_version="1.0.0",
                        step_type="condition",
                        input_data={"expression": cond_expr},
                    )

                data, branch_ids = self._run_branch(branch_executed, data, **kwargs)

                if cond_step_id and self.tracker:
                    executed_step_ids.append(cond_step_id)
                    executed_step_ids.extend(branch_ids)
                    alert_hooks = self.tracker.complete_step(
                        cond_step_id,
                        output_data={
                            "branch_taken": branch_taken,
                            "expression": cond_expr,
                        },
                        error_message=error_message,
                    )
                    data = self._handle_alert_hooks(alert_hooks, data)
            else:
                data = self._execute_step(item, data, **kwargs)
                if "error" in data:
                    break
        return data, executed_step_ids

    def _start_step_tracking(
        self,
        name: str,
        version: Optional[str] = None,
        step_type: str = "task",
        input_data: Optional[dict] = None,
        parent_step_id: Optional[int] = None,
        parallel_group: Optional[str] = None,
    ) -> Optional[int]:
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
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None,
        error_traceback: Optional[str] = None,
    ) -> list:
        if not self.tracker or not step_id:
            return []
        filtered_output = None
        if output_data:
            filtered_output = {
                k: v
                for k, v in output_data.items()
                if k not in ("progress_rich", "error") and not callable(v)
            }
        return self.tracker.complete_step(
            step_id=step_id,
            output_data=filtered_output,
            error_message=error_message,
            error_traceback=error_traceback,
            pipeline_id=self.pipeline_id,
        )

    def _handle_alert_hooks(self, hooks: list, data: dict) -> dict:
        if not hooks:
            return data
        if self.verbose:
            print(f"\n[ALERTS] Firing {len(hooks)} alert hooks...")
        for hook in hooks:
            try:
                data = self._execute_step(hook, data)
            except Exception as e:
                if self.verbose:
                    print(f"[ALERT HOOK ERROR] Hook failed: {e}")
        return data

    def _pipeline_run(self, *args: Any, **kwargs: Any) -> dict:
        data = args[0].copy() if args else {}
        checkpoint_mgr = kwargs.get("checkpoint_mgr")
        checkpoint_id = kwargs.get("checkpoint_id")

        # --- LÓGICA DE REANUDACIÓN NATIVA ---
        start_at_step = 0
        if (
            checkpoint_mgr
            and checkpoint_id
            and checkpoint_mgr.can_resume(checkpoint_id)
        ):
            last = checkpoint_mgr.get_last_checkpoint(checkpoint_id)
            data.update(last["data"] or {})
            start_at_step = last["step_order"] + 1
            if self.verbose:
                print(
                    f"\n[CHECKPOINT] Reanudando '{checkpoint_id}' desde el paso {start_at_step}"
                )

        error_message = None
        error_step = None
        metrics_collector = None

        if self.tracker:
            registration = self.tracker.register_pipeline(
                name=self.pipeline_name,
                steps=self.tasks_list,
                input_data=data,
                worker_id=self.worker_id,
                worker_name=self.worker_name,
                parent_pipeline_id=self.parent_pipeline_id,
            )
            self.pipeline_id = registration["pipeline_id"]
            self._step_order = start_at_step

            if self.verbose:
                print(f"\n[MATRÍCULA] Pipeline registered: {self.pipeline_id}")
                print(f"[MATRÍCULA] Config YAML: {registration['yaml_path']}")

            for event in self._pending_events:
                self.tracker.add_event(pipeline_id=self.pipeline_id, **event)
            self._pending_events = []

            if self._collect_system_metrics:
                metrics_collector = SystemMetricsCollector(
                    self.tracker, self.pipeline_id
                )
                metrics_collector.start()

        total_steps = len(self.tasks_list)

        def progress_bar_generator(size: int):
            # Si el usuario apaga la barra explícitamente, no la mostramos
            if not self.show_progress:
                for i in range(size):
                    yield i, None
                return

            # Si verbose está activo, Rich puede causar parpadeos, pero si el usuario
            # quiere ver el progreso, se lo permitimos.
            try:
                from wpipe.pipe.pipe import ProgressManager

                progress_manager = ProgressManager()
                with progress_manager as progress_rich_instance:
                    self.progress_rich = progress_rich_instance
                    task = progress_rich_instance.add_task(
                        f"[cyan][{self.worker_name}]{self.task_name}", total=size
                    )
                    for i in range(size):
                        yield i, progress_rich_instance
                        progress_rich_instance.update(task, advance=1)
            except (LiveError, ImportError):
                for i in tqdm(range(size), desc=self.task_name):
                    yield i, None

        # Limpiamos kwargs de parámetros técnicos antes de ejecutar pasos
        step_kwargs = kwargs.copy()
        step_kwargs.pop("checkpoint_mgr", None)
        step_kwargs.pop("checkpoint_id", None)

        try:
            # Evaluar checkpoints iniciales
            data = self._evaluate_checkpoints(data)

            for advance_id, progress in progress_bar_generator(size=total_steps):
                # SALTAR PASOS YA COMPLETADOS (RESUME)
                if advance_id < start_at_step:
                    continue

                item = self.tasks_list[advance_id]
                data["progress_rich"] = progress
                data = self._execute_step(item, data, **step_kwargs)

                # --- LIMPIEZA DE MEMORIA DE ERRORES ---
                # Si el paso ha terminado sin la llave 'error', garantizamos que
                # las variables de control de la pipeline reflejen éxito total.
                if "error" not in data:
                    error_message = None
                    error_step = None
                else:
                    # Solo si el error persiste tras reintentos y capturas, lo registramos
                    error_message = data.get("error")
                    error_step = getattr(item, "NAME", str(item))

                # Evaluar checkpoints después de cada paso
                data = self._evaluate_checkpoints(data)

                # GUARDAR PROGRESO AUTOMÁTICAMENTE
                if checkpoint_mgr and checkpoint_id and "error" not in data:
                    name = getattr(
                        item, "NAME", getattr(item, "__name__", f"step_{advance_id}")
                    )

                    # Limpiamos el contexto de objetos no serializables antes de guardar
                    checkpoint_data = data.copy()
                    checkpoint_data.pop("progress_rich", None)

                    checkpoint_mgr.save_checkpoint(
                        checkpoint_id, advance_id, name, "success", checkpoint_data
                    )

                if "error" in data:
                    if not self.continue_on_error:
                        break
                else:
                    # Recuperación exitosa: nos aseguramos de que el reporte final no vea errores
                    error_message = None
                    error_step = None
        except Exception as e:
            error_message = str(e)
            error_step = self.task_name
            if not self.continue_on_error:
                raise
        finally:
            data = self._execute_post_run_tasks(data)
            if metrics_collector:
                metrics_collector.stop()
            if self.tracker and self.pipeline_id:
                try:
                    alert_hooks = self.tracker.complete_pipeline(
                        pipeline_id=self.pipeline_id,
                        output_data=data if not error_message else None,
                        error_message=error_message,
                        error_step=error_step,
                    )
                    data = self._handle_alert_hooks(alert_hooks, data)
                except Exception as tracker_err:
                    if self.verbose:
                        print(f"\n[WARNING] Tracker completion failed: {tracker_err}")
                if self.verbose:
                    status = "ERROR" if error_message else "COMPLETED"
                    print(f"\n[MATRÍCULA] Pipeline {self.pipeline_id}: {status}")

            # Si terminó con éxito total, limpiamos el checkpoint
            if not error_message and checkpoint_mgr and checkpoint_id:
                checkpoint_mgr.clear_checkpoints(checkpoint_id)

        data.pop("progress_rich", None)
        return data

    def run(self, *args: Any, **kwargs: Any) -> dict:
        if "error" in (args[0] if args else {}):
            raise TaskError(
                f"[{self.task_name}] Initial data contains error", Codes.TASK_FAILED
            )
        return self._pipeline_run_with_report(*args, **kwargs)
