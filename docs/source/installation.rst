Installation Guide
==================

.. meta::
   :description: How to install WPipe v2.1.1-LTS on Linux, Windows, and macOS.
   :keywords: install, pip, source, docker, wpipe

WPipe is distributed via PyPI and is designed to be lightweight with minimal external dependencies.

1. Requirements
---------------

*   **Python**: 3.9, 3.10, 3.11, or 3.12+ (Recommended).
*   **OS**: Linux (Optimized for Ubuntu/Debian), macOS, Windows (WSL recommended).

2. Standard Installation
------------------------

Most users should install the stable release via ``pip``:

.. code-block:: bash

    pip install wpipe

3. Advanced Installation
------------------------

If you need specific development tools or the latest source code:

.. tab-set::

    .. tab-item:: Development
        :sync: dev

        Includes testing frameworks (pytest, ruff, mypy).
        
        .. code-block:: bash

            pip install "wpipe[dev]"

    .. tab-item:: Documentation
        :sync: docs

        Includes Sphinx and themes for building these docs locally.
        
        .. code-block:: bash

            pip install "wpipe[docs]"

    .. tab-item:: Source (Bleeding Edge)
        :sync: source

        .. code-block:: bash

            git clone https://github.com/wisrovi/wpipe
            cd wpipe
            pip install -e .

4. Containerized (Docker)
-------------------------

For cloud deployments, we recommend using the official Python slim images.

.. code-block:: dockerfile

    FROM python:3.11-slim
    RUN pip install wpipe
    COPY my_pipeline.py .
    CMD ["python", "my_pipeline.py"]

5. Verification
---------------

Ensure the engine is correctly balanced:

.. code-block:: python

    import wpipe
    print(wpipe.__version__)  # Should return 2.1.1

6. Troubleshooting
------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Issue
     - Solution
   * - **SQLite Error**
     - Ensure your filesystem supports file locking (required for WAL mode).
   * - **Memory Limit Failed**
     - ``memory_limit`` utilities require Linux cgroups. Use Docker if on Windows/Mac.
   * - **Module Not Found**
     - Ensure your virtual environment is active.
