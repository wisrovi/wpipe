Conditional Branches Tutorial
==============================

Learn how to execute different paths based on data conditions.

.. contents::
   :local:
   :depth: 2

1. Introduction
---------------

Conditional branches allow you to:

- Execute different steps based on data values
- Build decision trees
- Handle multiple scenarios in one pipeline

2. Using Condition Class
------------------------

2.1 Basic Conditional
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline, Condition

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (lambda d: {"status": "success"}, "Check Status", "v1.0"),
        Condition(
            expression="status == 'success'",
            branch_true=[(handle_success, "Handle Success", "v1.0")],
            branch_false=[(handle_failure, "Handle Failure", "v1.0")],
        ),
    ])

3. Complex Conditions
---------------------

3.1 Multiple Conditions
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    condition = Condition(
        expression="data_type == 'A'",
        branch_true=[(process_a, "Process A", "v1.0")],
        branch_false=[(process_b, "Process B", "v1.0")],
    )

4. Complete Example
------------------

.. code-block:: python

    from wpipe import Pipeline, Condition


    def detect_type(data):
        return {"data_type": "A"}


    def process_type_a(data):
        return {"result": "Processed as A"}


    def process_type_b(data):
        return {"result": "Processed as B"}


    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (detect_type, "Detect Type", "v1.0"),
        Condition(
            expression="data_type == 'A'",
            branch_true=[(process_type_a, "Process Type A", "v1.0")],
            branch_false=[(process_type_b, "Process Type B", "v1.0")],
        ),
    ])

    result = pipeline.run({})
    print(result)

5. Best Practices
-----------------

- Keep conditions simple and readable
- Test both branches
- Use meaningful expressions

6. Next Steps
-------------

- :doc:`advanced_patterns` - Advanced usage
- :doc:`production_deployment` - Deploy to production