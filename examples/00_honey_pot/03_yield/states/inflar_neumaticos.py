from dto.car import Car, Niveles

from wpipe import step, to_obj


@step(name="inflar_neumaticos", version="v1.0")
@to_obj
def inflar_neumaticos(my_car: Car):
    return {
        "nivel_neumaticos": Niveles.alto,
        "marca": my_car.marca,
    }
