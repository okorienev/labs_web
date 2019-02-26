# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('../'))
print(os.path.abspath('../'))


project = 'labs_web'
copyright = '2019, Oleksandr Korienev'
author = 'Oleksandr Korienev'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = None

html_theme = 'alabaster'

html_static_path = ['_static']

htmlhelp_basename = 'labs_webdoc'


latex_elements = {
}

latex_documents = [
    (master_doc, 'labs_web.tex', 'labs\\_web Documentation',
     'Oleksandr Korienev', 'manual'),
]

man_pages = [
    (master_doc, 'labs_web', 'labs_web Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'labs_web', 'labs_web Documentation',
     author, 'labs_web', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project

epub_exclude_files = ['search.html']

