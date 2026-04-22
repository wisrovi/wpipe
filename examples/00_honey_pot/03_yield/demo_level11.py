"""
DEMO LEVEL 11: Fallo de Sensores (Error Capture)
------------------------------------------------
Añade: Gestión de errores cuando la cámara se ensucia o falla.
Acumula: Parabrisas Inteligente (L10).

DIAGRAMA:
(Cámara) -- [¿Lente sucia?] -- ERROR! --> (Limpiaparabrisas Automático)
      |
      v
(Procesar Viaje)
"""

import random

from wpipe import Pipeline, step


def mantenimiento_emergencia(context, error):
    print(f"\n🔧 SISTEMA: Detectado error en '{error['step_name']}'.")
    print(f"🧼 ACCIÓN: Activando autolimpieza de sensores...\n")
    return context


@step(name="verificar_lente")
def verificar_lente(data):
    if random.random() < 0.3:
        raise RuntimeError("Visibilidad obstruida (Lente sucia)")
    print("👀 Sensores limpios. Visibilidad 100%.")
    return {"vision": "Clear"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L11_FaultTolerance", verbose=True)

    # El coche ahora sabe qué hacer si falla la visión
    pipe.add_error_capture([mantenimiento_emergencia])

    pipe.set_steps([verificar_lente])
    print(">>> Iniciando trayecto con sensores de seguridad...")
    pipe.run({})
