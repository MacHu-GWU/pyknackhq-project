#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyknackhq.py23compatible import ( 
    _str_type, _int_types, _number_types, is_py3)
from datetime import datetime, date, timedelta
import json

class BaseDataType(object):
    """Base type of all knackhq supported data type.
    
    **中文文档**
    
    所有DataType类的基类。其中 `._data` 属性是其可用于直接insert的Json Dict形式。
    """
    def __str__(self):
        return json.dumps(self._data, 
            sort_keys=True, indent=4, separators=("," , ": "))

#-----------------------------------------------------------------------------#
#                                 Basic Type                                  #
#-----------------------------------------------------------------------------#
class ShortTextType(BaseDataType):
    """Short text type.
    """
    def __init__(self, value):
        if not isinstance(value, _str_type):
            raise TypeError("'value' has to be str")
        self.value = value
        
        # construct data
        self._data = self.value
        
class ParagraphTextType(BaseDataType):
    """Paragraph text type.
    """
    def __init__(self, value):
        if not isinstance(value, _str_type):
            raise TypeError("'value' has to be str")
        self.value = value
        
        # construct data
        self._data = self.value
        
class YesNoType(BaseDataType):
    """Yes or No boolean type.
    """
    def __init__(self, value):
        if not isinstance(value, bool):
            raise TypeError("'value' has to be bool")
        
        self.value = value
        
        # construct data
        self._data = self.value
        
class SingleChoiceType(BaseDataType):
    """Single choice type.
    """
    def __init__(self, value):
        if not isinstance(value, _str_type):
            raise TypeError("'value' has to be str")
        self.value = value
        
        # construct data
        self._data = self.value
        
class MultipleChoiceType(BaseDataType):
    """Multiple choice type.
    """
    def __init__(self, value):
        if isinstance(value, list):
            for i in value:
                if not isinstance(i, _str_type):
                    raise TypeError("'value' has to be list of str")
        else:
            raise TypeError("'value' has to be list of str")
        self.value = value
        
        # construct data
        self._data = self.value
        
class DateTimeType(BaseDataType): # TODO
    """Date time type.
    
    :param value: Python datetime, date type
    :param is_date: Default False, True for date only
    """
    def __init__(self, value, is_date=False):
        if isinstance(value, datetime):
            if is_date:
                self.value = value.date()
                self._data = {"date": self.value.strftime("%m/%d/%Y")}
            else:
                self.value = value
                self._data = {
                    "date": self.value.strftime("%m/%d/%Y"),
                    "hours": self.value.hour,
                    "minutes": self.value.minute,
                }
        elif isinstance(value, date):
            self.value = value
            self._data = {"date": self.value.strftime("%m/%d/%Y")}

class DateTimeFromToType(BaseDataType):
    """From xxx to xxx Type.
    
    :param from_: from datetime or date
    :param to_: to datetime or date
    :param repeat: a python dict contains repeat information
    :param all_day: Default False, True for date only
    
    example repeat param::
    
        {
            "FR": true,
            "MO": true,
            "SA": false,
            "SU": false,
            "TH": true,
            "TU": true,
            "WE": true,
            "end_count": "",
            "end_date": "",
            "endson": "never",
            "frequency": "weekly",
            "interval": "1",
            "repeatby": "dom",
            "start_date": "11/01/2015"
        },
    """
    def __init__(self, from_, to_, repeat=None, all_day=False):
        from_and_to = list()
        from_and_to_data = list()
        for value in [from_, to_]:
            if isinstance(value, datetime):
                if all_day:
                    from_and_to.append(value.date())
                    from_and_to_data.append(
                        {"date": value.strftime("%m/%d/%Y")})
                else:
                    from_and_to.append(value)
                    from_and_to_data.append({
                        "date": value.strftime("%m/%d/%Y"),
                        "hours": value.hour,
                        "minutes": value.minute,
                    })
            elif isinstance(value, date):
                from_and_to.append(value)
                from_and_to_data.append(
                    {"date": value.strftime("%m/%d/%Y")}
                )

        self.from_ = from_and_to[0]
        self.to_ = from_and_to[1]
        self._data = from_and_to_data[0]
        self._data["to"] = from_and_to_data[1]

        if all_day:
            self._data["all_day"] = True
            
        if repeat:
            self.repeat = repeat
            self._data["repeat"] = repeat
            
class NumberType(BaseDataType):
    """Integer or Float Type.
    """
    def __init__(self, value):
        if not isinstance(value, _number_types):
            raise TypeError("'value' has to be int or float")
        
        self.value = value
        
        # construct data
        self._data = self.value

# class ImageType(BaseDataType):
#     def __init__(self, path_or_url):
#         if not isinstance(value, bytes):
#             raise TypeError("'value' has to be binary")
#         if not isinstance(filename, path_or_url):
#             raise TypeError("'value' has to be str")
#         self.url, self.path = None, None
# 
#         if path_or_url.startswith("http"):
#             self.url = path_or_url
#         else:
#             if os.path.exists(path_or_url):
#                 if os.path.isfile(path_or_url):
#                     self.path = path_or_url
#                 else:
#                     raise ValueError("'%s' is not a file." % path_or_url)
#             else:
#                 raise FileNotFoundError("'%s' is not found." % path_or_url)
#         
#     @property
#     def data(self):
#         if self.url:
#             return self.url
#         
#         if self.path:
#             upload_url = ("https://api.knackhq.com/v1/applications/"
#                           "%s/assets/file/upload" % self.application_id)
#             
#             basename = os.path.basename(self.path)
#             files = {
#                 basename: open(self.path)
#             }
#             res = self.auth.upload(upload_url, files)
#             return res["id"]
#         
#         raise Exception("data error")
#     
# class FileType(ImageType):
#     pass

#-----------------------------------------------------------------------------#
#                                Special Type                                 #
#-----------------------------------------------------------------------------#
class AddressType(BaseDataType):
    """Address type.
    """
    def __init__(self, street=None, street2=None, 
                 city=None, state=None, zipcode=None, country=None):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country
        
    @property
    def _data(self):
        attrs = ["street", "street2", 
                 "city", "state", "zipcode", "country"]
        d = dict()
        for attr in attrs:
            value = self.__getattribute__(attr)
            if value:
                d[attr] = value
        return d

class NameType(BaseDataType):
    """Name type.
    """
    def __init__(self, title=None, first=None, middle=None, last=None):
        self.title = title
        self.first = first
        self.middle = middle
        self.last = last

    @property
    def _data(self):
        attrs = ["title", "first", "middle", "last"]
        d = dict()
        for attr in attrs:
            value = self.__getattribute__(attr)
            if value:
                d[attr] = value
        return d

class LinkType(BaseDataType):
    """Link type.
    """
    def __init__(self, url, label=None):
        self.url = url
        self.label = label
        
    @property
    def _data(self):
        attrs = ["url", "label"]
        d = dict()
        for attr in attrs:
            value = self.__getattribute__(attr)
            if value:
                d[attr] = value
        return d

class EmailType(BaseDataType):
    """Email type.
    """
    def __init__(self, email, label=None):
        self.email = email
        self.label = label
        
    @property
    def _data(self):
        attrs = ["email", "label"]
        d = dict()
        for attr in attrs:
            value = self.__getattribute__(attr)
            if value:
                d[attr] = value
        return d
    
class PhoneType(BaseDataType):
    """Phone type.
    """
    def __init__(self, full=None, area=None, country=None, number=None):
        self.full = full
        self.area = area
        self.country = country
        self.number = number
        
    @property
    def _data(self):
        attrs = ["full", "area", "country", "number"]
        d = dict()
        for attr in attrs:
            value = self.__getattribute__(attr)
            if value:
                d[attr] = value
        return d

class RichTextType(BaseDataType):
    """Rich html text type.
    """
    def __init__(self, value):
        if not isinstance(value, _str_type):
            raise TypeError("'value' has to be str")
        self.value = value
        
        # construct data
        self._data = self.value


class TimerType(BaseDataType):
    """Timer type.
    
    :param from_: from datetime
    :param to_: to datetime
    """
    def __init__(self, from_, to_):
        from_and_to_data = list()
        for value in [from_, to_]: 
            from_and_to_data.append({
                "date": value.strftime("%m/%d/%Y"),
                "hours": value.hour,
                "minutes": value.minute,
            })

        self.from_ = from_
        self.to_ = to_
        
        times = [{"from": from_and_to_data[0], "to": from_and_to_data[1]}]
        self._data = {"times": times}

class CurrencyType(BaseDataType):
    """Currency type.
    """
    def __init__(self, value):
        if not isinstance(value, _number_types):
            raise TypeError("'value' has to be int or float")
        
        self.value = value
        
        # construct data
        self._data = self.value

class RatingType(BaseDataType):
    """Rating type.
    """
    def __init__(self, value):
        if not isinstance(value, _number_types):
            raise TypeError("'value' has to be int or float")
        
        self.value = value
        
        # construct data
        self._data = self.value

class DataType(object):
    # basic type
    ShortTextType = ShortTextType
    ParagraphTextType = ParagraphTextType
    YesNoType = YesNoType
    SingleChoiceType = SingleChoiceType
    MultipleChoiceType = MultipleChoiceType
    DateTimeType = DateTimeType
    DateTimeFromToType = DateTimeFromToType
    NumberType = NumberType
    # special type
    AddressType = AddressType
    NameType = NameType
    LinkType = LinkType
    EmailType = EmailType
    PhoneType = PhoneType
    RichTextType = RichTextType
    TimerType = TimerType
    CurrencyType = CurrencyType
    RatingType = RatingType
    
dtype = DataType()

if __name__ == "__main__":
    from pyknackhq.tests import AUTH_JSON_PATH, SCHEMA_JSON_PATH
    from pyknackhq.client import KnackhqAuth, KnackhqClient
    from pyknackhq.schema import Application
    from pyknackhq.js import prt_js
    from pprint import pprint as ppt
    import unittest
    
    # connect client    
    client =  KnackhqClient(
        auth=KnackhqAuth.from_json(AUTH_JSON_PATH),
        application=Application.from_json(SCHEMA_JSON_PATH),
    )
    # get collection
    test_obj = client.get_collection("test_object")
    
    # basic type
    short_text_obj = client.get_collection("short_text_object")
    paragraph_text_obj = client.get_collection("paragraph_text_object")
    yes_no_obj = client.get_collection("yes_no_object")
    multi_choice_obj = client.get_collection("multiple_choice_object")
    date_time_obj = client.get_collection("date_time_object")
    from_to_obj = client.get_collection("date_time_from_to_object")
    number_obj = client.get_collection("number_object")
    image_obj = client.get_collection("image_object")
    file_obj = client.get_collection("file_object")
    
    # special type
    address_obj = client.get_collection("address_object")
    name_obj = client.get_collection("name_object")
    link_obj = client.get_collection("link_object")
    email_obj = client.get_collection("email_object")
    phone_obj = client.get_collection("phone_object")
    rich_text_obj = client.get_collection("rich_text_object")
    currency_obj = client.get_collection("currency_object")
    timer_obj = client.get_collection("timer_object")
    rating_obj = client.get_collection("rating_object")
    
#     class ShortTextTypeUnittest(unittest.TestCase):
#         def test_all(self):        
#             record = {
#                 "short text field": ShortTextType(value="This is a short text"),
#             }
#             res = short_text_obj.insert_one(record, using_name=True)
#              
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             short_text_obj.delete_one(res["id"])
# 
#     class ParagraphTextTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "paragraph text field": ParagraphTextType(
#                     value="This is a pharagraph text"),
#             }
#             res = paragraph_text_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             paragraph_text_obj.delete_one(res["id"])
# 
#     class YesNoTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "yes no field": YesNoType(value=True),
#                 "on off field": YesNoType(value=True),
#                 "true false field": YesNoType(value=True),
#             }
#             res = yes_no_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             yes_no_obj.delete_one(res["id"])
#  
#     class MutltipleChoiceType(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "one selection field": SingleChoiceType(value="First Choice"),
#                 "multi-selection field": MultipleChoiceType(
#                     value=["Second Choice", "Third Choice"]
#                 ),
#             }
#             res = multi_choice_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             multi_choice_obj.delete_one(res["id"])
# 
#     class DateTimeTypeUnittest(unittest.TestCase):
#         """
#         """
#         def test_date_field(self):
#             record = {"date field": DateTimeType(date(2015, 7, 1))}
#             res = date_time_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#                 
#         def test_datetime_12hour_field(self):
#             record = {"datetime 12hour field": DateTimeType(
#                 datetime(2015, 7, 1, 14, 30))}
#             res = date_time_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#         
#         def test_datetime_24hour_field(self):
#             record = {"datetime 24hour field": DateTimeType(
#                 datetime(2015, 7, 1, 7, 30))}
#             res = date_time_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
# 
#     class DateTimeFromToTypeUnittest(unittest.TestCase):
#         def test_from_to_field(self):
#             record = {
#                 "weekly repeat field": DateTimeFromToType(
#                     from_=datetime(2015, 7, 1),
#                     to_=datetime(2015, 7, 31),
#                     all_day=True,
#                     repeat={
#                         "FR": True,
#                         "MO": True,
#                         "SA": False,
#                         "SU": False,
#                         "TH": True,
#                         "TU": True,
#                         "WE": True,
#                         "frequency": "weekly",
#                     },
#                 )
#             }
#             res = from_to_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             from_to_obj.delete_one(res["id"])
#             
#     #-------------------------------------------------------------------------#
#     #                               Special Type                              #
#     #-------------------------------------------------------------------------#
#     class AddressTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "us address": AddressType(
#                     street="2130 H St NW",
#                     city="Washington",
#                     state="DC",
#                     zipcode="20052",
#                 ),
#                 "international address": AddressType(
#                     street="5 Avenue Anatole France",
#                     city="Paris",
#                     zipcode="75007",
#                 ),
#                 "international with country address": AddressType(
#                     street="London SW1A 0AA",
#                     city="London",
#                     country="UK",
#                 ),
#             }
#             res = address_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             address_obj.delete_one(res["id"])
#             
#     class NameTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "first last field": NameType(
#                     first="Obama",
#                     last="Barrack",
#                 ),
#                 "title first last field": NameType(
#                     title="Mr.",
#                     first="Obama",
#                     last="Barrack",
#                 ),
#                 "last first": NameType(
#                     first="Obama",
#                     last="Barrack",
#                 ),
#                 "first middle last": NameType(
#                     first="Obama",
#                     middle="Hussein",
#                     last="Barrack",
#                 ),
#                 "last first middle": NameType(
#                     first="Obama",
#                     middle="Hussein",
#                     last="Barrack",
#                 ),
#             }
#             res = name_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             name_obj.delete_one(res["id"])
#     
#     class LinkTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "use the url field": LinkType(url="www.google.com"),
#                 "use the same text for all links field": LinkType(url="www.google.com"),
#                 "use unique text for each link field": LinkType(
#                     url="www.google.com", label="Google Homepage")
#             }
#             res = link_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             link_obj.delete_one(res["id"])
# 
#     class EmailTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "use the email address field": EmailType(email="test@example.com"),
#                 "use the same text for all emails field": EmailType(email="test@example.com"),
#                 "use unique text for each email field": EmailType(
#                     email="test@example.com", label="My Work Email")
#             }
#             res = email_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             email_obj.delete_one(res["id"])
#             
#     class PhoneTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "format1 field": PhoneType(
#                     area="123",
#                     number="4567890",
#                     full="1234567890",
#                 ),
#                 "format2 field": PhoneType(
#                     area="123",
#                     number="4567890",
#                     full="1234567890",
#                 ),
#                 "format3 field": PhoneType(
#                     country="99",
#                     area="999",
#                     number="999999",
#                     full="99999999999",
#                 ),
#                 "format4 field": PhoneType(
#                     country="99",
#                     area="999",
#                     number="999999",
#                     full="99999999999",
#                 ),
#                 "format5 field": PhoneType(
#                     number="9999999999",
#                     full="9999999999",
#                 ),
#                 "format6 field": PhoneType(
#                     number="9999999999",
#                     full="9999999999",
#                 ),
#                 "format7 field": PhoneType(
#                     number="1234567890",
#                     full="1234567890",
#                 ),
#             }
#             res = phone_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             phone_obj.delete_one(res["id"])
# 
#     class RichTextTypeUnittest(unittest.TestCase):
#         def test_all(self):        
#             record = {
#                 "rich text field": RichTextType(value="<strong>Important!</strong>"),
#             }
#             res = rich_text_obj.insert_one(record, using_name=True)
#               
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             rich_text_obj.delete_one(res["id"])
# 
#     class TimerTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "timer field": TimerType(
#                     from_=datetime(2015, 1, 1, 0, 0, 0),
#                     to_=datetime(2015, 1, 1, 23, 59, 59),
#                 ),
#             }
#             res = timer_obj.insert_one(record, using_name=True)
#                 
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             timer_obj.delete_one(res["id"])
# 
#     class CurrencyTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "usa currency": CurrencyType(3.14),
#                 "uk currency": CurrencyType(3.14),
#                 "eur after currency": CurrencyType(3.14),
#                 "eur before currency": CurrencyType(3.14),
#             }
#             res = currency_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             currency_obj.delete_one(res["id"])
#  
#     class RatingTypeUnittest(unittest.TestCase):
#         def test_all(self):
#             record = {
#                 "rating field": RatingType(4.5)
#             }
#             res = rating_obj.insert_one(record, using_name=True)
#             if not (isinstance(res, dict) and "id" in res):
#                 raise Exception("Failed")
#             rating_obj.delete_one(res["id"])
# 
#     unittest.main()