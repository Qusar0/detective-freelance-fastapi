# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys


sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../server'))
sys.path.insert(0, os.path.abspath('../../server/api'))
sys.path.insert(0, os.path.abspath('../../server/api/routers'))
sys.path.insert(0, os.path.abspath('../../server/api/dao'))
sys.path.insert(0, os.path.abspath('../../server/api/schemas'))
sys.path.insert(0, os.path.abspath('../../server/api/services'))
sys.path.insert(0, os.path.abspath('../../server/tasks'))
sys.path.insert(0, os.path.abspath('../../server/bots'))

project = 'Detective Freelance FastAPI'
copyright = '2025, Artyom Kovalev'
author = 'Artyom Kovalev'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

autosummary_generate = True
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
