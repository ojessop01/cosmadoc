# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'cosma'
copyright = '2026, COSMA'
author = 'cosma-support'

#COSMA version (COSMA8), update number (i.e. 0=2020, 1=2021, 2=2023), current year,month.
release = '8.2'
version = '8.2.2611'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    "sphinx.ext.githubpages",
    "sphinx_rtd_theme",
    'myst_parser',
]

#myst_enable_extensions=[
#    'attrs_inline'
#]


intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# Templates for writing new pages, not pages themselves
exclude_patterns = ['templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_logo = 'images/logo.png'
html_favicon = 'images/logocosmablack.ico'
html_theme_options = {
    'logo_only': True
}

# -- Options for EPUB output
epub_show_urls = 'footnote'

html_context = {
    'display_github': True,
    'github_user': 'agb32',
    'github_repo': 'cosmadoc',
    'github_version': 'main/docs/',
    'conf_py_path': '/source/', 
}
