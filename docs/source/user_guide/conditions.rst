Conditional Branching
====================

Execute different paths based on data conditions.

Overview
--------

The ``Condition`` class allows pipelines to branch based on data values.

**Important:** The condition must come AFTER a step that provides the data being 
evaluated. The condition evaluates data added by previous steps, not the initial input.

Basic Usage
-----------

.. code-block:: python

   from wpipe import Pipeline
   from wpipe.pipe import Condition

   def fetch_data(data):
       return {"value": 75, "status": "active"}

   def process_active(data):
       return {"processed": "active data"}

   def process_inactive(data):
       return {"processed": "inactive data"}

   condition = Condition(
       expression="value > 50",
       branch_true=[(process_active, "Process Active", "v1.0")],
       branch_false=[(process_inactive, "Process Inactive", "v1.0")],
   )

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (fetch_data, "Fetch", "v1.0"),
       condition,
   ])

   result = pipeline.run({})

Expression Syntax
-----------------

Available Operators
~~~~~~~~~~~~~~~~~~~

* **Comparisons**: ``==``, ``!=``, ``<``, ``>``, ``<=``, ``>=``
* **Logical**: ``and``, ``or``, ``not``
* **Membership**: ``in``, ``not in``

Safe Variables
~~~~~~~~~~~~~~

Only data keys and these constants are available: ``True``, ``False``, ``None``

**Numeric Comparisons:**

.. code-block:: python

   Condition(expression="count >= 10")
   Condition(expression="price < 100.00")
   Condition(expression="percentage != 0")

**String Comparisons:**

.. code-block:: python

   Condition(expression='status == "active"')
   Condition(expression='user_role in ["admin", "moderator"]')

**Boolean Expressions:**

.. code-block:: python

   Condition(expression="is_valid")
   Condition(expression="is_active and is_enabled")
   Condition(expression="not is_blocked")

Without Else
------------

Execute only when condition is true:

.. code-block:: python

   condition = Condition(
       expression="value > 100",
       branch_true=[(log_warning, "Log Warning", "v1.0")],
   )

Complete Example
----------------

.. code-block:: python

   from wpipe import Pipeline
   from wpipe.pipe import Condition

   def validate_order(data):
       order_value = data.get("order_value", 0)
       customer_tier = data.get("tier", "standard")
       return {
           "order_value": order_value,
           "tier": customer_tier,
           "validated": True
       }

   def apply_discount(data):
       return {"discount": data["order_value"] * 0.1}

   def apply_premium_discount(data):
       return {"discount": data["order_value"] * 0.2}

   def no_discount(data):
       return {"discount": 0}

   discount_condition = Condition(
       expression='tier in ["premium", "vip"] and order_value > 100',
       branch_true=[(apply_premium_discount, "Premium Discount", "v1.0")],
       branch_false=[(apply_discount, "Regular Discount", "v1.0")],
   )

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (validate_order, "Validate", "v1.0"),
       discount_condition,
   ])

Best Practices
-------------

1. **Always provide data first**: Condition must come after steps that add evaluation data
2. **Use .get() with defaults**: Handle missing keys in expressions
3. **Test conditions**: Verify conditions work as expected
4. **Keep expressions simple**: Complex expressions are harder to debug

Next Steps
----------

* Learn about :doc:`retry` for automatic retries
* Explore :doc:`error_handling` for error recovery
