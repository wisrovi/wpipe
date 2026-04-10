from dto.car import Car
from states import (
    cambiar_aceite,
    conducir,
    desinflar_neumaticos,
    hechar_gasolina,
    inflar_neumaticos,
    Print_info,
    print_gasolina,
    fase_preparacion,
)

from wpipe import (
    Condition,
    For,
    Metric,
    Pipeline,
    Severity,
    auto_dict_input,
)


def get_viaje_pipeline():
    viaje = Pipeline(
        pipeline_name="viaje", verbose=False, tracking_db="wpipe_dashboard.db",
        # 
        max_retries=3,  # Retry up to 3 times
        retry_delay=0.5,  # Wait 0.5 seconds between retries
        retry_on_exceptions=(RuntimeError,),  # Only retry on RuntimeError
        # 
        collect_system_metrics=True,  # Enable metrics collection
    )

    # NUEVA SINTAXIS SIMPLIFICADA
    # Alerta de pipeline lento (>500ms)
    viaje.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">500",
        severity=Severity.CRITICAL,
        steps=[Print_info(">>> [ALERTA] Protocolo de rendimiento global activado")],
    )

    # Alerta de paso lento (>1ms)
    viaje.tracker.add_alert_threshold(
        metric=Metric.STEP_DURATION,
        expression=">1000",
        severity=Severity.WARNING,
        steps=[(lambda d: print(">>> [ALERTA] Paso lento detectado"), "Audit", "v1.0")],
    )

    viaje.add_event(
        event_type="notification",
        event_name="authorized_person",
        message="Results sent to external APIs",
        steps=[
            Print_info(">>> [HOOK] El viaje ha terminado, enviando resumen final..."),
        ],
    )

    viaje.set_steps(
        [
            fase_preparacion,
            For(
                iterations=3,
                steps=[
                    Print_info(f"--- Nuevo viaje ---", "_loop_iteration"),
                    hechar_gasolina,
                    cambiar_aceite,
                    (print_gasolina, "Mostrar gasolina", "v1.0"),
                    For(
                        validation_expression="nivel_gasolina != 'Vacío'",
                        steps=[
                            conducir,
                            Condition(
                                expression="nivel_neumaticos == 'Bajo'",
                                branch_true=[
                                    Print_info("     * inflando neumaticos..."),
                                    inflar_neumaticos,
                                ],
                                branch_false=[desinflar_neumaticos],
                            ),
                            (print_gasolina, "Mostrar gasolina", "v1.0"),
                        ],
                    ),
                ],
            ),
        ],
    )
    return viaje


def main():
    viaje = get_viaje_pipeline()

    @auto_dict_input
    def run_pipeline(car_dict):
        return viaje.run(car_dict)

    car = Car(marca="Toyota", modelo="Corolla")
    print(f"Carro inicial: {car.nivel_gasolina}\n")
    results = run_pipeline(car)

    print(f"\nViajes completados: {results.get('_loop_iteration')}")
    print(f"Gasolina final: {results.get('nivel_gasolina')}")
    print(f"Aceite final: {results.get('nivel_aceite')}")


if __name__ == "__main__":
    main()
