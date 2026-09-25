Nivel 52: demo_level52.py
=========================

Este es el nivel 52 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
-------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level52.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
----------------------


   Carro inicial: Medium
   
   
   [ASYNC CHECKPOINT REACHED] trip_start
   >>> [CHECKPOINT] Inicio del trip
   --- Nuevo trip asíncrono --- (Iteration: 0)
   
   [PARALLEL ASYNC] Executing 3 steps concurrently
     [ERROR] Loop broken at iteration 0 due to: 'coroutine' object is not iterable
   
   [ASYNC STATUS] PIPE-2F402D3F: ERROR
   
   Resource Summary (Async):
     - Peak RAM: 52.02 MB
     - Avg CPU: 0.0%
   ✓ Total time monitored: 0.01s
   
   Viajes completados: 0
   
   ======================================================================
   📊 ANÁLISIS DE RENDIMIENTO ASÍNCRONO
   ======================================================================
     - Total Ejecuciones: 33
     - Tasa de Éxito: 66.7%
   /home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe_async.py:490: RuntimeWarning: coroutine 'check_lights' was never awaited
     return await self._execute_task(item, data, parent_step_id, parallel_group, **kwargs)
   RuntimeWarning: Enable tracemalloc to get the object allocation traceback