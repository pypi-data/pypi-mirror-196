# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
sys.path.append("../..")
from perennial import __version__

project = 'Perennial 🌱'
copyright = '2023, Madison Landry'
author = 'Madison Landry'
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
   "sphinx.ext.autodoc",
   "sphinx.ext.napoleon",
   "sphinx.ext.intersphinx",
   "sphinxcontrib_trio",
   "sphinx_autodoc_typehints",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = []

default_role = "py:obj"

