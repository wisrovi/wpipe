Nivel 130: Integración de API y Métricas de Negocio
==================================================

.. meta::
   :description: Demostración de integración con API y registro de métricas.
   :keywords: api, metrics, mastery, wpipe

Objetivo
--------
Continuar el ascenso por **La Senda del Maestro**. En este nivel, realizamos una demostración limpia y potente de integración con API y registro de métricas personalizadas.

Conceptos Clave
---------------
* **Métricas de Negocio**: Uso de `Metric.record` para capturar KPIs que no son solo técnicos.
* **Integración API**: Consolidación del flujo de registro de procesos remotos.
* **Trazabilidad**: Capacidad de monitorizar cada detalle del pipeline.

¿Qué estamos probando?
----------------------
Validamos el ciclo de vida de un pipeline con observabilidad:
1. Registro del proceso en el sistema.
2. Ejecución de pasos con metadatos.
3. Captura de métricas de negocio en tiempo real.
4. Finalización exitosa.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level130.py
   :language: python
   :linenos:

Resultado de Ejecución
----------------------

.. code-block:: text

   ==================================================
   🎉 DEMO FINAL - API Integration
   ==================================================
   🔑 Starting API system...
   ⚡ Processing data...
   viaje_l130 - Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

   ✅ Demo completed with success!
   📊 Metric: api_calls = 1
