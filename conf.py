"""
Sphinx configuration for wpipe documentation.
Professional documentation with modern design and features.
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath("."))

# -- Project Information -----------------------------------------------------
project = "wpipe"
copyright = f"{datetime.now().year}, William Steve Rodriguez Villamizar"
author = "William Steve Rodriguez Villamizar"
author_url = "https://github.com/wisrovi"
release = "1.0.0"
version = "1.0.0"

# -- General Configuration ---------------------------------------------------
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "_inc",
    "*.pyc",
    "*.tmp",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"
language = "en"

# -- Extensions Configuration ------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.graphviz",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
]

# -- Autodoc Configuration ---------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "show-inheritance": True,
    "exclude-members": "__weakref__",
    "inherited-members": True,
}

autodoc_typehints = "description"
autodoc_member_order = "bysource"

# -- Napoleon (Google/NumPy Style) -------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# -- Intersphinx Configuration -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# -- Viewcode Configuration --------------------------------------------------
viewcode_follow_imported_members = True

# -- Copybutton Configuration ------------------------------------------------
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[.*\]: |Out \[.*\]: "
copybutton_copy_empty_lines = False
copybutton_nesting_indent = False
copybutton_known_references = ["# In\\[.*\\]:", "# Out\\[.*\\]:"]
copybutton_gt_label = "Output"

# -- Graphviz Configuration -------------------------------------------------
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Helvetica",
    "-Nfontname=Helvetica",
    "-Efontname=Helvetica",
]

# -- HTML Output Configuration ----------------------------------------------
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "include_boostrap": True,
    "boostrap_version": "3",
}

html_title = "wpipe Documentation"
html_short_title = "wpipe"
html_description = "Python Pipeline Library for Sequential Data Processing - Task orchestration, API integration, and execution tracking"
html_last_updated = datetime.now().strftime("%B %d, %Y")

html_context = {
    "display_github": True,
    "github_user": "wisrovi",
    "github_repo": "wpipe",
    "github_version": "main",
    "conf_py_path": "/",
    "source_suffix": ".rst",
    "use_edit_page": True,
    "github_url": "https://github.com/wisrovi/wpipe",
}

html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

# -- Favicon -----------------------------------------------------------------
html_favicon = "_static/favicon.ico"

# -- Additional files --------------------------------------------------------
html_extra_path = ["_extra"]

# -- Templates --------------------------------------------------------------
templates_path = ["_templates"]

# -- Suppress Warnings -----------------------------------------------------
suppress_warnings = [
    "myst.xref_missing",
    "autosectionlabel.*",
    "image.not_readable",
]

# -- Extensions Settings ----------------------------------------------------
myst_heading_anchors = 3
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]

myst_substitutions = {
    "project": "wpipe",
    "version": "1.0.0",
    "author": "William Steve Rodriguez Villamizar",
    "year": datetime.now().year,
}
