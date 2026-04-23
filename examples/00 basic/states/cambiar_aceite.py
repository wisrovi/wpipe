from dto.car import Car, Niveles
from utils.dict2obj import to_obj
from utils.states import state


@state(name="cambiar_aceite", version="v1.0")
@to_obj
def cambiar_aceite(my_car: Car):
    return {
        "nivel_aceite": Niveles.alto,
        "marca": my_car.marca,
    }
