"""
DEMO LEVEL 40: THE GRAND FINALE (Autonomía Total)
--------------------------------------------------
Resumen: Integración de las 40 funcionalidades en un viaje real.
Acumula: ABSOLUTAMENTE TODO.

DIAGRAMA FINAL:
[Arrancar] -> (Cargar YAML) -> (Checkpoints) -> For(Ruta) {
   Parallel(IA Multiproceso) -> Condition(Obstáculo) -> Pydantic(Validar) -> Metric(Fuel)
} -> [Destino] -> (Hooks de Apagado) -> (Exportar CSV)
"""

import os
import random

from pydantic import BaseModel, Field

from wpipe import (
    CheckpointManager,
    Condition,
    For,
    Metric,
    Parallel,
    Pipeline,
    PipelineExporter,
    step,
    to_obj,
)


# 1. Definición de Datos Seguros
class CarStatus(BaseModel):
    gasolina: float = Field(..., ge=0, le=100)
    velocidad: float = Field(..., ge=0, le=200)


# 2. Inteligencia de Visión
@step(name="ia_vision_360")
def vision(d):
    peligro = random.random() < 0.2
    return {"obstaculo": peligro, "distancia": random.randint(2, 50)}


# 3. Respuesta Automática
@step(name="frenado_emergencia")
def frenado(d):
    print("🚨 ADAS: ¡FRENADO DE EMERGENCIA ACTIVADO!")
    return {"frenando": True}


# Validación y Métricas
@to_obj(CarStatus)
def telemetria(ctx):
    Metric.record("trip_speed", ctx.velocidad, "km/h")
    return {"v_ok": True}


if __name__ == "__main__":
    # Preparación de infraestructura
    os.makedirs("output", exist_ok=True)
    db_tracking = "output/gran_viaje_2026.db"
    ck_mgr = CheckpointManager("output/puntos_control_viaje.db")

    # EL SUPER PIPELINE: Configurado con todo el arsenal
    viaje = Pipeline(
        pipeline_name="VIAJE_AUTONOMO_TOTAL",
        tracking_db=db_tracking,
        collect_system_metrics=True,
        continue_on_error=True,
        verbose=True,
    )

    # Definición del flujo Maestro
    viaje.set_steps(
        [
            # Inicio y Preparación
            (lambda d: {"gasolina": 100, "velocidad": 120}, "arranque_inicial", "v1.0"),
            # Bucle de Conducción Principal
            For(
                iterations=3,
                steps=[
                    # Mirar en paralelo usando varios núcleos (Multiproceso)
                    Parallel(steps=[vision] * 3, use_processes=True, max_workers=3),
                    # Decisión lógica
                    Condition(expression="obstaculo == True", branch_true=[frenado]),
                    telemetria,
                ],
            ),
            (
                lambda d: print("🏁 DESTINO ALCANZADO: El coche ha llegado solo."),
                "fin",
                "v1",
            ),
        ]
    )

    # Registro de Eventos y Hooks
    viaje.add_event(
        event_type="log", event_name="Salida", message="Iniciando ruta Madrid-Valencia"
    )
    viaje.add_event(
        event_type="hook",
        event_name="Protocolo Final",
        steps=[(lambda d: print("🔌 Sistemas desconectados."), "shutdown", "v1")],
    )

    # EJECUCIÓN MAESTRA
    print("\n🚀 INICIANDO EL GRAN VIAJE (Integración de 40 niveles)...\n")
    viaje.run({}, checkpoint_mgr=ck_mgr, checkpoint_id="viaje_final_autonomo")

    # Exportación del informe final para el propietario
    PipelineExporter(db_tracking).export_pipeline_logs(
        "output/informe_propietario.csv", format="csv"
    )
    print("\n✅ TOUR DE APRENDIZAJE COMPLETADO. 40 NIVELES DE DOMINIO DE WPIPE.")
