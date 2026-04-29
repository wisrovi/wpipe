Nivel 2: Metadatos y Decorador @step
====================================

.. meta::
   :description: Introducción al decorador @step para trazabilidad y versionado.
   :keywords: decorator, step, metadata, traceability, wpipe

Objetivo
--------
Aprender a enriquecer las tareas del pipeline utilizando el decorador `@step` para proporcionar nombres legibles, versionado y trazabilidad mejorada.

Conceptos Clave
---------------
* **Decorador @step**: Cómo usar metadatos para identificar tareas en el Dashboard y logs.
* **Trazabilidad**: Identificación única de versiones de cada paso.
* **Flujo de Datos II**: Cómo el diccionario de salida de un paso se inyecta como entrada en el siguiente.

¿Qué estamos probando?
----------------------
En este nivel probamos la capacidad del motor para extraer metadatos de las funciones decoradas. Validamos que el orquestador respete el nombre y la versión definidos en el decorador, y que mantenga la integridad del flujo de datos entre un paso simple y un paso decorado.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level2.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   🔑 Turning key: Engine started. Input data: {'_pipeline_start_time': '2026-04-29T12:55:04.580892', 'progress_rich': <rich.progress.Progress object at 0x7ed3b0fa7230>}
   👟 Testing pedals: Brakes verified. Input data: {'_pipeline_start_time': '2026-04-29T12:55:04.580892', 'progress_rich': <rich.progress.Progress object at 0x7ed3b0fa7230>, 'engine': 'ON', 'fuel': 100}
   Trip_L2 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00