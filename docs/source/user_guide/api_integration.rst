API Integration
===============

Connect your pipelines to external APIs for worker registration and process tracking.

Overview
--------

wpipe can integrate with external APIs to:

* Register workers and track their health
* Log process executions
* Monitor task progress
* Store execution history

Basic Configuration
-------------------

.. code-block:: python

   from wpipe import Pipeline

   api_config = {
       "base_url": "http://localhost:8418",
       "token": "your_secret_token"
   }

   pipeline = Pipeline(
       worker_name="my_worker",
       api_config=api_config,
       verbose=True
   )

Configuration Options
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Option
     - Type
     - Description
   * - ``base_url``
     - str
     - API server URL (required)
   * - ``token``
     - str
     - Authentication token (required)
   * - ``timeout``
     - int
     - Request timeout in seconds (default: 30)
   * - ``headers``
     - dict
     - Custom HTTP headers
   * - ``max_retries``
     - int
     - API call retry attempts

Worker Registration
--------------------

Register your pipeline as a worker:

.. code-block:: python

   worker_id = pipeline.worker_register(
       name="data_processor",
       version="v1.0.0"
   )

   if worker_id:
       pipeline.set_worker_id(worker_id.get("id"))

Health Checks
-------------

Keep worker alive with health checks:

.. code-block:: python

   import threading
   import time

   def health_checker():
       while not stop_event.is_set():
           pipeline.healthcheck_worker(worker_id)
           time.sleep(30)

   stop_event = threading.Event()
   checker_thread = threading.Thread(target=health_checker)
   checker_thread.start()

   # Later, stop the checker
   stop_event.set()
   checker_thread.join()

Complete Example
----------------

.. code-block:: python

   from wpipe import Pipeline

   api_config = {
       "base_url": "http://localhost:8418",
       "token": "my_secret_token"
   }

   pipeline = Pipeline(
       worker_name="etl_pipeline",
       api_config=api_config,
       verbose=True
   )

   pipeline.set_steps([
       (extract_data, "Extract", "v1.0"),
       (transform_data, "Transform", "v1.0"),
       (load_data, "Load", "v1.0"),
   ])

   worker_id = pipeline.worker_register("etl_worker", "v1.0")
   pipeline.set_worker_id(worker_id.get("id"))

   result = pipeline.run({"source": "database"})

Error Handling
--------------

Handle API errors gracefully:

.. code-block:: python

   pipeline.SHOW_API_ERRORS = False  # Silent mode (default)
   pipeline.SHOW_API_ERRORS = True   # Raises exceptions

Local Mode
----------

Run without API (local only):

.. code-block:: python

   pipeline = Pipeline(verbose=True)
   # No api_config = local mode

Best Practices
--------------

1. **Handle unavailable API**: Design for graceful degradation
2. **Configure timeouts**: Prevent indefinite hanging
3. **Store worker_id**: Persist to avoid re-registration
4. **Use health checks**: Keep worker status updated

Next Steps
---------

* Learn about :doc:`sqlite` for local data storage
* Explore :doc:`error_handling` for error recovery
