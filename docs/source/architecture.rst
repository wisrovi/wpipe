Architecture
============

This section describes the architecture of wpipe, designed for building sequential data processing pipelines with task orchestration, API integration, and execution tracking.

1. System Overview
------------------

wpipe follows a layered architecture that separates concerns between pipeline orchestration, external communication, and data persistence.

1.1 High-Level Components
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    +------------------+     +------------------+     +------------------+
    |                  |     |                  |     |                  |
    |  Pipeline Layer  |<--->|   API Layer      |<--->|  External API    |
    |                  |     |                  |     |                  |
    +------------------+     +------------------+     +------------------+
            |                        |
            |                        v
            v                +------------------+
    +------------------+     |                  |
    |                  |     |   SQLite Layer   |
    |  Progress Layer  |     |                  |
    |                  |     +------------------+
    +------------------+

1.2 Component Responsibilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Pipeline Layer**

- Orchestrates step execution in sequence
- Manages data flow between steps
- Handles error propagation
- Supports nested pipelines

**API Layer**

- Worker registration with external services
- Health check monitoring
- Task status reporting
- Process tracking

**SQLite Layer**

- Persistent storage of execution results
- Input/output tracking
- Execution metadata storage

**Progress Layer**

- Visual progress tracking in terminal
- Step status indicators
- Rich console output

2. Core Components
------------------

2.1 Pipeline
~~~~~~~~~~~~

The Pipeline class is the main entry point for creating and executing pipelines.

::

    Pipeline
    ├── Steps (functions or classes)
    ├── API Client (optional)
    ├── Progress Manager
    ├── Logger
    └── Configuration

**Key Responsibilities:**

- Initialize and configure pipeline
- Register steps with metadata
- Execute steps in sequence
- Manage data flow between steps
- Handle errors and retries
- Report progress

**Class Definition:**

.. code-block:: python

    class Pipeline:
        def __init__(
            self,
            verbose: bool = False,
            api_config: Optional[dict] = None,
            log_level: str = "INFO"
        ):
            ...

2.2 Step Functions
~~~~~~~~~~~~~~~~~~

Steps are the atomic units of work in a pipeline.

**Function Signature:**

.. code-block:: python

    def step_function(data: dict) -> dict:
        # Process data
        return {"key": value}

**Class Steps:**

.. code-block:: python

    class MyStep:
        def __init__(self, param):
            self.param = param

        def __call__(self, data: dict) -> dict:
            return {"result": data["value"] * self.param}

2.3 API Client
~~~~~~~~~~~~~~

The APIClient handles communication with external APIs.

**Responsibilities:**

- Register workers with the API
- Perform health checks
- Report task status
- Track process execution

**Configuration:**

.. code-block:: python

    api_config = {
        "base_url": "https://api.example.com",
        "token": "your-auth-token",
        "timeout": 30
    }

2.4 SQLite Integration
~~~~~~~~~~~~~~~~~~~~~~

Wsqlite provides persistent storage for pipeline execution.

**Usage Pattern:**

.. code-block:: python

    from wpipe.sqlite import Wsqlite

    with Wsqlite(db_name="results.db") as db:
        db.input = {"key": "value"}
        result = pipeline.run({"key": "value"})
        db.output = result

3. Module Structure
-------------------

::

    wpipe/
    ├── __init__.py           # Package initialization
    ├── pipe/                 # Pipeline implementation
    │   ├── __init__.py
    │   ├── pipe.py          # Main Pipeline class
    │   ├── progress.py       # Progress tracking
    │   └── step.py          # Step utilities
    ├── api_client/          # API communication
    │   ├── __init__.py
    │   ├── client.py        # APIClient class
    │   └── endpoints.py     # API endpoints
    ├── sqlite/              # Database operations
    │   ├── __init__.py
    │   └── sqlite.py        # Wsqlite class
    ├── log/                 # Logging utilities
    │   ├── __init__.py
    │   └── logger.py        # Logger setup
    ├── ram/                 # Memory utilities
    │   ├── __init__.py
    │   └── ram.py           # RAM operations
    ├── util/                # YAML utilities
    │   ├── __init__.py
    │   └── yaml_util.py     # YAML loading
    └── exception/           # Custom exceptions
        ├── __init__.py
        ├── exception.py     # Exception classes
        └── codes.py          # Error codes

4. Design Patterns
------------------

4.1 Pipeline Pattern
~~~~~~~~~~~~~~~~~~~~

Each step receives accumulated results from previous steps:

::

    Input -> Step1 -> {data + result1} -> Step2 -> {data + result1 + result2} -> Output

4.2 Builder Pattern
~~~~~~~~~~~~~~~~~~~

Pipeline configuration uses a fluent interface:

.. code-block:: python

    pipeline = (
        Pipeline()
        .set_verbose(True)
        .set_api_config(api_config)
        .set_steps([...])
        .run(data)
    )

4.3 Context Manager Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~

SQLite operations use context managers:

.. code-block:: python

    with Wsqlite(db_name="results.db") as db:
        db.input = data
        result = pipeline.run(data)
        db.output = result

4.4 Strategy Pattern
~~~~~~~~~~~~~~~~~~~~

Different step types (functions, classes) are handled uniformly:

.. code-block:: python

    def execute_step(step, data):
        if callable(step):
            return step(data)
        return data

5. Data Flow
------------

5.1 Pipeline Execution Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    +-------------------------------------------------------------+
    |  Pipeline.run(initial_data)                                 |
    +-------------------------------------------------------------+
                              |
                              v
    +-------------------------------------------------------------+
    |  For each step in pipeline:                                  |
    |    1. Call step(data)                                       |
    |    2. Merge result into data                                |
    |    3. Update progress                                       |
    |    4. Check for errors                                      |
    +-------------------------------------------------------------+
                              |
                              v
    +-------------------------------------------------------------+
    |  Return accumulated data                                    |
    +-------------------------------------------------------------+

5.2 Data Accumulation
~~~~~~~~~~~~~~~~~~~~~

Each step receives all previous results:

.. code-block:: python

    # Step 1: returns {"step1_result": 10}
    # Step 2: receives {"step1_result": 10}, returns {"step2_result": 20}
    # Step 3: receives {"step1_result": 10, "step2_result": 20}

5.3 Error Propagation
~~~~~~~~~~~~~~~~~~~~~

Errors are caught and wrapped in TaskError:

.. code-block:: python

    try:
        result = pipeline.run(data)
    except TaskError as e:
        print(f"Pipeline failed at step {e.step_name}: {e.original_error}")

6. Concurrency Model
--------------------

6.1 Sequential Execution
~~~~~~~~~~~~~~~~~~~~~~~~

By default, pipeline steps execute sequentially:

::

    Step 1 -> Step 2 -> Step 3 -> Step 4
       │         │         │         │
       v         v         v         v
    Complete   Wait     Wait     Wait

6.2 Retry Mechanism
~~~~~~~~~~~~~~~~~~~~~

Failed steps can be automatically retried:

.. code-block:: python

    @retry(max_attempts=3, delay=1.0, backoff=2.0)
    def unreliable_step(data):
        # May fail occasionally
        ...

7. Extension Points
-------------------

7.1 Custom Step Decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create custom step decorators:

.. code-block:: python

    def validate_output(func):
        def wrapper(data):
            result = func(data)
            if not validate(result):
                raise ValueError("Invalid output")
            return result
        return wrapper

7.2 Custom Exceptions
~~~~~~~~~~~~~~~~~~~~~

Extend the exception hierarchy:

.. code-block:: python

    class PipelineWarning(UserWarning):
        pass

8. Configuration
----------------

8.1 Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``WPIPE_LOG_LEVEL``: Set logging level
- ``WPIPE_DB_PATH``: Default SQLite database path
- ``WPIPE_API_TIMEOUT``: Default API timeout

8.2 YAML Configuration
~~~~~~~~~~~~~~~~~~~~~~

Load configuration from YAML:

.. code-block:: yaml

    # config.yaml
    pipeline:
      verbose: true
      log_level: DEBUG

    api:
      base_url: https://api.example.com
      token: ${API_TOKEN}

9. Performance Considerations
------------------------------

9.1 Memory Management
~~~~~~~~~~~~~~~~~~~~

- Data accumulates between steps
- Use ``ram`` module to monitor memory
- Clear intermediate results when not needed

9.2 Large Data Sets
~~~~~~~~~~~~~~~~

For large data processing:

.. code-block:: python

    # Process in chunks
    def chunk_processor(data):
        for chunk in chunked(data, size=1000):
            yield process_chunk(chunk)

9.3 Timeout Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Set timeouts to prevent hanging:

.. code-block:: python

    pipeline = Pipeline(timeout=300)  # 5 minute timeout
