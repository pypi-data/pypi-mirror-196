from tkgen import __version__

project = 'tkgen'
copyright = '2023, Théo Cavignac'
author = 'Théo Cavignac'
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
    "pyskema": ("https://pyskema.readthedocs.io/en/latest/", None),
}

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
