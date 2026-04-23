Nivel 51: demo_level51.py
=========================

Este es el nivel 51 del tour de aprendizaje.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level51.py
   :language: python
   :linenos:

Resultado de Ejecución
----------------------

.. code-block:: text

   
   ============================================================
   🚀 PIPELINE RESUMIBLE: vacaciones_lts_2026
   ============================================================
   
   ⟲ ¡SISTEMA RECUPERADO! Detectado punto de control anterior.
     📍 Último hito guardado: step_0
     🔢 Índice del paso: 0
     🕒 Fecha del guardado: 2026-04-23T01:11:48.623260
     📦 Datos recuperados: 12 llaves en bodega
   
   >>> PASO 2: Reanudando viaje automáticamente desde el punto exacto...
   ------------------------------------------------------------
   
   [CHECKPOINT] Reanudando 'vacaciones_lts_2026' desde el paso 1
   
   [MATRÍCULA] Pipeline registered: PIPE-4496B595
   [MATRÍCULA] Config YAML: /home/wisrovi/Documentos/w_libraries/wpipe/wpipe/examples/00_honey_pot/03_yield/pipeline_configs/viaje.yaml
   
   [CHECKPOINT REACHED] inicio_viaje
   >>> [CHECKPOINT] Inicio del viaje
   --- Nuevo viaje --- (Iteración: 0)
   
   [DEBUG] item.use_processes value: False
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
   viaje - print_info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   [HOOKS] Executing post-run tasks...
   >>> [HOOK] El viaje ha terminado, enviando resumen final...
   
   [MATRÍCULA] Pipeline PIPE-4496B595: ERROR
   
   ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓
   🏁 ¡VIAJE COMPLETADO CON ÉXITO TRAS LA REANUDACIÓN!
   ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓

