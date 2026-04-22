from dto.car import Car, Niveles

from wpipe import step, timeout_sync, to_obj


@step(name="conducir", version="v1.0", timeout=10, description="Conducir el coche" , tags=["viaje", "coche"], retry_count=3, retry_delay=0.01)
@timeout_sync(seconds=2)
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
