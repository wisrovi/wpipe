Installation
============

Requirements
------------

- Python 3.9 or higher
- pip package manager

Dependencies
~~~~~~~~~~~~

wpipe requires the following packages:

- requests >= 2.31.0
- loguru >= 0.7.0
- pandas >= 2.0.0
- pyyaml >= 6.0.1
- tqdm >= 4.66.0
- prefect >= 2.14.0
- rich >= 13.7.0

Installation via pip
--------------------

The easiest way to install wpipe is using pip:

.. code-block:: bash

   pip install wpipe

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

To install from source:

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe
   cd wpipe
   pip install -e .

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For development, install with all dev dependencies:

.. code-block:: bash

   pip install wpipe[dev]

Docker Installation
~~~~~~~~~~~~~~~~~~~

You can also use the wpipe-api Docker container for the API backend:

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe-api
   cd wpipe-api
   docker-compose up -d

This will start:

- Backend API at http://localhost:8418
- Dashboard at http://localhost:8050

Troubleshooting
---------------

If you encounter installation issues:

1. Make sure you have Python 3.9+ installed
2. Upgrade pip: ``pip install --upgrade pip``
3. Try installing dependencies separately: ``pip install -r requirements.txt``
