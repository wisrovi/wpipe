Nivel 52: demo_level52.py
=========================

Este es el nivel 52 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level52.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   Traceback (most recent call last):
     File "/home/william.rodriguez/Documents/wpipe/examples/00_honey_pot/03_yield/demo_level52.py", line 179, in <module>
       asyncio.run(main())
       ~~~~~~~~~~~^^^^^^^^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/asyncio/runners.py", line 195, in run
       return runner.run(main)
              ~~~~~~~~~~^^^^^^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/asyncio/runners.py", line 118, in run
       return self._loop.run_until_complete(task)
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/asyncio/base_events.py", line 725, in run_until_complete
       return future.result()
              ~~~~~~~~~~~~~^^
     File "/home/william.rodriguez/Documents/wpipe/examples/00_honey_pot/03_yield/demo_level52.py", line 150, in main
       trip = await get_viaje_pipeline_async()
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     File "/home/william.rodriguez/Documents/wpipe/examples/00_honey_pot/03_yield/demo_level52.py", line 67, in get_viaje_pipeline_async
       trip = PipelineAsync(
           pipeline_name="viaje_async",
       ...<6 lines>...
           show_progress=True,
       )
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe_async.py", line 118, in __init__
       self.tracker = PipelineTracker(tracking_db, config_dir)
                      ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/tracking/tracker.py", line 161, in __init__
       self.db_pipelines = WSQLite(pipelines, db_path)
                           ~~~~~~~^^^^^^^^^^^^^^^^^^^^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wsqlite/core/repository.py", line 79, in __init__
       self._pool = get_pool(
                    ~~~~~~~~^
           db_path,
           ^^^^^^^^
           min_size=min_pool_size,
           ^^^^^^^^^^^^^^^^^^^^^^^
           max_size=pool_size,
           ^^^^^^^^^^^^^^^^^^^
       )
       ^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wsqlite/core/pool.py", line 459, in get_pool
       _global_sync_pool = ConnectionPool(
           db_path,
       ...<2 lines>...
           **kwargs,
       )
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wsqlite/core/pool.py", line 84, in __init__
       self._init_pragmas()
       ~~~~~~~~~~~~~~~~~~^^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wsqlite/core/pool.py", line 94, in _init_pragmas
       conn = self._create_connection()
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wsqlite/core/pool.py", line 125, in _create_connection
       conn.execute(f"PRAGMA journal_mode={self.journal_mode}")
       ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   sqlite3.DatabaseError: database disk image is malformed