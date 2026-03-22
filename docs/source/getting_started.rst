Getting Started with wpipe
==========================

Welcome to wpipe! This guide will help you get up and running with your first pipeline in minutes.

What You'll Learn
-----------------

* Installing wpipe
* Creating your first pipeline
* Understanding the data flow
* Running pipelines with different inputs
* Working with step functions and classes

Let's get started!

Installation
------------

Prerequisites
~~~~~~~~~~~~~

* Python 3.9 or higher
* pip package manager

Install from PyPI
~~~~~~~~~~~~~~~~~

The easiest way to install wpipe is via pip:

.. code-block:: bash

   pip install wpipe

Install from Source
~~~~~~~~~~~~~~~~~~~

For the latest development version:

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe.git
   cd wpipe
   pip install -e .

Verify Installation
~~~~~~~~~~~~~~~~~~

Verify wpipe is installed correctly:

.. code-block:: python

   import wpipe
   print(wpipe.__version__)  # Should print 1.0.0

Your First Pipeline
------------------

Basic Concepts
~~~~~~~~~~~~~

A **Pipeline** is a sequence of **Steps** that process data. Each step receives output from the previous step.

Step Structure
~~~~~~~~~~~~~~

Each step is defined as a tuple containing:

1. **Function/Callable**: The logic to execute
2. **Name**: A descriptive name (string)
3. **Version**: Version string (e.g., "v1.0")

Example:

.. code-block:: python

   (my_function, "Step Name", "v1.0")

Simple Pipeline
~~~~~~~~~~~~~~

Here's your first pipeline:

.. code-block:: python

   from wpipe import Pipeline

   def step1(data):
       """Multiply input by 2"""
       return {"result": data["x"] * 2}

   def step2(data):
       """Add 10 to the result"""
       return {"final": data["result"] + 10}

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (step1, "Double Value", "v1.0"),
       (step2, "Add Ten", "v1.0"),
   ])

   result = pipeline.run({"x": 5})
   print(result)
   # Output: {'x': 5, 'result': 10, 'final': 20}

Expected Output
~~~~~~~~~~~~~~

When you run this, you should see:

.. code-block:: text

   Pipeline started: 2 steps
   Step 1: Double Value (v1.0) - 0.001s
   Step 2: Add Ten (v1.0) - 0.001s
   Pipeline completed: 2 steps in 0.002s

Understanding Data Flow
----------------------

Data Accumulation
~~~~~~~~~~~~~~~~~

Each step's output is **merged** with existing data:

.. code-block:: text

   Input: {'x': 5}
        ↓
   Step 1: {'result': 10}
        ↓
   Merged: {'x': 5, 'result': 10}
        ↓
   Step 2: {'final': 20}
        ↓
   Output: {'x': 5, 'result': 10, 'final': 20}

Key Insight
~~~~~~~~~~~

**Previous step outputs are available to all subsequent steps:**

.. code-block:: python

   def step1(data):
       return {"step1_data": "first"}

   def step2(data):
       # Can access step1's output
       return {"step2_data": data["step1_data"] + "_second"}

   def step3(data):
       # Can access BOTH step1 and step2 outputs
       return {"step3_data": data["step1_data"] + "_" + data["step2_data"]}

Step Functions
-------------

Functions as Steps
~~~~~~~~~~~~~~~~~

The simplest way to define a step:

.. code-block:: python

   def validate(data):
       """Validate input data"""
       if "x" not in data:
           raise ValueError("Missing 'x' in data")
       return {"validated": True}

   pipeline.set_steps([(validate, "Validate", "v1.0")])

Lambda Functions
~~~~~~~~~~~~~~

For simple transformations:

.. code-block:: python

   pipeline.set_steps([
       ((lambda d: {**d, "doubled": d["x"] * 2}), "Double", "v1.0"),
   ])

Classes as Steps
~~~~~~~~~~~~~~~

For complex stateful logic:

.. code-block:: python

   class DataProcessor:
       def __init__(self, multiplier):
           self.multiplier = multiplier

       def __call__(self, data):
           return {"processed": data["x"] * self.multiplier}

   processor = DataProcessor(3)
   pipeline.set_steps([(processor, "Process", "v1.0")])

Running the Pipeline
-------------------

Basic Execution
~~~~~~~~~~~~~~

.. code-block:: python

   result = pipeline.run({"x": 10})
   print(result)

With Error Handling
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe.exception import TaskError, ProcessError

   try:
       result = pipeline.run({"x": 10})
   except (TaskError, ProcessError) as e:
       print(f"Pipeline failed: {e}")

Async Execution
~~~~~~~~~~~~~~

For async pipelines:

.. code-block:: python

   import asyncio

   async def main():
       result = await pipeline.run({"x": 10})
       print(result)

   asyncio.run(main())

Advanced Examples
-----------------

To learn more, explore:

* **100+ Examples**: Visit the :doc:`examples/index` section
* **User Guide**: Deep dive into features in :doc:`user_guide/index`
* **API Reference**: Complete documentation in :doc:`api_reference`

Next Steps
----------

Now that you've created your first pipeline, explore these topics:

* **User Guide**: Learn about conditions, retries, and more in :doc:`user_guide/index`
* **Examples**: Browse 100+ examples in :doc:`examples/index`
* **API Reference**: View complete API documentation in :doc:`api_reference`
