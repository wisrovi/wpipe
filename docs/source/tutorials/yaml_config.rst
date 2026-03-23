YAML Configuration Tutorial
============================

Learn how to configure pipelines using YAML files.

.. contents::
   :local:
   :depth: 2

1. Introduction
---------------

YAML configuration allows you to:

- Separate configuration from code
- Change behavior without modifying code
- Support multiple environments
- Share configurations across projects

2. Basic YAML Usage
-------------------

2.1 Creating Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # pipeline_config.yaml
    pipeline:
      name: "data_processing"
      version: "1.0.0"
      verbose: true

    api:
      base_url: "http://localhost:8418"
      token: "your-token-here"

    logging:
      level: "INFO"
      file: "pipeline.log"

2.2 Loading Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.util import leer_yaml
    from wpipe import Pipeline

    config = leer_yaml("pipeline_config.yaml")

    pipeline = Pipeline(
        verbose=config["pipeline"]["verbose"],
        api_config=config.get("api")
    )

3. Environment Variables
------------------------

3.1 Using env vars in YAML
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    api:
      token: ${API_TOKEN}

    database:
      path: ${DB_PATH:-default.db}

4. Complete Example
-------------------

.. code-block:: python

    from wpipe.util import leer_yaml
    from wpipe import Pipeline

    # Load configuration
    config = leer_yaml("config.yaml")

    # Create pipeline from config
    pipeline = Pipeline(
        verbose=config.get("pipeline", {}).get("verbose", False),
        api_config=config.get("api")
    )

    # Set steps
    pipeline.set_steps([
        (lambda d: {"data": "test"}, "Step 1", "v1.0"),
    ])

    result = pipeline.run({})
    print(result)

5. Best Practices
-----------------

- Use environment variables for secrets
- Keep configuration files in version control
- Validate configuration on load

6. Next Steps
-------------

- :doc:`conditions` - Add conditional logic
- :doc:`advanced_patterns` - Advanced usage