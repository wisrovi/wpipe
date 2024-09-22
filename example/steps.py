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
        a = data["a"]

        time.sleep(SLEEP)

        return {
            "x4": x1 * x3 * a,
        }
