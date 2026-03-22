SQLite Storage
==============

Persist pipeline execution results to SQLite databases.

Overview
--------

wpipe provides SQLite integration for storing pipeline results locally.

Basic Usage
-----------

**Write Results:**

.. code-block:: python

   from wpipe.sqlite import Wsqlite

   db = Wsqlite("pipeline_results.db")

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       (step1, "Step 1", "v1.0"),
       (step2, "Step 2", "v1.0"),
   ])

   db.write(input_data={"x": 10}, output_data=pipeline.run({"x": 10}))

**Read Results:**

.. code-block:: python

   results = db.read()
   for row in results:
       print(row)

**Query Results:**

.. code-block:: python

   results = db.query("SELECT * FROM results WHERE input_x > ?", (5,))

Class-Based Access
------------------

For more control:

.. code-block:: python

   from wpipe.sqlite import SQLite

   db = SQLite("custom_results.db")
   db.create_table()

   db.insert(input_data={"test": True}, output_data={"result": 42})

   results = db.select_all()
   db.close()

Methods
-------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Method
     - Description
   * - ``write(input_data, output_data)``
     - Insert pipeline results
   * - ``read()``
     - Read all results
   * - ``query(sql, params)``
     - Execute SQL query
   * - ``create_table()``
     - Create results table
   * - ``insert(input_data, output_data)``
     - Insert single result
   * - ``select_all()``
     - Select all rows
   * - ``close()``
     - Close database connection

Complete Example
----------------

.. code-block:: python

   from wpipe import Pipeline
   from wpipe.sqlite import Wsqlite

   db = Wsqlite("analytics.db")

   def collect_metrics(data):
       return {"requests": 100, "errors": 2}

   def calculate_rate(data):
       rate = (data["errors"] / data["requests"]) * 100
       return {"error_rate": rate}

   pipeline = Pipeline()
   pipeline.set_steps([
       (collect_metrics, "Collect", "v1.0"),
       (calculate_rate, "Calculate", "v1.0"),
   ])

   result = pipeline.run({})
   db.write(input_data={"service": "api"}, output_data=result)

   print(f"Error rate: {result['error_rate']}%")

Best Practices
--------------

1. **Use meaningful table names**: Easier to manage multiple databases
2. **Close connections**: Prevent resource leaks
3. **Handle large data**: Consider compressing for storage
4. **Backup regularly**: Protect against data loss

Next Steps
---------

* Learn about :doc:`yaml_config` for configuration management
* Explore :doc:`nested_pipelines` for complex workflows
