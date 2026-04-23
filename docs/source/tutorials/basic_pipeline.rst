Basic Pipeline Tutorial
========================

In this comprehensive tutorial, you'll learn how to create production-ready pipelines with wpipe from scratch. We'll cover everything from basic concepts to advanced patterns with detailed explanations and real-world examples.

.. contents::
   :local:
   :depth: 4

1. Introduction and Overview
-----------------------------

1.1 What is a Pipeline?
~~~~~~~~~~~~~~~~~~~~~~~

A pipeline in wpipe is a sequence of processing steps that execute in order, where each step receives all accumulated data from previous steps. This creates a powerful data flow model where information is progressively enriched as it moves through the pipeline.

**Key Characteristics:**

- **Sequential Execution**: Steps execute one after another in the order they're defined
- **Data Accumulation**: Each step receives a dictionary containing all data from previous steps
- **Failure Handling**: Pipeline stops on the first unhandled error by default
- **Configurable**: Extensive options for retry, logging, and error handling

**Why Use Pipelines?**

Pipelines provide several advantages over traditional sequential code:

1. **Declarative Structure**: The pipeline definition clearly shows the flow of data processing
2. **Reusability**: Steps can be easily recombined in different pipelines
3. **Testability**: Each step can be tested independently
4. **Maintainability**: Adding or removing steps doesn't require changing other code

1.2 What You'll Build
~~~~~~~~~~~~~~~~~~~~~~

Throughout this tutorial, we'll build a data processing pipeline that:

1. Generates sample data (simulating data ingestion)
2. Validates and cleans the data
3. Performs statistical analysis
4. Formats the results for output

This example demonstrates all the core concepts you'll need to build production pipelines.

2. Environment Setup
--------------------

2.1 Prerequisites
~~~~~~~~~~~~~~~~~

Before starting, ensure you have:

- Python 3.9 or higher installed
- A code editor or IDE (VS Code, PyCharm, etc.)
- Terminal access

Check your Python version:

.. code-block:: bash

    python --version
    # Should output something like: Python 3.11.4

2.2 Installation
~~~~~~~~~~~~~~~~

Install wpipe using pip:

.. code-block:: bash

    pip install wpipe

Verify the installation:

.. code-block:: python

    import wpipe
    print(f"wpipe version: {wpipe.__version__}")
    # Should output: wpipe version: 1.0.0

For development and testing, install with dev dependencies:

.. code-block:: bash

    pip install -e ".[dev]"

This will install:
- pytest for testing
- pytest-cov for coverage
- ruff for linting
- mypy for type checking

3. Your First Pipeline
----------------------

3.1 Basic Structure
~~~~~~~~~~~~~~~~~~~

Every wpipe pipeline follows this basic structure:

.. code-block:: python

    from wpipe import Pipeline

    # 1. Create a pipeline instance
    pipeline = Pipeline(verbose=True)

    # 2. Define your processing steps
    def step_function(data):
        # Process data and return results
        return {"key": "value"}

    # 3. Configure the pipeline with steps
    pipeline.set_steps([
        (step_function, "Step Name", "version"),
    ])

    # 4. Execute the pipeline
    result = pipeline.run(initial_data)

Let's break down each component:

**Pipeline Instance**: The Pipeline object manages execution, handles errors, and coordinates data flow between steps.

**Step Functions**: Each step is a callable (function or class) that receives a dictionary and returns a dictionary.

**Step Configuration**: Steps are defined as tuples of (function, name, version).

**Execution**: The run() method executes all steps in sequence.

3.2 Step-by-Step Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's build our pipeline step by step:

**Step 1: Create the Script**

Create a new Python file called ``pipeline_example.py``:

.. code-block:: python

    from wpipe import Pipeline

**Step 2: Define Your Steps**

Add the step functions:

.. code-block:: python

    from wpipe import Pipeline


    def generate_sample_data(data):
        """Generate sample numeric data for processing.
        
        This step simulates fetching data from an external source.
        In a real application, this might fetch from a database,
        API, or file system.
        
        Args:
            data: Initial input data (can be empty dict)
            
        Returns:
            Dictionary containing the generated data
        """
        return {
            "numbers": [12, 45, 67, 89, 23, 56, 78, 34, 90, 11],
            "source": "sample_generator"
        }


    def validate_data(data):
        """Validate that required data exists and is valid.
        
        This step performs data validation to ensure the pipeline
        has valid input before proceeding with processing.
        
        Args:
            data: Dictionary containing 'numbers' key
            
        Returns:
            Dictionary with validation result
            
        Raises:
            ValueError: If data is invalid
        """
        numbers = data.get("numbers", [])
        
        if not numbers:
            raise ValueError("No numbers provided in data")
        
        if not all(isinstance(n, (int, float)) for n in numbers):
            raise ValueError("All values in numbers must be numeric")
        
        return {"validation": "passed", "count": len(numbers)}


    def calculate_statistics(data):
        """Calculate statistical measures on the data.
        
        This step processes the validated data and produces
        statistical analysis.
        
        Args:
            data: Dictionary containing 'numbers' list
            
        Returns:
            Dictionary with statistical measures
        """
        numbers = data["numbers"]
        
        return {
            "min": min(numbers),
            "max": max(numbers),
            "sum": sum(numbers),
            "average": sum(numbers) / len(numbers),
            "count": len(numbers),
            "sorted": sorted(numbers)
        }


    def format_results(data):
        """Format the calculation results for output.
        
        This step takes the raw statistics and formats them
        into a human-readable string.
        
        Args:
            data: Dictionary containing statistical measures
            
        Returns:
            Dictionary with formatted output string
        """
        stats = {
            "min": data["min"],
            "max": data["max"],
            "sum": data["sum"],
            "average": data["average"],
            "count": data["count"]
        }
        
        output = f"""
    ╔══════════════════════════════════════════╗
    ║       STATISTICAL ANALYSIS RESULTS       ║
    ╠══════════════════════════════════════════╣
    ║  Count:   {stats['count']:>25} ║
    ║  Sum:     {stats['sum']:>25} ║
    ║  Average: {stats['average']:>25.2f} ║
    ║  Min:     {stats['min']:>25} ║
    ║  Max:     {stats['max']:>25} ║
    ╚══════════════════════════════════════════╝
        """
        
        return {"output": output.strip(), "stats": stats}


    def save_results(data):
        """Save results (simulated).
        
        In a real application, this would write to a database,
        file, or external service.
        
        Args:
            data: Dictionary containing results to save
            
        Returns:
            Dictionary with save confirmation
        """
        # Simulate saving
        return {"saved": True, "record_count": data["count"]}

**Step 3: Create and Configure the Pipeline**

Now assemble the pipeline:

.. code-block:: python

    # Create a new pipeline instance with verbose output
    pipeline = Pipeline(verbose=True)

    # Configure the pipeline with our steps
    # Each tuple is: (function, name, version)
    pipeline.set_steps([
        (generate_sample_data, "Generate Sample Data", "v1.0.0"),
        (validate_data, "Validate Data", "v1.0.0"),
        (calculate_statistics, "Calculate Statistics", "v1.0.0"),
        (format_results, "Format Results", "v1.0.0"),
        (save_results, "Save Results", "v1.0.0"),
    ])

**Step 4: Execute the Pipeline**

Run the pipeline:

.. code-block:: python

    # Execute with empty initial data
    result = pipeline.run({})

    # Display results
    print("\n" + "=" * 50)
    print("PIPELINE EXECUTION COMPLETE")
    print("=" * 50)
    print(result["output"])

**Step 5: Run the Complete Example**

Here's the complete script:

.. code-block:: python

    """
    Complete wpipe Basic Pipeline Example
    
    This example demonstrates creating a basic data processing pipeline
    with multiple steps, showing data flow and accumulation.
    """

    from wpipe import Pipeline


    def generate_sample_data(data):
        """Generate sample numeric data."""
        return {
            "numbers": [12, 45, 67, 89, 23, 56, 78, 34, 90, 11],
            "source": "sample_generator"
        }


    def validate_data(data):
        """Validate input data."""
        numbers = data.get("numbers", [])
        if not numbers:
            raise ValueError("No numbers provided")
        return {"validation": "passed", "count": len(numbers)}


    def calculate_statistics(data):
        """Calculate statistical measures."""
        numbers = data["numbers"]
        return {
            "min": min(numbers),
            "max": max(numbers),
            "sum": sum(numbers),
            "average": sum(numbers) / len(numbers),
            "count": len(numbers),
            "sorted": sorted(numbers)
        }


    def format_results(data):
        """Format results for output."""
        stats = {
            "count": data["count"],
            "sum": data["sum"],
            "average": data["average"],
            "min": data["min"],
            "max": data["max"]
        }
        
        output = f"""
    Statistical Analysis:
    ---------------------
    Count:   {stats['count']}
    Sum:     {stats['sum']}
    Average: {stats['average']:.2f}
    Min:     {stats['min']}
    Max:     {stats['max']}
        """
        
        return {"output": output.strip(), "stats": stats}


    def save_results(data):
        """Save results."""
        return {"saved": True, "record_count": data["count"]}


    # Create and run the pipeline
    if __name__ == "__main__":
        pipeline = Pipeline(verbose=True)
        
        pipeline.set_steps([
            (generate_sample_data, "Generate Data", "v1.0"),
            (validate_data, "Validate Data", "v1.0"),
            (calculate_statistics, "Calculate Stats", "v1.0"),
            (format_results, "Format Results", "v1.0"),
            (save_results, "Save Results", "v1.0"),
        ])
        
        result = pipeline.run({})
        
        print("\n" + "=" * 50)
        print("RESULTS:")
        print("=" * 50)
        print(result["output"])

4. Understanding Data Flow
---------------------------

4.1 How Data Accumulates
~~~~~~~~~~~~~~~~~~~~~~~~~

One of the most important concepts in wpipe is how data flows through the pipeline. Each step receives ALL data from all previous steps:

::

    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                           DATA FLOW DIAGRAM                                │
    └─────────────────────────────────────────────────────────────────────────────┘
    
    INITIAL DATA: {}
    
    ↓ (Step 1: generate_sample_data)
    
    data = {
        "numbers": [12, 45, 67, 89, 23, 56, 78, 34, 90, 11],
        "source": "sample_generator"
    }
    
    ↓ (Step 2: validate_data)
    
    data = {
        "numbers": [12, 45, 67, 89, 23, 56, 78, 34, 90, 11],
        "source": "sample_generator",
        "validation": "passed",
        "count": 10
    }
    
    ↓ (Step 3: calculate_statistics)
    
    data = {
        "numbers": [...],
        "source": "sample_generator",
        "validation": "passed",
        "count": 10,
        "min": 11,
        "max": 90,
        "sum": 505,
        "average": 50.5,
        "sorted": [11, 12, 23, ...]
    }
    
    ↓ (Step 4 & 5...)
    
    FINAL RESULT: All accumulated data from all steps

4.2 Practical Example of Data Evolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's trace through exactly what happens:

.. code-block:: python

    from wpipe import Pipeline


    def step1(data):
        """Add initial data."""
        return {"a": 1}


    def step2(data):
        """Step 2 can access step 1's data."""
        return {"b": data["a"] + 1}


    def step3(data):
        """Step 3 can access BOTH step 1 and step 2's data."""
        return {
            "c": data["a"] + data["b"],
            "note": f"a={data['a']}, b={data['b']}"
        }


    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
        (step3, "Step 3", "v1.0"),
    ])

    result = pipeline.run({})

    print("Final result:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    # Output:
    #   a: 1
    #   b: 2
    #   c: 3
    #   note: a=1, b=2

5. Passing Initial Data
-----------------------

5.1 Providing Input Data
~~~~~~~~~~~~~~~~~~~~~~~~

You can pass initial data to the pipeline:

.. code-block:: python

    initial_data = {
        "user_id": "user_123",
        "filter": "active",
        "limit": 100
    }

    result = pipeline.run(initial_data)

    # The initial data is preserved and passed through
    print(result["user_id"])   # "user_123"
    print(result["filter"])    # "active"
    print(result["limit"])      # 100

5.2 Use Case: Parameterized Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Passing initial data makes pipelines reusable:

.. code-block:: python

    def process_user_data(data):
        """Process data for a specific user."""
        return {"processed": True, "user": data["user_id"]}


    pipeline = Pipeline()
    pipeline.set_steps([
        (process_user_data, "Process User", "v1.0"),
    ])

    # Run for different users
    result1 = pipeline.run({"user_id": "user_1"})
    result2 = pipeline.run({"user_id": "user_2"})

6. Step Function Patterns
--------------------------

6.1 Lambda Functions
~~~~~~~~~~~~~~~~~~~~

For simple transformations, you can use lambda functions:

.. code-block:: python

    pipeline.set_steps([
        (lambda d: {"value": 42}, "Set Value", "v1.0"),
        (lambda d: {"doubled": d["value"] * 2}, "Double", "v1.0"),
        (lambda d: {"result": d["doubled"] + 1}, "Add One", "v1.0"),
    ])

    result = pipeline.run({})
    print(result)  # {'value': 42, 'doubled': 84, 'result': 85}

6.2 Class-Based Steps
~~~~~~~~~~~~~~~~~~~~~

Classes with ``__call__`` can be used as steps:

.. code-block:: python

    class Multiply:
        """Multiply a value by a factor."""
        
        def __init__(self, factor: float):
            self.factor = factor
        
        def __call__(self, data: dict) -> dict:
            value = data.get("value", 0)
            return {"result": value * self.factor}


    class Add:
        """Add an amount to a value."""
        
        def __init__(self, amount: float):
            self.amount = amount
        
        def __call__(self, data: dict) -> dict:
            value = data.get("result", 0)
            return {"result": value + self.amount}


    # Use class instances as steps
    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"value": 10}, "Set Value", "v1.0"),
        (Multiply(3), "Multiply by 3", "v1.0"),
        (Add(5), "Add 5", "v1.0"),
    ])

    result = pipeline.run({})
    print(result["result"])  # 35 (10 * 3 + 5)

7. Error Handling
-----------------

7.1 Basic Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~

When a step fails, wpipe raises a TaskError:

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.exception import TaskError


    def failing_step(data):
        raise ValueError("Something went wrong!")


    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (failing_step, "Failing Step", "v1.0"),
    ])

    try:
        result = pipeline.run({})
    except TaskError as e:
        print(f"Pipeline failed: {e}")
        print(f"Error code: {e.error_code}")

7.2 Validation Errors
~~~~~~~~~~~~~~~~~~~~~

Use validation to catch problems early:

.. code-block:: python

    def validated_step(data):
        """Step with input validation."""
        if "required_field" not in data:
            raise ValueError("Missing required_field!")
        
        if not isinstance(data["required_field"], str):
            raise ValueError("required_field must be a string!")
        
        return {"processed": True}

8. Advanced Features
-------------------

8.1 Conditional Execution
~~~~~~~~~~~~~~~~~~~~~~~~~

Execute different steps based on conditions:

.. code-block:: python

    from wpipe import Pipeline, Condition


    def process_a(data):
        return {"result": "Processed as A"}


    def process_b(data):
        return {"result": "Processed as B"}


    def detect_type(data):
        return {"data_type": "B"}


    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (detect_type, "Detect Type", "v1.0"),
        Condition(
            expression="data_type == 'A'",
            branch_true=[(process_a, "Process A", "v1.0")],
            branch_false=[(process_b, "Process B", "v1.0")],
        ),
    ])

    result = pipeline.run({})
    print(result["result"])  # "Processed as B"

8.2 Retry Logic
~~~~~~~~~~~~~~~

Configure automatic retries:

.. code-block:: python

    pipeline = Pipeline(
        verbose=True,
        max_retries=3,      # Try up to 3 times
        retry_delay=1.0,    # Wait 1 second between retries
        retry_on_exceptions=(ConnectionError, TimeoutError)
    )

9. Testing Your Pipeline
--------------------------

9.1 Unit Testing Steps
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pytest

    def test_calculate_statistics():
        """Test the statistics calculation step."""
        # Arrange
        data = {"numbers": [1, 2, 3, 4, 5]}
        
        # Act
        from your_module import calculate_statistics
        result = calculate_statistics(data)
        
        # Assert
        assert result["min"] == 1
        assert result["max"] == 5
        assert result["sum"] == 15
        assert result["average"] == 3.0
        assert result["count"] == 5

9.2 Integration Testing
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def test_full_pipeline():
        """Test the complete pipeline."""
        # Arrange
        pipeline = Pipeline()
        pipeline.set_steps([
            (lambda d: {"numbers": [10, 20, 30]}, "Generate", "v1.0"),
            (lambda d: {"sum": sum(d["numbers"])}, "Sum", "v1.0"),
        ])
        
        # Act
        result = pipeline.run({})
        
        # Assert
        assert result["sum"] == 60

10. Best Practices Summary
--------------------------

**Do:**

- Use descriptive step names
- Validate input early in the pipeline
- Keep steps focused on a single responsibility
- Use type hints for better IDE support
- Handle errors gracefully with appropriate error codes

**Don't:**

- Use vague step names like "Step 1", "Step 2"
- Skip validation - validate at the start
- Put multiple concerns in one step
- Hardcode secrets in your pipeline
- Forget to return dictionaries from steps

11. Exercises
--------------

Practice what you've learned:

11.1 Exercise 1: String Processing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a pipeline that:
1. Takes a sentence as input
2. Counts the words
3. Finds the longest word
4. Reverses the sentence
5. Formats all results

11.2 Exercise 2: Temperature Converter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a pipeline that:
1. Takes a temperature in Celsius
2. Converts to Fahrenheit
3. Converts to Kelvin
4. Determines if it's hot (>30°C), mild (15-30°C), or cold (<15°C)
5. Formats all conversions

11.3 Exercise 3: Shopping Cart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a pipeline that:
1. Takes a list of items with prices
2. Calculates subtotal
3. Applies discount (10% if subtotal > $100)
4. Calculates tax (8%)
5. Calculates final total

12. Next Steps
--------------

Now that you understand basic pipelines:

- Continue to :doc:`class_steps` - Learn to use classes as steps
- Explore :doc:`api_integration` - Add API tracking
- Learn :doc:`error_handling` - Handle errors gracefully
- Check :doc:`../best_practices` - More best practices

The :doc:`../tutorials` section contains many more detailed tutorials covering advanced topics.