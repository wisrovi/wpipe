from wkafka.controller import Wkafka
from wpipe.sqlite import Wsqlite
from wpipe.exception import ProcessError
from wpipe.util import leer_yaml

from microservice import Microservice

from steps import funcion_1, funcion_2, funcion_3, Demo


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
        microservice.logger.info(f"New msg: {data.value}, con clave: {data.key}")

        try:
            final_result = microservice.run(data.value)

            # preparo la respuesta segun el pipeline
            results = final_result.get("x4")

            # guardo los resultados, se debe ser meticulo para guardar solo lo escencial
            db.output = {"results": results}
        except ProcessError as e:
            microservice.logger.error(f"Error: {str(e)}")
            # si hay errores se guardan en la base de datos para posterior analisis
            results = {"error": str(e)}
            db.details = results  # optional

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

    microservice.logger.info(f"Kafka event receiver started")
    microservice.wait()
