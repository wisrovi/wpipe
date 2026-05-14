import os
import random
import tempfile
import threading
from datetime import datetime
from pathlib import Path

# Tracking start time for performance verification
start_time_global = datetime.now()

import cv2

# Efficient imports using WPipe Lazy Loading
from dto.car import Car
from states import (
    Print_info,
    cambiar_aceite,
    conducir,
    desinflar_neumaticos,
    fase_preparacion,
    hechar_gasolina,
    inflar_neumaticos,
    nested,
    print_gasolina,
)
from utils.export import exporter_data

from wpipe import (
    Condition,
    For,
    Metric,
    Parallel,
    Pipeline,
    PipelineContext,
    ResourceMonitor,
    Severity,
    TaskTimer,
    auto_dict_input,
    object_to_dict,
    step,
)
from wpipe.pipe.components.logic_blocks import Background
from wpipe.sqlite import Wsqlite


@step(name="revisar_luces", version="v1.0")
def revisar_luces(d):
    """Simple check task."""
    return d


@step(name="pinchazo_aleatorio", version="v1.0", retry_count=10, retry_delay=0.01)
def pinchazo_aleatorio(d):
    """Simulates a random flat tire with high retry capability."""
    if random.random() < 0.3:
        raise RuntimeError("Pinchazo aleatorio detectado")
    return d


@step(name="notificar_telegram_error", version="v1.0")
def notificar_telegram_error(context, error):
    """
    Simula el envío de una notificación detallada a Telegram.
    Recibe el contexto y los detalles técnicos del error.
    """
    print("\n" + "!" * 60)
    print("🚨 ALERTA DE SISTEMA: ERROR DETECTADO")
    print("!" * 60)
    print(f"📍 ESTADO FALLIDO: {error['step_name']}")
    print(f"📄 ARCHIVO: {error['file_path']}")
    print(f"🔢 LÍNEA: {error['line_number']}")
    print(f"⚠️ MENSAJE: {error['error_message']}")
    print("-" * 60)
    # print("🔍 INFO DE LA BODEGA (CONTEXTO):")
    # print(
    #     f"   Modelo: {context.get('modelo')} | Gasolina: {context.get('nivel_gasolina')}"
    # )
    # print("-" * 60)
    # Aquí podrías usar requests.post para enviar el mensaje real
    return context


@step(name="log_background", version="v1.0")
def log_background(data):
    """Simulated background logging task - runs without blocking pipeline."""
    import time

    print("[BACKGROUND] Logging task started...")
    time.sleep(5)  # Reduced for validation
    print("[BACKGROUND] Logging task completed!")
    return {}


def create_complex_handler():
    class InternalSystemHandler:
        """
        A class defined inside a function scope.
        It manages a threading lock and an open temporary file.
        """

        def __init__(self):
            # Reason 1: Locks are tied to the OS process state
            self.lock = threading.Lock()
            # Reason 2: File handles are specific OS descriptors
            self.resource = tempfile.NamedTemporaryFile(mode="w+")
            self.data = "Sensitive Runtime State"

        def __repr__(self):
            return "<InternalSystemHandler active>"

    return InternalSystemHandler()


db_path = "output/wpipe_dashboard.db"


def get_viaje_pipeline():
    """Builds the complex travel pipeline with nested logic."""
    viaje = Pipeline(
        pipeline_name="viaje_pot",
        verbose=False,
        tracking_db=db_path,
        max_retries=3,
        retry_delay=0,
        retry_on_exceptions=(RuntimeError,),
        collect_system_metrics=False,  # Performance optimization
        show_progress=True,
    )

    # Registro del capturador de errores
    viaje.add_error_capture([notificar_telegram_error])

    # Global alerts
    viaje.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">1000",  # Warn if total takes >1s
        severity=Severity.WARNING,
        steps=[Print_info(">>> [PERFORMANCE ALERT] Pipeline execution slow")],
    )
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

    viaje.add_checkpoint(
        checkpoint_name="inicio_viaje",
        expression="True",  # Se dispara al arrancar
        steps=[
            Print_info(">>> [CHECKPOINT] Inicio del viaje"),
        ],
    )

    viaje.add_checkpoint(
        checkpoint_name="combustible_bajo",
        expression="nivel_gasolina == 'Bajo'",  # Se dispara cuando baje el nivel
        steps=[
            Print_info(">>> [CHECKPOINT] Alerta de combustible bajo detectada"),
        ],
    )

    viaje.set_steps(
        [
            fase_preparacion,
            # Background task: runs without blocking the pipeline
            Background(log_background),
            Print_info(
                ">>> El pipeline continúa mientras el log se procesa en segundo plano..."
            ),
            For(
                iterations=3,
                steps=[
                    Print_info("--- Iniciando Ciclo de Viaje ---", "_loop_iteration"),
                    Parallel(
                        steps=[hechar_gasolina, cambiar_aceite, revisar_luces],
                        max_workers=3,
                        use_processes=False,  # Thread-based for ultra-fast orchestration
                    ),
                    For(
                        validation_expression="nivel_gasolina != 'Vacío'",
                        steps=[
                            conducir,
                            Condition(
                                expression="nivel_neumaticos == 'Bajo'",
                                branch_true=[nested, inflar_neumaticos],
                                branch_false=[desinflar_neumaticos],
                            ),
                            pinchazo_aleatorio,
                        ],
                    ),
                    (print_gasolina, "Mostrar gasolina", "v1.0"),
                    (
                        lambda c: print(
                            f"[non_serializable_obj]: {c.get('non_serializable_obj')}",
                            "non_serializable_obj",
                            "v1.0",
                        )
                    ),
                ],
            ),
        ]
    )
    return viaje


def main():
    # Load and initialize pipeline
    viaje = get_viaje_pipeline()

    after_load_time = datetime.now()
    load_ms = (after_load_time - start_time_global).total_seconds() * 1000
    print(f"Startup Time (Imports + Init): {load_ms:.2f} ms")

    # Start high-frequency execution
    start_exec = datetime.now()

    with ResourceMonitor("Full_Trip_Monitor") as monitor:
        with TaskTimer("viaje_pipeline", timeout_seconds=30) as timer:
            # Run pipeline
            @auto_dict_input
            def run_pipeline(car_dict):
                # Injected runtime resource
                car_dict["system_handler"] = create_complex_handler()
                return viaje.run(car_dict)

            if timer.exceeded_timeout():
                print("⚠ Work exceeded timeout!")
                pass
            else:
                print("✓ Work completed within timeout")
                pass

            car = Car(marca="Toyota", modelo="Corolla")
            results = run_pipeline(car)

    stop_exec = datetime.now()
    exec_ms = (stop_exec - start_exec).total_seconds() * 1000

    print(f"\nResource Summary:")
    summary = monitor.get_summary()
    print(f"  - Peak RAM: {summary['peak_ram_mb']} MB")
    print(f"  - Avg CPU: {summary['avg_cpu_percent']}%")
    print(f"✓ Total time monitored: {timer.elapsed_seconds:.2f}s")

    if "error" in results:
        print(f"Error detectado: {results.get('error')}")

    print("\nFired Alerts:")
    fired = viaje.tracker.get_fired_alerts(limit=10)
    for alert in fired:
        print(
            f"  - [{alert['severity'].upper()}] {alert.get('alert_name', 'Unknown')}: {alert['message']}"
        )

    print("\n" + "=" * 70)
    print("📊 ANÁLISIS DE RENDIMIENTO (AnalysisManager)")
    print("=" * 70)

    analysis = viaje.tracker.analysis
    stats = analysis.get_stats()

    print(f"\nResumen Global:")
    print(f"  - Total Ejecuciones: {stats['total_pipelines']}")
    print(f"  - Tasa de Éxito: {stats['success_rate']}%")
    print(f"  - Duración Media: {stats['avg_duration_ms']:.2f} ms")

    slow_steps = analysis.get_top_slow_steps(limit=3)
    if slow_steps:
        print(f"\nPasos más lentos (Cuellos de botella):")
        for step in slow_steps:
            print(f"  - {step['step_name']}: {step['avg_duration_ms']:.2f} ms")

    trends = analysis.get_trend_data(days=1)
    if trends:
        print(f"\nTendencia de Hoy:")
        print(f"  - Ejecuciones realizadas: {trends[0]['count']}")
        print(f"  - Éxitos: {trends[0]['success']}")

    print(f"\nFinal Gas Level: {results.get('nivel_gasolina')}")
    print(f"PIPELINE EXECUTION TIME: {exec_ms:.2f} ms")
    print(f"TOTAL TIME: {load_ms + exec_ms:.2f} ms")


def test_Wsqlite():
    image = cv2.imread("images.jpeg")

    with Wsqlite(db_name="output/demo.db") as db:

        args_dict = {
            "inference": {
                "source": image,
            },
            "conf": 0.5,
        }

        db.input = args_dict

        db.details = {"info": "Starting the process..."}

        db.output = {"queso": "delicioso"}
        db.error = {"error": "simulated error"}


if __name__ == "__main__":
    test_Wsqlite()
    main()

    # Initialize exporter
    exporter_data()
