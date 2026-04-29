Nivel 133: Múltiples Background Tasks
=====================================

.. meta::
   :description: Múltiples tareas background ejecutándose en paralelo.
   :keywords: background, multiple, parallel, wpipe

Objetivo
--------
Demostrar que múltiples tareas background pueden ejecutarse simultáneamente.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level133.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   >>> DEMO 133: Múltiples Background Tasks
   ==================================================
   📌 Iniciando pipeline...
   🔄 [BG-1] Contador: 1
   ✅ Pipeline terminado. Contador final: 1
   demo_133 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   ⏱️ Tiempo de pipeline: 7ms
   💡 Las 3 tareas background se ejectaron en paralelo!
   💡 (Nota: Algunas pueden no completar antes de que el proceso termine)