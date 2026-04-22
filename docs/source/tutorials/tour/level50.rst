Nivel 50: demo_level50.py
=========================

Este es el nivel 50 del tour de aprendizaje.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level50.py
   :language: python
   :linenos:

Resultado de Ejecución
----------------------

.. code-block:: text

   >>> [CHECKPOINT] Inicio del viaje
   --- Nuevo viaje --- (Iteración: 0)
   viaje - print_info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   >>> [HOOK] El viaje ha terminado, enviando resumen final...
   
   Resource Summary:
     - Peak RAM: 4207.94 MB
     - Avg CPU: 56.83%
   ✓ Total time monitored: 8.08s
   
   Viajes completados: 0
   Gasolina final: Medio
   Aceite final: Medio
   
   Fired Alerts:
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
     - [CRITICAL] Unknown: Pipeline viaje_tmp alert
   
   ======================================================================
   SUPPORTED EXPORT FORMATS
   ======================================================================
   
   JSON Export:
     - Human readable
     - Best for nested/complex data
     - Supported by: Python, JavaScript, most tools
     - Usage: exporter.export_pipeline_logs(format='json')
   
   CSV Export:
     - Spreadsheet compatible
     - Best for tabular data
     - Supported by: Excel, Google Sheets, Pandas
     - Usage: exporter.export_pipeline_logs(format='csv')
   
   ======================================================================
   EXPORTING DATA
   ======================================================================
   
   1. Exporting statistics to JSON...
      ✓ Saved to: output/export_output/pipeline_statistics.json
   
      Statistics:
        - total_executions: 121
        - successful_executions: 36
        - success_rate_percent: 29.75
        - average_execution_time_seconds: 0.48
        - exported_at: 2026-04-23T01:14:40.683798
   
   2. Exporting pipeline logs...
   
   ======================================================================
   JSON EXPORT
   ======================================================================
   ✓ Exported to: output/export_output/pipeline_logs.json
     File size: 250713 bytes
     Records: 121
     Sample record keys: ['id', 'name', 'worker_id', 'worker_name', 'status', 'started_at', 'completed_at', 'total_duration_ms', 'input_data', 'output_data', 'error_message', 'error_step', 'parent_pipeline_id', 'yaml_path']
   
   ======================================================================
   CSV EXPORT
   ======================================================================
   ✓ Exported to: output/export_output/pipeline_logs.csv
     File size: 211217 bytes
     Records: 121
     Columns: 14
     Header: id,name,worker_id,worker_name,status,started_at,completed_at,total_duration_ms,input_data,output_data,error_message,error_step,parent_pipeline_id,yaml_path
   
   ======================================================================
   AVAILABLE EXPORTS
   ======================================================================
   
   ✓ pipeline_logs.json (250713 bytes)
   ✓ pipeline_logs.csv (211217 bytes)
   ✓ pipeline_statistics.json (182 bytes)
   
   ✓ Export demo completed!
   
   ======================================================================
   📊 ANÁLISIS DE RENDIMIENTO (AnalysisManager)
   ======================================================================
   
   Resumen Global:
     - Total Ejecuciones: 121
     - Tasa de Éxito: 29.8%
     - Duración Media: 1274.01 ms
   
   Tendencia de Hoy:
     - Ejecuciones realizadas: 94
     - Éxitos: 30

