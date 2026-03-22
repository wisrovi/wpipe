User Guide
==========

This guide provides in-depth documentation on all wpipe features and capabilities.

Pipeline Basics
--------------

Learn the core concepts, data flow, and step execution.

* :doc:`pipeline_basics` - Core concepts and data flow

Features
--------

Conditions
~~~~~~~~~~

Conditional branching based on data values.

:doc:`conditions`

Retry Logic
~~~~~~~~~~~

Automatic retries for failed steps.

:doc:`retry`

API Integration
~~~~~~~~~~~~~~~

Connect to external APIs for tracking.

:doc:`api_integration`

SQLite Storage
~~~~~~~~~~~~~~

Persist pipeline results to database.

:doc:`sqlite`

YAML Configuration
~~~~~~~~~~~~~~~~~~

Load pipeline config from YAML files.

:doc:`yaml_config`

Nested Pipelines
~~~~~~~~~~~~~~~~

Compose complex workflows.

:doc:`nested_pipelines`

Error Handling
~~~~~~~~~~~~~~

Robust error handling and recovery.

:doc:`error_handling`

.. toctree::
   :maxdepth: 1
   :hidden:

   pipeline_basics
   conditions
   retry
   api_integration
   sqlite
   yaml_config
   nested_pipelines
   error_handling
