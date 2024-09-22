import os
import time
import threading
from datetime import datetime

from wkafka.controller import Wkafka
from wpipe.pipe import Pipeline
from wpipe.util import escribir_yaml, leer_yaml
from wpipe.log import new_logger


"""
    eg. config.yaml
        name: Microservicio_1
        version: v1.0
        # kafka
        kafka_server: 192.168.1.60:9092
        # pipeline
        worker_id_file: worker_id.yaml # yaml 
        pipeline_use: true
        pipeline_server: http://192.168.1.60:8418
        pipeline_token_server: mysecrettoken
        # sqlite
        sqlite_db_name: register.db
"""


class Microservice:
    complete_steps = False

    def __init__(self, kafka_instance: Wkafka, config_file: str = "config.yaml"):
        # Leer la configuración
        self.config = leer_yaml(config_file)

        # Configurar atributos
        self.worker_id_file = self.config.get("worker_id_file", "worker_id.yaml")
        self.kafka_server = self.config.get("kafka_server", "192.168.1.60:9092")
        self.pipeline_use = self.config.get("pipeline_use", False)
        self.pipeline_server = self.config.get(
            "pipeline_server", "http://192.168.1.60:8418"
        )
        self.pipeline_token_server = self.config.get(
            "pipeline_token_server", "mysecrettoken"
        )
        self.stop_event = threading.Event()

        self.kafka_instance = kafka_instance

        # Iniciar logger
        os.makedirs("logs", exist_ok=True)
        self.logger = new_logger(
            process_name=self.config["name"], path_file="logs/file_{time}.log"
        )

        # Iniciar Pipeline
        self.pipeline_server_data = (
            {"base_url": self.pipeline_server, "token": self.pipeline_token_server}
            if self.pipeline_use
            else None
        )
        self.microservice = Pipeline(api_config=self.pipeline_server_data)

    def set_steps(self, steps: list):
        self.microservice.set_steps(steps)
        self.complete_steps = True

    def _worker_register(self, worker_id: dict = None):
        if not worker_id:
            worker_id = self.microservice.worker_register(
                name=self.config["name"], version=self.config["version"]
            )

        if worker_id and isinstance(worker_id, dict):
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worker_id["update"] = timestamp_str
            escribir_yaml(self.worker_id_file, worker_id)

    def _worker_healthchecker(self):
        while not self.stop_event.is_set():
            if not os.path.exists(self.worker_id_file):
                worker_id = self._worker_register()

            worker_id = leer_yaml(self.worker_id_file)

            if "id" in worker_id:
                self.microservice.set_worker_id(worker_id.get("id"))

            status = self.microservice.healthcheck_worker(worker_id)
            if isinstance(status, dict):
                if status["health"] == 0:
                    # Si falla el healthcheck, invocar un nuevo registro
                    os.remove(self.worker_id_file)
                    self.microservice.set_worker_id("-")
                else:
                    self._worker_register(worker_id)

            for _ in range(20):
                if not self.stop_event.is_set():
                    time.sleep(1)
                else:
                    break

    def start_healthchecker(self):
        if not self.complete_steps:
            raise Exception("Not step configured")

        if self.pipeline_use:

            self.healthchecker_thread = threading.Thread(
                target=self._worker_healthchecker
            )
            self.healthchecker_thread.start()
            # Se da tiempo para el registro y el primer healthcheck
            time.sleep(20)

        self.logger.info("[MICROSERVICE] Process started")

    def wait(self):
        if not self.pipeline_use:
            return

        self.healthchecker_thread.join()

    def run(self, data: dict):
        return self.microservice.run(data)

    def stop_healthchecker(self):
        if not self.pipeline_use:
            return

        self.stop_event.set()
