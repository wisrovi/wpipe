"""
DEMO LEVEL 31: Escaneo de Seguridad (Validators)
-----------------------------------------------
Añade: Validadores personalizados en Pydantic para seguridad física.
Acumula: Telemetría Pydantic (L16).

DIAGRAMA:
(leer_presion) -> [presion: 1.0 bar]
      |
      v
[Validator] -- [¿Es < 1.5?] -- ERROR! --> (Alerta: Neumático pinchado)
"""

import random

from pydantic import BaseModel, Field, validator

from wpipe import Pipeline, step, to_obj


class SafetyCheck(BaseModel):
    presion: float = Field(..., ge=1.0, le=4.0)

    @validator("presion")
    def alerta_presion_baja(cls, v):
        if v < 2.0:
            print("⚠️ AVISO: Presión baja detectada. Recomendado inflar.")
        return v


@step(name="sensor_presion")
def sensor_presion(d):
    # Simulamos lectura de un neumático bajo de aire
    presion_random = round(random.randint(10, 30) / 10, 2)

    return {"presion": presion_random}


@step(name="verificar_integridad")
@to_obj(SafetyCheck)
def verificar_integridad(ctx: SafetyCheck):
    print(f"🛞  Neumáticos: {ctx.presion} bar. Integridad física confirmada.")
    return {"neumaticos_ok": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Safety_Scan_L31", verbose=True)
    pipe.set_steps([sensor_presion, verificar_integridad])
    pipe.run({})
