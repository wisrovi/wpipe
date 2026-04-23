Contributing
============

Thank you for your interest in contributing to wpipe! This guide will help you get started.

1. Getting Started
------------------

1.1 Fork the Repository
~~~~~~~~~~~~~~~~~~~~~~~

Start by forking the wpipe repository on GitHub:

1. Navigate to `https://github.com/wisrovi/wpipe <https://github.com/wisrovi/wpipe>`_
2. Click the "Fork" button
3. Clone your fork locally:

.. code-block:: bash

    git clone https://github.com/YOUR_USERNAME/wpipe.git
    cd wpipe

1.2 Set Up Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a virtual environment and install dependencies:

.. code-block:: bash

    # Create virtual environment
    python -m venv venv

    # Activate it
    source venv/bin/activate  # Linux/macOS
    # or
    venv\Scripts\activate  # Windows

    # Install in development mode
    pip install -e ".[dev]"

1.3 Run Tests
~~~~~~~~~~~~~

Verify your setup by running the test suite:

.. code-block:: bash

    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=wpipe --cov-report=html

    # Open coverage report
    open htmlcov/index.html

2. Development Workflow
-----------------------

2.1 Create a Branch
~~~~~~~~~~~~~~~~~~~

Create a feature branch for your changes:

.. code-block:: bash

    # Create and switch to new branch
    git checkout -b feature/your-feature-name

    # Or for bug fixes
    git checkout -b fix/your-bug-fix

2.2 Make Your Changes
~~~~~~~~~~~~~~~~~~~~

Follow these guidelines:

**Code Style:**

- Follow PEP 8
- Use meaningful variable names
- Add type hints where possible
- Write docstrings for public functions

**Example:**

.. code-block:: python

    def process_data(data: dict, multiplier: int = 1) -> dict:
        """Process input data with optional multiplication.

        Args:
            data: Input dictionary with 'value' key
            multiplier: Factor to multiply by (default: 1)

        Returns:
            Dictionary with processed 'result' key

        Raises:
            ValueError: If 'value' key is missing
        """
        if "value" not in data:
            raise ValueError("Missing required 'value' key")
        return {"result": data["value"] * multiplier}

2.3 Run Quality Checks
~~~~~~~~~~~~~~~~~~~~~~

Before committing, run all quality checks:

.. code-block:: bash

    # Run linting
    ruff check wpipe/

    # Auto-fix linting issues
    ruff check wpipe/ --fix

    # Run type checking
    mypy wpipe/

    # Run tests
    pytest

    # Or run all at once
    ruff check wpipe/ && mypy wpipe/ && pytest

3. Testing Guidelines
----------------------

3.1 Write Tests
~~~~~~~~~~~~~~~

All new features should include tests:

.. code-block:: python

    # test/test_new_feature.py
    import pytest
    from wpipe import Pipeline

    def test_new_feature():
        def my_step(data):
            return {"result": data["x"] * 2}

        pipeline = Pipeline()
        pipeline.set_steps([
            (my_step, "Test Step", "v1.0"),
        ])

        result = pipeline.run({"x": 5})
        assert result["result"] == 10

3.2 Test File Naming
~~~~~~~~~~~~~~~~~~~~

Follow the naming convention:

- Test files: ``test_<module_name>.py``
- Example: ``test_pipeline.py`` for ``pipeline.py``

3.3 Run Specific Tests
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Run specific test file
    pytest test/test_pipeline.py

    # Run specific test function
    pytest test/test_pipeline.py::test_basic_pipeline

    # Run tests matching pattern
    pytest -k "test_name"

4. Documentation
----------------

4.1 Update Documentation
~~~~~~~~~~~~~~~~~~~~~~~~

If your changes affect the API or user experience, update the documentation:

**Files to update:**

- ``docs/source/getting_started.rst`` - For new users
- ``docs/source/api_reference.rst`` - For API changes
- ``docs/source/user_guide/`` - For feature guides
- ``docs/source/examples/`` - For new examples
- ``README.md`` - Main project readme

4.2 Build Documentation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Install documentation dependencies
    pip install -r docs/requirements.txt

    # Build HTML documentation
    cd docs && make html

    # View documentation
    open build/html/index.html

4.3 Documentation Style
~~~~~~~~~~~~~~~~~~~~~~~

- Use RST format for ``.rst`` files
- Follow existing section numbering
- Include code examples
- Add parameter tables for new functions

5. Commit Guidelines
--------------------

5.1 Commit Messages
~~~~~~~~~~~~~~~~~~~

Write clear, concise commit messages:

.. code-block:: bash

    # Good commit messages
    git commit -m "Add retry decorator for failed steps"
    git commit -m "Fix memory leak in long-running pipelines"
    git commit -m "Update API reference documentation"

    # Bad commit messages
    git commit -m "fix"  # Too vague
    git commit -m "Changes"  # Not informative

5.2 Commit Message Format
~~~~~~~~~~~~~~~~~~~~~~~~~

Follow this format:

.. code-block:: text

    <type>: <short description>

    <detailed description (if needed)>

**Types:**

- ``feat``: New feature
- ``fix``: Bug fix
- ``docs``: Documentation changes
- ``style``: Code style changes (formatting, etc.)
- ``refactor``: Code refactoring
- ``test``: Adding or updating tests
- ``chore``: Maintenance tasks

**Example:**

.. code-block:: text

    feat: Add conditional pipeline branching

    Implement Condition class for executing different paths
    based on data values. Supports ==, !=, >, <, >=, <= operators.

    Closes #45

6. Pull Request Process
-----------------------

6.1 Create Pull Request
~~~~~~~~~~~~~~~~~~~~~~~

When your changes are ready, create a pull request:

1. Push your branch to your fork:

.. code-block:: bash

    git push origin feature/your-feature-name

2. Navigate to the original repository
3. Click "New Pull Request"
4. Select your branch
5. Fill in the PR template

6.2 Pull Request Template
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: markdown

    ## Description
    Brief description of your changes

    ## Type of Change
    - [ ] Bug fix
    - [ ] New feature
    - [ ] Documentation update
    - [ ] Code refactoring

    ## Testing
    Describe how you tested your changes

    ## Checklist
    - [ ] Code follows project style guidelines
    - [ ] Self-review completed
    - [ ] Comments added for complex code
    - [ ] Documentation updated
    - [ ] Tests added/updated
    - [ ] All tests pass

6.3 What Happens Next
~~~~~~~~~~~~~~~~~~~~~

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

7. Reporting Issues
-------------------

7.1 Bug Reports
~~~~~~~~~~~~~~~

Report bugs using GitHub Issues with this template:

.. code-block:: markdown

    **Description**
    Clear description of the bug

    **Steps to Reproduce**
    1. Go to '...'
    2. Run '...'
    3. See error

    **Expected Behavior**
    What you expected to happen

    **Actual Behavior**
    What actually happened

    **Environment**
    - OS: [e.g., Ubuntu 22.04]
    - Python version: [e.g., 3.10.12]
    - wpipe version: [e.g., 1.0.0]

7.2 Feature Requests
~~~~~~~~~~~~~~~~~~~~

For new features, open a GitHub Discussion or Issue:

.. code-block:: markdown

    **Feature Description**
    Clear description of the proposed feature

    **Use Case**
    Who would use this and why?

    **Proposed Solution**
    How you think it should work

    **Alternatives Considered**
    Other approaches you've considered

8. Code of Conduct
------------------

Please be respectful and constructive in all interactions:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what's best for the community
- Show empathy towards other community members

9. Questions?
--------------

If you have questions, feel free to:

- Open a GitHub Discussion
- Email the maintainers
- Check the documentation

Thank you for contributing to wpipe!
