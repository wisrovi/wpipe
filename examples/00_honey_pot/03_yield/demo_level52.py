import os
import random
import json
import asyncio
from pathlib import Path
from dto.car import Car
from states import (
    Print_info,
    cambiar_aceite,
    conducir,
    desinflar_neumaticos,
    fase_preparacion,
    hechar_gasolina,
    inflar_neumaticos,
    print_gasolina,
    nested
)

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

# Definimos revisar_luces para que el bloque Parallel no falle por NameError
@step(name="revisar_luces", version="v1.0")
async def revisar_luces(d): 
    print("     * [ASYNC] Revisando luces traseras y delanteras... OK")
    await asyncio.sleep(0.01) # Simulación de trabajo I/O
    return d

@step(name="pinchazo_aleatorio", version="v1.0", retry_count=10, retry_delay=0)
async def pinchazo_aleatorio(d):
    if random.random() < 0.5:
        raise RuntimeError("Pinchazo aleatorio")
    return d

@step(name="notificar_telegram_error", version="v1.0")
async def notificar_telegram_error(context, error):
    print("\n" + "!" * 60)
    print("🚨 [ASYNC] ALERTA DE SISTEMA: ERROR DETECTADO")
    print("!" * 60)
    print(f"📍 ESTADO FALLIDO: {error['step_name']}")
    print(f"⚠️ MENSAJE: {error['error_message']}")
    print("-" * 60)
    return context

db_path = "wpipe_dashboard_async.db"

async def get_viaje_pipeline_async():
    viaje = PipelineAsync(
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
    viaje.add_error_capture([notificar_telegram_error])

    # Alerta de pipeline lento (>500ms)
    viaje.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">500",
        severity=Severity.CRITICAL,
        steps=[Print_info(">>> [ALERTA] Protocolo de rendimiento global activado")],
    )

    viaje.add_event(
        event_type="notification",
        event_name="authorized_person",
        message="Results sent to external APIs",
        steps=[
            Print_info(">>> [HOOK] El viaje ha terminado, enviando resumen final..."),
        ],
    )

    viaje.add_checkpoint(
        checkpoint_name="inicio_viaje",
        expression="True",
        steps=[
            Print_info(">>> [CHECKPOINT] Inicio del viaje"),
        ],
    )

    viaje.set_steps(
        [
            fase_preparacion,
            For(
                iterations=3,
                steps=[
                    Print_info(f"--- Nuevo viaje asíncrono ---", "_loop_iteration"),
                    Parallel(
                        steps=[
                            hechar_gasolina,
                            cambiar_aceite,
                            revisar_luces
                        ],
                        max_workers=3
                    ),
                    Print_info("Resumen post-paralelo"),
                    (print_gasolina, "Mostrar gasolina", "v1.0"),
                    For(
                        validation_expression="nivel_gasolina != 'Vacío'",
                        steps=[
                            conducir,
                            Condition(
                                expression="nivel_neumaticos == 'Bajo'",
                                branch_true=[
                                    nested,
                                    inflar_neumaticos,
                                ],
                                branch_false=[desinflar_neumaticos],
                            ),
                            (print_gasolina, "Mostrar gasolina", "v1.0"),
                            pinchazo_aleatorio,
                        ],
                    ),
                ],
            ),
        ],
    )
    return viaje

async def main():
    # Usamos ResourceMonitor para medir el consumo de hardware (RAM/CPU)
    with ResourceMonitor("Viaje_Completo_Async") as monitor:
        # Usamos TaskTimer para control de tiempos de ejecución
        with TaskTimer("viaje_pipeline_async", timeout_seconds=30) as timer:
            viaje = await get_viaje_pipeline_async()

            @auto_dict_input
            async def run_pipeline(car_dict):
                return await viaje.run(car_dict)

            car = Car(marca="Toyota", modelo="Corolla")
            print(f"Carro inicial: {car.nivel_gasolina}\n")
            results = await run_pipeline(car)

    # Resumen de recursos al terminar
    print(f"\nResource Summary (Async):")
    summary = monitor.get_summary()
    print(f"  - Peak RAM: {summary['peak_ram_mb']} MB")
    print(f"  - Avg CPU: {summary['avg_cpu_percent']}%")
    print(f"✓ Total time monitored: {timer.elapsed_seconds:.2f}s")

    print(f"\nViajes completados: {results.get('_loop_iteration')}")
    
    # --- ANÁLISIS DE DATOS ---
    analysis = viaje.tracker.analysis
    stats = analysis.get_stats()
    print("\n" + "=" * 70)
    print("📊 ANÁLISIS DE RENDIMIENTO ASÍNCRONO")
    print("=" * 70)
    print(f"  - Total Ejecuciones: {stats['total_pipelines']}")
    print(f"  - Tasa de Éxito: {stats['success_rate']}%")

if __name__ == "__main__":
    asyncio.run(main())
