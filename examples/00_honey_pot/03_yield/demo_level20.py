"""
DEMO LEVEL 20: Decisiones de Emergencia (Condition)
---------------------------------------------------
Añade: Decisiones dinámicas basadas en la IA y la velocidad.
Acumula: Inferencia (L10) y Telemetría (L16).

DIAGRAMA:
(Sistema_Vision) -> [Obstáculo detectado]
      |
      v
Condition(¿Frenado de emergencia?)
      |--- [SI] -> (Activar Frenos ABS)
      |--- [NO] -> (Mantener Velocidad)
"""
from wpipe import Pipeline, step, Condition, to_obj

@step(name="ia_radar")
def ia_radar(d):
    # Simulamos detección de obstáculo a 5 metros
    return {"distancia": 5, "obstaculo": True}

@step(name="frenado_abs")
def frenado_abs(d):
    print("🚨 ABS: ¡Frenando bruscamente para evitar colisión!")
    return {"frenando": True}

@step(name="mantener_marcha")
def mantener_marcha(d):
    print("🛣️  Todo despejado. Manteniendo velocidad de crucero.")
    return {"frenando": False}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L20_EmergencyLogic", verbose=True)
    
    pipe.set_steps([
        ia_radar,
        # NUEVO EN L20: El coche decide qué rama ejecutar
        Condition(
            expression="obstaculo == True and distancia < 10",
            branch_true=[frenado_abs],
            branch_false=[mantener_marcha]
        )
    ])
    
    pipe.run({})
