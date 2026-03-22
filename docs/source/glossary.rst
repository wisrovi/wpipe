Glossary
========

This section contains definitions of terms and concepts used in wpipe.

1. Core Concepts
----------------

1.1 Pipeline
~~~~~~~~~~~~

A sequence of steps that process input data and produce results. The Pipeline class is the main entry point for creating and executing data processing workflows.

**Example:**

.. code-block:: python

    pipeline = Pipeline()
    pipeline.set_steps([(step1, "Step 1", "v1.0"), (step2, "Step 2", "v1.0")])
    result = pipeline.run({"input": "data"})

1.2 Step
~~~~~~~~

A single unit of work within a pipeline. Steps can be functions or callable classes that receive data, process it, and return modified data.

**Requirements:**

- Must accept a ``data`` dictionary parameter
- Must return a dictionary with results
- Should be idempotent when possible

**Function Step:**

.. code-block:: python

    def my_step(data):
        return {"processed": data["input"] * 2}

**Class Step:**

.. code-block:: python

    class MyStep:
        def __call__(self, data):
            return {"processed": data["input"] * 2}

1.3 Data Flow
~~~~~~~~~~~~

The mechanism by which data passes through a pipeline. Each step receives accumulated results from all previous steps and adds its own results.

**Flow Diagram:**

.. code-block:: text

    Input Data
        │
        ▼
    ┌─────────┐
    │ Step 1  │───returns {key1: value1}
    └─────────┘
        │
        ▼ Data: {input, key1}
    ┌─────────┐
    │ Step 2  │───returns {key2: value2}
    └─────────┘
        │
        ▼ Data: {input, key1, key2}
    ┌─────────┐
    │ Step 3  │───returns {key3: value3}
    └─────────┘
        │
        ▼
    Output Data: {input, key1, key2, key3}

1.4 Step Name
~~~~~~~~~~~~~

A human-readable identifier for a step, used in logging and progress display.

**Convention:**

- Use descriptive names: "Fetch User Data" not "Step 1"
- Include the action: "Validate Email" not "Validation"
- Keep concise but informative

1.5 Step Version
~~~~~~~~~~~~~~~

A version identifier for tracking changes to pipeline steps. Format follows semantic versioning (e.g., "v1.0", "v1.1", "v2.0").

**Usage:**

.. code-block:: python

    pipeline.set_steps([
        (step1, "Fetch Data", "v1.0"),
        (step2, "Process Data", "v1.0"),  # Changed to v1.1 after updates
    ])

2. API Integration
------------------

2.1 API Client
~~~~~~~~~~~~~~

A component that handles communication with external APIs for worker registration, health checks, and task tracking.

**Configuration:**

.. code-block:: python

    api_config = {
        "base_url": "https://api.example.com",
        "token": "auth-token",
        "timeout": 30
    }

2.2 Worker
~~~~~~~~~

A registered instance that executes pipeline processes. Workers are registered with an external API for tracking and monitoring.

**Registration:**

.. code-block:: python

    worker_id = pipeline.worker_register(
        name="processor_1",
        version="1.0.0"
    )

2.3 Worker ID
~~~~~~~~~~~~

A unique identifier assigned to a registered worker. Used to associate pipeline executions with a specific worker.

**Format:** Typically a string (e.g., "worker_123", "abc-456")

2.4 Health Check
~~~~~~~~~~~~~~~~

A periodic verification that a worker is still responsive. Health checks are performed automatically when configured.

**Configuration:**

.. code-block:: python

    pipeline = Pipeline(
        api_config=api_config,
        health_check_interval=60  # Seconds between checks
    )

2.5 Task Status
~~~~~~~~~~~~~~~

The current state of a pipeline task. Common statuses include:

- ``PENDING``: Task created but not started
- ``RUNNING``: Task is executing
- ``COMPLETED``: Task finished successfully
- ``FAILED``: Task encountered an error

3. Data Persistence
-------------------

3.1 SQLite
~~~~~~~~~

A lightweight, file-based database used by wpipe for persistent storage of pipeline execution results.

**Database File:** ``pipeline_results.db``

3.2 Execution Record
~~~~~~~~~~~~~~~~~~~~

A record of a single pipeline execution stored in SQLite, containing:

- Execution ID
- Input data (JSON)
- Output data (JSON)
- Start timestamp
- End timestamp
- Status

3.3 Wsqlite
~~~~~~~~~~

The wpipe class for SQLite operations. Provides a context manager for safe database operations.

**Usage:**

.. code-block:: python

    from wpipe.sqlite import Wsqlite

    with Wsqlite(db_name="results.db") as db:
        db.input = {"key": "value"}
        result = pipeline.run({"key": "value"})
        db.output = result

4. Error Handling
-----------------

4.1 TaskError
~~~~~~~~~~~~

The main exception class raised when a pipeline step fails. Contains information about the failed step and the original error.

**Attributes:**

- ``step_name``: Name of the step that failed
- ``code``: Error code for categorization
- ``original_error``: The underlying exception

**Usage:**

.. code-block:: python

    from wpipe.exception import TaskError

    try:
        result = pipeline.run(data)
    except TaskError as e:
        print(f"Failed at {e.step_name}: {e.original_error}")

4.2 Error Codes
~~~~~~~~~~~~~~

Standardized codes for categorizing errors:

- ``UNKNOWN_ERROR``: Generic error
- ``VALIDATION_ERROR``: Input validation failed
- ``API_ERROR``: API communication error
- ``RETRYABLE_ERROR``: Error that may succeed on retry
- ``TIMEOUT_ERROR``: Operation timed out

4.3 Validation Error
~~~~~~~~~~~~~~~~~~~~

An error occurring when input data fails validation. These are typically non-recoverable (retrying won't help).

4.4 Retryable Error
~~~~~~~~~~~~~~~~~~~

An error that may succeed if the operation is retried. Examples include temporary network failures and rate limiting.

5. Configuration
----------------

5.1 YAML Configuration
~~~~~~~~~~~~~~~~~~~~~~~

Configuration stored in YAML format files for loading pipeline settings.

**Example:**

.. code-block:: yaml

    pipeline:
      verbose: true
      log_level: DEBUG

    api:
      base_url: "https://api.example.com"
      token: ${API_TOKEN}

5.2 Environment Variable
~~~~~~~~~~~~~~~~~~~~~~~~

A variable set in the operating system environment. Referenced in YAML using ``${VAR}`` syntax.

**Example:**

.. code-block:: yaml

    api:
      token: ${API_TOKEN}

5.3 Default Value
~~~~~~~~~~~~~~~~~

A fallback value for environment variables when the variable is not set. Format: ``${VAR:-default}``

**Example:**

.. code-block:: yaml

    database:
      path: ${DB_PATH:-default.db}

6. Progress and Logging
-----------------------

6.1 Verbose Mode
~~~~~~~~~~~~~~~~

A mode that displays detailed progress information during pipeline execution.

**Enable:**

.. code-block:: python

    pipeline = Pipeline(verbose=True)
    # or
    result = pipeline.run(data, verbose=True)

6.2 Progress Manager
~~~~~~~~~~~~~~~~~~~~

A component that tracks and displays pipeline execution progress.

6.3 Logger
~~~~~~~~~~

A component that records pipeline events and errors.

7. Advanced Concepts
--------------------

7.1 Nested Pipeline
~~~~~~~~~~~~~~~~~~~

A pipeline that includes another pipeline as one of its steps. Enables composition of complex workflows.

**Example:**

.. code-block:: python

    inner = Pipeline()
    inner.set_steps([...])

    outer = Pipeline()
    outer.set_steps([
        (inner.run, "Run Inner", "v1.0"),
    ])

7.2 Condition
~~~~~~~~~~~~~

A rule that determines which path a pipeline takes based on data values. Enables conditional branching.

**Example:**

.. code-block:: python

    pipeline.add_condition(
        condition=Condition(data_key="mode", operator="==", value="prod"),
        then_steps=[...],
        else_steps=[...],
    )

7.3 Decorator
~~~~~~~~~~~~~

A function that wraps another function to extend its behavior. Used for cross-cutting concerns like retry logic.

**Example:**

.. code-block:: python

    @retry(max_attempts=3)
    def unreliable_step(data):
        ...

7.4 Callback
~~~~~~~~~~~

A function passed to the pipeline that is called at specific events (e.g., step completion, pipeline completion).

**Example:**

.. code-block:: python

    def on_complete(result):
        notify(result)

    pipeline.on_complete(on_complete)

7.5 Idempotent Step
~~~~~~~~~~~~~~~~~~~

A step that can be executed multiple times with the same input and produce the same result. Recommended for reliable pipelines.

8. Testing Terms
----------------

8.1 Unit Test
~~~~~~~~~~~~~

A test that verifies a single function or class in isolation.

8.2 Integration Test
~~~~~~~~~~~~~~~~~~~~

A test that verifies multiple components working together.

8.3 Mock
~~~~~~~~

A fake object that simulates the behavior of real components for testing.

9. Acronyms
-----------

**API**
    Application Programming Interface

**JSON**
    JavaScript Object Notation

**LTS**
    Long Term Support

**RAM**
    Random Access Memory

**REST**
    Representational State Transfer

**SQLite**
    Structured Query Language Lite

**YAML**
    YAML Ain't Markup Language

10. Related Libraries
----------------------

**wpipe** is part of the wFabric family of libraries:

- **wFabricSecurity**: Security utilities
- **wFabricIO**: Input/Output utilities
- **wFabricML**: Machine learning utilities

For more information, visit https://github.com/wisrovi/
