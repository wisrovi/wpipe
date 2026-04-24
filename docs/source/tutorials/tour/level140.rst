Nivel 140: El Zen de WPipe - Demo Final de Background Tasks
============================================================

.. meta::
   :description: El último nivel del tour de aprendizaje. Repaso completo de Background.
   :keywords: finale, zen, mastery, background, wpipe

Objetivo
--------
Llegar a la cima de **La Senda del Maestro** con un demo final que resume toda la funcionalidad de Background Tasks.

Conceptos Clave
---------------
* **Fire & Forget**: Ejecución sin bloquear.
* **Daemon Threads**: No bloquean terminación del proceso.
* **Error Handling Opcional**: capture_error para robustez.
* **Universal**: Funciona con funciones, tuplas, pipelines anidados, y en async.

¿Qué estamos probando?
----------------------
Un pipeline completo que demuestra:
1. Múltiples backgrounds en paralelo.
2. Captura de errores sin detener.
3. Pipeline continúa normalmente.

Código Fuente
-------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level140.py
   :language: python
   :linenos:

Cierre del Tour
---------------

¡Felicidades! Has completado los **140 niveles** de la **Senda del Maestro de WPipe**. Ahora tienes el conocimiento necesario para:
* Diseñar arquitecturas de datos de alto rendimiento.
* Construir sistemas resilientes con checkpoints.
* Escalar con paralelismo nativo y Background Tasks.
* Monitorizar desde el Dashboard.
* Manejar errores con precisión forense.

**¡Bienvenido al nivel de Maestro de WPipe!**

Resultado de Ejecución
----------------------

.. code-block:: text

   ==================================================
   🎉 DEMO FINAL - Background Tasks
   ==================================================

   📋 Características de Background:
     • Ejecución sin bloquear el pipeline
     • Retorno ignorado (no afecta datos)
     • capture_error=True para manejar fallos
     • Funciona con PipelineAsync
     • Acepta funciones, tuplas, y pipelines anidados

   📝 [BG] Enviando logs...
   📡 [BG] Enviando telemetría...
   ✅ Tarea normal completada

   ==================================================
   📊 Ejecución completada!
      Log: ['normal']
   ==================================================
   demo_140 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

   ✅ Demo completado exitosamente!
      - Background tasks ejecutados en paralelo
      - Error capturado sin detener pipeline
      - Pipeline continuó normalmente