API Reference
=============

This section contains the complete API documentation for wpipe v1.0.0.

1. Main Classes
---------------

1.1 Pipeline
~~~~~~~~~~~~

The main class for creating and executing sequential data processing pipelines.

.. autoclass:: wpipe.pipe.Pipeline
   :members:
   :undoc-members:
   :show-inheritance:

**Constructor Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``worker_name``
     - ``str``
     - Name identifier for the worker process
   * - ``api_config``
     - ``dict``, optional
     - API configuration with keys: ``base_url``, ``token``, ``timeout``
   * - ``max_retries``
     - ``int``
     - Maximum retry attempts for failed steps (default: 3)
   * - ``verbose``
     - ``bool``
     - Enable verbose logging to console (default: False)
   * - ``log_level``
     - ``str``
     - Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)

**Returns:** ``Pipeline`` instance

**Raises:** ``TypeError`` if parameters are invalid

**Example:**

.. code-block:: python

    from wpipe import Pipeline

    # Basic pipeline
    pipeline = Pipeline()

    # Verbose pipeline
    pipeline = Pipeline(verbose=True)

    # Pipeline with API integration
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "my-token",
        "timeout": 30
    }
    pipeline = Pipeline(
        worker_name="processor_1",
        api_config=api_config,
        max_retries=5,
        verbose=True
    )

**Core Methods:**

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - ``set_steps(steps)``
     - Set the list of pipeline steps with metadata
   * - ``run(input_data)``
     - Execute the pipeline with input data
   * - ``worker_register(name, version)``
     - Register worker with API server
   * - ``set_worker_id(worker_id)``
     - Set the worker ID for tracking
   * - ``process_register(process_name, process_description)``
     - Register a process with the API
   * - ``task_register(task_name, process_id)``
     - Register a task with the API
   * - ``process_update(process_id, status, result)``
     - Update process status with API

**Pipeline.set_steps()**

Set the list of pipeline steps with name and version metadata.

.. code-block:: python

    def step1(data):
        return {"result": data["x"] * 2}

    def step2(data):
        return {"final": data["result"] + 10}

    pipeline.set_steps([
        (step1, "Double Value", "v1.0"),
        (step2, "Add Ten", "v1.0"),
    ])

**Pipeline.run()**

Execute the pipeline with input data.

.. code-block:: python

    result = pipeline.run({"x": 5})
    # Returns: {'x': 5, 'result': 10, 'final': 20}

**Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``input_data``
     - ``dict``
     - Initial data dictionary passed to first step
   * - ``verbose``
     - ``bool``, optional
     - Override verbose setting for this run

**Returns:** ``dict`` - Accumulated results from all steps

**Raises:** ``TaskError`` if any step fails

1.2 APIClient
~~~~~~~~~~~~~

Client for API communication with external services.

.. autoclass:: wpipe.api_client.APIClient
   :members:
   :undoc-members:
   :show-inheritance:

**Constructor Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``base_url``
     - ``str``
     - Base URL of the API server
   * - ``token``
     - ``str``
     - Authentication token for API access
   * - ``timeout``
     - ``int``, optional
     - Request timeout in seconds (default: 30)

**Example:**

.. code-block:: python

    from wpipe.api_client import APIClient

    client = APIClient(
        base_url="http://localhost:8418",
        token="my-auth-token",
        timeout=60
    )

    # Register worker
    worker = client.worker_register(
        name="processor",
        version="1.0.0"
    )

    # Health check
    is_healthy = client.health_check(worker["id"])

2. SQLite Classes
----------------

2.1 Wsqlite
~~~~~~~~~~

High-level SQLite wrapper for pipeline results persistence.

.. autoclass:: wpipe.sqlite.Wsqlite
   :members:
   :undoc-members:
   :show-inheritance:

**Constructor Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``db_name``
     - ``str``
     - Database file name (e.g., "results.db")
   * - ``table_name``
     - ``str``, optional
     - Table name for storing results (default: "pipeline_executions")

**Example:**

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite

    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"result": d["x"] * 2}, "Double", "v1.0"),
    ])

    with Wsqlite(db_name="results.db") as db:
        # Store input
        db.input = {"x": 10}

        # Execute pipeline
        result = pipeline.run({"x": 10})

        # Store output
        db.output = result

**Attributes:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``input``
     - Set the input data before running pipeline
   * - ``output``
     - Get the output data after running pipeline

**Properties:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Property
     - Description
   * - ``input``
     - Get/set the input data dictionary
   * - ``output``
     - Get/set the output data dictionary

2.2 Sqlite
~~~~~~~~~~

Lower-level SQLite interface for direct database operations.

.. autoclass:: wpipe.sqlite.Sqlite
   :members:
   :undoc-members:
   :show-inheritance:

**Constructor Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``db_name``
     - ``str``
     - Database file name
   * - ``table_name``
     - ``str``, optional
     - Table name (default: "pipeline_executions")
   * - ``create``
     - ``bool``, optional
     - Create table if not exists (default: True)

**Example:**

.. code-block:: python

    from wpipe.sqlite import Sqlite

    db = Sqlite(db_name="data.db")

    # Insert data
    db.insert({
        "input": '{"x": 10}',
        "output": '{"result": 20}',
        "status": "completed"
    })

    # Query data
    cursor = db.execute("SELECT * FROM pipeline_executions")
    results = cursor.fetchall()

    db.close()

3. Security Services
--------------------

3.1 Condition
~~~~~~~~~~~~~

Conditional branching in pipelines based on data evaluation.

.. autoclass:: wpipe.pipe.Condition
   :members:
   :undoc-members:
   :show-inheritance:

**Constructor Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``data_key``
     - ``str``
     - Key in data dictionary to evaluate
   * - ``operator``
     - ``str``
     - Comparison operator: ``==``, ``!=``, ``>``, ``<``, ``>=``, ``<=``
   * - ``value``
     - ``Any``
     - Value to compare against

**Example:**

.. code-block:: python

    from wpipe import Pipeline, Condition

    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"mode": "production"}, "Detect Mode", "v1.0"),
    ])

    # Add conditional branching
    prod_steps = [(lambda d: {"env": "prod"}, "Production Task", "v1.0")]
    dev_steps = [(lambda d: {"env": "dev"}, "Dev Task", "v1.0")]

    pipeline.add_condition(
        condition=Condition(data_key="mode", operator="==", value="production"),
        then_steps=prod_steps,
        else_steps=dev_steps,
    )

4. Exception Classes
--------------------

.. automodule:: wpipe.exception
   :members:
   :undoc-members:
   :show-inheritance:

4.1 wpipeException
~~~~~~~~~~~~~~~~~~

Base exception class for all wpipe exceptions.

.. code-block:: python

    from wpipe.exception import wpipeException

    try:
        # Your code here
        pass
    except wpipeException as e:
        print(f"wpipe error: {e}")

4.2 TaskError
~~~~~~~~~~~~~

Exception raised when a pipeline step fails.

**Constructor Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``message``
     - ``str``
     - Error message describing the failure
   * - ``step_name``
     - ``str``, optional
     - Name of the step that failed
   * - ``code``
     - ``Codes``, optional
     - Error code for categorization
   * - ``original_error``
     - ``Exception``, optional
     - The original exception that caused the failure

**Attributes:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``step_name``
     - Name of the failed step
   * - ``code``
     - Error code enum value
   * - ``original_error``
     - Original exception object

**Example:**

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    try:
        result = pipeline.run({"x": 5})
    except TaskError as e:
        print(f"Failed at step: {e.step_name}")
        print(f"Error code: {e.code}")
        print(f"Original error: {e.original_error}")

4.3 ProcessError
~~~~~~~~~~~~~~~

Exception for process-related errors.

.. code-block:: python

    from wpipe.exception import ProcessError

    raise ProcessError("Process execution failed")

4.4 ApiError
~~~~~~~~~~~~

Exception for API communication errors.

.. code-block:: python

    from wpipe.exception import ApiError

    raise ApiError("Failed to connect to API server")

4.5 Exception Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~

::

    BaseException
    └── Exception
        └── wpipeException
            ├── TaskError
            │   └── Args: message, step_name, code, original_error
            ├── ProcessError
            │   └── Args: message
            └── ApiError
                └── Args: message, status_code, response

4.6 Error Codes
~~~~~~~~~~~~~~~

Standardized error codes for categorization:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Code
     - Value
     - Description
   * - ``UNKNOWN_ERROR``
     - 500
     - Generic/unknown error
   * - ``VALIDATION_ERROR``
     - 400
     - Input validation failed
   * - ``API_ERROR``
     - 501
     - API communication error
   * - ``RETRYABLE_ERROR``
     - 503
     - Error that may succeed on retry
   * - ``TIMEOUT_ERROR``
     - 504
     - Operation timed out
   * - ``TASK_FAILED``
     - 502
     - Task execution failed
   * - ``UPDATE_PROCESS_OK``
     - 503
     - Process update succeeded
   * - ``UPDATE_PROCESS_ERROR``
     - 504
     - Process update failed

**Example:**

.. code-block:: python

    from wpipe.exception import Codes

    # Using error codes
    raise TaskError(
        "Invalid input",
        code=Codes.VALIDATION_ERROR
    )

5. Utility Functions
--------------------

5.1 leer_yaml
~~~~~~~~~~~~~

Read and parse a YAML configuration file.

.. autofunction:: wpipe.util.leer_yaml

**Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``archivo``
     - ``str``
     - Path to the YAML file
   * - ``verbose``
     - ``bool``, optional
     - Print errors if True (default: False)

**Returns:** ``dict`` - Parsed YAML content, or empty dict on error

**Raises:** ``FileNotFoundError`` if file doesn't exist

**Example:**

.. code-block:: python

    from wpipe.util import leer_yaml

    # Load configuration
    config = leer_yaml("config.yaml")

    # Access configuration values
    base_url = config.get("api", {}).get("base_url")
    token = config.get("api", {}).get("token")

5.2 escribir_yaml
~~~~~~~~~~~~~~~~~

Write data to a YAML file.

.. autofunction:: wpipe.util.escribir_yaml

**Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``archivo``
     - ``str``
     - Path to the output YAML file
   * - ``contenido``
     - ``dict``
     - Dictionary to write as YAML
   * - ``verbose``
     - ``bool``, optional
     - Print success message if True

**Returns:** ``bool`` - True on success, None on error

**Example:**

.. code-block:: python

    from wpipe.util import escribir_yaml

    config = {
        "pipeline": {"verbose": True},
        "api": {"base_url": "http://localhost:8418"}
    }

    escribir_yaml("config.yaml", config, verbose=True)

5.3 load_config
~~~~~~~~~~~~~~~

Load configuration with environment variable substitution.

.. code-block:: python

    from wpipe.util import load_config

    # Supports ${VAR} and ${VAR:-default} syntax
    config = load_config("config.yaml")

    # Environment variables are automatically substituted
    # ${API_TOKEN} -> value from os.environ["API_TOKEN"]

6. Logging
----------

6.1 new_logger
~~~~~~~~~~~~~

Create a configured logger instance.

.. autofunction:: wpipe.log.new_logger

**Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``name``
     - ``str``
     - Logger name (usually module name)
   * - ``level``
     - ``str``, optional
     - Log level: DEBUG, INFO, WARNING, ERROR (default: INFO)
   * - ``log_file``
     - ``str``, optional
     - Optional file path for log output

**Returns:** ``logging.Logger`` - Configured logger instance

**Example:**

.. code-block:: python

    from wpipe.log import new_logger

    logger = new_logger(__name__, level="DEBUG")

    logger.info("Pipeline started")
    logger.debug("Processing data: %s", data)
    logger.warning("Retrying step")
    logger.error("Step failed: %s", error)

7. RAM Utilities
----------------

7.1 memory
~~~~~~~~~

Get current memory usage in MB.

.. autofunction:: wpipe.ram.memory

**Returns:** ``float`` - Current memory usage in megabytes

**Example:**

.. code-block:: python

    from wpipe.ram import memory

    initial_memory = memory()
    print(f"Initial memory: {initial_memory:.2f} MB")

    # Process data
    large_data = [i for i in range(1000000)]

    final_memory = memory()
    print(f"Final memory: {final_memory:.2f} MB")
    print(f"Memory used: {final_memory - initial_memory:.2f} MB")

7.2 get_memory
~~~~~~~~~~~~~

Get detailed memory information.

.. autofunction:: wpipe.ram.ram.get_memory

**Returns:** ``dict`` - Dictionary with memory statistics

**Example:**

.. code-block:: python

    from wpipe.ram import get_memory

    stats = get_memory()
    print(f"RSS: {stats['rss']} bytes")
    print(f"VMS: {stats['vms']} bytes")

8. Module Structure
-------------------

The wpipe package is organized into the following modules:

::

    wpipe/
    ├── __init__.py           # Package exports
    ├── pipe/                 # Pipeline implementation
    │   ├── __init__.py
    │   ├── pipe.py          # Pipeline class
    │   ├── progress.py       # Progress tracking
    │   └── step.py          # Step utilities
    ├── api_client/          # API integration
    │   ├── __init__.py
    │   └── api_client.py    # APIClient class
    ├── sqlite/              # Database operations
    │   ├── __init__.py
    │   └── sqlite.py        # Sqlite and Wsqlite classes
    ├── log/                 # Logging utilities
    │   ├── __init__.py
    │   └── logger.py        # Logger configuration
    ├── ram/                 # Memory utilities
    │   ├── __init__.py
    │   └── ram.py           # Memory functions
    ├── util/                # Utility functions
    │   ├── __init__.py
    │   └── utils.py         # YAML utilities
    └── exception/           # Exception classes
        ├── __init__.py
        ├── exception.py     # Exception definitions
        └── codes.py         # Error codes

9. Indices and tables
---------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
