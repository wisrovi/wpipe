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

print(f"\n" + "="*60)
print(f"🚀 PIPELINE RESUMIBLE: {ID_VIAJE}")
print("="*60 + "\n")

# 2. Datos iniciales
car = Car(marca="Toyota", modelo="Corolla").__dict__

try:
    if not chk.can_resume(ID_VIAJE):
        print("⊘ No se encontró punto de control previo. Iniciando viaje desde el garaje...")
        print("\n[!] PASO 1: Ejecución inicial con caída simulada.")
        print("-" * 60)
        
        # Inyectamos una excepción que ocurrirá DESPUÉS del primer paso exitoso (fase_preparacion)
        # pero antes de completar el bucle de viajes.
        # Para esta demo, simplemente lanzamos el error manualmente tras una ejecución parcial.
        
        # Ejecutamos la pipeline con el gestor de checkpoints activo
        viaje.run(car, checkpoint_mgr=chk, checkpoint_id=ID_VIAJE)
        
        # Si por algún motivo termina sin errores, forzamos la caída para la demo
        if not os.path.exists("checkpoints.db"):
             print("ℹ Nota: No se generaron checkpoints. Asegúrate de que el viaje sea lo suficientemente largo.")
        
        raise RuntimeError("🔌 FALLO ELÉCTRICO CRÍTICO: El sistema se ha apagado inesperadamente.")
    
    else:
        print("⟲ ¡SISTEMA RECUPERADO! Detectado punto de control anterior.")
        last = chk.get_last_checkpoint(ID_VIAJE)
        
        print(f"  📍 Último hito guardado: {last['step_name']}")
        print(f"  🔢 Índice del paso: {last['step_order']}")
        print(f"  🕒 Fecha del guardado: {last['created_at']}")
        print(f"  📦 Datos recuperados: {len(last['data'])} llaves en bodega")
        
        print("\n>>> PASO 2: Reanudando viaje automáticamente desde el punto exacto...")
        print("-" * 60)
        
        # Al pasar el mismo ID_VIAJE y el gestor, la pipeline saltará los pasos ya hechos
        res = viaje.run(car, checkpoint_mgr=chk, checkpoint_id=ID_VIAJE)
        
        print("\n" + "✓" * 60)
        print("🏁 ¡VIAJE COMPLETADO CON ÉXITO TRAS LA REANUDACIÓN!")
        print("✓" * 60)
        
        # Limpiamos para que se pueda volver a probar la demo desde cero
        chk.clear_checkpoints(ID_VIAJE)
        if os.path.exists("checkpoints.db"):
            os.remove("checkpoints.db")

except Exception as e:
    print(f"\n" + "!" * 60)
    print(f"✘ SISTEMA CAÍDO: {e}")
    print("!" * 60)
    print("\n>>> INSTRUCCIONES: Ejecuta este script una vez más para ver cómo WPipe")
    print(">>> reanuda el viaje saltándose la fase de preparación.")
