from dto.car import Car, Niveles

from wpipe import state, to_obj


@state(name="cambiar_aceite", version="v1.0")
@to_obj
def cambiar_aceite(my_car: Car):
    return {
        "nivel_aceite": Niveles.alto,
        "marca": my_car.marca,
    }
