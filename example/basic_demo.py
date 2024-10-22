import time
from functools import lru_cache

from wpipe.pipe.pipe import Pipeline
from wpipe.exception.api_error import ProcessError


SLEEP = 0.0001


# Definición de funciones externas que reciben y devuelven parámetros
# @lru_cache(maxsize=1024)
def funcion_1(data: dict):

    x = data["x"]

    time.sleep(SLEEP)

    # print("\t", f"Función 1 ejecutada con {x}")

    return {"x1": x + 1}


# @lru_cache(maxsize=1024)
def funcion_2(data: dict):

    x1 = data["x1"]

    time.sleep(SLEEP)

    # print("\t", f"Función 2 ejecutada con {x1}")

    return {
        "x2": x1 + 1,
    }


# @lru_cache(maxsize=1024)
def funcion_3(data: dict):

    x1 = data["x1"]
    x2 = data["x2"]

    time.sleep(SLEEP)

    # print("\t", f"Función 3 ejecutada con {x1} y {x2}")

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


demo_microservice = Pipeline(
    api_config={"base_url": "http://localhost:8418", "token": "mysecrettoken"},
    # api_config={"base_url": "http://192.168.1.60:8418", "token": "mysecrettoken"},
)
demo_microservice.set_steps(
    [
        (funcion_1, "Primera_Funcion", "v1.0"),
        (funcion_2, "Segunda_Funcion", "v1.0"),
        (funcion_3, "Tercera_funcion", "v1.0"),
    ]
)  # Asigna una lista de funciones al objeto


demo2_microservice = Pipeline(
    api_config={"base_url": "http://localhost:8418", "token": "mysecrettoken"},
    # api_config={"base_url": "http://192.168.1.60:8418", "token": "mysecrettoken"},
)
demo2_microservice.set_steps(
    [
        (demo_microservice.run, "pipeline_into_pipeline", "v1.0"),        
        (Demo(), "Cuarta_funcion", "v1.0"),
    ]
)  # Asigna una lista de funciones al objeto


if __name__ == "__main__":
    try:
        resultado_final = demo2_microservice.run(dict(x=5, y="a"))

        print(f"Resultado final: {resultado_final}")
    except ProcessError as error:
        print(error)
