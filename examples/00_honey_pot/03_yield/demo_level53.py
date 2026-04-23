from typing import Any, Dict
from pydantic import BaseModel, Field
from wpipe import Pipeline, step, to_obj, Condition
import random

# 1. ESQUEMA DE VALIDACIÓN CON PYDANTIC
class SensorData(BaseModel):
    temperature: float = Field(..., ge=-50, le=100)
    humidity: float = Field(..., ge=0, le=100)
    status: str = "ok"

@step(name="read_sensor")
@to_obj(SensorData) # <--- VALIDACIÓN PYDANTIC ACTIVA
def read_sensor(context: SensorData):
    print(f"--- Datos validados: Temp={context.temperature}, Hum={context.humidity}%")
    return {"processed": True}

# 2. LÓGICA DE REINTENTOS ESPECÍFICOS
class HardwareConnectionError(Exception):
    pass

@step(
    name="unstable_step",
    retry_count=3,
    retry_delay=0.1,
    retry_on_exceptions=(HardwareConnectionError,) # <--- SOLO REINTENTA ESTA EXCEPCIÓN
)
def unstable_step(context: Any) -> dict:

    """Unstable step step.

    Args:

        context: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    val = random.random()
    if val < 0.7:
        print("  [!] Fallo de hardware... reintentando")
        raise HardwareConnectionError("Error de conexión física")
    elif val < 0.8:
        print("  [X] Error fatal de lógica... fallando inmediatamente")
        raise ValueError("Valor no permitido") # Esto NO se reintentará
    
    print("  [✓] Paso inestable completado")
    return {"hardware_ready": True}

# 3. PASOS PARA LA RAMIFICACIÓN
@step(name="alert_high_temp")
def alert_high_temp(context: Any) -> None:
    """Alert high temp step.

    Args:
        context: Input data for the step.

    Returns:
        dict: Result of the step.
    """
    print("🚨 ALERTA: ¡Temperatura crítica detectada!")
    return {"alert_sent": True}

@step(name="normal_operation")
def normal_operation(context: Any) -> None:

    """Normal operation step.

    Args:

        context: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("✅ Operación normal: Clima controlado")
    return {"alert_sent": False}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="advanced_features_demo", verbose=True)
    
    # Definición del flujo con Condition
    pipe.set_steps([
        unstable_step,
        # Probamos la validación Pydantic
        (lambda ctx: {"temperature": 45.5, "humidity": 30.0}, "mock_sensor", "v1.0"),
        read_sensor,
        # 4. RAMIFICACIÓN COMPLEJA (Condition)
        Condition(
            expression="temperature > 40",
            branch_true=[alert_high_temp],
            branch_false=[normal_operation]
        )
    ])
    
    print("\n>>> Startsndo demo de funcionalidades avanzadas...\n")
    try:
        pipe.run({})
    except Exception as e:
        print(f"\nFinishesdo con error esperado: {e}")
