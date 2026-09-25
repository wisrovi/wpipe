Nivel 51: demo_level51.py
=========================

Este es el nivel 51 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
-------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level51.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
----------------------


   
   ============================================================
   🚀 PIPELINE RESUMIBLE: vacaciones_lts_2026
   ============================================================
   
   ⊘ No se encontró punto de control previo. Startsndo trip desde el garaje...
   
   [!] PASO 1: Ejecución inicial con caída simulada.
   ------------------------------------------------------------
   [PIPELINE STATUS] Registered: PIPE-30526082
   
   [CHECKPOINT REACHED] trip_start
   >>> [CHECKPOINT] Trip start
   --- New trip ---_loop_iteration
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
        * Checking front and rear lights... OK
   [CONDITION] Evaluating: tire_level == 'Low'
   [CONDITION] Evaluating: tire_level == 'Low'
   
   [ERROR CAPTURE] Processing error in state 'random_flat_tire'...
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   🚨 SYSTEM ALERT: ERROR DETECTED
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   📍 FAILED STATE: random_flat_tire
   📄 FILE: /home/william.rodriguez/Documents/w_libraries/w_libraries/wpipe_os/wpipe/examples/00_honey_pot/03_yield/demo_level50.py
   🔢 LINE: 70
   ⚠️ MESSAGE: Random puncture
   🔄 ATTEMPT: 1
   🕒 TIMESTAMP: 2026-09-25T10:04:06.110846
   ------------------------------------------------------------
   [RETRY] random_flat_tire failed (attempt 1): Random puncture
   [CONDITION] Evaluating: tire_level == 'Low'
   
   [ERROR CAPTURE] Processing error in state 'random_flat_tire'...
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   🚨 SYSTEM ALERT: ERROR DETECTED
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   📍 FAILED STATE: random_flat_tire
   📄 FILE: /home/william.rodriguez/Documents/w_libraries/w_libraries/wpipe_os/wpipe/examples/00_honey_pot/03_yield/demo_level50.py
   🔢 LINE: 70
   ⚠️ MESSAGE: Random puncture
   🔄 ATTEMPT: 1
   🕒 TIMESTAMP: 2026-09-25T10:04:06.122743
   ------------------------------------------------------------
   [RETRY] random_flat_tire failed (attempt 1): Random puncture
   [non_serializable_obj]: None non_serializable_objv1.0
   --- New trip ---_loop_iteration
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
        * Checking front and rear lights... OK
   [CONDITION] Evaluating: tire_level == 'Low'
   [CONDITION] Evaluating: tire_level == 'Low'
   
   [ERROR CAPTURE] Processing error in state 'random_flat_tire'...
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   🚨 SYSTEM ALERT: ERROR DETECTED
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   📍 FAILED STATE: random_flat_tire
   📄 FILE: /home/william.rodriguez/Documents/w_libraries/w_libraries/wpipe_os/wpipe/examples/00_honey_pot/03_yield/demo_level50.py
   🔢 LINE: 70
   ⚠️ MESSAGE: Random puncture
   🔄 ATTEMPT: 1
   🕒 TIMESTAMP: 2026-09-25T10:04:06.139564
   ------------------------------------------------------------
   [RETRY] random_flat_tire failed (attempt 1): Random puncture
   [CONDITION] Evaluating: tire_level == 'Low'
   
   [ERROR CAPTURE] Processing error in state 'random_flat_tire'...
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   🚨 SYSTEM ALERT: ERROR DETECTED
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   📍 FAILED STATE: random_flat_tire
   📄 FILE: /home/william.rodriguez/Documents/w_libraries/w_libraries/wpipe_os/wpipe/examples/00_honey_pot/03_yield/demo_level50.py
   🔢 LINE: 70
   ⚠️ MESSAGE: Random puncture
   🔄 ATTEMPT: 1
   🕒 TIMESTAMP: 2026-09-25T10:04:06.151443
   ------------------------------------------------------------
   [RETRY] random_flat_tire failed (attempt 1): Random puncture
   
   [ERROR CAPTURE] Processing error in state 'random_flat_tire'...
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   🚨 SYSTEM ALERT: ERROR DETECTED
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   📍 FAILED STATE: random_flat_tire
   📄 FILE: /home/william.rodriguez/Documents/w_libraries/w_libraries/wpipe_os/wpipe/examples/00_honey_pot/03_yield/demo_level50.py
   🔢 LINE: 70
   ⚠️ MESSAGE: Random puncture
   🔄 ATTEMPT: 2
   🕒 TIMESTAMP: 2026-09-25T10:04:06.162172
   ------------------------------------------------------------
   [RETRY] random_flat_tire failed (attempt 2): Random puncture
   [non_serializable_obj]: None non_serializable_objv1.0
   --- New trip ---_loop_iteration
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
        * Checking front and rear lights... OK
   [CONDITION] Evaluating: tire_level == 'Low'
   [CONDITION] Evaluating: tire_level == 'Low'
   [CONDITION] Evaluating: tire_level == 'Low'
   [non_serializable_obj]: None non_serializable_objv1.0
   trip ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   [HOOKS] Executing post-run tasks...
   >>> [HOOK] Trip finished sending final summary...
   [PIPELINE STATUS] PIPE-30526082: COMPLETED
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   ✘ SISTEMA CAÍDO: 🔌 FALLO ELÉCTRICO CRÍTICO: El sistema se ha apagado inesperadamente.
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   
   >>> INSTRUCCIONES: Ejecuta este script una vez más para ver cómo WPipe
   >>> reanuda el trip saltándose la fase de preparación.