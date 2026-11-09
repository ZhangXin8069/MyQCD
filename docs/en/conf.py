# Sphinx configuration for the English myqcd documentation.
# This file must not import myqcd: the docs build has no runtime dependency
# on the package or on SymPy.

project = "myqcd"
author = "ZhangXin8069"
copyright = "2026, ZhangXin8069"

extensions = ["myst_parser", "sphinx.ext.mathjax"]
myst_enable_extensions = ["dollarmath", "amsmath"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
exclude_patterns = ["_build"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
