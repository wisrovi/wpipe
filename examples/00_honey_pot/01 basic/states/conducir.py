from dto.car import Car, Niveles
from wpipe import to_obj
from wpipe import state


@state(name="conducir", version="v1.0")
@to_obj
def conducir(my_car: Car):
    if my_car.nivel_gasolina == Niveles.alto:
        my_car.nivel_gasolina = Niveles.medio
    elif my_car.nivel_gasolina == Niveles.medio:
        my_car.nivel_gasolina = Niveles.bajo
    elif my_car.nivel_gasolina == Niveles.bajo:
        my_car.nivel_gasolina = Niveles.vacio

    return {
        "nivel_gasolina": my_car.nivel_gasolina,
        "nivel_aceite": Niveles.bajo,
        "marca": my_car.marca,
    }
