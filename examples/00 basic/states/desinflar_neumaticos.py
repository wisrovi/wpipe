from dto.car import Car, Niveles
from utils.states import state
from utils.dict2obj import to_obj


@state(name="desinflar_neumaticos", version="v1.0")
@to_obj
def desinflar_neumaticos(my_car: Car):
    if my_car.nivel_neumaticos == Niveles.alto:
        my_car.nivel_neumaticos = Niveles.medio
    elif my_car.nivel_neumaticos == Niveles.medio:
        my_car.nivel_neumaticos = Niveles.bajo
    elif my_car.nivel_neumaticos == Niveles.bajo:
        my_car.nivel_neumaticos = Niveles.vacio

    return {
        "nivel_neumaticos": my_car.nivel_neumaticos,
        "marca": my_car.marca,
    }

