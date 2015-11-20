#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from pyknackhq.js import load_js, safe_dump_js, js2str, prt_js
from pyknackhq.schema import Application, Object
import requests
import json

class Collection(Object):
    """A collection is the equivalent of an RDBMS table, collection of MongoDB 
    and object of Knackhq. Most of CRUD method can be executed using this.
    
    - :meth:`~Collection.insert_one`
    - :meth:`~Collection.insert`
    - :meth:`~Collection.find_one`
    - :meth:`~Collection.find`
    - :meth:`~Collection.update_one`
    - :meth:`~Collection.delete_one`
    - :meth:`~Collection.delete_all` 
    """
    def __str__(self):
        return "Collection('%s')" % self.name
                
    def __repr__(self):
        return "Collection(key='%s', name='%s')" % (self.key, self.name)

    @staticmethod
    def from_dict(d):
        return Collection(**d)
    
    @property
    def get_url(self):
        return "https://api.knackhq.com/v1/objects/%s/records" % self.key
        
    @property
    def post_url(self):
        return "https://api.knackhq.com/v1/objects/%s/records" % self.key
        
    def convert_keys(self, pydict):
        """Convert field_name to field_key.
               
        {"field_name": value} => {"field_key": value}
        """
        new_dict = dict()
        for key, value in pydict.items():
            new_dict[self.get_field_key(key)] = value
        return new_dict
    
    def get_html_values(self, pydict, recovery_name=True):
        """Convert naive get response data to human readable field name format.
        
        using html data format.
        """
        new_dict = {"id": pydict["id"]}
        for field in self:
            if field.key in pydict:
                if recovery_name:
                    new_dict[field.name] = pydict[field.key]
                else:
                    new_dict[field.key] = pydict[field.key]
        return new_dict
    
    def get_raw_values(self, pydict, recovery_name=True):
        """Convert naive get response data to human readable field name format.
        
        using raw data format.
        """
        new_dict = {"id": pydict["id"]}
        for field in self:
            raw_key = "%s_raw" % field.key
            if raw_key in pydict:
                if recovery_name:
                    new_dict[field.name] = pydict[raw_key]
                else:
                    new_dict[field.key] = pydict[raw_key]
        return new_dict
    
    def convert_values(self, pydict):
        """Convert knackhq data type instance to json friendly data.
        """
        new_dict = dict()
        for key, value in pydict.items():
            try: # is it's BaseDataType Instance
                new_dict[key] = value._data
            except AttributeError:
                new_dict[key] = value
        return new_dict

    #-------------------------------------------------------------------------#   
    #                               CRUD method                               #
    #-------------------------------------------------------------------------#   
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
        data = self.convert_values(data)
        if using_name:
            data = self.convert_keys(data)
        res = self.post(self.post_url, data)
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
            for d in data:
                self.insert_one(d, using_name=using_name)
        else: # not iterable, execute insert_one
            self.insert_one(data, using_name=using_name)

    def find_one(self, id_, raw=True, recovery_name=True):
        """Find one record.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#retrieve
        
        :param id_: record id_
        :param using_name: if you are using field name in filter and sort_field, 
          please set using_name = True (it's the default), otherwise, False
        :param raw: Default True, set True if you want the data in raw format. 
          Otherwise, html format
        :param recovery_name: Default True, set True if you want field name 
          instead of field key
          
        **中文文档**
        
        返回一条记录
        """
            
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (
            self.key, id_)
        res = self.get(url)
        
        if raw:
            try:
                res = self.get_raw_values(res, recovery_name=recovery_name)
            except:
                pass
        else:
            try:
                res = self.get_html_values(res, recovery_name=recovery_name)
            except:
                pass
        return res

    def find(self, filter=list(), 
             sort_field=None, sort_order=None, 
             page=None, rows_per_page=None,
             using_name=True, data_only=True, raw=True, recovery_name=True):
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
        :param raw: Default True, set True if you want the data in raw format. 
          Otherwise, html format
        :param recovery_name: Default True, set True if you want field name
          instead of field key
        
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
            
        res = self.get(self.get_url, params)
        
        # handle data_only and recovery
        if data_only:
            try:
                res = res["records"]
                if raw:
                    res = [self.get_raw_values(data, recovery_name) for data in res]
                else:
                    res = [self.get_html_values(data, recovery_name) for data in res]
            except KeyError:
                pass
        else:
            if raw:
                try:
                    res["records"] = [
                        self.get_raw_values(data, recovery_name) for data in res["records"]]
                except KeyError:
                    pass
            else:
                try:
                    res["records"] = [
                        self.get_html_values(data, recovery_name) for data in res["records"]]
                except KeyError:
                    pass
        return res
    
    def update_one(self, id_, data, using_name=True):
        """Update one record. Any fields you don't specify will remain unchanged.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#update
        
        :param id_: record id_
        :param data: the new data fields and values
        :param using_name: if you are using field name in data,
          please set using_name = True (it's the default), otherwise, False
          
        **中文文档**
        
        对一条记录进行更新
        """
        data = self.convert_values(data)
        if using_name:
            data = self.convert_keys(data)
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (
            self.key, id_)
        res = self.put(url, data)
         
        return res
    
    def delete_one(self, id_):
        """Delete one record.
        
        Ref: http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#delete
        
        :param id_: record id_
          
        **中文文档**
        
        删除一条记录
        """        
        url = "https://api.knackhq.com/v1/objects/%s/records/%s" % (
            self.key, id_)
        res = self.delete(url)
        return res
    
    def delete_all(self): 
        """Delete all record in the table/collection of this object.
        
        **中文文档**
        
        删除表中的所有记录
        """
        for record in self.find(using_name=False, data_only=True):
            res = self.delete_one(record["id"])

class KnackhqAuth(object):
    """Knackhq API authentication class.
    
    :param application_id: str type, Application ID
    :param api_key: str type, API Key
    
    To get your Application ID and API Key, read this tutorial:
    http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#key
    """
    def __init__(self, application_id, api_key):
        self.application_id = application_id
        self.api_key = api_key
        self.headers = {
            "X-Knack-Application-Id": self.application_id,
            "X-Knack-REST-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    @staticmethod
    def from_dict(d):
        return KnackhqAuth(**d)
    
    @staticmethod
    def from_json(abspath):
        return KnackhqAuth.from_dict(load_js(abspath, enable_verbose=False))
    
    def get(self, url, params=dict()):
        """Http get method wrapper, to support search.
        """
        try:
            res = requests.get(url, headers=self.headers, params=params)
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
    
    def post(self, url, data):
        """Http post method wrapper, to support insert.
        """
        try:
            res = requests.post(
                url, headers=self.headers, data=json.dumps(data))
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
    
    def put(self, url, data):
        """Http put method wrapper, to support update.
        """
        try:
            res = requests.put(
                url, headers=self.headers, data=json.dumps(data))
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
    
    def delete(self, url):
        """Http delete method wrapper, to support delete.
        """
        try:
            res = requests.delete(url, headers=self.headers)
            return json.loads(res.text)
        except Exception as e:
            print(e)
            return "error"
        
class KnackhqClient(object):
    """Knackhq API client class.
    
    :param auth: A :class:`KnackAuth` instance.
    :param application: An :class:`~pyknackhq.schema.Application` instance. 
      If it is not given, the client automatically pull it from knack server.
    
    How to construct a knackhq api client::
    
        from pyknackhq import KnackhqClient, KnackhqAuth
        
        auth = KnackhqAuth(application_id="your app id", api_key="your api key")
        client = KnackClient(auth=auth)
    """
    def __init__(self, auth, application=None):
        self.auth = auth
        if isinstance(application, Application):
            self.application = application
        else: # get the schema json, construct Application instance
            res = requests.get(
                "https://api.knackhq.com/v1/applications/%s" % 
                self.auth.application_id)
            self.application = Application.from_dict(json.loads(res.text))
    
    def __str__(self):
        return "KnackhqClient(application='%s')" % self.application
    
    def __repr__(self):
        return str(self)
    
    @property
    def all_object_key(self):
        return self.application.all_object_key
    
    @property
    def all_object_name(self):
        return self.application.all_object_name
    
    def get_collection(self, key, using_name=True):
        """Get :class:`Collection` instance.
        
        :param key: object_key or object_name
        :param using_name: True if getting object by object name
        """
        object_ = self.application.get_object(key, using_name=using_name)
        collection = Collection.from_dict(object_.__dict__)
        for http_cmd in ["get", "post", "put", "delete"]:
            collection.__setattr__(http_cmd, self.auth.__getattribute__(http_cmd))
        return collection
    
    def export_schema(self, abspath):
        """Export application detailed information to a nicely formatted json
        file.
        """
        self.application.to_json(abspath)

if __name__ == "__main__":
    from pyknackhq.tests import AUTH_JSON_PATH, SCHEMA_JSON_PATH
    from pprint import pprint as ppt
    import unittest
    
    def crud_basic_test():
        client =  KnackhqClient(
            auth=KnackhqAuth.from_json(AUTH_JSON_PATH),
            application=Application.from_json(SCHEMA_JSON_PATH),
        )
        short_text_object = client.get_collection("short_text_object")
        
        # delete all, initialize database
        short_text_object.delete_all()
         
        # insert one record
        record = {"short text field": "word1"}
        res = short_text_object.insert_one(record)
         
        # insert two records
        records = [{"short text field": "word2"}, {"short text field": "word3"}]
        short_text_object.insert(records)
        
        # find all
        res = short_text_object.find()
        
        # update
        new_record = {"short text field": "Hello World"}
        res = short_text_object.update_one(res[0]["id"], new_record)
        
        # find one
        res = short_text_object.find_one(res["id"])
        
#     crud_basic_test()