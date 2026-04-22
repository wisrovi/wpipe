"""
DEMO LEVEL 3: Bodega como Objeto (@to_obj)
------------------------------------------
Añade: Uso de @to_obj para acceder a la bodega con '.' (Puntos).
Acumula: Paso 1 (encender_motor), Paso 2 (revisar_frenos).

DIAGRAMA:
[Bodega Inicial]
      |
      v
(encender_motor) ----> [motor: 'ON', gasolina: 100]
      |
      v
(revisar_frenos @step) -> [frenos: 'OK']
      |
      v
(validar_estado @to_obj) -> ¡Accede a ctx.motor y ctx.frenos!
"""

from wpipe import Pipeline, step, to_obj


# Heredados:
def encender_motor(data):
    print("🔑 Motor encendido.")
    return {"motor": "ON", "gasolina": 100}


@step(name="revisar_frenos")
def revisar_frenos(data):
    print("👟 Frenos verificados.")
    return {"frenos": "OK"}


# NUEVO EN L3: Acceso a datos más limpio
@step(name="validar_estado")
@to_obj  # <--- Permite usar ctx.nombre_campo
def validar_estado(ctx):
    # Accedemos de forma elegante a datos de pasos anteriores
    if ctx.motor == "ON" and ctx.frenos == "OK":
        print(f"✅ Bodega verificada. Gasolina: {ctx.gasolina}%")
    return {"todo_listo": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L3", verbose=True)
    pipe.set_steps([encender_motor, revisar_frenos, validar_estado])
    pipe.run({})
