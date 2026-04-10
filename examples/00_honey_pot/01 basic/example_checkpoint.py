from datetime import datetime
from dto.car import Car
from example import get_viaje_pipeline
from wpipe import CheckpointManager

dia_hora_hoy = datetime.now().strftime("%Y-%m-%d_%H_%M")
print(f"Fecha y hora de inicio: {dia_hora_hoy}")

# 1. Configuración de fiabilidad
viaje = get_viaje_pipeline()
viaje.verbose = True
chk = CheckpointManager("checkpoints.db")
ID_VIAJE = f"vacaciones_2026_{dia_hora_hoy}"

print(f"\n--- Iniciando Pipeline resumible [{ID_VIAJE}] ---")

# 2. Resumen automático
car = Car(marca="Toyota", modelo="Corolla").__dict__
try:
    if not chk.can_resume(ID_VIAJE):
        print("\n[!] PRIMERA EJECUCIÓN: Completará la Fase 0 y luego simularemos una caída.")
        res = viaje.run(car, checkpoint_mgr=chk, checkpoint_id=ID_VIAJE)
    else:
        print("\n>>> SEGUNDA EJECUCIÓN: Reanudando automáticamente desde el paso 1...")
        res = viaje.run(car, checkpoint_mgr=chk, checkpoint_id=ID_VIAJE)
        print("\n✓ ¡VIAJE COMPLETADO CON ÉXITO!")

except Exception as e:
    # Esto ocurre la primera vez tras completar el paso 0
    print(f"\n✘ SISTEMA CAÍDO: {e}. El progreso del Paso 0 ya está a salvo en el checkpoint.")
    print(">>> Ejecuta de nuevo para ver la reanudación.")
