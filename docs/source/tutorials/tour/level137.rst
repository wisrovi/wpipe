Nivel 137: Background con Tuple Steps
=====================================

.. meta::
   :description: Background acepta tuplas (func, name, version).
   :keywords: background, tuple, wpipe

Objetivo
--------
Mostrar que Background acepta tuplas como pasos.

Código Fuente
-------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level137.py
   :language: python
   :linenos:

Key Takeaway
------------
`Background((func, "name", "v1.0"))` funciona exactamente igual que `Background(func)`.