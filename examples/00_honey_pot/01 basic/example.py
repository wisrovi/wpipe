import os
import random
import tempfile
import threading
from datetime import datetime
from pathlib import Path

# Tracking start time for performance verification
start_time_global = datetime.now()

# Efficient imports using WPipe Lazy Loading
from dto.car import Car
from states import (
    Print_info, cambiar_aceite, conducir, desinflar_neumaticos,
    fase_preparacion, hechar_gasolina, inflar_neumaticos,
    nested, print_gasolina,
)

from wpipe import (
    Condition, For, Metric, Parallel, Pipeline, PipelineContext,
    ResourceMonitor, Severity, TaskTimer,
    auto_dict_input, object_to_dict, step
)
from wpipe.pipe.components.logic_blocks import Background

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
    """Simulated error notification."""
    print(f"\n🚨 ALERT: Error in '{error['step_name']}' -> {error['error_message']}")
    return context


@step(name="log_background", version="v1.0")
def log_background(data):
    """Simulated background logging task - runs without blocking pipeline."""
    import time
    print("[BACKGROUND] Logging task started...")
    time.sleep(30.1)  # Simulate async work
    print("[BACKGROUND] Logging task completed!")
    return {}

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
        collect_system_metrics=False, # Performance optimization
        show_progress=True,
    )

    # Global alerts
    viaje.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">1000", # Warn if total takes >1s
        severity=Severity.WARNING,
        steps=[Print_info(">>> [PERFORMANCE ALERT] Pipeline execution slow")],
    )

    viaje.set_steps([
        fase_preparacion,
        # Background task: runs without blocking the pipeline
        Background(log_background),
        Print_info(">>> El pipeline continúa mientras el log se procesa en segundo plano..."),
        For(
            iterations=3,
            steps=[
                Print_info("--- Iniciando Ciclo de Viaje ---", "_loop_iteration"),
                Parallel(
                    steps=[hechar_gasolina, cambiar_aceite, revisar_luces],
                    max_workers=3,
                    use_processes=False # Thread-based for ultra-fast orchestration
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
            ],
        ),
    ])
    return viaje

def create_complex_handler():
    """Simulates a non-serializable system resource."""
    class InternalSystemHandler:
        def __init__(self):
            self.lock = threading.Lock()
            self.resource = tempfile.NamedTemporaryFile(mode="w+")
        def __repr__(self):
            return "<SystemResource Active>"
    return InternalSystemHandler()

def main():
    # Load and initialize pipeline
    viaje = get_viaje_pipeline()
    
    after_load_time = datetime.now()
    load_ms = (after_load_time - start_time_global).total_seconds() * 1000
    print(f"Startup Time (Imports + Init): {load_ms:.2f} ms")

    # Start high-frequency execution
    start_exec = datetime.now()

    with ResourceMonitor("Full_Trip_Monitor") as monitor:
        @auto_dict_input
        def run_pipeline(car_dict):
            # Injected runtime resource
            car_dict["system_handler"] = create_complex_handler()
            return viaje.run(car_dict)

        car = Car(marca="Toyota", modelo="Corolla")
        results = run_pipeline(car)

    stop_exec = datetime.now()
    exec_ms = (stop_exec - start_exec).total_seconds() * 1000
    
    print(f"\nFinal Gas Level: {results.get('nivel_gasolina')}")
    print(f"PIPELINE EXECUTION TIME: {exec_ms:.2f} ms")
    print(f"TOTAL TIME: {load_ms + exec_ms:.2f} ms")

if __name__ == "__main__":
    main()
