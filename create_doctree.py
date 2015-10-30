#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from docfly import Docfly
import os

try:
    os.remove(r"source\pyknackhq")
except Exception as e:
    print(e)

docfly = Docfly("pyknackhq", dst="source")
docfly.fly()