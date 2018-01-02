# -*- coding: utf-8 -*-
#
#   Copyright © 2017 rsiddharth <s@rickteyspace.net>.
#
#    This file is part of markdown-textwrap.
#
#   markdown-textwrap is free software: you can redistribute it
#   and/or modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation, either version 3 of
#   the License, or (at your option) any later version.
#
#   markdown-textwrap is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#   See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with markdown-textwrap (see COPYING).  If not, see
#   <http://www.gnu.org/licenses/>.

"""
markdown-textwrap setup.
"""


from setuptools import setup, find_packages
from codecs import open
from os import path


from markdown_textwrap._version import __version__


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

config = {
    'name': 'markdown-textwrap',
    'version': __version__,
    'description': 'Texwrap Markdown Documents',
    'long_description': long_description,
    'platforms': 'GNU/Linux',
    'url': 'https://git.ricketyspace.net/markdown-textwrap',
    'author': 'rsiddharth',
    'author_email': 's@ricketyspace.net',
    'license': 'GNU General Public License version 3 or later',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: ' +
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Documentation',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
    ],
    'keywords': 'markdown text wrap textwrap',
    'py_modules': ['md_tw'],
    'packages': ['markdown_textwrap'],
    'install_requires': ['mistune==0.8.3'],
    'entry_points': {
        'console_scripts': ['md-tw = md_tw:main']
    }
}
setup(**config)
