Tutorials
=========

This section contains tutorials for learning how to use wpipe.

Tutorial 1: Basic Setup
-----------------------

Learn how to create your first pipeline.

.. code-block:: python

   from wpipe.pipe import Pipeline

   def step1(data):
       return {"result": data["x"] * 2}

   def step2(data):
       return {"final": data["result"] + 10}

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (step1, "Double", "v1.0"),
       (step2, "Add Ten", "v1.0"),
   ])

   result = pipeline.run({"x": 5})

Tutorial 2: Worker Registration
-------------------------------

Learn how to register workers with the API.

.. code-block:: python

   api_config = {
       "base_url": "http://localhost:8418",
       "token": "mysecrettoken"
   }

   pipeline = Pipeline(api_config=api_config)
   pipeline.set_steps([...])

   worker_id = pipeline.worker_register(
       name="my_worker",
       version="v1.0.0"
   )

   pipeline.set_worker_id(worker_id.get("id"))

Tutorial 3: Using Classes as Steps
---------------------------------

Learn how to use classes with __call__ as pipeline steps.

.. code-block:: python

   class ProcessData:
       def __init__(self, multiplier):
           self.multiplier = multiplier

       def __call__(self, data):
           return {"result": data["x"] * self.multiplier}

   pipeline = Pipeline()
   pipeline.set_steps([
       (ProcessData(2), "Step 1", "v1.0"),
       (ProcessData(3), "Step 2", "v1.0"),
   ])

Tutorial 4: Error Handling
-------------------------

Learn how to handle errors in pipelines.

.. code-block:: python

   from wpipe.exception import TaskError

   def validate(data):
       if "x" not in data:
           raise ValueError("Missing 'x' field")
       return {"validated": True}

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([(validate, "Validate", "v1.0")])

   try:
       result = pipeline.run({})
   except TaskError as e:
       print(f"Pipeline failed: {e}")

Tutorial 5: Nested Pipelines
----------------------------

Learn how to nest pipelines within each other.

.. code-block:: python

   pipeline1 = Pipeline()
   pipeline1.set_steps([...])

   pipeline2 = Pipeline()
   pipeline2.set_steps([
       (pipeline1.run, "Nested", "v1.0"),
       ...
   ])

Tutorial 6: SQLite Integration
-----------------------------

Learn how to persist pipeline execution results.

.. code-block:: python

   from wpipe.sqlite import Wsqlite

   with Wsqlite(db_name="results.db") as db:
       db.input = {"x": 10}
       result = pipeline.run({"x": 10})
       db.output = result
