from wkafka.controller import Wkafka
from wpipe.sqlite.Wsqlite import Wsqlite
from wpipe.util.utils import leer_yaml

from microservice import Microservice
import time


SLEEP = 0.0001
SLEEP = 1


def funcion_1(data: dict):

    assert "x" in data, "var not found"

    x = data["x"]

    time.sleep(SLEEP)

    # print(f"Función 1 ejecutada con {x}")

    return {"x1": x + 1}


# @lru_cache(maxsize=1024)
def funcion_2(data: dict):

    x1 = data["x1"]

    time.sleep(SLEEP)

    # print(f"Función 2 ejecutada con {x1}")

    return {
        "x2": x1 + 1,
    }


# @lru_cache(maxsize=1024)
def funcion_3(data: dict):

    x1 = data["x1"]
    x2 = data["x2"]

    time.sleep(SLEEP)

    # print(f"Función 3 ejecutada con {x1} y {x2}")

    return {
        "x3": x1 + x2,
    }


class Demo:
    # @lru_cache(maxsize=1024)
    def __call__(self, data: dict):

        x1 = data["x1"]
        x3 = data["x3"]

        time.sleep(SLEEP)

        return {
            "x4": x1 * x3,
        }


config_file = "config.yaml"
CONFIG = leer_yaml(config_file)

# Iniciar Kafka
kafka_instance = Wkafka(server=CONFIG["kafka_server"], name=CONFIG["name"])
microservice = Microservice(kafka_instance, config_file=config_file)

# Configurar estados a usar
microservice.set_steps(
    [
        (funcion_1, "Primera_Funcion", "v1.0"),
        (funcion_2, "Segunda_Funcion", "v1.0"),
        (funcion_3, "Tercera_funcion", "v1.0"),
        (Demo(), "Cuarta_funcion", "v1.0"),
    ]
)


# set received events of kafka for topic mi_tema and key clave1
@kafka_instance.consumer(
    topic="mi_tema",
    value_convert_to="json",
    key_filter="clave1",
)
def process_message(data):
    print(f"Mensaje recibido: {data.value}, con clave: {data.key}")

    args_dict = data.value

    # datos extras como: response_to y otros datos importantes del mensaje
    header = data.header

    # separar los datos importantes de entrada para guardarlos en la DB
    data_input = {"mensaje": args_dict["mensaje"], "topic": data.topic}

    # set results
    results = {}

    with Wsqlite(db_name=CONFIG["sqlite_db_name"]) as db:
        db.input = data_input

        """
        # NO usar print sino el logger
        # eg.
        #    logger.info
        #    logger.error
        #    logger.warning
        #    logger.debug
        """

        microservice.logger.info(
            f"Mensaje recibido: {data.value}, con clave: {data.key}"
        )

        final_result = microservice.run(data.value)
        results = (
            final_result.get("results")
            if "error" not in final_result
            else final_result["error"]
        )

        # si hay errores se guardan en la base de datos para posterior analisis
        if "error" in final_result:
            db.details = {"error": final_result["error"]}  # optional

        # guardo los resultados, se debe ser meticulo para guardar solo lo escencial
        db.output = {"results": results}

    # despues de procesar el pipeline, se enviar la respuesta por kafka al destinatario definido
    if "response_to" in header:
        results = {"results": results}
        with kafka_instance.producer() as producer:
            producer.async_send(
                topic=header["response_to"],
                value=results,
                key=data.key,  # se usa la misma key de entrada para responder
                value_type="json",
            )


if __name__ == "__main__":
    microservice.start_healthchecker()
    kafka_instance.run_consumers()
    microservice.wait()
