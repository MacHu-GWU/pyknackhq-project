Quick Start
===================================================================================================

There's three basic data model in a knackhq application:

1. Application
2. Object
3. Field

To get started, you have to connect to your application and database first.

**Notice, pyknackhq only support root access API.**

1. Authentication
---------------------------------------------------------------------------------------------------

There's two way you can pass your API credential.

First, include your ``application_id`` and ``api_key`` in your script. (NOT RECOMMENDED)

::

	from __future__ import print_function
	import pyknackhq

	# Getting your Knack Application ID and API Key:
	# http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#key
	auth = pyknackhq.Auth(application_id="your application id", api_key="your api key")

Second, create a json file, place it somewhere safe, and read your credential from it.

For example, create a file ``auth.json``:

.. code-block:: json

	{"application_id": "your application id", "api_key": "your api key"}

In python script, read your credential this way::

	auth = pyknackhq.Auth.from_json("auth.json")


2. Connect to your application and object
---------------------------------------------------------------------------------------------------

Any database operation has to be executed via :class:`pyknackhq.Object`. And you can easily get 
object instance by its name. Before that, you have to connect to your application first::
	
	from __future__ import print_function
	import pyknackhq

	auth = pyknackhq.Auth.from_json("auth.json")

	# connect to application
	
	app = pyknackhq.Application(
	    application_name="what ever you want.",
	    auth=auth,
	)

	# print all object you defined in this app
	
	print(app.all_object_name)

	# connect to object by its name
	
	employee = app.get_object("employee")

	# make a simple query, return all records
	
	for record in employee.find():
	    print(record)


OK, let's take a look at how to perform CRUD.


3. Execute insert, select, update and delete
---------------------------------------------------------------------------------------------------

Insert
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

insert one::

	data = {
	    "date of birth": {"date": "08/15/1982"},
	    "first name": "Michael",
	    "last name": "Jackson",
	}
	employee.insert(data)

insert many::

	data = [
	    {
	        "date of birth": {"date": "08/15/1982"},
	        "first name": "Michael",
	        "last name": "Jackson",
	    },
	    {
	        "date of birth": {"date": "12/06/1952"},
	        "first name": "Bruce",
	        "last name": "Lee",
	        "work email": {"email": "bruce.lee@gmail.com"},
	    },
	]

employee.insert(data)

Find
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

find one record::
	
	record = employee.find(_id="5637e518a8c941a86c325243")

filter record::
	
	result = employee.find(
	    filter=[
	        {
	            "field": "last name",
	            "operator": "is",
	            "value": "Lee",
	        },
	    ],
	)
	for record in result:
		print(record)

sort record::
	
	# order by "last name", descending
	result = employee.find(
	    sort_field="last name", sort_order=-1,
	)

Update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

update one record::

	employee.update_one(
	    _id="5637e518a8c941a86c325243", data={"first name": "Ram"})

Delete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

delete one record::

	employee.delete_one(_id="5637e518a8c941a86c325243")

delete all record of one object::
	
	# watch out! there's no way to get it back
	employee.delete_all()

when reading this, you basically is able to program knackhq. If you want to know more useful feature about ``pyknackhq``, please read: :ref:`Advance Feature <advance_feature>`.