from wpipe import For, Pipeline, state, to_obj

from dto.car import Car, Niveles
from states import (
    hechar_gasolina,
    cambiar_aceite,
    conducir,
)


@to_obj
def print_gasolina(data):
    print(f"    Nivel gasolina: {data.nivel_gasolina}")
    return {}


def main():
    viaje = Pipeline(
        pipeline_name="viaje",
        verbose=False,
    )

    viaje.set_steps(
        [
            For(
                iterations=3,
                steps=[
                    (hechar_gasolina, "Llenar gasolina", "v1.0"),
                    (cambiar_aceite, "Cambiar aceite", "v1.0"),
                    (print_gasolina, "Mostrar gasolina", "v1.0"),
                    For(
                        validation_expression="nivel_gasolina != 'Vacío'",
                        steps=[
                            (conducir, "Conducir", "v1.0"),
                            (print_gasolina, "Mostrar gasolina", "v1.0"),
                        ],
                    ),
                ],
            )
        ],
    )

    car = Car(marca="Toyota", modelo="Corolla")
    print(f"Carro inicial: {car.nivel_gasolina}\n")

    results = viaje.run(car.model_dump())

    print(f"\nViajes completados: {results.get('_loop_iteration')}")
    print(f"Gasolina final: {results.get('nivel_gasolina')}")
    print(f"Aceite final: {results.get('nivel_aceite')}")


if __name__ == "__main__":
    main()
