.. _advance_feature:

Advance Feature
===================================================================================================

1. Field key and name handling
---------------------------------------------------------------------------------------------------

http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#response

By default, field record response format contains both html and raw data version, and its in field key version, which is not explicit:

.. code-block:: python

	{
	    "field_19": 1,
	    "field_19_raw": 1,
	    "field_20": "Obama",
	    "field_20_raw": "Obama",
	    "field_21": "Barrack",
	    "field_21_raw": "Barrack",
	    "field_22": "01/31/1975",
	    "field_22_raw": {
	        "am_pm": "AM",
	        "date": "01/31/1975",
	        "date_formatted": "01/31/1975",
	        "hours": "12",
	        "minutes": "00",
	        "timestamp": "01/31/75Y 12:00 am",
	        "unix_timestamp": 160358400000
	    },
	    "field_23": "<a href="mailto:obama@gmail.com">obama@gmail.com</a>",
	    "field_23_raw": {"email": "obama@gmail.com"},
	    "field_24": "<a href="tel:1234567890">(123) 456-7890</a>",
	    "field_24_raw": {
	        "area": "123",
	        "formatted": "(123) 456-7890",
	        "full": "1234567890",
	        "number": "4567890"
	    },
	    "id": "5637e558d8c931a86c325143"
	}

In pyknackhq, the field record response using human readable key that matching the schema you defined in the backend by default. For the same purpose, the insert operation is designed to be compatible with human readable field name. The Python API client automatically read the schema and handle the field name to key mapping for you.

.. code-block:: python

	import pyknackhq
	import pprint
	
	app = pyknackhq.Application(
	    application_name="what ever you want.",
	    auth=pyknackhq.Auth.from_json("auth.json"),
	)
	employee = app.get_object("employee")
	for record in employee.find():
	    pprint.pprint(record)

	# screen display:

	{
	    "id": "5637e558d8c931a86c325143",
	    "employee_id": 1,
	    "first name": "Obama",
	    "last name": "Barrack",
	    "date of birth": {
	        "am_pm": "AM",
	        "date": "01/31/1975",
	        "date_formatted": "01/31/1975",
	        "hours": "12",
	        "minutes": "00",
	        "timestamp": "01/31/75Y 12:00 am",
	        "unix_timestamp": 160358400000
	    },
	    "mobile phone": {
	        "area": "123",
	        "formatted": "(123) 456-7890",
	        "full": "1234567890",
	        "number": "4567890"
	    },
	    "work email": {"email": "obama@gmail.com"}
	}


2. Browse schema
---------------------------------------------------------------------------------------------------

This is how knackhq organize your data. You can have multiple objects for each application. Each object has its object_key, object_name and many fields. Each field has its field_key, field_name, field_data_type and whether it is required. And :class:`pyknackhq.Schema` is a container having those information. I provide a way to print it in human readable format::

	pprint.pprint(app.schema.structure)

	# screen display:

	{
	    "name": "apitest",
	    "objects": {
	        "object_4": {
	            "name": "employee",
	            "key": "object_4",
	            "fields": {
	                "field_19": {
	                    "dtype": "auto_increment",
	                    "key": "field_19",
	                    "name": "employee_id",
	                    "required": False
	                },
	                "field_20": {
	                    "dtype": "short_text",
	                    "key": "field_20",
	                    "name": "first name",
	                    "required": False
	                },
	                "field_21": {
	                    "dtype": "short_text",
	                    "key": "field_21",
	                    "name": "last name",
	                    "required": False
	                },
	                "field_22": {
	                    "dtype": "date_time",
	                    "key": "field_22",
	                    "name": "date of birth",
	                    "required": False
	                },
	                "field_23": {
	                    "dtype": "email",
	                    "key": "field_23",
	                    "name": "work email",
	                    "required": False
	                },
	                "field_24": {
	                    "dtype": "phone",
	                    "key": "field_24",
	                    "name": "mobile phone",
	                    "required": False
	                }
	            }	        
	        }
	    }
	}

In addition, you can easily access object_key, object_name, :class:`pyknackhq.Object` instance, field_key, field_name, :class:`pyknackhq.Field` instance by simply calling the following methods or attributes::

	>>> app.all_object_key
	["object_4"]
	
	>>> app.all_object_name
	["employee"]
	
	>>> employee = app.get_object("employee")
	>>> employee.all_field_key
	['field_20', 'field_24', 'field_21', 'field_19', 'field_23', 'field_22']

	>>> employee.all_field_name
	['first name', 'mobile phone', 'last name', 'employee_id', 'work email', 'date of birth']

	>>> date_of_birth = employee.get_field("date of birth")
	>>> date_of_birth
	Field(key='field_22', name='date of birth', dtype='date_time', required=False)


Read and write your schema info
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Everytime when you create an :class:`pyknackhq.Application` instance, if the schema are not defined, then several API call are made silently, which is a little expensive. Pyknackhq allow developer to dump schema info to a json file in one line::
	
	app = pyknackhq.Application(
	    application_name="what ever you want.",
	    auth=pyknackhq.Auth.from_json("auth.json"),
	)
	app.schema.to_json("application_schema.json") # "application_schema.json" is the default file name

And next time, if no change are made in your schema, then you can read it from json file rather than making expensive API call::

	app = pyknackhq.Application(
	    application_name="what ever you want.",
	    auth=pyknackhq.Auth.from_json("auth.json"),
	    schema=pyknackhq.Schema.from_json("application_schema.json"),
	) # no API call is made


3. Easy query
---------------------------------------------------------------------------------------------------

If you are familiar with `MongoDB <https://www.mongodb.com/>`_, you may notice that the syntax of pyknackhq API is very similar to `pymongo <https://api.mongodb.org/python/current/>`_. Using filter, sort, pagination is super simple with pyknackhq. For arguments reference, read :meth:`pyknackhq.Object.find`.

Let's see how it works with a real example::

	res = employee.find(
	    filter=[
	        {
	            "field": "date of birth",
	            "operator": "is after",
	            "value": "01/01/1970",
	        },
	    ],
	    sort_field="date of birth", sort_order=-1,
	    page=1, rows_per_page=10,
	)
	pprint.pprint(res)

OK, you just finshed! For the source code and argument reference, please read :mod:`API Reference <pyknackhq>`.