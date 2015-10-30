#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reference: http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#about
"""

from __future__ import print_function
from pprint import pprint as ppt
from collections import OrderedDict
import requests
import json

__version__ = "0.0.1"
__short_description__ = "A minimal knackhq API Python wrapper."

class Auth(object):
    """Knackhq API authentication class.
    """
    def __init__(self, application_id, api_key=None):
        self.application_id = application_id
        if api_key:
            print("Using root access. For more information, visit: "
                  "http://helpdesk.knackhq.com/support/solutions/articles/"
                  "5000444173-working-with-the-api#levels")
            self.api_key = api_key
        else:
            print("Using page access. For more information, visit: "
                  "http://helpdesk.knackhq.com/support/solutions/articles/"
                  "5000444173-working-with-the-api#levels")
            self.api_key = "knack"
        self.headers = {
            "X-Knack-Application-Id": self.application_id,
            "X-Knack-REST-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        
    @staticmethod
    def from_json(abspath):
        """Read authentication info from json file.
        """
        with open(abspath, "rb") as f:
            data = json.loads(f.read().decode("utf-8"))
        auth = Auth(application_id=data["application_id"], 
                    api_key=data.get("api_key"))
        return auth
    
    def __str__(self):
        return "application_id = '%s', api_key = '%s'" % (
            self.application_id, self.api_key)

class Field(object):
    """Field of object class.
    """
    def __init__(self, _id, name, dtype, required):
        self._id = _id
        self.name = name
        self.dtype = dtype
        self.required = required 

    def __repr__(self):
        return "Field(_id='%s', name='%s', dtype='%s', required=%s)" % (
            self._id, self.name, self.dtype, self.required)
    
class Object(object):
    """Data object class.
    """
    def __init__(self, _id, name, *args):
        self._id = _id
        self.name = name
        self.f = OrderedDict() # {field_id: Field instance}
        self.f_name = OrderedDict() # {field_name: Field instance}
        for field in args:
            self.f[field._id] = field
            self.f_name[field.name] = field
    
    @property
    def all_field_id(self):
        """Return all field_id.
        """
        return list(self.f)
    
    @property
    def all_field_name(self):
        """Return all field name
        """
        return [f.name for f in self.f.values()]
    
    def __repr__(self):
        return "Object(_id='%s', name='%s')" % (self._id, self.name)
    
    def get_field_id(self, field_name):
        """Given a field name, return it's field_id.
        """
        try:
            return self.f_name[field_name]._id
        except KeyError:
            raise ValueError("'%s' are not found!" % field_name)

    def get_field(self, field_name):
        """Given a field name, return the Field instance.
        """
        try:
            return self.f_name[field_name]
        except KeyError:
            raise ValueError("'%s' are not found!" % field_name)

class Schema(object):
    """Schema class that holding object and its fields information.
    """
    def __init__(self, *args):
        self.o = OrderedDict() # {object_id: Object instance}
        self.o_name = OrderedDict() # {object_name: Object instance}
        for object_ in args:
            self.o[object_._id] = object_
            self.o_name[object_.name] = object_
            
    @property
    def all_object_id(self):
        """Return all object_id.
        """
        return list(self.o)

    @property
    def all_object_name(self):
        """Return all object name.
        """
        return list(self.o_name)

    def get_object_id(self, object_name):
        """Given an object name, return it's object_id.
        """
        try:
            return self.o_name[object_name]._id
        except KeyError:
            raise ValueError("'%s' are not found!" % object_name)
    
    def get_object(self, object_name):
        """Given an object name, return the Object instance.
        """
        try:
            return self.o_name[object_name]
        except KeyError:
            raise ValueError("'%s' are not found!" % object_name)
    
class Client(object):
    """Knackhq API client class.
    """
    def __init__(self, auth, read_schema=True):
        self.auth = auth
        if read_schema:
            self.get_schema()
        
    def _get(self, url, params=dict()):
        """
        """
        try:
            res = requests.get(url, headers=self.auth.headers, params=params)
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
    
    def _post(self, url, data):
        """
        """
        try:
            res = requests.post(
                url, headers=self.auth.headers, data=json.dumps(data))
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"

    def _put(self, url, data):
        """
        """
        try:
            res = requests.put(
                url, headers=self.auth.headers, data=json.dumps(data))
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
    
    def _delete(self, url):
        """
        """
        try:
            res = requests.delete(url, headers=self.auth.headers)
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
        
    def get_schema(self):
        """Get object, field, field type schema information.
        """
        object_list = list()
        
        url = "https://api.knackhq.com/v1/objects"    
        data = self._get(url)
        for d in data["objects"]:
            object_id, object_name = d["key"], d["name"]
            
            field_list = list()
            
            url = "https://api.knackhq.com/v1/objects/%s/fields" % object_id
            data = self._get(url)
            for d in data["fields"]:
                field = Field(_id=d["key"], name=d["label"], 
                                dtype=d["type"], required=d["required"])
                field_list.append(field)
                object_ = Object(object_id, object_name, *field_list)
            
            object_list.append(object_)
            
        self.schema = Schema(*object_list)
    
    def convert_data(self, object_name, data):
        """{"field_name": value} => {"field_id": value}
        """
        object_ = self.schema.get_object(object_name)
        new_data = dict()
        for key, value in data.items():
            new_data[object_.get_field_id(key)] = value
        return new_data
    
    def recover_data(self, object_name, data):
        """{"field_id": value} => {"field_name": value}
        """
        object_ = self.schema.get_object(object_name)
        
    # CRUD method
    def insert_one(self, object_id, data, using_name=True):
        """Create
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#create
        """
        if using_name:            
            data = self.convert_data(object_id, data)
            object_id = self.schema.get_object_id(object_id)
            
        url = "https://api.knackhq.com/v1/objects/%s/records" % object_id
        res = self._post(url, data)
        return res

    def select_one(self, object_id, _id, using_name=True):
        """Read one record
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#retrieve
        """
        if using_name:
            object_id = self.schema.get_object_id(object_id)
            
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (object_id, _id)
        res = self._get(url)
        return res
    
    def select_all(self, object_id, using_name=True):
        """Read all records
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#retrieve
        """
        if using_name:
            object_id = self.schema.get_object_id(object_id)
            
        url = "https://api.knackhq.com/v1/objects/%s/records" % object_id
        res = self._get(url)
        return res
    
    def update_one(self, object_id, _id, data, using_name=True):
        """Update one record. Any fields you don't specify will remain unchanged.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#update
        """
        if using_name:
            data = self.convert_data(object_id, data)
            object_id = self.schema.get_object_id(object_id)
            
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (object_id, _id)
        res = self._put(url, data)
        return res
    
    def delete_one(self, object_id, _id, using_name=True):
        """Delete one record.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#delete
        """
        if using_name:
            object_id = self.schema.get_object_id(object_id)
        
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (object_id, _id)
        res = self._delete(url)
        return res
    
if __name__ == "__main__":
    import unittest

    class CreateUnittest(unittest.TestCase):
        def setUp(self):
            self.client = Client(auth=Auth.from_json("auth.json"))

        def test_schema(self):
            schema = self.client.schema
            print(schema.all_object_id)
            print(schema.all_object_name)
             
            object_test_id = schema.get_object_id("text_type")
            object_special_id = schema.get_object_id("special")
            print(object_test_id)
            print(object_special_id)
             
            object_test = schema.get_object("text_type")
            object_special = schema.get_object("special")
            print(object_test)
            print(object_special)
              
            print(object_test.all_field_id)
            print(object_test.all_field_name)
            print(object_special.all_field_id)
            print(object_special.all_field_name)
         
        def test_create(self):
            res = self.client.insert_one(
                object_id="text_type", 
                data={
                    "test_id": "ID-0001",
                    "short_text": "Hello World",
                    "paragraph_text": "A very long paragraph",
                    "rich_text": "<strong>Emphasized Text</strong>",
                    "name": {
                        "title": "Mr.",
                        "first": "James",
                        "middle": "F",
                        "last": "Bonder",
                    },
                    "address": {
                        "street":"123 Street",
                        "street2":"Apt 456",
                        "city":"New York",
                        "state":"NY",
                        "zip":"10023",
                    },
                    "email": {
                        "email": "example@gmail.com",
                    },
                    "link": {
                        "url": "www.google.com",
                    }
                },
                using_name=True,
            )
            ppt(res)
         
        def test_select_one(self):
            res = self.client.select_one(
                "text_type", _id="5632caf696aca78b43ea7c47", using_name=True)
            ppt(res)
             
            res = self.client.select_one(
                "object_1", _id="5632caf696aca78b43ea7c47", using_name=False)
            ppt(res)
             
        def test_select_all(self):
            res = self.client.select_all("text_type", using_name=True)
            ppt(res)
                
            res = self.client.select_all("object_1", using_name=False)
            ppt(res)
             
        def test_update_one(self):
            res = self.client.update_one(
                "text_type", _id="5632caf696aca78b43ea7c47", 
                data={"short_text": "Updated Short Text"}, using_name=True)
            ppt(res)

        def test_delete_one(self):
            res = self.client.delete_one("text_type", _id="5632caf696aca78b43ea7c47")
            ppt(res)
            
    unittest.main()