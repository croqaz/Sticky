#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/kennethreitz/setup.py ❤️ ✨ 🍰 ✨

import os
from setuptools import setup

NAME = 'sticky'
DESCRIPTION = 'Library for adding "sticky" comment headers inside Python source code files.'
KEYWORDS = 'sticky header comment'
URL = 'https://github.com/ShinyTrinkets/Sticky'
AUTHOR = 'Cristi Constantin'
EMAIL = 'cristi.constantin@live.com'

here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    version = about['__version__'],
    name = NAME,
    description = DESCRIPTION,
    keywords = KEYWORDS,
    url = URL,
    author = AUTHOR,
    author_email = EMAIL,
    license = 'MIT',
    packages = ['sticky', 'tests'],
    include_package_data = True,
    zip_safe = True,
    python_requires = '>= 3.5',
    extras_require = {
        'dev': ['flake8', 'codecov'],
        'test': ['pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'sticky=sticky.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)
