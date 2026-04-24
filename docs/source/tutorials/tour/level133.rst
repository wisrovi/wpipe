Nivel 133: Múltiples Background Tasks
=====================================

.. meta::
   :description: Múltiples tareas background ejecutándose en paralelo.
   :keywords: background, multiple, parallel, wpipe

Objetivo
--------
Demostrar que múltiples tareas background pueden ejecutarse simultáneamente.

Código Fuente
-------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level133.py
   :language: python
   :linenos:

Key Takeaway
------------
Todas las tareas background se ejecutan en paralelo como daemon threads.