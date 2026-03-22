.. wpipe documentation master file

Welcome to wpipe |version|
======================================

**wpipe** is a powerful Python library for creating and executing sequential data processing pipelines with task orchestration, API integration, and execution tracking.

.. image:: https://img.shields.io/pypi/v/wpipe.svg
   :target: https://pypi.org/project/wpipe/

.. image:: https://img.shields.io/pypi/pyversions/wpipe.svg
   :target: https://pypi.org/project/wpipe/

.. image:: https://img.shields.io/github/license/wisrovi/wpipe.svg
   :target: https://github.com/wisrovi/wpipe/blob/main/LICENSE

.. image:: https://img.shields.io/badge/tests-206%20passing-blue

|

1. About wpipe
--------------

wpipe facilitates the execution of a pipeline of tasks and the interaction with external APIs. The library provides the ability to register workers, processes, and tasks, allowing you to report the status of each step in real-time.

**Why wpipe?**

- **Simple API**: Get started in minutes with an intuitive interface
- **Flexible**: Use functions or classes as pipeline steps
- **Extensible**: Add custom decorators and error handling
- **Production-Ready**: Comprehensive error handling and logging
- **Well-Documented**: Extensive documentation and examples
- **LTS Release**: Stable API with guaranteed backward compatibility

2. Key Features
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feature
     - Description
   * - **Pipeline Orchestration**
     - Create pipelines with step functions and classes
   * - **Conditional Branches**
     - Execute different paths based on data conditions
   * - **Retry Logic**
     - Automatic retries for failed steps with configurable parameters
   * - **API Integration**
     - Connect to external APIs for tracking and monitoring
   * - **Worker Management**
     - Register workers and perform health checks
   * - **SQLite Storage**
     - Persist pipeline execution results to database
   * - **YAML Configuration**
     - Load and manage configurations from YAML files
   * - **Error Handling**
     - Robust error handling with custom exceptions and error codes
   * - **Progress Tracking**
     - Visual progress with rich terminal output
   * - **Nested Pipelines**
     - Compose complex workflows from smaller pipelines

3. Quick Start
--------------

Get started with wpipe in minutes:

.. code-block:: python

    from wpipe import Pipeline

    def fetch_data(data):
        """Fetch data from a source."""
        return {"users": [{"name": "Alice"}, {"name": "Bob"}]}

    def process_data(data):
        """Process the fetched data."""
        return {"count": len(data["users"])}

    def save_data(data):
        """Save results."""
        return {"status": "saved"}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (fetch_data, "Fetch Data", "v1.0"),
        (process_data, "Process Data", "v1.0"),
        (save_data, "Save Data", "v1.0"),
    ])

    result = pipeline.run({})
    print(result)
    # {'users': [...], 'count': 2, 'status': 'saved'}

4. Documentation Structure
--------------------------

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

5. Installation
--------------

Install wpipe with pip:

.. code-block:: bash

    pip install wpipe

Or install from source:

.. code-block:: bash

    git clone https://github.com/wisrovi/wpipe
    cd wpipe
    pip install -e .

**Requirements:**

- Python 3.9 or higher
- requests (for API integration)
- pyyaml (for YAML configuration)

6. Use Cases
-----------

wpipe is ideal for:

6.1 Data Processing Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ETL (Extract, Transform, Load) workflows:

.. code-block:: python

    def extract(data):
        return {"raw": fetch_from_api()}

    def transform(data):
        return {"cleaned": clean_data(data["raw"])}

    def load(data):
        save_to_database(data["cleaned"])
        return {"loaded": True}

6.2 Task Automation
~~~~~~~~~~~~~~~~~~

Automate complex multi-step workflows:

.. code-block:: python

    def validate(data):
        return {"valid": check_input(data)}

    def process(data):
        return {"processed": run_processing(data)}

    def notify(data):
        return {"notified": send_notification(data)}

6.3 API Integration
~~~~~~~~~~~~~~~~~~

Track and monitor external API calls:

.. code-block:: python

    api_config = {
        "base_url": "http://api.example.com",
        "token": "your-token"
    }

    pipeline = Pipeline(api_config=api_config)
    pipeline.worker_register(name="processor", version="1.0.0")

7. Architecture Overview
-----------------------

::

    ┌─────────────────────────────────────────────────────────────────────┐
    │                         Pipeline Layer                              │
    │  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
    │  │ Step 1  │ -> │ Step 2  │ -> │ Step 3  │ -> │ Step N  │          │
    │  └─────────┘    └─────────┘    └─────────┘    └─────────┘          │
    └─────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
            ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
            │ API Client   │  │   SQLite     │  │   Logger     │
            │ (Optional)   │  │  (Optional)  │  │              │
            └──────────────┘  └──────────────┘  └──────────────┘

8. Error Handling
----------------

wpipe provides robust error handling with custom exceptions:

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    try:
        result = pipeline.run(data)
    except TaskError as e:
        print(f"Step: {e.step_name}")
        print(f"Code: {e.code}")
        print(f"Error: {e.original_error}")

**Error Codes:**

- ``UNKNOWN_ERROR`` (500) - Generic error
- ``VALIDATION_ERROR`` (400) - Input validation failed
- ``API_ERROR`` (501) - API communication error
- ``RETRYABLE_ERROR`` (503) - Error that may succeed on retry
- ``TIMEOUT_ERROR`` (504) - Operation timed out

9. Testing
---------

wpipe includes a comprehensive test suite:

.. code-block:: bash

    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=wpipe --cov-report=html

    # Run specific test file
    pytest test/test_pipeline.py

**Test Results:** 106 tests passing (100% core + examples)

10. Community and Support
-------------------------

10.1 Resources
~~~~~~~~~~~~~~

- **Documentation**: https://wpipe.readthedocs.io/
- **GitHub**: https://github.com/wisrovi/wpipe
- **PyPI**: https://pypi.org/project/wpipe/
- **Issues**: https://github.com/wisrovi/wpipe/issues

10.2 Contributing
~~~~~~~~~~~~~~~~

We welcome contributions! See :doc:`contributing` for guidelines.

.. code-block:: bash

    git clone https://github.com/wisrovi/wpipe
    cd wpipe
    pip install -e ".[dev]"
    pytest

11. License
----------

wpipe is released under the **MIT License**.

See the `LICENSE <https://github.com/wisrovi/wpipe/blob/main/LICENSE>`_ file for details.

12. Author
---------

**William Steve Rodriguez Villamizar**

- GitHub: https://github.com/wisrovi
- Email: will contact via GitHub

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
