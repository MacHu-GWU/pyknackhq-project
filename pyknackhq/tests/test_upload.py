#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyknackhq.tests import (AUTH_JSON_PATH, SCHEMA_JSON_PATH, 
    read_binary, write_binary)
from pyknackhq.client import KnackhqAuth, KnackhqClient
from pyknackhq.schema import Application
from pprint import pprint as ppt
import requests
import json
import os

auth = KnackhqAuth.from_json(AUTH_JSON_PATH)
application = Application.from_json(SCHEMA_JSON_PATH)
client = KnackhqClient(auth=auth, application=application)

upload_url = "https://api.knackhq.com/v1/applications/%s/assets/file/upload" % auth.application_id
abspath = os.path.abspath("__init__.py")