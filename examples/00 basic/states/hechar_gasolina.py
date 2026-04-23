from dto.car import Car, Niveles
from wpipe import Condition, For, Pipeline, step
from utils.dict2obj import to_obj


@step(name="HecharGasolina", version="v1.0")
@to_obj
def hechar_gasolina(my_car: Car):
    return {
        "nivel_gasolina": Niveles.alto,
        "marca": my_car.marca,
    }


HecharGasolina = hechar_gasolina
