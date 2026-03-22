YAML Configuration
==================

Load and manage pipeline configuration from YAML files.

Overview
--------

YAML configuration allows you to define pipeline settings externally, making it 
easy to modify configuration without changing code.

Reading YAML
------------

.. code-block:: python

   from wpipe.util import leer_yaml

   config = leer_yaml("config.yaml")
   print(config)

Writing YAML
------------

.. code-block:: python

   from wpipe.util import escribir_yaml

   config = {
       "name": "my_pipeline",
       "version": "v1.0",
       "steps": [
           {"name": "step1", "version": "v1.0"},
           {"name": "step2", "version": "v1.0"},
       ]
   }

   escribir_yaml("config.yaml", config)

YAML File Structure
-------------------

.. code-block:: yaml

   # config.yaml
   name: data_processing
   version: 1.0.0
   
   pipeline:
     verbose: true
   
   api:
     base_url: http://localhost:8418
     token: my_secret_token
   
   steps:
     - name: fetch
       version: v1.0
     - name: process
       version: v1.0

Loading Configuration
----------------------

.. code-block:: python

   from wpipe import Pipeline
   from wpipe.util import leer_yaml

   config = leer_yaml("pipeline_config.yaml")

   api_config = {
       "base_url": config["api"]["base_url"],
       "token": config["api"]["token"]
   }

   pipeline = Pipeline(
       worker_name=config["name"],
       api_config=api_config,
       verbose=config["pipeline"]["verbose"]
   )

Saving Results
--------------

.. code-block:: python

   from wpipe.util import escribir_yaml

   result = pipeline.run({"x": 10})

   output = {
       "input": {"x": 10},
       "output": result,
       "timestamp": "2026-03-22"
   }

   escribir_yaml("output.yaml", {"result": result})

Best Practices
--------------

1. **Separate config from code**: Easier to modify settings
2. **Use descriptive keys**: self-documenting configuration
3. **Validate on load**: Check required fields exist
4. **Version control configs**: Track configuration changes

Next Steps
---------

* Learn about :doc:`nested_pipelines` for complex workflows
* Explore :doc:`error_handling` for error recovery
