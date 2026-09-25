from dto.car import Car, Niveles

from wpipe import PipelineContext, step, timeout_sync, to_obj


# Esquema dummy para evitar errores de importación
class ViajeContext(PipelineContext):
    marca: str
    modelo: str
    nivel_gasolina: str
    nivel_aceite: str
    nivel_neumaticos: str


@timeout_sync(seconds=2)
@step(name="HecharGasolina", version="v1.0", parallel=True)
@to_obj(ViajeContext)
def hechar_gasolina(my_car: Car):
    return {
        "nivel_gasolina": Niveles.alto,
        "marca": my_car.marca,
    }
