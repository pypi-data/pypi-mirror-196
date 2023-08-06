# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
from pathlib import Path
from typing import TypeVar

root = Path(__file__).parents[2]
sys.path.append(str(root))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cincodex'
copyright = '2023, Adam Meily'
author = 'Adam Meily'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_class_signature = 'separated'

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
typehints_defaults = 'braces-after'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


def typehints_formatter(annotation, _):
    if isinstance(annotation, TypeVar):
        return f':class:`{annotation.__name__}`'

    return None
