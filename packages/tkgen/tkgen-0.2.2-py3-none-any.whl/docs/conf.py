from tkgen import __version__

project = 'tkgen'
copyright = '2023, Théo Cavignac'
author = 'Théo Cavignac'
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



html_theme = 'alabaster'
html_static_path = ['_static']
