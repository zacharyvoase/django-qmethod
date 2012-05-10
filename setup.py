#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from distutils.core import setup


rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def read_from(filename):
    fp = open(filename)
    try:
        return fp.read()
    finally:
        fp.close()

def get_version():
    data = read_from(rel_file('djqmethod.py'))
    return re.search(r"__version__ = '([^']+)'", data).group(1)


setup(
    name             = 'django-qmethod',
    version          = get_version(),
    author           = "Zachary Voase",
    author_email     = 'z@zacharyvoase.com',
    url              = 'http://github.com/zacharyvoase/django-qmethod',
    description      = "Define methods on QuerySets without custom manager and QuerySet subclasses.",
    py_modules       = ['djqmethod'],
)
