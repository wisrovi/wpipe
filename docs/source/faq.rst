FAQ
===

General Questions
-----------------

What is wpipe?
~~~~~~~~~~~~~~

wpipe is a Python library for creating and executing pipelines with task orchestration, API integration, and execution tracking.

What are the main features?
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Pipeline creation with step functions
- API integration for tracking execution
- Worker registration and health checks
- SQLite integration for persistence
- YAML configuration support
- Nested pipeline execution
- Rich progress visualization

Is wpipe free to use?
~~~~~~~~~~~~~~~~~~~~

Yes, wpipe is released under the MIT License.

Installation Questions
----------------------

What Python version is required?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wpipe requires Python 3.9 or higher.

How do I install wpipe?
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install wpipe

How do I install from source?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe
   cd wpipe
   pip install -e .

Usage Questions
---------------

How do I create a basic pipeline?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe.pipe import Pipeline

   def step(data):
       return {"result": data["x"] * 2}

   pipeline = Pipeline()
   pipeline.set_steps([(step, "Step", "v1.0")])
   result = pipeline.run({"x": 5})

How do I connect to an API?
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   api_config = {
       "base_url": "http://localhost:8418",
       "token": "mysecrettoken"
   }

   pipeline = Pipeline(api_config=api_config)

How do I handle errors?
~~~~~~~~~~~~~~~~~~~~~~

Use try/except with TaskError:

.. code-block:: python

   from wpipe.exception import TaskError

   try:
       result = pipeline.run({"x": 5})
   except TaskError as e:
       print(f"Pipeline failed: {e}")

Troubleshooting
---------------

My pipeline is not connecting to the API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Check if the API server is running
2. Verify the base_url is correct
3. Ensure the token is valid

The pipeline is stuck on a step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Check if the step function is returning
2. Look for infinite loops in your code
3. Check the verbose output for errors

How do I report an issue?
~~~~~~~~~~~~~~~~~~~~~~~~~

Report issues at: https://github.com/wisrovi/wpipe/issues
