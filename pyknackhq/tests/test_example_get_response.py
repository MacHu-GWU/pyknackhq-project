from pyknackhq import KnackhqAuth, KnackhqClient, Application
from pyknackhq.tests import AUTH_JSON_PATH, SCHEMA_JSON_PATH
from pyknackhq.js import prt_js

client = KnackhqClient(KnackhqAuth.from_json(AUTH_JSON_PATH),
                       Application.from_json(SCHEMA_JSON_PATH),)

collection = client.get_collection("test_object")
prt_js(collection.find(raw=False)[0])
prt_js(collection.find(raw=True)[0])