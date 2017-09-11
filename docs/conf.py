# -*- coding: utf-8 -*-


import sys
import os
import shlex


sys.path.insert(0, os.path.abspath(".."))
import order as od


project = "order"
author = od.__author__
copyright = od.__copyright__
version = od.__version__
release = od.__version__


templates_path = ["_templates"]
html_static_path = ["_static"]
master_doc = "index"
source_suffix = ".rst"


exclude_patterns = []
pygments_style = "sphinx"
html_logo = "../logo.png"
html_theme = "alabaster"
html_sidebars = {"**": [
    "about.html",
    "localtoc.html",
    "searchbox.html"]
}
html_theme_options = {
    "github_user": "riga",
    "github_repo": "order",
    "travis_button": True
}


extensions = [
    "sphinx.ext.autodoc"
]