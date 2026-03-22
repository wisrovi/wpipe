import os
import sys

sys.path.insert(0, os.path.abspath("."))

project = "wpipe"
copyright = "2024-2026, William Steve Rodriguez Villamizar"
author = "William Steve Rodriguez Villamizar"
version = "1.0.0"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.graphviz",
    "sphinx_design",
    "sphinx_copybutton",
    "myst_parser",
    "sphinx.ext.imgconverter",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_css_files = ["css/custom.css"]

html_context = {
    "github_user": "wisrovi",
    "github_repo": "wpipe",
    "github_version": "main",
    "doc_path": ".",
}

html_theme_options = {
    "github_url": "https://github.com/wisrovi/wpipe",
    "show_toc_level": 2,
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "footer_start": ["copyright", "sphinx-version"],
    "footer_end": [],
}

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}

autodoc_typehints = "description"
autodoc_member_order = "bysource"

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

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

graphviz_output_format = "svg"

copybutton_prompt_text = r">>> |\.\.\. |\$ |In |\Out "
copybutton_prompt_is_regexp = True
copybutton_copy_empty_lines = False
copybutton_here_doc_delimiter = "<<<<"

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "fieldlist",
    "吹_table",
]

myst_heading_anchors = 3

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"
