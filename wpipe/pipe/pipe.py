import json
import time
import traceback

from prefect import flow, task
from rich.errors import LiveError
from rich.progress import Progress
from tqdm import tqdm

from wpipe.api_client.api_client import APIClient
from wpipe.exception import ApiError, Codes, ProcessError, TaskError
from wpipe.exception.api_error import TaskError
from build.lib.wpipe.exception.api_error import logger


class ProgressManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.progress = Progress()
        return cls._instance

    def __enter__(self):
        self.progress.__enter__()
        return self.progress

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.__exit__(exc_type, exc_val, exc_tb)


# Definición de la clase
class Pipeline(APIClient):
    worker_id: str = None
    worker_name: str = "worker"
    verbose: bool = False
    task_id: str = None

    process_id: str = None
    send_to_api: bool = False
    api_config: dict = None
    tasks_list: list = []

    SHOW_API_ERRORS = False

    task_name: str = "Processing pipeline tasks"
    progress_rich: Progress = None

    def __init__(
        self,
        worker_id: str = None,
        worker_name: str = None,
        api_config: dict = None,
        verbose: bool = False,
    ):
        if api_config:
            # invoca el constructor de APIClient
            super().__init__(
                base_url=api_config.get("base_url"), token=api_config.get("token")
            )
            self.api_config = api_config

        if worker_id:
            self.set_worker_id(worker_id)

        if worker_name:
            self.worker_name = worker_name

        self.verbose = verbose

    def set_worker_id(self, id: str):
        if id and isinstance(id, str):
            if len(id) > 5:
                if self.api_config and not self.worker_id:
                    self.send_to_api = True
                    print("[INFO] worker_id defined correct")

                self.worker_id = id
            else:
                self.worker_id = None
        else:
            raise Exception(f"[ERROR] {id} is not correct, have to be a string")

    def worker_register(self, name: str, version: str):
        data = {
            "name": name,
            "version": version,
            "tasks": [
                {
                    "name": name,
                    "version": version,
                }
                for func, name, version, _id in self.tasks_list
            ],
        }

        if self.api_config:
            worker_id = self.register_worker(data)

            if worker_id and "id" in worker_id:
                self.set_worker_id(worker_id.get("id"))

                return worker_id

    def _api_task_update(self, msg: dict):
        if self.send_to_api:
            try:
                task_updated = self.update_task(msg)
                if self.verbose:
                    print(
                        f"[task] [ERROR] '{self.task_name}': {task_updated}",
                    )
            except:
                print("Problem update task")
                if self.SHOW_API_ERRORS:
                    raise ApiError("Problem update task", Codes.UPDATE_TASK)

    def _api_process_update(self, msg: dict, start: bool = False):
        if self.send_to_api:
            try:
                if start:
                    process_registed = self.register_process(msg)

                    self.tasks_list = [
                        (rta[0], rta[1], rta[2], son["id"])
                        for son, rta in zip(process_registed["sons"], self.tasks_list)
                    ]

                    self.process_id = process_registed["father"]

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
            except:
                print("Problem update Process")
                if self.SHOW_API_ERRORS:
                    raise ApiError("Problem update Process", Codes.UPDATE_PROCESS_ERROR)

    def _decorator_task_report(func):
        """Decorador para reportar la ejecución de cada tarea."""

        def wrapper(self, *args, **kwargs):

            self._api_task_update({"task_id": self.task_id, "status": "start"})

            resultado = {}
            try:
                if isinstance(func, Pipeline):
                    resultado = func.run(self, *args, **kwargs)
                else:
                    resultado = func(self, *args, **kwargs)

                self._api_task_update({"task_id": self.task_id, "status": "success"})
            except Exception as e:
                errors_traceback = traceback.extract_tb(e.__traceback__)

                errors_list = []
                for error_traceback in errors_traceback:
                    errors_list.append(
                        {
                            "file": error_traceback.filename,
                            "line": error_traceback.lineno,
                            "method": error_traceback.name,
                        }
                    )

                error = {
                    "task_name": self.task_name,
                    "error_traceback": errors_list,
                    "error_message": str(e),  # Agrega el mensaje del error
                    "task_id": self.task_id,
                }

                resultado["error"] = error["error_message"]

                self._api_task_update(
                    {
                        "task_id": self.task_id,
                        "status": "error",
                        "details": json.dumps(error),
                    }
                )

                if self.verbose:
                    for error in errors_list:
                        logger.error(error)

                raise TaskError(error, Codes.TASK_FAILED)

            return resultado

        return wrapper

    def _decorator_pipeline_report(func):
        """Decorador para reportar la ejecución del pipeline completo."""

        def wrapper(self, *args, **kwargs):

            worker_id = self.worker_id

            if self.verbose:
                print("\n", "\t", "*" * 50)
                print("\n", f"\t [WORKER] {self.worker_id}")
                print("\n\t", "*" * 50)

            self._api_process_update({"id": worker_id}, start=True)

            resultado = {}
            try:
                resultado = func(self, *args, **kwargs)

                self._api_process_update({"id": self.process_id, "details": ""})
            except TaskError as te:
                error = te.args[0]

                error["process_name"] = self.process_id
                error["worker_id"] = self.worker_id
                error["worker_name"] = self.worker_name or "worker"
                error["task_name"] = self.task_name
                error["task_id"] = self.task_id

                self._api_process_update(
                    {"id": self.process_id, "details": json.dumps(error)}
                )
                # logger.error(error)
                raise ProcessError(error, Codes.TASK_FAILED)
            except ApiError as ae:
                raise ApiError(str(ae), Codes.API_ERROR)

            return resultado

        return wrapper

    def set_steps(self, lista):
        """
        Define los pasos del pipeline, verificando que cada elemento sea una tupla
        compuesta por una función y un nombre en string.
        """

        new_list = []

        for item in lista:
            if not (
                isinstance(item, tuple)
                and len(item) == 3
                and callable(item[0])
                and isinstance(item[1], str)
            ):
                raise ValueError(
                    "Cada elemento de la lista debe ser una tupla (función, nombre)."
                )
            else:
                new_list.append((item[0], item[1], item[2], ""))

        self.tasks_list = new_list

    @_decorator_task_report
    def _task_invoke(self, func, name, *args, **kwargs):
        return func(*args, **kwargs)

    @_decorator_pipeline_report
    def run(self, *args, **kwargs):
        """
        Ejecuta el pipeline completo, pasando los resultados de una función como
        entrada a la siguiente.
        """

        resultado = None
        data = {}

        def ProgressBar(size: int):
            try:
                advance_id = 0
                progress_manager = ProgressManager()

                with progress_manager as progress_rich:
                    self.progress_rich = progress_rich

                    task = progress_rich.add_task(
                        f"[cyan][{self.worker_name}]{self.task_name}", total=size
                    )
                    while not progress_rich.finished:
                        progress_rich.update(
                            task,
                            description=f"[cyan][{self.worker_name}]{self.task_name}",
                        )

                        yield advance_id, progress_rich

                        advance_id += 1
                        progress_rich.update(task, advance=1)
            except LiveError as e:
                for advance_id in tqdm(
                    range(size),
                    desc=f"{self.task_name}",
                    unit="steps",
                ):
                    yield advance_id, None

        for advance_id, progress in ProgressBar(size=len(self.tasks_list)):
            if advance_id >= len(self.tasks_list):
                return data

            (func, name, version, _id) = self.tasks_list[advance_id]

            self.task_name = name
            self.task_id = _id
            self.progress_rich = progress

            data.update(args[0])

            if advance_id == 0:
                data.update({"progress_rich": progress})
                resultado = self._task_invoke(func, name, *(data,), **kwargs)
            else:
                resultado = self._task_invoke(func, name, *(data,), **kwargs)

            assert isinstance(
                resultado, dict
            ), f"[ERROR] The result of state ({self.task_name}) on pipeline have to a dict"

            data.update(resultado)

            if self.verbose:
                print()

            if "error" in data:
                break

        if "error" in data:
            raise TaskError(
                f"[{self.task_name}] Fail the pipeline:{data['error']}",
                Codes.TASK_FAILED,
            )

        # remove the progress_rich from the data
        data.pop("progress_rich", None)

        return data
