#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Sanic-Auth documentation build configuration file
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, PROJECT_DIR)
import sanic_auth  # noqa

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'

master_doc = 'index'

project = 'Sanic-Auth'
copyright = '2017-2020, Philip Xu'
author = 'Philip Xu and contributors'

release = sanic_auth.__version__
version = release.rsplit('.', 1)[0]

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = 'alabaster'

html_theme_options = {
    'github_banner': True,
    'github_repo': 'sanic-auth',
    'github_user': 'pyx',
}

htmlhelp_basename = 'Sanic-Authdoc'

latex_documents = [
    (master_doc, 'Sanic-Auth.tex', 'Sanic-Auth Documentation',
     'Philip Xu and contributors', 'manual'),
]


man_pages = [
    (master_doc, 'sanic-auth', 'Sanic-Auth Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'Sanic-Auth', 'Sanic-Auth Documentation',
     author, 'Sanic-Auth', 'One line description of project.',
     'Miscellaneous'),
]
