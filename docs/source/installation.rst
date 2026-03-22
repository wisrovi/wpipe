Installation
============

This guide covers all installation methods for wpipe.

Requirements
------------

Python
~~~~~~

* Python 3.9 or higher
* Python 3.10 recommended
* Python 3.11+ fully supported

Operating System
~~~~~~~~~~~~~~~~

wpipe works on all major operating systems:

* **Linux**: Ubuntu, Debian, CentOS, Fedora
* **macOS**: All versions with Python 3.9+
* **Windows**: Windows 10/11 with WSL or native Python

Dependencies
~~~~~~~~~~~~

wpipe requires the following packages:

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Package
     - Version
     - Purpose
   * - requests
     - >=2.31.0
     - HTTP client for API calls
   * - pandas
     - >=2.0.0
     - Data manipulation
   * - pyyaml
     - >=6.0.1
     - YAML configuration
   * - tabulate
     - >=0.9.0
     - Terminal output formatting

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Package
     - Purpose
   * - rich
     - Enhanced terminal output
   * - loguru
     - Advanced logging
   * - tqdm
     - Progress bars

Installation via pip
--------------------

The easiest method
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install wpipe

Install Specific Version
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install wpipe==1.0.0

Upgrade Existing Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install --upgrade wpipe

Virtual Environment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create an isolated environment:

.. code-block:: bash

   python -m venv wpipe-env
   source wpipe-env/bin/activate  # Linux/macOS
   # wpipe-env\Scripts\activate  # Windows
   pip install wpipe

Installation from Source
-----------------------

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe.git
   cd wpipe

Editable Install
~~~~~~~~~~~~~~~~

For development, install in editable mode:

.. code-block:: bash

   pip install -e .

Install with Dev Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -e ".[dev]"

Install Specific Branch
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install git+https://github.com/wisrovi/wpipe.git@develop

Docker Installation
-------------------

Using Docker
~~~~~~~~~~~~

.. code-block:: bash

   docker run -it python:3.11-slim pip install wpipe

Docker Compose
~~~~~~~~~~~~~~

Create a ``docker-compose.yml``:

.. code-block:: yaml

   version: '3.8'
   services:
     wpipe:
       image: python:3.11-slim
       command: python -c "from wpipe import Pipeline; print('wpipe installed!')"
       install:
         - wpipe

Verification
------------

Verify Installation
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import wpipe
   print(wpipe.__version__)  # Should print 1.0.0

Test Basic Functionality
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wpipe import Pipeline

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       ((lambda d: {"ok": True}), "Test", "v1.0"),
   ])
   result = pipeline.run({})
   print(f"Test passed: {result}")

Configuration
-------------

First-Time Setup
~~~~~~~~~~~~~~~~

Create a configuration file ``~/.wpipe/config.yaml``:

.. code-block:: yaml

   default:
     verbose: true
     timeout: 30

   api:
     base_url: http://localhost:8418
     token: your_token_here

Troubleshooting
---------------

Import Errors
~~~~~~~~~~~~~

If you see ``ModuleNotFoundError``:

.. code-block:: bash

   pip install --upgrade pip
   pip install wpipe

Permission Errors
~~~~~~~~~~~~~~~~~

Avoid system-wide installs:

.. code-block:: bash

   pip install --user wpipe
   # Or use virtual environment

Python Version Issues
~~~~~~~~~~~~~~~~~~~~~

Check your Python version:

.. code-block:: bash

   python --version
   # Should be 3.9 or higher

Uninstallation
--------------

Remove wpipe
~~~~~~~~~~~~~

.. code-block:: bash

   pip uninstall wpipe

Keep Dependencies
~~~~~~~~~~~~~~~~

To keep the dependencies:

.. code-block:: bash

   pip uninstall wpipe-pipeline
   # Keep: requests, pandas, pyyaml, tabulate

Next Steps
----------

Now that wpipe is installed:

1. Follow the :doc:`getting_started` guide
2. Explore :doc:`usage` examples
3. Check :doc:`api_reference` for details
