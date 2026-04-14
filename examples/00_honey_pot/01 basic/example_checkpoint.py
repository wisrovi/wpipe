import os
from datetime import datetime

from dto.car import Car
from example import get_viaje_pipeline

from wpipe import CheckpointManager

# 1. Configuración de fiabilidad
viaje = get_viaje_pipeline()
viaje.verbose = True
chk = CheckpointManager("checkpoints.db")

# ID estable para la demostración
ID_VIAJE = "vacaciones_lts_2026"

print(f"\n--- Iniciando Pipeline resumible [{ID_VIAJE}] ---")

# 2. Datos iniciales
car = Car(marca="Toyota", modelo="Corolla").__dict__

try:
    if not chk.can_resume(ID_VIAJE):
        print("\n[!] PRIMERA EJECUCIÓN: Completará la Fase 0 y luego simularemos una caída.")
        # Ejecutamos la pipeline. Para simular la caída DESPUÉS de un paso, 
        # podríamos meter una excepción en un paso específico, pero para este ejemplo
        # simplemente lanzaremos una tras una ejecución parcial si fuera posible.
        # Aquí, para que sea "perfecto", haremos que falle si es la primera vez.
        res = viaje.run(car, checkpoint_mgr=chk, checkpoint_id=ID_VIAJE)
        
        # Si llega aquí sin fallar (lo cual no queremos en la primera vuelta de la demo)
        # forzamos la caída para demostrar el checkpoint.
        raise RuntimeError("Simulación de caída del sistema (Fase 1)")
    else:
        print("\n>>> SEGUNDA EJECUCIÓN: Reanudando automáticamente...")
        res = viaje.run(car, checkpoint_mgr=chk, checkpoint_id=ID_VIAJE)
        print("\n✓ ¡VIAJE COMPLETADO CON ÉXITO!")
        # Limpiamos para la próxima vez que se quiera probar
        chk.clear_checkpoints(ID_VIAJE)
        if os.path.exists("checkpoints.db"):
            os.remove("checkpoints.db")

except Exception as e:
    print(f"\n✘ SISTEMA CAÍDO: {e}")
    print(">>> Ejecuta de nuevo para ver la reanudación desde el último punto a salvo.")
