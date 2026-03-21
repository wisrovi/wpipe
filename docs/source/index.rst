wpipe Documentation
==================

.. image:: https://img.shields.io/pypi/v/wpipe.svg
   :target: https://pypi.org/project/wpipe/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/wpipe.svg
   :target: https://pypi.org/project/wpipe/
   :alt: Python Versions

.. image:: https://img.shields.io/github/license/wisrovi/wpipe.svg
   :target: https://github.com/wisrovi/wpipe/blob/main/LICENSE
   :alt: License

**wpipe** is a Python library for creating and executing pipelines with task orchestration,
API integration, and execution tracking.

Features
--------

- Easy pipeline creation with step functions
- API integration for tracking pipeline execution
- Worker registration and health checks
- SQLite integration for persistent storage
- YAML configuration support
- Nested pipeline execution
- Rich progress visualization
- Comprehensive error handling
- Type hints and comprehensive docstrings
- High code quality (Pylint 9.47/10)

Quick Start
-----------

Installation
~~~~~~~~~~~~

Install wpipe using pip:

.. code-block:: bash

   pip install wpipe

Basic Usage
~~~~~~~~~~~

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
   print(result)  # {'result': 10, 'final': 20}

Code Quality
-----------

- **Pylint Score**: 9.47/10
- **Tests**: 84 passing
- **Python Support**: 3.9, 3.10, 3.11, 3.12, 3.13

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   installation
   usage
   api_reference
   tutorials
   architecture
   glossary
   faq
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
