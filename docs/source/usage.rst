Usage Examples
=============

This section contains comprehensive examples demonstrating all wpipe features.

Basic Pipeline
--------------

Simple Pipeline with Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most basic use case:

.. code-block:: python

   from wpipe import Pipeline

   def step1(data):
       return {"result": data["x"] * 2}

   def step2(data):
       return {"final": data["result"] + 10}

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (step1, "Step 1", "v1.0"),
       (step2, "Step 2", "v1.0"),
   ])

   result = pipeline.run({"x": 5})
   # {'x': 5, 'result': 10, 'final': 20}

Pipeline with Class Steps
~~~~~~~~~~~~~~~~~~~~~~~~~

Using class instances for stateful operations:

.. code-block:: python

   class DataProcessor:
       def __init__(self, multiplier):
           self.multiplier = multiplier

       def __call__(self, data):
           return {"processed": data["value"] * self.multiplier}

   processor = DataProcessor(3)
   pipeline.set_steps([
       (processor, "Process", "v1.0"),
   ])

   result = pipeline.run({"value": 10})
   # {'value': 10, 'processed': 30}

Pipeline with Lambda Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~

For simple one-liner transformations:

.. code-block:: python

   pipeline.set_steps([
       ((lambda d: {**d, "doubled": d["x"] * 2}), "Double", "v1.0"),
       ((lambda d: {**d, "tripled": d["x"] * 3}), "Triple", "v1.0"),
   ])

Mixed Step Types
~~~~~~~~~~~~~~~~

Combine functions, classes, and lambdas:

.. code-block:: python

   def fetch(data):
       return {"items": [1, 2, 3]}

   class Transformer:
       def __call__(self, data):
           return {"transformed": [x * 2 for x in data["items"]]}

   pipeline = Pipeline()
   pipeline.set_steps([
       (fetch, "Fetch", "v1.0"),
       (Transformer(), "Transform", "v1.0"),
       ((lambda d: {**d, "count": len(d["transformed"])}), "Count", "v1.0"),
   ])

Data Flow Examples
-----------------

Understanding Accumulated Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each step can access all previous results:

.. code-block:: python

   def step_a(data):
       return {"from_a": "hello"}

   def step_b(data):
       return {
           "from_b": "world",
           "combined": f"{data['from_a']} {data['from_b']}"
       }

   def step_c(data):
       return {"from_c": True, "all": data}

Conditional Branching
~~~~~~~~~~~~~~~~~~~~~

Execute different paths based on data:

.. code-block:: python

   from wpipe.pipe import Condition

   def fetch_status(data):
       return {"status": "active", "value": 75}

   def process_active(data):
       return {"processed": True, "type": "active"}

   def process_inactive(data):
       return {"processed": True, "type": "inactive"}

   condition = Condition(
       expression="status == 'active'",
       branch_true=[(process_active, "Process Active", "v1.0")],
       branch_false=[(process_inactive, "Process Inactive", "v1.0")],
   )

   pipeline = Pipeline()
   pipeline.set_steps([
       (fetch_status, "Fetch", "v1.0"),
       condition,
   ])

API Integration
---------------

Basic API Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Connect to an external API:

.. code-block:: python

   from wpipe import Pipeline

   api_config = {
       "base_url": "http://localhost:8418",
       "token": "my_secret_token"
   }

   pipeline = Pipeline(
       worker_name="my_worker",
       api_config=api_config,
       verbose=True
   )

Worker Registration
~~~~~~~~~~~~~~~~~~

Register your pipeline as a worker:

.. code-block:: python

   worker_id = pipeline.worker_register(
       name="data_processor",
       version="1.0.0"
   )

   if worker_id:
       pipeline.set_worker_id(worker_id.get("id"))

Health Checks
~~~~~~~~~~~~~

Keep worker alive with periodic checks:

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

SQLite Storage
--------------

Write Results to Database
~~~~~~~~~~~~~~~~~~~~~~~~~

Persist pipeline results:

.. code-block:: python

   from wpipe import Pipeline
   from wpipe.sqlite import Wsqlite

   db = Wsqlite("results.db")

   pipeline = Pipeline()
   pipeline.set_steps([
       (step1, "Step 1", "v1.0"),
       (step2, "Step 2", "v1.0"),
   ])

   result = pipeline.run({"input": "data"})
   db.write(input_data={"input": "data"}, output_data=result)

Read and Query
~~~~~~~~~~~~~~

Retrieve stored results:

.. code-block:: python

   results = db.read()
   for row in results:
       print(row)

   # Custom queries
   filtered = db.query("SELECT * FROM results WHERE input_x > ?", (5,))

YAML Configuration
-----------------

Load Configuration from YAML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe.util import leer_yaml

   config = leer_yaml("config.yaml")
   # config = {'name': 'pipeline', 'version': '1.0'}

Save Results to YAML
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe.util import escribir_yaml

   result = pipeline.run({"x": 10})
   escribir_yaml("output.yaml", {"result": result})

Error Handling
--------------

Basic Error Catching
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe.exception import TaskError, ProcessError

   try:
       result = pipeline.run({"x": 10})
   except (TaskError, ProcessError) as e:
       print(f"Error: {e}")
       print(f"Code: {e.error_code}")

Accessing Partial Results
~~~~~~~~~~~~~~~~~~~~~~~~~

Get data accumulated before failure:

.. code-block:: python

   try:
       result = pipeline.run({"x": 10})
   except (TaskError, ProcessError) as e:
       if hasattr(e, 'data'):
           print(f"Partial results: {e.data}")

Retry Logic
-----------

Automatic Retries
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe.pipe import Retry

   def unstable_api(data):
       import random
       if random.random() < 0.5:
           raise ConnectionError("Network error")
       return {"success": True}

   retry_step = Retry(
       func=unstable_api,
       name="API Call",
       version="v1.0",
       attempts=3,
       wait=1.0,
   )

   pipeline.set_steps([retry_step])

Exponential Backoff
~~~~~~~~~~~~~~~~~~~

Increasing wait between retries:

.. code-block:: python

   retry_step = Retry(
       func=unstable_api,
       name="API Call",
       version="v1.0",
       attempts=5,
       wait=1.0,
       backoff=2.0,  # 1s, 2s, 4s, 8s, 16s
   )

Nested Pipelines
----------------

Compose Complex Workflows
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   extract_pipeline = Pipeline()
   extract_pipeline.set_steps([
       (fetch_data, "Fetch", "v1.0"),
       (parse_data, "Parse", "v1.0"),
   ])

   transform_pipeline = Pipeline()
   transform_pipeline.set_steps([
       (clean_data, "Clean", "v1.0"),
       (enrich_data, "Enrich", "v1.0"),
   ])

   main_pipeline = Pipeline()
   main_pipeline.set_steps([
       (extract_pipeline, "Extract", "v1.0"),
       (transform_pipeline, "Transform", "v1.0"),
   ])

Async Execution
--------------

Async Pipeline
~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio

   async def main():
       result = await pipeline.run({"x": 10})
       return result

   result = asyncio.run(main())

Running Examples
----------------

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe.git
   cd wpipe/examples

Run Specific Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd examples/01_basic_pipeline/01_simple_function
   python example.py

View Examples Directory
~~~~~~~~~~~~~~~~~~~~~~

All 100+ examples are organized in ``examples/``:

* ``01_basic_pipeline/`` - Basic usage (15 examples)
* ``02_api_pipeline/`` - API integration (21 examples)
* ``03_error_handling/`` - Error handling (10 examples)
* ``04_condition/`` - Conditional logic (9 examples)
* ``05_retry/`` - Retry patterns (9 examples)
* ``06_sqlite_integration/`` - SQLite storage (9 examples)
* ``07_nested_pipelines/`` - Nested workflows (9 examples)
* ``08_yaml_config/`` - YAML configuration (9 examples)
* ``09_microservice/`` - Microservice patterns (9 examples)
