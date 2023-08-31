# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Setup root --------------------------------------------------------------
import os
import sys

# import sphinx_pdj_theme

root = os.path.abspath('../..')
sys.path.insert(0, root)

# -- Project information -----------------------------------------------------
project = 'sitecheck'
copyright = u''
author = 'Dan Edens'
release = u''
master_doc = 'index'
todo_include_todos = False

pygments_style = 'sphinx'

# -- General configuration ---------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage',
              'sphinx.ext.napoleon']

source_suffix = {'.rst': 'restructuredtext'}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['build/*']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'
# html_theme = 'sphinx_pdj_theme'

# html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]

html_static_path = []

html_show_sourcelink = False

html_show_sphinx = False

html_show_copyright = False

htmlhelp_basename = 'Sitecheck Scanner'
