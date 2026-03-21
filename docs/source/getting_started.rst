Getting Started
===============

This guide will help you get started with wpipe.

Prerequisites
------------

- Python 3.9 or higher
- pip package manager

Installation
------------

Install wpipe using pip:

.. code-block:: bash

   pip install wpipe

Or install from source:

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe
   cd wpipe
   pip install .

Quick Start
-----------

Basic Pipeline
~~~~~~~~~~~~~

Here's a simple example of using wpipe:

.. code-block:: python

   from wpipe.pipe import Pipeline

   def step1(data):
       return {"value": data["x"] * 2}

   def step2(data):
       return {"result": data["value"] + 10}

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (step1, "Double Value", "v1.0"),
       (step2, "Add Ten", "v1.0"),
   ])

   result = pipeline.run({"x": 5})
   print(result)

Pipeline with API
~~~~~~~~~~~~~~~~~

Connect your pipeline to an external API for tracking:

.. code-block:: python

   from wpipe.pipe import Pipeline

   def process(data):
       return {"processed": True, "value": data["x"]}

   api_config = {
       "base_url": "http://localhost:8418",
       "token": "mysecrettoken"
   }

   pipeline = Pipeline(
       worker_name="my_worker",
       api_config=api_config,
       verbose=True
   )

   pipeline.set_steps([
       (process, "Process Data", "v1.0"),
   ])

   worker_id = pipeline.worker_register(
       name="my_pipeline",
       version="v1.0.0"
   )

   pipeline.set_worker_id(worker_id.get("id"))
   result = pipeline.run({"x": 42})

Next Steps
----------

- Learn more about :doc:`usage` patterns
- Explore :doc:`tutorials` for detailed examples
- Check the :doc:`api_reference` for complete API documentation
