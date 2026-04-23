Nivel 25: Super-Computación (Threads vs Processes)
===================================================

.. meta::
   :description: Benchmarking de ejecución paralela: Hilos vs Procesos en WPipe.
   :keywords: benchmark, parallel, multi-core, threads, processes, wpipe

Objetivo
--------
Entender la diferencia técnica y de rendimiento entre usar hilos (`Threads`) y procesos (`Processes`) para tareas pesadas. Aprenderás a elegir la mejor herramienta según la carga de trabajo (I/O vs CPU).

Conceptos Clave
---------------
* **GIL (Global Interpreter Lock)**: La barrera de Python para el verdadero paralelismo en hilos.
* **ProcessPoolExecutor**: Cómo WPipe utiliza múltiples núcleos del procesador para tareas matemáticas o de visión artificial.
* **Serialización**: La necesidad de que los datos sean "picklable" cuando se cruzan las fronteras de los procesos.

¿Qué estamos probando?
----------------------
En este nivel realizamos un benchmark real. Ejecutamos 4 tareas de visión artificial simuladas (carga intensa de CPU) de dos formas:
1. **Eco Mode (Hilos)**: Comparten el mismo núcleo, limitados por el GIL.
2. **Sport Mode (Procesos)**: Se expanden por todos los núcleos disponibles del sistema.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level25.py
   :language: python
   :linenos:

Análisis de Resultados
----------------------

Al ejecutar este nivel, notarás que:
* El tiempo de los **procesos** es aproximadamente 4 veces menor en sistemas multi-núcleo.
* WPipe abstrae toda la complejidad de creación de pools y gestión de señales de terminación.
* Solo necesitas cambiar `use_processes=True` para liberar el poder total de tu hardware.

Resultado de Ejecución
----------------------

.. code-block:: text

   >>> [TEST 1] Processing with THREADS (Sharing resources)...
   ⏱️ Threads Time: 1.25s

   >>> [TEST 2] Processing with PROCESSES (Total Power)...
   ⏱️ Processes Time: 0.35s
