#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The official knackhq API documentation:
http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#about
"""

from __future__ import print_function
from pprint import pprint as ppt
from collections import OrderedDict
import requests
import json

__version__ = "0.0.1"
__short_description__ = "knackhq root access Python API."

class Auth(object):
    """Knackhq API authentication class.
    
    :param application_id: str type, Application ID
    :param api_key: str type, API Key
    
    To get your Application ID and API Key, read this tutorial:
    http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#key
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

    def __str__(self):
        if self.api_key == "knack":
            access = "page"
        else:
            access = "root"  
            
        return "application_id = '%s', using %s access" % (
            self.application_id, access)
         
    @staticmethod
    def from_json(abspath):
        """Read authentication information from a ``.json`` file.
        
        The ``.json`` file looks like::
        
            {"application_id": "your Application ID", "api_key": "your API Key"}
        """
        with open(abspath, "rb") as f:
            data = json.loads(f.read().decode("utf-8"))
        auth = Auth(application_id=data["application_id"], 
                    api_key=data.get("api_key"))
        return auth

    def get(self, url, params=dict()):
        """Http get method wrapper.
        """
        try:
            res = requests.get(url, headers=self.headers, params=params)
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
    
    def post(self, url, data):
        """Http post method wrapper.
        """
        try:
            res = requests.post(
                url, headers=self.headers, data=json.dumps(data))
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
    
    def put(self, url, data):
        """Http put method wrapper.
        """
        try:
            res = requests.put(
                url, headers=self.headers, data=json.dumps(data))
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
    
    def delete(self, url):
        """Http delete method wrapper.
        """
        try:
            res = requests.delete(url, headers=self.headers)
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"


class Field(object):
    """Field of object class.
    
    Fields are used to define specific attributes of and object.
    
    :param key: str type, object_key
    :param name: str type, object_name
    :param dtype: str type, data type name
    :param required: boolean type, if true, then this field is not nullable
    """
    def __init__(self, key, name, dtype, required):
        self.key = key
        self.name = name
        self.dtype = dtype
        self.required = required 

    def __repr__(self):
        return "Field(key='%s', name='%s', dtype='%s', required=%s)" % (
            self.key, self.name, self.dtype, self.required)


class Object(object):
    """Data object class.
    
    Object are used to define an abstract concept of thing. For example, an
    employee can be an object having attributes: name, date of birth, phone,
    email, etc...
    
    :param key: object_key
    :param name: object_name
    :param auth: an instance of :class:`~Auth`
    """
    def __init__(self, key, name, auth, *args):
        self.key = key
        self.name = name
        self.auth = auth
        self.f = OrderedDict() # {field_key: Field instance}
        self.f_name = OrderedDict() # {field_name: Field instance}
        for field in args:
            self.f[field.key] = field
            self.f_name[field.name] = field
            
        self.get_url = "https://api.knackhq.com/v1/objects/%s/records" % key
        self.post_url = "https://api.knackhq.com/v1/objects/%s/records" % key
        
    def __repr__(self):
        return "Object(key='%s', name='%s')" % (self.key, self.name)
    
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

    def convert_data(self, data):
        """Convert field name like key to field key.
               
        {"field_name": value} => {"field_key": value}
        """
        new_data = dict()
        for key, value in data.items():
            new_data[self.get_field_key(key)] = value
        return new_data
    
    def recover_data(self, data):
        """Convert field_key like key to field name.
        
        {"field_key": value} => {"field_name": value}
        """
        new_data = {"id": data["id"]}
        for field in self:
            raw_key = "%s_raw" % field.key
            if raw_key in data:
                new_data[field.name] = data[raw_key]
        return new_data
            
    # CRUD method
    def insert_one(self, data, using_name=True):
        """Insert one record.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#create
        
        For more information of the raw structure of all data type, read this:
        http://helpdesk.knackhq.com/support/solutions/articles/5000446405-field-types
        
        :param data: dict type data
        :param using_name: if you are using field_name in data,
          please set using_name = True (it's the default), otherwise, False
        
        **中文文档**
        
        插入一条记录
        """
        if using_name:
            data = self.convert_data(data)
        res = self.auth.post(self.post_url, data)
        return res
    
    def insert(self, data, using_name=True):
        """Insert one or many records.

        :param data: dict type data or list of dict
        :param using_name: if you are using field name in data,
          please set using_name = True (it's the default), otherwise, False
          
        **中文文档**
        
        插入多条记录
        """
        if isinstance(data, list): # if iterable, insert one by one
            if using_name:
                data = [self.convert_data(d) for d in data]
            for d in data:
                self.insert_one(d, using_name=False)
        else: # not iterable, execute insert_one
            self.insert_one(data, using_name=using_name)

    def find_one(self, _id, using_name=True, recovery=True):
        """Find one record.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#retrieve
        
        :param _id: record id
        :param using_name: if you are using field name in filter and sort_field,
          please set using_name = True (it's the default), otherwise, False
        :param recovery: set True if you want the key to be field name rather 
          than field id 
          
        **中文文档**
        
        返回一条记录
        """
            
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (
            self.key, _id)
        res = self.auth.get(url)
        
        if recovery:
            try:
                res = self.recover_data(res)
            except:
                pass
        return res

    def find(self, filter=list(), 
             sort_field=None, sort_order=None, 
             page=None, rows_per_page=None,
             using_name=True, data_only=True, recovery=True):
        """Execute a find query.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#retrieve
        
        :param filter: list of criterions. For more information: 
          http://helpdesk.knackhq.com/support/solutions/articles/5000447623-api-reference-filters-search
        :param sort_field: field_name or field_id, taking field_name by default.
          if using field_id, please set using_name = False.
        :param sort_order: -1 or 1, 1 means ascending, -1 means descending
        :param page and rows_per_page: skip first #page * #rows_per_page, 
          returns #rows_per_page of records. For more information:
          http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#pagination
        :param using_name: if you are using field_name in filter and sort_field,
          please set using_name = True (it's the default), otherwise, False
        :param data_only: set True you only need the data or the full api
          response
        :param recovery: set True if you want the key to be field_name rather 
          than field_key 

        **中文文档**
        
        返回多条记录
        """
        if using_name:            
            for criterion in filter:
                criterion["field"] = self.get_field_key(criterion["field"])
            
            if sort_field:
                sort_field = self.get_field_key(sort_field)
            
        if sort_order is None:
            pass
        elif sort_order == 1:
            sort_order = "asc"
        elif sort_order == -1:
            sort_order = "desc"
        else:
            raise ValueError
        
        params = dict()
        if len(filter) >= 1:
            params["filters"] = json.dumps(filter)
        
        if sort_field:
            params["sort_field"] = sort_field
            params["sort_order"] = sort_order
        
        if (page is not None) \
            and (rows_per_page is not None) \
            and isinstance(page, int) \
            and isinstance(rows_per_page, int) \
            and (page >= 1) \
            and (rows_per_page >= 1):
            params["page"] = page
            params["rows_per_page"] = rows_per_page
        
        res = self.auth.get(self.get_url, params)
        
        # handle data_only and recovery
        if data_only:
            try:
                res = res["records"]
                if recovery:
                    res = [self.recover_data(data) for data in res]
            except KeyError:
                pass
        else:
            if recovery:
                try:
                    res["records"] = [
                        self.recover_data(data) for data in res["records"]]
                except KeyError:
                    pass
        return res
    
    def update_one(self, _id, data, using_name=True):
        """Update one record. Any fields you don't specify will remain unchanged.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#update
        
        :param _id: record id
        :param data: the new data fields and values
        :param using_name: if you are using field name in data,
          please set using_name = True (it's the default), otherwise, False
          
        
        **中文文档**
        
        对一条记录进行更新
        """
        if using_name:
            data = self.convert_data(data)
        
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (
            self.key, _id)
        res = self.auth.put(url, data)
        return res
    
    def delete_one(self, _id, using_name=True):
        """Delete one record.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#delete
        
        :param _id: record id
        :param using_name: if you are using field name in data,
          please set using_name = True (it's the default), otherwise, False
          
        **中文文档**
        
        删除一条记录
        """        
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (
            self.key, _id)
        res = self.auth.delete(url)
        return res
    
    def delete_all(self, using_name=True): 
        """Delete all record in the table/collection of this object.
        
        **中文文档**
        
        删除表中的所有记录
        """
        for record in self.find(using_name=False, data_only=True):
            res = self.delete_one(record["id"], using_name=False)


class Schema(object):
    """Schema class that holding object and its fields information.
    """
    def __init__(self, name, *args):
        self.name = name
        self.o = OrderedDict() # {object_key: Object instance}
        self.o_name = OrderedDict() # {object_name: Object instance}
        for object_ in args:
            self.o[object_.key] = object_
            self.o_name[object_.name] = object_
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return "Schema(name='%s')" % self.name
    
    def __iter__(self):
        return iter(self.o.values())
    
    @property
    def all_object_key(self):
        """Return all object_key.
        """
        return list(self.o)

    @property
    def all_object_name(self):
        """Return all object name.
        """
        return list(self.o_name)

    def get_object_key(self, key, using_name=True):
        """Given an object_key or object_name, return it's object_key.
        """
        try:
            if using_name:
                return self.o_name[key].key
            else:
                return self.o[key].key
        except KeyError:
            raise ValueError("'%s' are not found!" % key)
    
    def get_object(self, key, using_name=True):
        """Given an object_key or object_name, return the Object instance.
        """
        try:
            if using_name:
                return self.o_name[key]
            else:
                return self.o[key]
        except KeyError:
            raise ValueError("'%s' are not found!" % key)
    
    @property
    def structure(self):
        d = {"name": self.name, "objects": dict()}
        for object_ in self.o.values():
            d["objects"][object_.key] = {
                "key": object_.key, "name": object_.name, "fields": dict(),
            }
            for field in object_.f.values():
                d["objects"][object_.key]["fields"][field.key] = {
                    "key": field.key, "name": field.name, 
                    "dtype": field.dtype, "required": field.required,
                }
        return d
    
    def to_json(self, abspath="application_schema.json"):
        """Dump schema structure data to a json file.
        
        example json data:: 
        
            {
                "name": schema_name,
                "objects": {
                    object_key1: {
                        "key": object_key1,
                        "name": object_name1,
                        "fields": {
                            field_key1: {
                                "key": field_key1,
                                "name": field_name1,
                                "dtype": field_dtype1,
                                "required": field_required1,
                            },
                            field_key2: ...
                        },
                    },
                    object_key2: ...
                },
            }
        """
        with open(abspath, "wb") as f:
            f.write(json.dumps(self.structure, sort_keys=True,
                indent=4, separators=("," , ": ")).encode("utf-8"))
    
    @staticmethod
    def from_json(abspath="application_schema.json"):
        """Read schema structure data from json file.
        
        **中文文档**
        
        从json数据中读取Schema信息, 并返回据此创建的Schema对象。
        """
        with open(abspath, "rb") as f:
            d = json.loads(f.read().decode("utf-8"))
            
        application_name = d["name"]
        object_list = list()
        for object_data in d["objects"].values():
            field_list = list()
            for field_data in d["objects"][object_data["key"]]["fields"].values():
                field_list.append(Field(
                    field_data["key"],
                    field_data["name"],
                    field_data["dtype"],                    
                    field_data["required"],
                ))
            object_list.append(Object(
                object_data["key"],
                object_data["name"],
                None,
                *field_list                
            ))
        
        schema = Schema(application_name, *object_list)
        return schema

class Application(object):
    """Knackhq application class.

    :param application_name: name of your application
    :param auth: :class:`~Auth` instance
    :param schema: :class:`~Schema` instance
    
    **中文文档**
    

    """
    def __init__(self, application_name, auth, schema=None):
        self.application_name = application_name
        self.auth = auth
        if schema is not None:
            self.schema = schema
        else:
            self.pull_schema_from_server()
        
    def pull_schema_from_server(self):
        """Get object, field, field type schema information.
        """
        object_list = list()
        
        url = "https://api.knackhq.com/v1/objects"    
        data = self.auth.get(url)
        for d in data["objects"]:
            object_key, object_name = d["key"], d["name"]
            
            field_list = list()
            
            url = "https://api.knackhq.com/v1/objects/%s/fields" % object_key
            data = self.auth.get(url)
            for d in data["fields"]:
                field = Field(key=d["key"], name=d["label"], 
                                dtype=d["type"], required=d["required"])
                field_list.append(field)
                object_ = Object(object_key, object_name, self.auth, *field_list)
            
            object_list.append(object_)
            
        self.schema = Schema(self.application_name, *object_list)

    @property
    def all_object_key(self):
        """Return all object_key.
        """
        return self.schema.all_object_key
    
    @property
    def all_object_name(self):
        """Return all object name.
        """
        return self.schema.all_object_name
    
    def get_object(self, key, using_name=True):
        """Get :class:`~Object` instance.
        
        :param key: object_key or object_name
        :param using_name: True if getting object by object name
        """
        object_ = self.schema.get_object(key, using_name=using_name)
        object_.auth = self.auth
        return object_

if __name__ == "__main__":
    import unittest
    import random
    import os
    
    AUTH_FILE = os.path.join(
        os.path.dirname(os.getcwd()), "auth.json")
    SCHEMA_FILE = os.path.join(
        os.path.dirname(os.getcwd()), "application_schema.json")

    def prepare_schema_data():
        if not os.path.exists(SCHEMA_FILE):
            app = Application(application_name="apitest",
                            auth=Auth.from_json(AUTH_FILE))
            app.schema.to_json(SCHEMA_FILE)

    def prepare_test_data():
        app = Application(
            application_name="apitest",
            auth=Auth.from_json(AUTH_FILE),
            schema=Schema.from_json(SCHEMA_FILE),
        )
        
        text_type = app.get_object("text_type")
        text_type.delete_all()
        data = {
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
            },
        }
        text_type.insert(data)
        
        number_type = app.get_object("number_type")
        number_type.delete_all()
        data = [{
            "integer": i,
            "float": float("%.2f" % random.random()),
        } for i in range(1, 10+1)]
        number_type.insert(data)
        
#     prepare_schema_data()
#     prepare_test_data()
        
    class SchemaUnittest(unittest.TestCase):
        def test_from_json(self):
            """检查从json文件中读取Schema信息。
            """
            schema = Schema.from_json(SCHEMA_FILE)
            print(schema.all_object_key)
            print(schema.all_object_name)
            number_type = schema.get_object("number_type")
            integer_field = number_type.get_field("integer")
            float_field = number_type.get_field("float")
            self.assertEqual(integer_field.name, "integer")
            self.assertEqual(float_field.name, "float")
             
    class FindUnittest(unittest.TestCase):
        def setUp(self):
            app = Application(
                application_name="apitest",
                auth=Auth.from_json(AUTH_FILE),
                schema=Schema.from_json(SCHEMA_FILE),
            )
            self.number_type = app.get_object("number_type")
  
        def test_find_all(self):
            res = self.number_type.find()
            for record in res:
                print(record)
              
        def test_find_one(self):
            res = self.number_type.find()
            for record in res:
                res = self.number_type.find_one(record["id"])
                print(res)
                res = self.number_type.find_one(record["id"], recovery=False)
                print(res) 
                break
  
        def test_filter(self):
            res = self.number_type.find(
                filter=[
                    {
                        "field": "integer",
                        "operator": "higher than",
                        "value": 3.99,
                    },
                    {
                        "field": "integer",
                        "operator": "lower than",
                        "value": 6.01,
                    },
                ],
            )
            ppt(res)
  
        def test_sort(self):
            res = self.number_type.find(
                sort_field="float", sort_order=-1,
            )
            ppt(res)
          
        def test_pagination(self):
            res = self.number_type.find(
                page=2, rows_per_page=3,
            )
            ppt(res)
        
        def test_complex_find(self):
            res = self.number_type.find(
                filter=[
                    {
                        "field": "integer",
                        "operator": "higher than",
                        "value": 2.99,
                    },
                    {
                        "field": "integer",
                        "operator": "lower than",
                        "value": 7.01,
                    },
                ],
                sort_field="float", sort_order=-1,
                page=2, rows_per_page=3,
            )
            ppt(res)
            
    class UpdateUnittest(unittest.TestCase):
        def setUp(self):
            app = Application(
                application_name="apitest",
                auth=Auth.from_json(AUTH_FILE),
                schema=Schema.from_json(SCHEMA_FILE),
            )
            self.text_type = app.get_object("text_type")
              
        def test_update_one(self):
            for record in self.text_type.find():
                _id = record["id"]
            short_text = "Text_" + str(random.randint(1, 1024)).zfill(4)
            res = self.text_type.update_one(
                _id=_id, 
                data={"short_text": short_text}, using_name=True,
            )
            res = self.text_type.find_one(_id=_id)
            self.assertEqual(res["short_text"], short_text)
            
    unittest.main()