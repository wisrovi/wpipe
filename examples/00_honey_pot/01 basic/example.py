import json
import os
import random
import tempfile
import threading
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
    nested,
    print_gasolina,
)

from wpipe import (
    Condition,
    For,
    Metric,
    Parallel,
    Pipeline,
    PipelineContext,
    PipelineExporter,
    ResourceMonitor,
    Severity,
    TaskTimer,
    auto_dict_input,
    object_to_dict,
    step,
)
from wpipe.sqlite import Wsqlite

# ToDo:  APIClient AnalysisManager,


# Definimos revisar_luces para que el bloque Parallel no falle por NameError
@step(name="revisar_luces", version="v1.0")
def revisar_luces(d):
    # print("     * Revisando luces traseras y delanteras... OK")
    return d


@step(name="pinchazo_aleatorio", version="v1.0", retry_count=10, retry_delay=0.01)
def pinchazo_aleatorio(d):
    if random.random() < 0.5:
        raise RuntimeError("Pinchazo aleatorio")
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


db_path = "wpipe_dashboard.db"


def get_viaje_pipeline():
    viaje = Pipeline(
        pipeline_name="viaje",
        verbose=True,
        tracking_db=db_path,
        #
        max_retries=3,
        retry_delay=0,  # Recuperación instantánea
        retry_on_exceptions=(RuntimeError,),
        #
        collect_system_metrics=True,
        #
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
            For(
                iterations=3,
                steps=[
                    Print_info(f"--- Nuevo viaje ---", "_loop_iteration"),
                    Parallel(
                        steps=[
                            hechar_gasolina,  # Se ejecuta en hilo A
                            cambiar_aceite,  # Se ejecuta en hilo B
                            revisar_luces,  # Se ejecuta en hilo C
                        ],
                        max_workers=3,
                        # use_processes=False  # Cambiado a False para evitar errores de pickling con objetos complejos
                    ),
                    Print_info("Resumen post-paralelo"),
                    # (print_gasolina, "Mostrar gasolina", "v1.0"),
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
                            # (print_gasolina, "Mostrar gasolina", "v1.0"),
                            pinchazo_aleatorio,
                        ],
                    ),
                    (lambda c: print(f"[non_serializable_obj]: {c.get('non_serializable_obj')}", "non_serializable_obj", "v"))               ],
            ),
        ],
    )
    return viaje


def export_logs_to_json(exporter: PipelineExporter, output_path: str) -> None:
    """Export logs to JSON format."""
    print("\n" + "=" * 70)
    print("JSON EXPORT")
    print("=" * 70)

    try:
        json_data = exporter.export_pipeline_logs(format="json")

        if json_data:
            Path(output_path).write_text(json_data)
            print(f"✓ Exported to: {output_path}")
            print(f"  File size: {len(json_data)} bytes")

            # Show sample
            data = json.loads(json_data)
            if isinstance(data, list) and data:
                print(f"  Records: {len(data)}")
                print(f"  Sample record keys: {list(data[0].keys())}")
        else:
            print("ℹ No execution data to export yet")
    except Exception as e:
        print(f"ℹ JSON export: {e}")


def export_logs_to_csv(exporter: PipelineExporter, output_path: str) -> None:
    """Export logs to CSV format."""
    print("\n" + "=" * 70)
    print("CSV EXPORT")
    print("=" * 70)

    try:
        csv_data = exporter.export_pipeline_logs(format="csv")

        if csv_data:
            # Fix path for CSV
            csv_path = output_path.replace(".json", ".csv")
            Path(csv_path).write_text(csv_data)
            print(f"✓ Exported to: {csv_path}")

            lines = csv_data.split("\n")
            print(f"  File size: {len(csv_data)} bytes")
            print(f"  Records: {len(lines) - 1}")  # Exclude header
            print(f"  Columns: {len(lines[0].split(','))}")
            print(f"  Header: {lines[0]}")
        else:
            print("ℹ No execution data to export yet")
    except Exception as e:
        print(f"ℹ CSV export: {e}")


def exporter_data():
    print("\n" + "=" * 70)
    print("SUPPORTED EXPORT FORMATS")
    print("=" * 70 + "\n")

    print("JSON Export:")
    print("  - Human readable")
    print("  - Best for nested/complex data")
    print("  - Supported by: Python, JavaScript, most tools")
    print("  - Usage: exporter.export_pipeline_logs(format='json')\n")

    print("CSV Export:")
    print("  - Spreadsheet compatible")
    print("  - Best for tabular data")
    print("  - Supported by: Excel, Google Sheets, Pandas")
    print("  - Usage: exporter.export_pipeline_logs(format='csv')\n")
    output_dir = "export_output"

    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)

    # Initialize exporter
    exporter = PipelineExporter(db_path)

    print("=" * 70)
    print("EXPORTING DATA")
    print("=" * 70 + "\n")

    # Export statistics
    print("1. Exporting statistics to JSON...")
    stats_path = os.path.join(output_dir, "pipeline_statistics.json")
    try:
        exporter.export_statistics(format="json", output_path=stats_path)
        print(f"   ✓ Saved to: {stats_path}\n")

        with open(stats_path) as f:
            stats = json.load(f)
            print("   Statistics:")
            for key, value in stats.items():
                print(f"     - {key}: {value}")
    except Exception as e:
        print(f"   ⚠ Stats export note: {e}\n")

    # Export logs
    print("\n2. Exporting pipeline logs...")
    logs_json_path = os.path.join(output_dir, "pipeline_logs.json")
    export_logs_to_json(exporter, logs_json_path)
    export_logs_to_csv(exporter, logs_json_path)

    # Show available files
    print("\n" + "=" * 70)
    print("AVAILABLE EXPORTS")
    print("=" * 70 + "\n")

    if Path(output_dir).exists():
        for file in Path(output_dir).glob("*"):
            size = file.stat().st_size
            print(f"✓ {file.name} ({size} bytes)")
    else:
        print("Output directory not yet created")

    print("\n✓ Export demo completed!")


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


def main():
    # Usamos ResourceMonitor para medir el consumo de hardware (RAM/CPU)
    with ResourceMonitor("Viaje_Completo") as monitor:
        # Usamos TaskTimer para control de tiempos de ejecución
        with TaskTimer("viaje_pipeline", timeout_seconds=30) as timer:
            viaje = get_viaje_pipeline()

            @auto_dict_input
            def run_pipeline(car_dict):

                # This instance is complex because it is locally scoped and holds system resources
                complex_obj = create_complex_handler()
                car_dict["non_serializable_obj"] = complex_obj

                return viaje.run(car_dict)

            car = Car(marca="Toyota", modelo="Corolla")
            # print(f"Carro inicial: {car.nivel_gasolina}\n")
            results = run_pipeline(car)
            if timer.exceeded_timeout():
                # print("⚠ Work exceeded timeout!")
                pass
            else:
                # print("✓ Work completed within timeout")
                pass

    # Resumen de recursos al terminar
    print(f"\nResource Summary:")
    summary = monitor.get_summary()
    print(f"  - Peak RAM: {summary['peak_ram_mb']} MB")
    print(f"  - Avg CPU: {summary['avg_cpu_percent']}%")
    print(f"✓ Total time monitored: {timer.elapsed_seconds:.2f}s")

    # print(f"\nViajes completados: {results.get('_loop_iteration')}")
    # print(f"Gasolina final: {results.get('nivel_gasolina')}")
    # print(f"Aceite final: {results.get('nivel_aceite')}")

    if "error" in results:
        print(f"Error detectado: {results.get('error')}")

    # Show fired alerts
    # print("\nFired Alerts:")
    fired = viaje.tracker.get_fired_alerts(limit=10)
    # for alert in fired:
    #     print(
    #         f"  - [{alert['severity'].upper()}] {alert.get('alert_name', 'Unknown')}: {alert['message']}"
    #     )

    # Initialize exporter
    # exporter_data()

    # --- ANÁLISIS DE DATOS INTELIGENTE ---
    # print("\n" + "=" * 70)
    # print("📊 ANÁLISIS DE RENDIMIENTO (AnalysisManager)")
    # print("=" * 70)

    analysis = viaje.tracker.analysis
    stats = analysis.get_stats()

    # print(f"\nResumen Global:")
    # print(f"  - Total Ejecuciones: {stats['total_pipelines']}")
    # print(f"  - Tasa de Éxito: {stats['success_rate']}%")
    # print(f"  - Duración Media: {stats['avg_duration_ms']:.2f} ms")

    slow_steps = analysis.get_top_slow_steps(limit=3)
    # if slow_steps:
    #     print(f"\nPasos más lentos (Cuellos de botella):")
    #     for step in slow_steps:
    #         print(f"  - {step['step_name']}: {step['avg_duration_ms']:.2f} ms")

    trends = analysis.get_trend_data(days=1)
    # if trends:
    #     print(f"\nTendencia de Hoy:")
    #     print(f"  - Ejecuciones realizadas: {trends[0]['count']}")
    #     print(f"  - Éxitos: {trends[0]['success']}")


if __name__ == "__main__":
    with Wsqlite(db_name="demo.db") as db:
        args_dict = {
            "inference": {
                "source": "<image>",
            },
            "conf": 0.5,
        }

        db.input = args_dict

        db.details = {"info": "Starting the process..."}

        db.output = {"queso": "delicioso"}
        
        db.error = {"simulated_error": "error "}

        main()
