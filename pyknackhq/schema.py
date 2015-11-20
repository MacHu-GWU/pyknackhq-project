#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from pyknackhq.js import load_js, safe_dump_js, js2str, prt_js
from collections import OrderedDict
        
class Field(object):
    """Field of object class.
    
    Fields are used to define specific attributes of an object.
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)
            
    def __str__(self):
        return "Field('%s')" % self.name
    
    def __repr__(self):
        return ("Field(key='%s', name='%s', type='%s', "
                "required=%s, unique=%s)") % (
                self.key, self.name, self.type, self.required, self.unique)
    
    @staticmethod
    def from_dict(d):
        return Field(**d)
    
    @staticmethod
    def from_json(abspath):
        return Field.from_dict(load_js(abspath, enable_verbose=False))

class Object(object):
    """Data object class.
    
    Object are used to define an abstract concept of thing. For example, an
    employee can be an object having attributes: name, date of birth, phone,
    email, etc...
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)
            
        self.f = OrderedDict() # {field_key: Field instance}
        self.f_name = OrderedDict() # {field_name: Field instance}
        for d in self.fields:
            field = Field.from_dict(d)
            self.f.setdefault(d["key"], field)
            self.f_name.setdefault(d["name"], field)
            
    def __str__(self):
        return "Object('%s')" % self.name
                
    def __repr__(self):
        return "Object(key='%s', name='%s')" % (self.key, self.name)

    @staticmethod
    def from_dict(d):
        return Object(**d)
    
    @staticmethod
    def from_json(abspath):
        return Object.from_dict(load_js(abspath, enable_verbose=False))
    
    def __iter__(self):
        return iter(self.f.values())
    
    @property
    def all_field_key(self):
        """Return all available field_key.
        """
        return [f.key for f in self.f.values()]
    
    @property
    def all_field_name(self):
        """Return all available field_name.
        """
        return [f.name for f in self.f.values()]
    
    def get_field_key(self, key, using_name=True):
        """Given a field key or name, return it's field key.
        """
        try:
            if using_name:
                return self.f_name[key].key
            else:
                return self.f[key].key
        except KeyError:
            raise ValueError("'%s' are not found!" % key)

    def get_field(self, key, using_name=True):
        """Given a field key or name, return the Field instance.
        """
        try:
            if using_name:
                return self.f_name[key]
            else:
                return self.f[key]
        except KeyError:
            raise ValueError("'%s' are not found!" % key)

class Application(object):
    """Application class that holding object and its fields information.
    """
    def __init__(self, **kwargs):
        self.data = {"application": kwargs}
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)
            
        self.o = OrderedDict() # {field_key: Field instance}
        self.o_name = OrderedDict() # {field_name: Field instance}
        for d in self.objects:
            object_ = Object.from_dict(d)
            self.o.setdefault(d["key"], object_)
            self.o_name.setdefault(d["name"], object_)
            
    def __str__(self):
        return "Application('%s')" % self.name
                
    def __repr__(self):
        return "Application('%s')" % self.name

    @staticmethod
    def from_dict(d):
        return Application(**d["application"])
    
    @staticmethod
    def from_json(abspath):
        return Application.from_dict(load_js(abspath, enable_verbose=False))
    
    def to_json(self, abspath):
        safe_dump_js(self.data, abspath, enable_verbose=False)
        
    def __iter__(self):
        return iter(self.o.values())
    
    @property
    def all_object_key(self):
        """Return all available object_key.
        """
        return [o.key for o in self.o.values()]
    
    @property
    def all_object_name(self):
        """Return all available object_name.
        """
        return [o.name for o in self.o.values()]
    
    def get_object_key(self, key, using_name=True):
        """Given a object key or name, return it's object key.
        """
        try:
            if using_name:
                return self.o_name[key].key
            else:
                return self.o[key].key
        except KeyError:
            raise ValueError("'%s' are not found!" % key)

    def get_object(self, key, using_name=True):
        """Given a object key or name, return the Object instance.
        """
        try:
            if using_name:
                return self.o_name[key]
            else:
                return self.o[key]
        except KeyError:
            raise ValueError("'%s' are not found!" % key)
    
if __name__ == "__main__":
    from pyknackhq.tests import AUTH_JSON_PATH, SCHEMA_JSON_PATH
    from pprint import pprint as ppt
    import unittest
    
    class FieldUnittest(unittest.TestCase):
        def test_from_dict(self):
            d = load_js(SCHEMA_JSON_PATH, enable_verbose=False)
            for object_dict in d["application"]["objects"]:
                for field_dict in object_dict["fields"]:
                    field = Field.from_dict(field_dict)
                    
    class ObjectUnittest(unittest.TestCase):
        def test_from_dict(self):
            d = load_js(SCHEMA_JSON_PATH, enable_verbose=False)
            for object_dict in d["application"]["objects"]:
                object_ = Object.from_dict(object_dict)
                
    class ApplicationUnittest(unittest.TestCase):
        def test_from_dict(self):
            d = load_js(SCHEMA_JSON_PATH, enable_verbose=False)
            application = Application.from_dict(d)
        
        def test_from_json(self):
            application = Application.from_json(SCHEMA_JSON_PATH)
        
        def test_to_json(self):
            application = Application.from_json(SCHEMA_JSON_PATH)
            application.to_json("schema.json")
            
        def test_all(self):
            d = load_js(SCHEMA_JSON_PATH, enable_verbose=False)
            application = Application.from_dict(d)
            print(application.all_object_key)
            print(application.all_object_name)
            
            test_object = application.get_object("test_object")
            print(test_object.all_field_key)
            print(test_object.all_field_name)
            
            short_text_field = test_object.get_field("short text field")

    unittest.main()