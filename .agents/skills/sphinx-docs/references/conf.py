"""
Sphinx Configuration for Project Documentation

Copy this file to: docs/source/conf.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "Project Name"
copyright = "2024, wisrovi"
author = "wisrovi"
version = "1.0"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "myst_parser",
    "sphinx.ext.todo",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "navigation_depth": 4,
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

pygments_style = "sphinx"

html_use_index = True
html_split_index = False
html_copy_source = True

html_show_sourcelink = True
html_sourcelink_suffix = ".txt"

html_add_permalinks = "¶"
