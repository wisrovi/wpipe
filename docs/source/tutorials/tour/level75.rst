Nivel 75: Orquestación Híbrida (For + Parallel)
===============================================

.. meta::
   :description: Combinación de bucles For y ejecución paralela para sistemas complejos.
   :keywords: hybrid, for, parallel, orchestration, hierarchy, wpipe

Objetivo
--------
Dominar la jerarquía de orquestación. Aprenderás a anidar un bloque `Parallel` dentro de un bucle `For`, permitiendo ejecuciones masivas y estructuradas de tareas que requieren procesamiento simultáneo en cada iteración.

Conceptos Clave
---------------
* **Jerarquía de Control**: La capacidad de WPipe de manejar estructuras anidadas sin perder la trazabilidad.
* **Fusión de Datos**: Cómo múltiples tareas paralelas consolidan su información antes de que el bucle continúe a la siguiente iteración.
* **Escalabilidad Vertical**: Optimización del tiempo de ciclo en procesos repetitivos.

¿Qué estamos probando?
----------------------
Simulamos el sistema de percepción de un vehículo autónomo. En cada iteración del bucle principal (el ciclo de control del coche), debemos leer tres sensores críticos (Cámara, Radar y LiDAR) en paralelo para minimizar la latencia, y luego fusionar esos datos.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
-------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level75.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
----------------------


   
   >>> Sensores en paralelo dentro de bucle...
   
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
     📷 Cámara
     📡 Radar
     🔴 LiDAR
   🧠 Fusionando datos...
   [PARALLEL] Executing 3 steps using THREADS (workers=3)
     📷 Cámara
     📡 Radar
     🔴 LiDAR
   🧠 Fusionando datos...
   viaje_l75_forparallel ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00