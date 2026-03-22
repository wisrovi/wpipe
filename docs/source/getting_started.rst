Getting Started
===============

This guide will help you get started with wpipe, a powerful Python library for creating and executing sequential data processing pipelines.

1. Overview
----------

**wpipe** is a pipeline orchestration library that enables you to:

- Create sequential data processing workflows
- Orchestrate complex multi-step processes
- Integrate with external APIs for tracking and monitoring
- Persist execution results to SQLite databases
- Handle errors gracefully with custom exceptions
- Monitor progress with rich terminal output

**Key Benefits:**

- **Simple API**: Get started in minutes with an intuitive interface
- **Flexible**: Use functions or classes as pipeline steps
- **Extensible**: Add custom decorators and error handling
- **Production-Ready**: Comprehensive error handling and logging
- **Well-Documented**: Extensive documentation and examples

2. Prerequisites
----------------

Before installing wpipe, ensure you have:

2.1 Python Version
~~~~~~~~~~~~~~~~~~

- **Minimum**: Python 3.9
- **Recommended**: Python 3.10 or higher

Check your Python version:

.. code-block:: bash

    python --version
    # Python 3.10.12

2.2 Operating System
~~~~~~~~~~~~~~~~~~~

wpipe supports all major operating systems:

- Linux (Ubuntu, Debian, CentOS, Fedora)
- macOS
- Windows (10/11)

2.3 Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

For full functionality:

- **requests**: Required for API integration
- **pyyaml**: Required for YAML configuration
- **rich**: Enhanced terminal output (optional)

3. Installation
--------------

3.1 Install via pip
~~~~~~~~~~~~~~~~~~~

The easiest way to install wpipe:

.. code-block:: bash

    pip install wpipe

3.2 Install Specific Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install a specific version for reproducibility:

.. code-block:: bash

    pip install wpipe==1.0.0

3.3 Install from Source
~~~~~~~~~~~~~~~~~~~~~~~

For development or latest features:

.. code-block:: bash

    git clone https://github.com/wisrovi/wpipe
    cd wpipe
    pip install -e .

3.4 Development Install
~~~~~~~~~~~~~~~~~~~~~~

Install with all development dependencies:

.. code-block:: bash

    pip install -e ".[dev]"

4. Verification
---------------

4.1 Verify Installation
~~~~~~~~~~~~~~~~~~~~~~~

Verify wpipe is installed correctly:

.. code-block:: python

    import wpipe
    print(wpipe.__version__)
    # 1.0.0

4.2 Check Available Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~

List all available classes:

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite
    from wpipe.exception import TaskError

    print("Pipeline:", Pipeline)
    print("Wsqlite:", Wsqlite)
    print("TaskError:", TaskError)

5. Quick Start
-------------

This section walks you through creating your first pipeline step by step.

5.1 Step 1: Basic Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create your first pipeline:

.. code-block:: python

    from wpipe import Pipeline

    # Create a new pipeline instance
    pipeline = Pipeline(verbose=True)

    print("Pipeline created successfully!")

5.2 Step 2: Define Step Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define functions that process data:

.. code-block:: python

    def load_data(data):
        """Load or initialize data for processing.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Dictionary with loaded data
        """
        return {"numbers": [1, 2, 3, 4, 5]}

    def calculate_sum(data):
        """Calculate the sum of numbers.
        
        Args:
            data: Must contain 'numbers' key
            
        Returns:
            Dictionary with sum result
        """
        numbers = data["numbers"]
        return {"sum": sum(numbers)}

    def calculate_average(data):
        """Calculate the average of numbers.
        
        Args:
            data: Must contain 'numbers' key
            
        Returns:
            Dictionary with average result
        """
        numbers = data["numbers"]
        return {"average": sum(numbers) / len(numbers)}

5.3 Step 3: Configure Pipeline Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Register your functions as pipeline steps:

.. code-block:: python

    # Register steps with name and version
    pipeline.set_steps([
        (load_data, "Load Data", "v1.0"),
        (calculate_sum, "Calculate Sum", "v1.0"),
        (calculate_average, "Calculate Average", "v1.0"),
    ])

    print(f"Pipeline has {len(pipeline.steps)} steps configured")

5.4 Step 4: Execute the Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the pipeline with input data:

.. code-block:: python

    # Execute the pipeline
    result = pipeline.run({})

    # View results
    print("Pipeline Results:")
    print(f"  Numbers: {result['numbers']}")
    print(f"  Sum: {result['sum']}")
    print(f"  Average: {result['average']}")

**Expected Output:**

::

    Pipeline Results:
      Numbers: [1, 2, 3, 4, 5]
      Sum: 15
      Average: 3.0

5.5 Complete Example
~~~~~~~~~~~~~~~~~~~~

Here is the complete quick start example:

.. code-block:: python

    from wpipe import Pipeline

    def load_data(data):
        return {"numbers": [1, 2, 3, 4, 5]}

    def calculate_sum(data):
        return {"sum": sum(data["numbers"])}

    def calculate_average(data):
        return {"average": sum(data["numbers"]) / len(data["numbers"])}

    def format_result(data):
        return {
            "formatted": f"Sum: {data['sum']}, Average: {data['average']}"
        }

    # Create and configure pipeline
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (load_data, "Load Data", "v1.0"),
        (calculate_sum, "Calculate Sum", "v1.0"),
        (calculate_average, "Calculate Average", "v1.0"),
        (format_result, "Format Result", "v1.0"),
    ])

    # Execute pipeline
    result = pipeline.run({})

    # Access results
    print(result["formatted"])
    # Output: Sum: 15, Average: 3.0

6. Core Concepts
----------------

Understanding these concepts will help you use wpipe effectively.

6.1 Pipeline
~~~~~~~~~~~~

A pipeline is a sequence of steps that process data. Each step receives the accumulated results from all previous steps.

**Characteristics:**

- **Sequential**: Steps execute in order
- **Accumulating**: Data builds up through the pipeline
- **Failing Fast**: Pipeline stops on first error
- **Configurable**: Customize with options and callbacks

6.2 Steps
~~~~~~~~

Steps are the building blocks of a pipeline. They can be:

**Function Steps:**

.. code-block:: python

    def my_step(data):
        # Process data
        return {"key": "value"}

**Class Steps:**

.. code-block:: python

    class MyStep:
        def __init__(self, multiplier):
            self.multiplier = multiplier

        def __call__(self, data):
            return {"result": data["value"] * self.multiplier}

**Lambda Steps (for simple operations):**

.. code-block:: python

    pipeline.set_steps([
        (lambda d: {"doubled": d["x"] * 2}, "Double", "v1.0"),
    ])

6.3 Data Flow
~~~~~~~~~~~~~

Data flows through the pipeline as follows:

::

    Input Data ─────────────────────────────────────────────────────────┐
                                                                    │
                                                                    ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Step 1    │───▶│   Step 2    │───▶│   Step 3    │───▶│   Output    │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
    {step1_result}    {step1_result,    {step1_result,
                                 step2_result}    step2_result,
                                                step3_result}

**Example:**

.. code-block:: python

    def step1(data):
        return {"a": 1}

    def step2(data):
        return {"b": data["a"] + 1}  # Can access data["a"]

    def step3(data):
        return {"c": data["a"] + data["b"]}  # Can access all previous

6.4 Step Metadata
~~~~~~~~~~~~~~~~

Each step has metadata:

- **Name**: Human-readable identifier
- **Version**: Version string for tracking

.. code-block:: python

    pipeline.set_steps([
        (fetch_data, "Fetch User Data from API", "v1.0"),
        (validate, "Validate Email Format", "v1.0"),
        (save, "Save User to Database", "v1.0"),
    ])

7. Common Patterns
-----------------

7.1 ETL Pipeline
~~~~~~~~~~~~~~~

Extract, Transform, Load pattern:

.. code-block:: python

    def extract(data):
        return {"raw_data": fetch_from_api()}

    def transform(data):
        return {"cleaned_data": clean(data["raw_data"])}

    def load(data):
        save_to_database(data["cleaned_data"])
        return {"status": "loaded"}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (extract, "Extract Data", "v1.0"),
        (transform, "Transform Data", "v1.0"),
        (load, "Load Data", "v1.0"),
    ])

    result = pipeline.run({})

7.2 Validation Pipeline
~~~~~~~~~~~~~~~~~~~~~~~

Input validation with error handling:

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    def validate_input(data):
        if "email" not in data:
            raise TaskError(
                "Email is required",
                step_name="Validate Input",
                code=Codes.VALIDATION_ERROR
            )
        if "@" not in data["email"]:
            raise TaskError(
                "Invalid email format",
                step_name="Validate Email",
                code=Codes.VALIDATION_ERROR
            )
        return {"validated": True}

    def process(data):
        return {"processed": True}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (validate_input, "Validate Input", "v1.0"),
        (process, "Process Data", "v1.0"),
    ])

    try:
        result = pipeline.run({"email": "user@example.com"})
    except TaskError as e:
        print(f"Validation failed: {e}")

7.3 Class-Based Processing
~~~~~~~~~~~~~~~~~~~~~~~~~

Use classes for stateful processing:

.. code-block:: python

    class DataTransformer:
        def __init__(self, operations):
            self.operations = operations

        def __call__(self, data):
            result = data.copy()
            for op in self.operations:
                result = op(result)
            return result

    class Multiply:
        def __init__(self, factor):
            self.factor = factor

        def __call__(self, data):
            return {"value": data["value"] * self.factor}

    class Add:
        def __init__(self, amount):
            self.amount = amount

        def __call__(self, data):
            return {"value": data["value"] + self.amount}

    pipeline = Pipeline()
    pipeline.set_steps([
        (DataTransformer([
            Multiply(2),
            Add(10),
            Multiply(3),
        ]), "Transform", "v1.0"),
    ])

    result = pipeline.run({"value": 5})
    # 5 * 2 + 10 = 20
    # 20 * 3 = 60
    print(result["value"])  # 60

8. Error Handling
-----------------

8.1 Understanding TaskError
~~~~~~~~~~~~~~~~~~~~~~~~~~

When a step fails, wpipe raises a TaskError:

.. code-block:: python

    from wpipe.exception import TaskError

    try:
        result = pipeline.run(data)
    except TaskError as e:
        print(f"Step: {e.step_name}")
        print(f"Code: {e.code}")
        print(f"Error: {e.original_error}")

8.2 Error Codes
~~~~~~~~~~~~~~~

Standard error codes:

.. code-block:: python

    from wpipe.exception import Codes

    # UNKNOWN_ERROR: 500 - Generic error
    # VALIDATION_ERROR: 400 - Input validation failed
    # API_ERROR: 501 - API communication error
    # RETRYABLE_ERROR: 503 - May succeed on retry
    # TIMEOUT_ERROR: 504 - Operation timed out

8.3 Graceful Degradation
~~~~~~~~~~~~~~~~~~~~~~~~

Handle errors gracefully:

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    def risky_step(data):
        try:
            return call_unreliable_api()
        except NetworkError:
            return {"status": "fallback_used"}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (risky_step, "Call API", "v1.0"),
    ])

9. API Integration
-----------------

9.1 Configure API Client
~~~~~~~~~~~~~~~~~~~~~~~~

Connect to external APIs:

.. code-block:: python

    api_config = {
        "base_url": "http://localhost:8418",
        "token": "your-auth-token",
        "timeout": 30,
    }

    pipeline = Pipeline(api_config=api_config)

9.2 Register Worker
~~~~~~~~~~~~~~~~~~~

Register your pipeline as a worker:

.. code-block:: python

    worker_info = pipeline.worker_register(
        name="data_processor",
        version="1.0.0"
    )

    worker_id = worker_info.get("id")
    pipeline.set_worker_id(worker_id)

9.3 Health Checks
~~~~~~~~~~~~~~~~

Configure automatic health checks:

.. code-block:: python

    pipeline = Pipeline(
        api_config=api_config,
        health_check_interval=60,  # Check every 60 seconds
    )

10. Next Steps
-------------

Congratulations! You've learned the basics of wpipe.

**Continue learning:**

- :doc:`installation` - Detailed installation guide
- :doc:`usage` - Comprehensive usage examples
- :doc:`user_guide/index` - In-depth user guide
- :doc:`tutorials` - Step-by-step tutorials
- :doc:`api_reference` - Complete API reference
