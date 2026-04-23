Nivel 75: Orquestación Híbrida (For + Parallel)
==================================================

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

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level75.py
   :language: python
   :linenos:

Análisis de la Arquitectura
---------------------------

Este nivel demuestra la **potencia compositiva** de WPipe:
1. El `For` dicta el ritmo global (2 iteraciones).
2. Dentro de cada iteración, el `Parallel` lanza 3 hilos de ejecución.
3. El motor garantiza que la función `process` (fusión de datos) solo se ejecute cuando los 3 sensores hayan terminado su lectura.
4. Se mantiene un único contexto (`Warehouse`) que se enriquece de forma atómica.

Resultado de Ejecución
----------------------

.. code-block:: text

   >>> Sensores en paralelo dentro de bucle...

   📷 Cámara
   📡 Radar
   🔴 LiDAR
   🧠 Fusionando datos...
   
   (Iteración 2)
   📷 Cámara
   📡 Radar
   🔴 LiDAR
   🧠 Fusionando datos...
   
   viaje_l75_forparallel - Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
