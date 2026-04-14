# Sphinx Documentation Examples

## Example 1: Complete docs/ Structure

```
docs/
├── Makefile
├── make.bat
├── requirements.txt
└── source/
    ├── conf.py
    ├── index.rst
    ├── installation.rst
    ├── usage.rst
    ├── faq.rst
    ├── contributing.rst
    ├── api/
    │   └── modules.rst
    ├── tutorials/
    │   ├── index.rst
    │   └── first_steps.rst
    ├── _static/
    │   ├── css/
    │   │   └── custom.css
    │   └── images/
    │       └── logo.png
    └── diagrams/
```

## Example 2: Makefile (Required by RTD)

```makefile
# Minimal makefile for Sphinx documentation
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

## Example 3: .readthedocs.yaml

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/source/conf.py

python:
  install:
    - requirements: docs/requirements.txt
```

## Example 4: docs/requirements.txt

```txt
sphinx>=7.0.0
sphinx-rtd-theme>=2.0.0
sphinx-autodoc-typehints>=1.25.0
sphinx-copybutton>=0.5.2
myst-parser>=2.0.0
```

## Example 5: Custom CSS

```css
/* source/_static/css/custom.css */

.wy-nav-content {
    max-width: 900px;
}

.highlight-python {
    background: #f8f8f8;
}

.section h1 {
    color: #4479a1;
}
```

## Example 6: Commands Output

```bash
# Install dependencies
$ pip install sphinx sphinx-rtd-theme

# Quick start
$ sphinx-quickstart docs

# Generate autodoc
$ sphinx-apidoc -f -o docs/source/api app/

# Build HTML
$ cd docs && make html

# Serve locally
$ python -m http.server 8000 -d docs/_build/html
```

## Example 7: index.rst with Images

```rst
Project Overview
================

.. image:: _static/architecture.png
   :alt: System Architecture
   :align: center
   :width: 600

Features
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
   api

.. include needs to be at bottom
.. include <common_footer.rst>
```
