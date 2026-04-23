import os
import random
import json
import asyncio
from pathlib import Path
from dto.car import Car
from states.car_info_printer import CarInfoPrinter
from states.change_oil import change_oil
from states.drive import drive
from states.deflate_tires import deflate_tires
from states.preparation import preparation_phase
from states.refuel import refuel
from states.inflate_tires import inflate_tires
from states.print_fuel_level import print_fuel_level
from states.car_info_printer import nested_step

from wpipe import (
    Condition, 
    For, 
    Metric, 
    PipelineAsync, 
    Severity, 
    auto_dict_input, 
    PipelineExporter, 
    TaskTimer, 
    ResourceMonitor,
    step,
    Parallel,
    PipelineContext,
    object_to_dict
)

# Definimos el esquema de la Bodega (Contexto)
class ViajeContext(PipelineContext):
    marca: str
    modelo: str
    nivel_gasolina: str
    nivel_aceite: str
    nivel_neumaticos: str

# Definimos check_lights para que el bloque Parallel no falle por NameError
@step(name="check_lights", version="v1.0")
async def check_lights(d): 
    print("     * [ASYNC] Revisando lights traseras y delanteras... OK")
    await asyncio.sleep(0.01) # Simulación de trabajo I/O
    return d

@step(name="random_flat_tire", version="v1.0", retry_count=10, retry_delay=0)
async def random_flat_tire(d):
    if random.random() < 0.5:
        raise RuntimeError("Pinchazo aleatorio")
    return d

@step(name="notify_telegram_error", version="v1.0")
async def notify_telegram_error(context, error):
    print("\n" + "!" * 60)
    print("🚨 [ASYNC] ALERTA DE SISTEMA: ERROR DETECTADO")
    print("!" * 60)
    print(f"📍 ESTADO FALLIDO: {error['step_name']}")
    print(f"⚠️ MENSAJE: {error['error_message']}")
    print("-" * 60)
    return context

db_path = "wpipe_dashboard_async.db"

async def get_viaje_pipeline_async():
    trip = PipelineAsync(
        pipeline_name="viaje_async",
        verbose=True,
        tracking_db=db_path,
        max_retries=3,
        retry_delay=0,
        retry_on_exceptions=(RuntimeError,),
        collect_system_metrics=True,
        show_progress=True,
    )

    # Registro del capturador de errores
    trip.add_error_capture([notify_telegram_error])

    # Alerta de pipeline lento (>500ms)
    trip.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">500",
        severity=Severity.CRITICAL,
        steps=[CarInfoPrinter(">>> [ALERTA] Protocolo de rendimiento global activado")],
    )

    trip.add_event(
        event_type="notification",
        event_name="authorized_person",
        message="Results sent to external APIs",
        steps=[
            CarInfoPrinter(">>> [HOOK] El trip ha terminado, enviando resumen final..."),
        ],
    )

    trip.add_checkpoint(
        checkpoint_name="trip_start",
        expression="True",
        steps=[
            CarInfoPrinter(">>> [CHECKPOINT] Inicio del trip"),
        ],
    )

    trip.set_steps(
        [
            preparation_phase,
            For(
                iterations=3,
                steps=[
                    CarInfoPrinter(f"--- Nuevo trip asíncrono ---", "_loop_iteration"),
                    Parallel(
                        steps=[
                            refuel,
                            change_oil,
                            check_lights
                        ],
                        max_workers=3
                    ),
                    CarInfoPrinter("Resumen post-paralelo"),
                    (print_fuel_level, "Mostrar fuel", "v1.0"),
                    For(
                        validation_expression="nivel_gasolina != 'Vacío'",
                        steps=[
                            drive,
                            Condition(
                                expression="nivel_neumaticos == 'Bajo'",
                                branch_true=[
                                    nested_step,
                                    inflate_tires,
                                ],
                                branch_false=[deflate_tires],
                            ),
                            (print_fuel_level, "Mostrar fuel", "v1.0"),
                            random_flat_tire,
                        ],
                    ),
                ],
            ),
        ],
    )
    return trip

async def main():
    # Usamos ResourceMonitor para measure el consumption de hardware (RAM/CPU)
    with ResourceMonitor("Viaje_Completo_Async") as monitor:
        # Usamos TaskTimer para control de tiempos de ejecución
        with TaskTimer("viaje_pipeline_async", timeout_seconds=30) as timer:
            trip = await get_viaje_pipeline_async()

            @auto_dict_input
            async def run_pipeline(car_dict):
                return await trip.run(car_dict)

            car = Car(make="Toyota", model="Corolla")
            print(f"Carro inicial: {car.fuel_level}\n")
            results = await run_pipeline(car)

    # Resumen de recursos al terminar
    print(f"\nResource Summary (Async):")
    summary = monitor.get_summary()
    print(f"  - Peak RAM: {summary['peak_ram_mb']} MB")
    print(f"  - Avg CPU: {summary['avg_cpu_percent']}%")
    print(f"✓ Total time monitored: {timer.elapsed_seconds:.2f}s")

    print(f"\nViajes completados: {results.get('_loop_iteration')}")
    
    # --- ANÁLISIS DE DATOS ---
    analysis = trip.tracker.analysis
    stats = analysis.get_stats()
    print("\n" + "=" * 70)
    print("📊 ANÁLISIS DE RENDIMIENTO ASÍNCRONO")
    print("=" * 70)
    print(f"  - Total Ejecuciones: {stats['total_pipelines']}")
    print(f"  - Tasa de Éxito: {stats['success_rate']}%")

if __name__ == "__main__":
    asyncio.run(main())
