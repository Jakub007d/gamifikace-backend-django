import os
import sys
import django


sys.path.insert(0, os.path.abspath('..'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamifikace.settings')

# Inicializácia Django
django.setup()

# -- Project information -----------------------------------------------------

project = 'Gamifikace'
copyright = '2025'
author = 'Tvoje meno'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
