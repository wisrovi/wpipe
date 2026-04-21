from wpipe import Condition, For, Pipeline

from dto.car import Car, Niveles
from states import (
    HecharGasolina,
    cambiar_aceite,
    conducir,
    desinflar_neumaticos,
    inflar_neumaticos,
)
from utils.dict2obj import to_obj
from utils.obj2dict import auto_dict_input
from utils.states import state


def main():
    db_path = "wpipe_dashboard.db"
    config_dir = "configs"

    viaje = Pipeline(
        pipeline_name="viaje",
        verbose=False,
        tracking_db=db_path,
        config_dir=config_dir,
    )

    viaje.add_event(
        event_type="notification",
        event_name="authorized_person",
        message="Results sent to external APIs",
    )

    viaje.set_steps(
        [
            (HecharGasolina, "HecharGasolina", "v1.0"),
            (cambiar_aceite, cambiar_aceite.NAME, cambiar_aceite.VERSION),
            (
                For(
                    validation_expression="nivel_gasolina != 'Vacío'",
                    steps=[
                        (conducir, conducir.NAME, conducir.VERSION),
                        (
                            Condition(
                                expression="nivel_neumaticos == 'Bajo'",
                                branch_true=[
                                    (
                                        inflar_neumaticos,
                                        inflar_neumaticos.NAME,
                                        inflar_neumaticos.VERSION,
                                    ),
                                ],
                                branch_false=[
                                    (
                                        desinflar_neumaticos,
                                        desinflar_neumaticos.NAME,
                                        desinflar_neumaticos.VERSION,
                                    ),
                                ],
                            )
                        ),
                        (
                            lambda my_car: print(
                                f"Nivel de gasolina: {my_car.nivel_gasolina}"
                            ),
                            "print_nivel_gasolina",
                            "v1.0",
                        ),
                    ],
                )
            ),
            (lambda my_car: print("Viaje terminado"), "print_viaje_terminado", "v1.0"),
        ]
    )

    @auto_dict_input
    def run(args_dict):
        return viaje.run(args_dict)

    results = run(Car(marca="Toyota", modelo="Corolla"))
    print(results)
    results = run({"marca": "Toyota", "modelo": "Corolla"})
    print(results)


if __name__ == "__main__":
    main()
