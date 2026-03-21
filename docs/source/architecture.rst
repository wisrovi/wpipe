Architecture
===========

This section describes the architecture of wpipe.

System Overview
--------------

wpipe is designed as a pipeline orchestration library with the following components:

.. graphviz::

   digraph G {
      rankdir=LR;
      Pipeline -> APIClient;
      Pipeline -> SQLite;
      Pipeline -> Logger;
      APIClient -> "External API";
      SQLite -> "Database";
   }

Core Components
--------------

Pipeline
~~~~~~~~

The Pipeline class is the main entry point for creating and executing pipelines.

.. graphviz::

   digraph G {
      rankdir=TB;
      Pipeline [shape=box];
      "Step 1" -> "Step 2" -> "Step 3";
   }

APIClient
~~~~~~~~~

The APIClient handles communication with external APIs for worker registration and health checks.

SQLite
~~~~~~

SQLite provides persistent storage for pipeline execution results.

Modules
-------

wpipe/
  - pipe/          Pipeline implementation
  - api_client/    API communication
  - sqlite/         Database operations
  - log/           Logging utilities
  - ram/           Memory utilities
  - util/          YAML utilities
  - exception/     Custom exceptions

Design Patterns
---------------

Pipeline Pattern
~~~~~~~~~~~~~~~

Each step receives the accumulated results from previous steps and returns its own results.

Decorator Pattern
~~~~~~~~~~~~~~~~~

Decorators are used for automatic task and pipeline reporting.

Context Manager
~~~~~~~~~~~~~~~

Wsqlite uses context managers for automatic resource cleanup.

Data Flow
---------

1. Input data is passed to the pipeline
2. Each step processes the data and returns results
3. Results are accumulated and passed to the next step
4. Final results are returned after all steps complete
