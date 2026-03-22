Pipeline Basics
===============

Understanding how pipelines work is fundamental to using wpipe effectively.

Core Concepts
-------------

Pipeline
~~~~~~~~

The ``Pipeline`` class orchestrates the execution of multiple steps in sequence.

.. code-block:: python

   from wpipe import Pipeline

   pipeline = Pipeline(verbose=True)

Step
~~~~

A step is a tuple containing:

* **callable**: Function or class that processes data
* **name**: Descriptive string identifier
* **version**: Version string

.. code-block:: python

   def my_step(data):
       return {"result": data["x"] * 2}

   step = (my_step, "My Step", "v1.0")

Data Flow
---------

Each step receives all accumulated data from previous steps. Steps return 
dictionaries that are merged with existing data.

**Data Flow Example:**

.. code-block:: text

   Input Data: {'x': 5}
        ↓
   Step 1: {'y': 10}  →  Accumulated: {'x': 5, 'y': 10}
        ↓
   Step 2: {'z': 20}  →  Output: {'x': 5, 'y': 10, 'z': 20}

Creating a Pipeline
-------------------

Basic Example
~~~~~~~~~~~~~

.. code-block:: python

   from wpipe import Pipeline

   def fetch(data):
       return {"users": ["Alice", "Bob"]}

   def process(data):
       return {"count": len(data["users"])}

   def save(data):
       return {"saved": True}

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (fetch, "Fetch Users", "v1.0"),
       (process, "Count Users", "v1.0"),
       (save, "Save Results", "v1.0"),
   ])

   result = pipeline.run({})

Step Types
----------

Function Steps
~~~~~~~~~~~~~~

Most common step type:

.. code-block:: python

   def add_numbers(data):
       a = data.get("a", 0)
       b = data.get("b", 0)
       return {"sum": a + b}

Lambda Steps
~~~~~~~~~~~

For simple transformations:

.. code-block:: python

   pipeline.set_steps([
       ((lambda d: {**d, "doubled": d["x"] * 2}), "Double", "v1.0"),
   ])

Class Steps
~~~~~~~~~~~

For complex stateful operations:

.. code-block:: python

   class DataTransformer:
       def __init__(self, factor):
           self.factor = factor

       def __call__(self, data):
           return {"transformed": data["value"] * self.factor}

   transformer = DataTransformer(3)
   pipeline.set_steps([(transformer, "Transform", "v1.0")])

Running the Pipeline
--------------------

Synchronous
~~~~~~~~~~~

.. code-block:: python

   result = pipeline.run({"input": "value"})
   print(result)

Asynchronous
~~~~~~~~~~~~

.. code-block:: python

   import asyncio

   async def run():
       result = await pipeline.run({"input": "value"})
       return result

   result = asyncio.run(run())

Verbose Mode
~~~~~~~~~~~

Enable detailed logging:

.. code-block:: python

   pipeline = Pipeline(verbose=True)
   # Shows step progress, timing, and status

Pipeline Reuse
--------------

Reuse the same pipeline with different steps:

.. code-block:: python

   pipeline = Pipeline()

   pipeline.set_steps([(step_a, "A", "v1.0"), (step_b, "B", "v1.0")])
   result1 = pipeline.run({"x": 1})

   pipeline.set_steps([(step_c, "C", "v1.0"), (step_d, "D", "v1.0")])
   result2 = pipeline.run({"x": 2})

Best Practices
-------------

1. **Return dictionaries**: Always return a dict from steps
2. **Use .get()**: Handle missing keys gracefully
3. **Descriptive names**: Use clear step names
4. **Versioning**: Track step versions
5. **Small steps**: Keep steps focused and testable

Next Steps
---------

* Learn about :doc:`conditions` for conditional execution
* Explore :doc:`retry` for automatic retries
* Check :doc:`api_integration` for API tracking
