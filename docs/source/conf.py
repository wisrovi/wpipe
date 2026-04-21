"""
Sphinx configuration for wpipe documentation.

This file configures Sphinx to generate professional documentation
with a modern design and extensive features.
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath("../.."))

project = "wpipe"
copyright = f"2024-{datetime.now().year}, William Steve Rodriguez Villamizar"
author = "William Steve Rodriguez Villamizar"
author_url = "https://github.com/wisrovi"
version = "1.6.15"
release = "1.6.15"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.graphviz",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.pyc",
    "**.pyo",
    "**.pyd",
    ".Python",
    "*.tmp",
    "*.bak",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"
language = "en"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_title = "wpipe Documentation"
html_short_title = "wpipe"
html_description = (
    "wpipe - Python Library for Sequential Data Processing Pipelines. "
    "Task orchestration, API integration, and execution tracking."
)
html_last_updated = datetime.now().strftime("%B %d, %Y")
html_copy_source = True
html_show_sourcelink = True
html_use_index = True
html_split_index = False
html_show_navigation = True
html_show_copyright = True
html_output_encoding = "utf-8"

html_css_files = [
    "css/custom.css",
]

html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
    "allow_authors": True,
    "roadmap": False,
    "navigation_with_keys": True,
    "flyout_display": "hidden",
}

html_scaled_image_link = False
html_permalinks_icon = "¶"
html_math_renderer = "mathjax"

html_context = {
    "display_github": True,
    "github_user": "wisrovi",
    "github_repo": "wpipe",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
    "source_suffix": ".rst",
    "use_edit_page": True,
    "github_url": "https://github.com/wisrovi/wpipe",
}

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "show-inheritance": True,
    "exclude-members": "__weakref__",
    "inherited-members": False,
    "private-members": "_",
}

autodoc_typehints = "description"
autodoc_member_order = "bysource"
autodoc_docstring_signature = True

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "numpy": ("https://numpy.org/devdocs/", None),
}

intersphinx_disabled_reftypes = [
    "std:doc",
]

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Helvetica",
    "-Nfontname=Helvetica",
    "-Efontname=Helvetica",
    "-Grankdir=LR",
]

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[.*\]: |Out \[.*\]: "
copybutton_prompt_is_regexp = True
copybutton_copy_empty_lines = False
copybutton_nesting_indent = False
copybutton_known_references = ["# In\\[.*\\]:", "# Out\\[.*\\]:"]
copybutton_gt_label = "Output"
copybutton_remove_prompts = False

todo_include_todos = True
todo_emit_warnings = True

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "strikethrough",
    "amsmath",
]

myst_heading_anchors = 3
myst_html_math_renderer = "mathjax"
myst_enable_checkboxes = True

suppress_warnings = [
    "myst.xref_missing",
    "autosectionlabel.*",
    "image.not_readable",
    "ref.python",
]

numfig = True
numfig_format = {
    "figure": "Figure %s",
    "table": "Table %s",
    "code-block": "Listing %s",
}

add_function_parentheses = True

rst_prolog = """
.. |wpipe| replace:: **wpipe**
.. |version| replace:: 2.0.0-LTS
.. |date| replace:: {date}
""".format(date=datetime.now().strftime("%B %d, %Y"))

rst_epilog = """
.. |author| replace:: William Steve Rodriguez Villamizar
.. |github| replace:: https://github.com/wisrovi/wpipe
"""

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 3
