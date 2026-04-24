Nivel 132: Background con Captura de Errores
=============================================

.. meta::
   :description: Aprende a manejar errores en background tasks sin detener el pipeline.
   :keywords: background, error handling, capture_error, wpipe

Objetivo
--------
Mostrar cómo manejar errores en tareas background sin que el pipeline se detenga.

Conceptos Clave
---------------
* **capture_error=True**: Permite capturar errores del background en handlers.
* **Error Handling**: Los errores se manejan pero no detienen el pipeline.
* **Silent Fail**: Por defecto los errores se ignoran silenciosamente.

¿Qué estamos probando?
----------------------
Una tarea en background que falla se captura mediante error handlers sin detener la ejecución:

1. La tarea background genera un error.
2. El error handler lo captura.
3. El pipeline continúa normalmente.

Código Fuente
-------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level132.py
   :language: python
   :linenos:

Resultado de Ejecución
----------------------

.. code-block:: text

   >>> DEMO 132: Background con Capture Error
   ==================================================
   📌 Iniciando...
   🔄 [BACKGROUND] Iniciando tarea que fallará...
   ✅ Pipeline continúa a pesar del error en background!
   demo_132 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

   ✅ El pipeline NO se detuvo por el error!

Key Takeaway
------------
Background tasks con `capture_error=True` permiten robustez - el pipeline nunca falla por tareas secundarias.