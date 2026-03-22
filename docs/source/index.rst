Overview
========

**wpipe** is a powerful Python library for creating and executing sequential data processing pipelines with task orchestration, API integration, and execution tracking.

.. image:: https://img.shields.io/pypi/v/wpipe.svg
   :target: https://pypi.org/project/wpipe/

.. image:: https://img.shields.io/pypi/pyversions/wpipe.svg
   :target: https://pypi.org/project/wpipe/

.. image:: https://img.shields.io/github/license/wisrovi/wpipe.svg
   :target: https://github.com/wisrovi/wpipe/blob/main/LICENSE

.. image:: https://img.shields.io/badge/tests-206%20passing-blue

Purpose
-------

**wpipe** facilitates the execution of a pipeline of tasks and the interaction with an external API. The library provides the ability to register workers, processes, and tasks, allowing you to report the status of each step in real-time.

Key Features
-------------

* **Pipeline Orchestration**: Create pipelines with step functions and classes
* **Conditional Branches**: Execute different paths based on data conditions
* **Retry Logic**: Automatic retries for failed steps with configurable parameters
* **API Integration**: Connect to external APIs for tracking and monitoring
* **Worker Management**: Register workers and perform health checks
* **SQLite Storage**: Persist pipeline execution results
* **YAML Configuration**: Load and manage configurations
* **Error Handling**: Robust error handling with custom exceptions
* **Progress Tracking**: Visual progress with rich terminal output
* **Nested Pipelines**: Compose complex workflows

Quick Example
-------------

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

Contents
--------

.. toctree::
   :maxdepth: 2
   :numbered: 5
   :caption: Contents

   1. Getting Started <getting_started>
   2. Installation <installation>
   3. Usage Examples <usage>
   4. User Guide <user_guide/index>
   5. Tutorials <tutorials>
   6. API Reference <api_reference>
   7. FAQ <faq>
   8. Architecture <architecture>
   9. Glossary <glossary>
   10. Contributing <contributing>
   11. Changelog <changelog>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
-------

MIT License - See LICENSE file

Author
------

William Steve Rodriguez Villamizar
