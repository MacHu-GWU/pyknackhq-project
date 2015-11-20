#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyknackhq import KnackhqAuth, KnackhqClient, Application, dtype
from pyknackhq import AddressType
from pyknackhq.tests import AUTH_JSON_PATH, SCHEMA_JSON_PATH

"Example 1, put credential in script::"
# from pyknackhq import KnackhqAuth, KnackhqClient
#   
# client = KnackhqClient(
#     auth=KnackhqAuth(
#         application_id="56325e4a5839b2486913f542",
#         api_key="b32f8cb0-7e66-11e5-8bf6-d9d03ae276fc",
#     ),
# )
# print(client)

"Example 2, put your credential in a json file:"
# from pyknackhq import KnackhqAuth, KnackhqClient
# 
# client = KnackhqClient(auth=KnackhqAuth.from_json("auth.json"))
# print(client) 

"Print all object name"
client = KnackhqClient(auth=KnackhqAuth.from_json(AUTH_JSON_PATH),
                       application=Application.from_json(SCHEMA_JSON_PATH),)
# print(client.all_object_name)

"Get Collection instance"
test_object = client.get_collection("test_object")
# print(test_object)

"Print all field name"
# print(test_object.all_field_name)

"Get Field instance"
# short_text_field = test_object.get_field("short text field")
# print(short_text_field)

"Insert one record"
from pprint import pprint
# 
# record = {
#     "short text field": "Hello World",
#     "paragraph text field": "This is a paragraph text",
#     "yes no field": True,
#     "multiple choice field": ["First Choice", "Second Choice"],
# }
# res = test_object.insert_one(record)
# pprint(res)

"Insert many record"
# records = [
#     {"short text field": "a"},
#     {"short text field": "b"},
# ]
# test_object.insert(records)

"Find one record"
# record = test_object.find_one(id_="564020bd465539a51dede83f")
# pprint(record)

"Find all records"
# for record in test_object.find():
#     print(1)

"data type constructor"
# record = {"email field": EmailType(email="example@gmail.com")}
# test_object.insert(record)