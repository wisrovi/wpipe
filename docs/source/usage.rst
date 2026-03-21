Usage
=====

Basic Usage
-----------

Creating a Pipeline
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe.pipe import Pipeline

   def my_step(data):
       return {"result": data["input"] * 2}

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (my_step, "My Step", "v1.0"),
   ])

   result = pipeline.run({"input": 10})

Adding Multiple Steps
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def step1(data):
       return {"step1": "completed"}

   def step2(data):
       return {"step2": "completed"}

   class Step3:
       def __call__(self, data):
           return {"step3": "completed"}

   pipeline.set_steps([
       (step1, "First", "v1.0"),
       (step2, "Second", "v1.0"),
       (Step3(), "Third", "v1.0"),
   ])

Using API Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   api_config = {
       "base_url": "http://localhost:8418",
       "token": "mysecrettoken"
   }

   pipeline = Pipeline(
       api_config=api_config,
       worker_name="my_worker",
       verbose=True
   )

Worker Registration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   worker_id = pipeline.worker_register(
       name="my_pipeline",
       version="v1.0.0"
   )

   if worker_id:
       pipeline.set_worker_id(worker_id.get("id"))

SQLite Integration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe.sqlite import Wsqlite

   with Wsqlite(db_name="results.db") as db:
       db.input = {"data": "input_value"}
       result = pipeline.run({"data": "input_value"})
       db.output = result

Configuration
-------------

API Configuration
~~~~~~~~~~~~~~~~~

The API configuration dictionary can include:

- ``base_url``: The URL of the API server
- ``token``: Authentication token

Step Definition
~~~~~~~~~~~~~~

Steps are defined as tuples of (function, name, version):

- ``function``: A callable that accepts a dict and returns a dict
- ``name``: A string identifier for the step
- ``version``: A string version identifier
