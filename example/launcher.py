import os
import time
import threading
from tqdm import tqdm
from datetime import datetime
from demo_microservice import demo_microservice
from wpipe.util.utils import escribir_yaml, leer_yaml
from wpipe.sqlite.Wsqlite import Wsqlite
from wpipe.log.log import new_logger


CWD = os.getcwd()
WORKER_ID_FILE = f"{CWD}/worker_id.yaml"
microservice_config = leer_yaml("data.yaml")
logger = new_logger(process_name="microservicio_1", path_file="file_{time}.log")


# Evento global para controlar la finalización de los hilos
stop_event = threading.Event()
worker_id = None


def worker_register(worker_id: dict = None):
    if not worker_id:
        worker_id = demo_microservice.worker_register(
            name=microservice_config["name"], version=microservice_config["version"]
        )
    if worker_id and isinstance(worker_id, dict):
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_datetime = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        worker_id["update"] = timestamp_str

        escribir_yaml(WORKER_ID_FILE, worker_id)


def worker_healthchecker():
    global worker_id

    while not stop_event.is_set():
        if not os.path.exists(WORKER_ID_FILE):
            worker_register()
            worker_id = leer_yaml(WORKER_ID_FILE)

        demo_microservice.set_worker_id(worker_id.get("id"))

        status = demo_microservice.healthcheck_worker(worker_id)
        if isinstance(status, dict):
            if status["health"] == 0:
                os.remove(WORKER_ID_FILE)
                demo_microservice.set_worker_id("-")
            else:
                worker_register(worker_id)
        # print(status)

        time.sleep(20)


def kafka_event(data: dict):
    with Wsqlite(db_name="register.db") as db:
        db.input = {"x1": 1, "x2": 5}

        # print("\n" * 3, "-" * 100, "\n", "[KAFKA EMULATOR] new data received")
        resultado_final = demo_microservice.run(data)

        logger.info(f"[KAFKA EMULATOR] Resultado final: {resultado_final}")

        db.output = {"X": 4, "Y": 3, "Z": 2}
        db.details = {"status": "ok"}  # optional


def worker(data: dict = {}):
    # se espera un tiempo para que el "healthcheck_worker" inicie la primera comunicacion
    time.sleep(20)

    # aca se inician los procesos de kafka, y cualquier otro proceso del WORKER
    for i in tqdm(range(1), desc="Emulando worker", unit="kafka_msg"):
        kafka_event(dict(x=5, y="a"))

    stop_event.set()


if __name__ == "__main__":
    worker_id = leer_yaml(WORKER_ID_FILE)

    healthchecker_thread = threading.Thread(target=worker_healthchecker)

    workers = []
    for _ in range(1):
        worker_thread = threading.Thread(target=worker, args=({},))
        workers.append(worker_thread)

    # Iniciar ambos hilos
    healthchecker_thread.start()
    for _worker in workers:
        _worker.start()

    # Esperar a que ambos hilos terminen
    healthchecker_thread.join()
    for _worker in workers:
        _worker.join()

    print("Todos los procesos se han detenido.")
