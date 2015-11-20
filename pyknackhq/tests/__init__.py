#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Import Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from pyknackhq.tests import (AUTH_JSON_PATH, SCHEMA_JSON_PATH, 
    read_binary, write_binary)
"""

from __future__ import print_function
import site
import os

AUTH_JSON_PATH = os.path.join(site.getsitepackages()[1], 
    "pyknackhq", "tests", "auth.json")
SCHEMA_JSON_PATH = os.path.join(site.getsitepackages()[1], 
    "pyknackhq", "tests", "schema.json")

def read_binary(abspath):
    with open(abspath, "rb") as f:
        return f.read()
    
def write_binary(binary, abspath):
    with open(abspath, "wb") as f:
        return f.write(binary)
    
if __name__ == "__main__":
    print(AUTH_FILE)
    print(SCHEMA_FILE)
    prt_js({"a": 1, "b": 2})