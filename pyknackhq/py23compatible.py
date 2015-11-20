#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Import Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from pyknackhq.py23compatible import ( 
    _str_type, _int_types, _number_types, is_py3)
"""

import sys

if sys.version_info[0] == 3:
    _str_type = str
    _int_types = (int,)
    _number_types = (int, float)
    is_py3 = True
else:
    _str_type = basestring
    _int_types = (int, long)
    _number_types = (int, long, float)
    is_py3 = False