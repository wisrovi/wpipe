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

Advanced Features
-----------------

Parallel Execution with ParallelExecutor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute multiple steps concurrently for improved performance:

.. code-block:: python

   from wpipe.parallel import ParallelExecutor, ExecutionMode
   import time

   def fetch_url(data):
       time.sleep(1)  # Simulates IO wait
       return {"url_data": "fetched"}

   def process_data(data):
       time.sleep(1)
       return {"processed": True}

   def compute_heavy(data):
       time.sleep(1)
       return {"computed": True}

   # IO_BOUND: Best for network/disk operations
   executor = ParallelExecutor(mode=ExecutionMode.IO_BOUND, max_workers=10)
   executor.set_steps([
       (fetch_url, "Fetch URL", "v1.0"),
       (process_data, "Process", "v1.0"),
       (compute_heavy, "Compute", "v1.0"),
   ])

   result = executor.run({"input": "data"})

   # CPU_BOUND: Best for computation-heavy tasks
   cpu_executor = ParallelExecutor(mode=ExecutionMode.CPU_BOUND, max_workers=4)
   cpu_executor.set_steps([
       (compute_heavy, "Compute 1", "v1.0"),
       (compute_heavy, "Compute 2", "v1.0"),
   ])

   result = cpu_executor.run({"input": "data"})

For Loops in Pipelines
~~~~~~~~~~~~~~~~~~~~~~

Iterate over collections within a pipeline:

.. code-block:: python

   from wpipe.pipe import ForLoop

   def fetch_item(data):
       return {"items": [1, 2, 3, 4, 5]}

   def process_item(item_data):
       item = item_data["item"]
       return {"processed_item": item * 2}

   def aggregate(data):
       results = data.get("_loop_results", [])
       return {"all_processed": results, "count": len(results)}

   # Create a for loop step that iterates over 'items'
   loop_step = ForLoop(
       func=process_item,
       name="Process Each Item",
       version="v1.0",
       iterable_key="items",
   )

   pipeline = Pipeline()
   pipeline.set_steps([
       (fetch_item, "Fetch Items", "v1.0"),
       loop_step,
       (aggregate, "Aggregate Results", "v1.0"),
   ])

   result = pipeline.run({})
   # result['all_processed'] = [2, 4, 6, 8, 10]

Pipeline Composition with NestedPipelineStep
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Embed entire pipelines as single steps within larger workflows:

.. code-block:: python

   from wpipe.pipe import NestedPipelineStep

   # Create a sub-pipeline for data extraction
   extract_pipeline = Pipeline()
   extract_pipeline.set_steps([
       (lambda d: {"raw": "data"}, "Fetch Raw", "v1.0"),
       (lambda d: {"cleaned": d["raw"].upper()}, "Clean", "v1.0"),
   ])

   # Create a sub-pipeline for data transformation
   transform_pipeline = Pipeline()
   transform_pipeline.set_steps([
       (lambda d: {"transformed": d["cleaned"] + "_v2"}, "Transform", "v1.0"),
   ])

   # Wrap pipelines as nested steps
   extract_step = NestedPipelineStep(
       pipeline=extract_pipeline,
       name="Extract Phase",
       version="v1.0",
   )

   transform_step = NestedPipelineStep(
       pipeline=transform_pipeline,
       name="Transform Phase",
       version="v1.0",
   )

   # Build main pipeline using nested steps
   main_pipeline = Pipeline()
   main_pipeline.set_steps([
       extract_step,
       transform_step,
   ])

   result = main_pipeline.run({})
   # result['transformed'] = 'DATA_v2'

@step Decorator Usage
~~~~~~~~~~~~~~~~~~~~~

Simplify step creation with a decorator:

.. code-block:: python

   from wpipe.decorators import step

   @step(name="Fetch Data", version="v1.0")
   def fetch_data(data):
       return {"fetched": True, "records": [1, 2, 3]}

   @step(name="Transform", version="v1.0")
   def transform(data):
       return {"transformed": [r * 10 for r in data["records"]]}

   @step(name="Validate", version="v1.0")
   def validate(data):
       return {"valid": len(data["transformed"]) > 0}

   pipeline = Pipeline()
   pipeline.set_steps([
       fetch_data,
       transform,
       validate,
   ])

   result = pipeline.run({})
   # result['valid'] = True

   # Decorator with error handling
   @step(name="Risky Operation", version="v1.0", retry=3)
   def risky_op(data):
       import random
       if random.random() < 0.5:
           raise RuntimeError("Temporary failure")
       return {"success": True}

Checkpointing with CheckpointManager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Save and restore pipeline state for long-running workflows:

.. code-block:: python

   from wpipe.checkpoint import CheckpointManager

   def long_task_1(data):
       return {"task1_done": True}

   def long_task_2(data):
       return {"task2_done": True}

   def long_task_3(data):
       return {"task3_done": True}

   # Initialize checkpoint manager
   checkpoint_mgr = CheckpointManager(
       checkpoint_dir="./checkpoints",
       pipeline_name="my_pipeline",
   )

   pipeline = Pipeline()
   pipeline.set_steps([
       (long_task_1, "Task 1", "v1.0"),
       (long_task_2, "Task 2", "v1.0"),
       (long_task_3, "Task 3", "v1.0"),
   ])

   # Run with checkpointing - saves state after each step
   result = pipeline.run({"input": "data"})
   checkpoint_mgr.save(pipeline.get_accumulated_data())

   # Restore from checkpoint
   if checkpoint_mgr.exists():
       restored_data = checkpoint_mgr.load()
       print(f"Restored: {restored_data}")

   # List available checkpoints
   checkpoints = checkpoint_mgr.list_checkpoints()
   for cp in checkpoints:
       print(f"Checkpoint: {cp['name']} at {cp['timestamp']}")

   # Delete old checkpoints
   checkpoint_mgr.delete("my_pipeline_2024-01-01")

Resource Monitoring with ResourceMonitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Track CPU, memory, and disk usage during pipeline execution:

.. code-block:: python

   from wpipe.monitor import ResourceMonitor

   def heavy_computation(data):
       import time
       time.sleep(2)
       return {"computed": True}

   # Initialize monitor
   monitor = ResourceMonitor(
       interval=1.0,  # Sample every 1 second
       log_file="resource_usage.log",
   )

   # Start monitoring before pipeline
   monitor.start()

   pipeline = Pipeline()
   pipeline.set_steps([
       (heavy_computation, "Heavy Task 1", "v1.0"),
       (heavy_computation, "Heavy Task 2", "v1.0"),
   ])

   result = pipeline.run({"input": "data"})

   # Stop monitoring and get report
   monitor.stop()
   report = monitor.get_report()

   print(f"Peak CPU: {report['cpu']['peak']}%")
   print(f"Peak Memory: {report['memory']['peak']} MB")
   print(f"Average Disk I/O: {report['disk']['avg']} MB/s")

   # Export monitoring data
   monitor.export_report("monitoring_summary.json")

Exporting to JSON/CSV with PipelineExporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Serialize pipeline configurations and results:

.. code-block:: python

   from wpipe.export import PipelineExporter

   def step1(data):
       return {"value": data["x"] * 2}

   def step2(data):
       return {"final": data["value"] + 10}

   pipeline = Pipeline()
   pipeline.set_steps([
       (step1, "Double", "v1.0"),
       (step2, "Add Ten", "v1.0"),
   ])

   result = pipeline.run({"x": 5})

   # Export pipeline configuration to JSON
   exporter = PipelineExporter()
   exporter.to_json(pipeline, "pipeline_config.json")

   # Export results to JSON
   exporter.results_to_json(result, "pipeline_results.json")

   # Export results to CSV (for list-based results)
   results_list = [
       {"id": 1, "value": 10, "status": "ok"},
       {"id": 2, "value": 20, "status": "ok"},
   ]
   exporter.results_to_csv(results_list, "pipeline_results.csv")

   # Load pipeline from JSON config
   loaded_pipeline = exporter.from_json("pipeline_config.json")

Timeout Decorators
~~~~~~~~~~~~~~~~~~

Enforce time limits on long-running steps:

.. code-block:: python

   from wpipe.decorators import timeout
   from wpipe.exception import TimeoutError

   @timeout(seconds=5)
   def potentially_slow_operation(data):
       import time
       time.sleep(10)  # Will be interrupted
       return {"completed": True}

   @timeout(seconds=10, fallback={"status": "timed_out"})
   def with_fallback(data):
       import time
       time.sleep(15)
       return {"completed": True}

   pipeline = Pipeline()
   pipeline.set_steps([
       (potentially_slow_operation, "Timed Step", "v1.0"),
   ])

   try:
       result = pipeline.run({})
   except TimeoutError as e:
       print(f"Operation timed out after {e.seconds} seconds")

Async Pipelines with PipelineAsync
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fully asynchronous pipeline execution:

.. code-block:: python

   import asyncio
   from wpipe.asyncio import PipelineAsync

   async def async_fetch(data):
       await asyncio.sleep(1)
       return {"fetched": True, "data": [1, 2, 3]}

   async def async_transform(data):
       await asyncio.sleep(0.5)
       return {"transformed": [x * 2 for x in data["data"]]}

   async def async_save(data):
       await asyncio.sleep(0.5)
       return {"saved": True, "result": data["transformed"]}

   async def run_pipeline():
       pipeline = PipelineAsync(verbose=True)
       pipeline.set_steps([
           (async_fetch, "Async Fetch", "v1.0"),
           (async_transform, "Async Transform", "v1.0"),
           (async_save, "Async Save", "v1.0"),
       ])

       result = await pipeline.run({"input": "data"})
       return result

   # Execute async pipeline
   result = asyncio.run(run_pipeline())
   # result['saved'] = True
   # result['result'] = [2, 4, 6]

   # Async with error handling
   async def run_pipeline_safe():
       pipeline = PipelineAsync()
       pipeline.set_steps([
           (async_fetch, "Async Fetch", "v1.0"),
       ])

       try:
           result = await pipeline.run({})
           return result
       except Exception as e:
           print(f"Async pipeline error: {e}")
           return None
