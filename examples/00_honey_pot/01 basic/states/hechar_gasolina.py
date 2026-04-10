from wpipe import Condition, For, Pipeline, state, to_obj, timeout_sync

from dto.car import Car, Niveles


@timeout_sync(seconds=2)
@state(name="HecharGasolina", version="v1.0")
@to_obj
def hechar_gasolina(my_car: Car):
    return {
        "nivel_gasolina": Niveles.alto,
        "marca": my_car.marca,
    }
