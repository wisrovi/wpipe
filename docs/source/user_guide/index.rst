User Guide
==========

This guide provides in-depth documentation on all wpipe features and capabilities.

1. Getting Started
------------------

Pipeline Basics
~~~~~~~~~~~~~~

Learn the core concepts, data flow, and step execution.

:doc:`pipeline_basics`

2. Core Features
----------------

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
~~~~~~~~~~~~~

Persist pipeline results to database.

:doc:`sqlite`

YAML Configuration
~~~~~~~~~~~~~~~~~~~

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

3. Advanced Topics
------------------

Best Practices
~~~~~~~~~~~~~~

Recommended patterns for building robust pipelines.

:doc:`best_practices`

Troubleshooting
~~~~~~~~~~~~~~~

Solutions to common issues and debugging techniques.

:doc:`troubleshooting`

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
   best_practices
   troubleshooting
