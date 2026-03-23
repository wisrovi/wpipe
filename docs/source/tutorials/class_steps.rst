Class-Based Steps Tutorial
===========================

This tutorial covers using Python classes as pipeline steps, enabling more sophisticated processing patterns.

.. contents::
   :local:
   :depth: 2

1. Introduction
--------------

While function-based steps are simple and effective, class-based steps offer several advantages:

- **State Management**: Maintain state across multiple calls
- **Configuration**: Configure behavior at initialization
- **Encapsulation**: Bundle related functionality together
- **Reusability**: Create reusable step classes

2. The __call__ Protocol
-----------------------

For a class to work as a pipeline step, it must implement the ``__call__`` method:

.. code-block:: python

    class MyStep:
        def __call__(self, data: dict) -> dict:
            # Your processing logic here
            return {"result": "value"}

When the pipeline calls the step, it actually calls the ``__call__`` method.

3. Creating Step Classes
-------------------------

3.1 Basic Step Class
~~~~~~~~~~~~~~~~~~~~

Here's a basic step class that multiplies a value:

.. code-block:: python

    class Multiply:
        """Multiply a value by a factor.
        
        Args:
            factor: The multiplier to apply
        """
        
        def __init__(self, factor: float):
            self.factor = factor
        
        def __call__(self, data: dict) -> dict:
            value = data.get("value", 0)
            return {"result": value * self.factor}

Usage:

.. code-block:: python

    from wpipe import Pipeline

    pipeline = Pipeline()
    pipeline.set_steps([
        (Multiply(2), "Multiply by 2", "v1.0"),
    ])

    result = pipeline.run({"value": 10})
    print(result["result"])  # 20

3.2 Configurable Step Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create more flexible steps with configuration options:

.. code-block:: python

    class DataTransformer:
        """Transform data with configurable operations.
        
        Args:
            multiplier: Value to multiply by
            offset: Value to add after multiplication
            round_digits: Number of decimal places to round to
        """
        
        def __init__(
            self, 
            multiplier: float = 1.0, 
            offset: float = 0.0,
            round_digits: int = None
        ):
            self.multiplier = multiplier
            self.offset = offset
            self.round_digits = round_digits
        
        def __call__(self, data: dict) -> dict:
            value = data.get("value", 0)
            result = value * self.multiplier + self.offset
            
            if self.round_digits is not None:
                result = round(result, self.round_digits)
            
            return {"transformed": result}

Usage:

.. code-block:: python

    # Create pipeline with different configurations
    pipeline = Pipeline()
    pipeline.set_steps([
        (DataTransformer(multiplier=2, offset=10, round_digits=2), 
         "Transform Data", "v1.0"),
    ])

    result = pipeline.run({"value": 5})
    # 5 * 2 + 10 = 20, rounded to 2 decimals
    print(result["transformed"])  # 20.0

4. Stateful Steps
----------------

Classes can maintain state across multiple pipeline executions:

4.1 Running Total
~~~~~~~~~~~~~~~~~

.. code-block:: python

    class RunningTotal:
        """Maintain a running total across multiple calls."""
        
        def __init__(self):
            self.total = 0
            self.call_count = 0
        
        def __call__(self, data: dict) -> dict:
            value = data.get("value", 0)
            self.total += value
            self.call_count += 1
            
            return {
                "running_total": self.total,
                "calls": self.call_count,
                "last_value": value
            }

Usage with separate calls:

.. code-block:: python

    step = RunningTotal()
    
    result1 = step({"value": 10})
    print(result1)  # {'running_total': 10, 'calls': 1, 'last_value': 10}
    
    result2 = step({"value": 20})
    print(result2)  # {'running_total': 30, 'calls': 2, 'last_value': 20}

4.2 Accumulator Pattern
~~~~~~~~~~~~~~~~~~~~~~~

Build up data across multiple steps:

.. code-block:: python

    class Accumulator:
        """Accumulate values into a list."""
        
        def __init__(self, key: str = "items"):
            self.key = key
            self.items = []
        
        def __call__(self, data: dict) -> dict:
            # Add new item to accumulator
            if "item" in data:
                self.items.append(data["item"])
            
            return {self.key: self.items.copy()}

5. Composable Steps
------------------

Create reusable building blocks:

5.1 Pipeline Building Blocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class Add:
        def __init__(self, amount: float):
            self.amount = amount
        
        def __call__(self, data: dict) -> dict:
            value = data.get("value", 0)
            return {"value": value + self.amount}


    class Multiply:
        def __init__(self, factor: float):
            self.factor = factor
        
        def __call__(self, data: dict) -> dict:
            value = data.get("value", 1)
            return {"value": value * self.factor}


    class Square:
        def __call__(self, data: dict) -> dict:
            value = data.get("value", 0)
            return {"value": value ** 2}

Combine them:

.. code-block:: python

    from wpipe import Pipeline

    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"value": 2}, "Initialize", "v1.0"),
        (Add(5), "Add 5", "v1.0"),           # 2 + 5 = 7
        (Multiply(3), "Multiply by 3", "v1.0"),  # 7 * 3 = 21
        (Square(), "Square", "v1.0"),        # 21 ^ 2 = 441
    ])

    result = pipeline.run({})
    print(result["value"])  # 441

6. Class Methods as Steps
-------------------------

Use class methods for more complex processing:

.. code-block:: python

    class DataProcessor:
        def __init__(self, config: dict):
            self.config = config
        
        def extract(self, data: dict) -> dict:
            """Extract relevant fields."""
            fields = self.config.get("fields", [])
            extracted = {k: data.get(k) for k in fields if k in data}
            return {"extracted": extracted}
        
        def transform(self, data: dict) -> dict:
            """Transform extracted data."""
            extracted = data.get("extracted", {})
            transformed = {k: v.upper() if isinstance(v, str) else v 
                          for k, v in extracted.items()}
            return {"transformed": transformed}
        
        def load(self, data: dict) -> dict:
            """Prepare for output."""
            return {"result": data.get("transformed", {})}

Usage:

.. code-block:: python

    processor = DataProcessor(fields=["name", "email"])

    pipeline = Pipeline()
    pipeline.set_steps([
        (processor.extract, "Extract", "v1.0"),
        (processor.transform, "Transform", "v1.0"),
        (processor.load, "Load", "v1.0"),
    ])

    result = pipeline.run({"name": "john", "email": "john@example.com"})
    print(result["result"])  # {'name': 'JOHN', 'email': 'JOHN@EXAMPLE.COM'}

7. Best Practices
-----------------

7.1 Keep Steps Focused
~~~~~~~~~~~~~~~~~~~~~

Each step should do one thing well:

.. code-block:: python

    # Good: Single responsibility
    class ValidateEmail:
        def __call__(self, data: dict) -> dict:
            email = data.get("email", "")
            if "@" not in email:
                raise ValueError("Invalid email format")
            return {"valid": True}

7.2 Use Type Hints
~~~~~~~~~~~~~~~~~~

Add type hints for better IDE support:

.. code-block:: python

    class TypedStep:
        def __init__(self, multiplier: float) -> None:
            self.multiplier = multiplier
        
        def __call__(self, data: dict) -> dict:
            value: float = data.get("value", 0.0)
            result: float = value * self.multiplier
            return {"result": result}

7.3 Document Your Classes
~~~~~~~~~~~~~~~~~~~~~~~~~

Add docstrings for clarity:

.. code-block:: python

    class DocumentedStep:
        """Description of what this step does.
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Returns:
            Dictionary with key descriptions
        """
        
        def __init__(self, param1: str, param2: int = 10):
            self.param1 = param1
            self.param2 = param2
        
        def __call__(self, data: dict) -> dict:
            # Implementation
            return {}

8. Advanced Patterns
--------------------

8.1 Step Factory
~~~~~~~~~~~~~~~~

Create steps dynamically:

.. code-block:: python

    def create_multiplier(factor: float):
        """Factory function for creating multiplier steps."""
        class Multiplier:
            def __call__(self, data: dict) -> dict:
                value = data.get("value", 0)
                return {"result": value * factor}
        return Multiplier()

    pipeline = Pipeline()
    pipeline.set_steps([
        (create_multiplier(2), "Double", "v1.0"),
        (create_multiplier(3), "Triple", "v1.0"),
    ])

8.2 Decorator Pattern
~~~~~~~~~~~~~~~~~~~~~~

Wrap steps with additional functionality:

.. code-block:: python

    class TimedStep:
        """Wrap a step to measure execution time."""
        
        def __init__(self, step):
            self.step = step
        
        def __call__(self, data: dict) -> dict:
            import time
            start = time.time()
            result = self.step(data)
            elapsed = time.time() - start
            result["elapsed_time"] = elapsed
            return result

9. Complete Example
------------------

Here's a complete example combining many concepts:

.. code-block:: python

    from wpipe import Pipeline
    import time


    class RetryableStep:
        """Step that can retry on failure."""
        
        def __init__(self, max_retries: int = 3):
            self.max_retries = max_retries
        
        def __call__(self, data: dict) -> dict:
            for attempt in range(self.max_retries):
                try:
                    # Simulate work
                    result = data["value"] * 2
                    return {"result": result, "attempts": attempt + 1}
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    time.sleep(0.1)  # Wait before retry
            return {}


    class LoggingStep:
        """Step that logs its execution."""
        
        def __init__(self, name: str):
            self.name = name
        
        def __call__(self, data: dict) -> dict:
            print(f"[{self.name}] Input: {data}")
            result = {"logged": True, "input_data": data}
            print(f"[{self.name}] Output: {result}")
            return result


    # Create pipeline with class-based steps
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (lambda d: {"value": 10}, "Initialize", "v1.0"),
        (LoggingStep("Processing"), "Log Start", "v1.0"),
        (RetryableStep(max_retries=3), "Process", "v1.0"),
        (LoggingStep("Complete"), "Log End", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Final result: {result}")

10. Next Steps
--------------

Now you understand class-based steps, continue to:

- :doc:`api_integration` - Add API tracking
- :doc:`error_handling` - Handle errors gracefully
- :doc:`nested_pipelines` - Combine pipelines together