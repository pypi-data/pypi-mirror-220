#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
It is aimed to get rid of repetitive lines of code by integrating tools
that use multiple APIs for FastApi and facilitate repetitive operations.

Details will be shared at
https://www.ibrahimcorut.com/tr/projects/pypi-corut_fastapi_tools.
"""

import importlib_metadata as _importlib_metadata
from ._content_types import ALL_TYPES, get_special_content_types
from ._content_types import APPS, FONTS, IMAGES, SOUNDS, TEXTS, VIDEOS

__all__ = (
    '__author__',
    '__copyright__',
    '__email__',
    '__license__',
    '__summary__',
    '__title__',
    '__uri__',
    '__version__',

    'ALL_TYPES',
    'APPS',
    'FONTS',
    'IMAGES',
    'SOUNDS',
    'TEXTS',
    'VIDEOS',
    'get_special_content_types',
)

__copyright__ = 'Copyright 2023 ibrahim CÖRÜT'
metadata = _importlib_metadata.metadata('corut_fastapi_tools')
__title__ = metadata['name']
__summary__ = metadata['summary']
__uri__ = metadata['home-page']
__version__ = metadata['version']
__author__ = metadata['author']
__email__ = metadata['author-email']
__license__ = metadata['license']
