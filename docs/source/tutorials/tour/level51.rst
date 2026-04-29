Nivel 51: demo_level51.py
=========================

Este es el nivel 51 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level51.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   
   ============================================================
   🚀 PIPELINE RESUMIBLE: vacaciones_lts_2026
   ============================================================
   
   ⊘ No se encontró punto de control previo. Startsndo trip desde el garaje...
   
   [!] PASO 1: Ejecución inicial con caída simulada.
   ------------------------------------------------------------
   [PIPELINE STATUS] Registered: PIPE-08E3ABAB
   
   [CHECKPOINT REACHED] trip_start
   >>> [CHECKPOINT] Trip start
   --- New trip ---_loop_iteration
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
        * Checking front and rear lights... OK
   [CONDITION] Evaluating: tire_level == 'Low'
   
   [ERROR CAPTURE] Processing error in state 'random_flat_tire'...
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   🚨 SYSTEM ALERT: ERROR DETECTED
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   📍 FAILED STATE: random_flat_tire
   📄 FILE: /home/william.rodriguez/Documents/wpipe/examples/00_honey_pot/03_yield/demo_level50.py
   🔢 LINE: 72
   ⚠️ MESSAGE: Random puncture
   🔄 ATTEMPT: 1
   🕒 TIMESTAMP: 2026-04-29T13:32:31.116224
   ------------------------------------------------------------
   [RETRY] random_flat_tire failed (attempt 1): Random puncture
   [CONDITION] Evaluating: tire_level == 'Low'
   [non_serializable_obj]: None non_serializable_objv1.0
   --- New trip ---_loop_iteration
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
        * Checking front and rear lights... OK
   [non_serializable_obj]: None non_serializable_objv1.0
   --- New trip ---_loop_iteration
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
        * Checking front and rear lights... OK
   [non_serializable_obj]: None non_serializable_objv1.0
   trip ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   [HOOKS] Executing post-run tasks...
   >>> [HOOK] Trip finished sending final summary...
   [PIPELINE STATUS] PIPE-08E3ABAB: COMPLETED
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   ✘ SISTEMA CAÍDO: 🔌 FALLO ELÉCTRICO CRÍTICO: El sistema se ha apagado inesperadamente.
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   
   >>> INSTRUCCIONES: Ejecuta este script una vez más para ver cómo WPipe
   >>> reanuda el trip saltándose la fase de preparación.