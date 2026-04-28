Nivel 134: Background con Pipeline Anidado
==========================================

.. meta::
   :description: Background ejecutando un pipeline completo.
   :keywords: background, nested, pipeline, wpipe

Objetivo
--------
Mostrar que Background puede ejecutar pipelines anidados completos.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level134.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   >>> DEMO 134: Background con Pipeline Anidado
   ==================================================
   📌 Preparando...
     📦 [Nested] Procesando paso 1...
     📦 [Nested] Procesando paso 2...
   ✅ Pipeline principal continúa sin esperar el nested!
   demo_134     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   sub_pipeline ━━━━━━━━━━━━━━━━━━━━                      50% -:--:--
   
   ✅ Pipeline principal NO esperó el sub-pipeline!