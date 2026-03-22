wpipe - Python Pipeline Library
==============================

**wpipe** is a powerful Python library for creating and executing sequential data 
processing pipelines with task orchestration, API integration, and execution tracking.

.. image:: https://img.shields.io/pypi/v/wpipe.svg
   :target: https://pypi.org/project/wpipe/

.. image:: https://img.shields.io/pypi/pyversions/wpipe.svg
   :target: https://pypi.org/project/wpipe/

.. image:: https://img.shields.io/github/license/wisrovi/wpipe.svg
   :target: https://github.com/wisrovi/wpipe/blob/main/LICENSE

Why wpipe?
----------

.. list-table::
   :header-rows: 1
   :class: stripe

   * - Feature
     - Description
   * - 🚀 Simple & Intuitive
     - Create pipelines with just a few lines of code
   * - 📊 Progress Tracking
     - Real-time progress visualization with rich terminal output
   * - ☁️ API Integration
     - Connect to external APIs for worker registration and tracking
   * - 💾 Data Persistence
     - Built-in SQLite integration for storing results
   * - 🌿 Conditional Logic
     - Execute different paths based on data conditions
   * - 🔄 Retry Mechanism
     - Automatic retries for failed steps

Quick Start
----------

Installation
~~~~~~~~~~~

.. code-block:: bash

   pip install wpipe

Or install from source:

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe.git
   cd wpipe
   pip install -e .

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
   # {'result': 10, 'final': 20}

Key Features
------------

* **Getting Started** - Learn how to install and use wpipe: :doc:`getting_started`
* **User Guide** - Deep dive into all features: :doc:`user_guide/index`
* **API Reference** - Complete API documentation: :doc:`api_reference`
* **Examples** - 100+ examples organized by functionality: :doc:`examples/index`

Architecture Overview
--------------------

Each step receives output from the previous step for chained processing:

.. code-block:: text

   Input → Step 1 → Step 2 → Step 3 → Output
   
   {'x': 5} → {'result': 10} → {'final': 20}

Code Quality
-----------

* Tests: 206 passing
* Type Hints: 100% coverage
* Docstrings: Google-style
* Examples: 100+
* Python Support: 3.9 - 3.13

Community & Support
------------------

* `Report a Bug <https://github.com/wisrovi/wpipe/issues>`_ - Open an issue on GitHub
* `Join Discussion <https://github.com/wisrovi/wpipe/discussions>`_ - Ask questions and share ideas
* `View on GitHub <https://github.com/wisrovi/wpipe>`_ - Star and contribute

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   getting_started
   installation
   user_guide/index
   examples/index
   api_reference
   tutorials
   faq
   changelog

.. toctree::
   :maxdepth: 2
   :caption: Reference

   Glossary <glossary>
   architecture

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

---

*wpipe is maintained by William Steve Rodriguez Villamizar and distributed under the MIT License.*
