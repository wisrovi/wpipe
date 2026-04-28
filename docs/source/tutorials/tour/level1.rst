Nivel 1: Conceptos Básicos de Pipeline
======================================

.. meta::
   :description: Fundamentos de WPipe: Creación de tu primer pipeline.
   :keywords: pipeline, setup, beginner, tutorial, wpipe

Objetivo
--------
Aprender a instanciar el motor de orquestación de **WPipe** y ejecutar una tarea atómica para verificar que el sistema está correctamente instalado y configurado.

Conceptos Clave
---------------
* **Instanciación**: Creación del objeto `Pipeline`.
* **Verbose Mode**: Uso del flag `verbose=True` para ver el progreso detallado en consola.
* **Flujo de Trabajo**: Registro de funciones simples como pasos del pipeline.

¿Qué estamos probando?
----------------------
En este nivel validamos la conectividad básica del motor. Estamos probando que una función estándar de Python pueda ser inyectada en el orquestador, ejecutada sin errores y que el sistema sea capaz de mostrar la barra de progreso de `Rich`.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level1.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   🔑 Turning key: Engine started. Input data: {'_pipeline_start_time': '2026-04-28T08:50:03.797476', 'progress_rich': <rich.progress.Progress object at 0x761b9c6eb0e0>}
   Trip_L1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00