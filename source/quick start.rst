Quick Start
===================================================================================================

There are three level of data model in a knackhq application:

1. Application
2. Object
3. Field

``Application`` is a database backed web app with customizable view and interface. ``Object`` is equivalent to a table in RDBMS. ``Field`` can be considered as a column of a table.

There are two classes you mainly interact with in pyknackhq:

1. KnackhqClient
2. Collection

``KnackhqClient`` is a client instance connected to knackhq API server. And the schema information is also hold in it. ``Collection`` is equivalent to the collection in MongoDB. Because knackhq uses the schemaless database as the backend, which is very similar to MongoDB. So I use ``Collection`` instead of the naive ``Object``, and provide group of simliar CRUD utility methods.

Basically, a standard work flow looks like:

1. `Authorize your knackhq API client <authentication_>`_
2. `Connect your Client and Collection <connect_>`_
3. `Manipulate database via API (Create, Read, Update, Delete) <manipulate_>`_


.. _authentication:

Authorize your knackhq API client
---------------------------------------------------------------------------------------------------

**Notice, pyknackhq only support root access API.**

knackhq use ``application_id`` and ``api_key`` to verify your identity. You can find yours at http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#key.

There are two ways you can include your API credential.

1. Put your credential in your script. (NOT RECOMMENDED)
2. Create a json file including your credential, and keep it safe. So client can read from it. (RECOMMENDED)

Example 1, put credential in script::

	from __future__ import print_function # for python2, 3 compatible
	from pyknackhq import KnackhqAuth, KnackhqClient

	client = KnackhqClient(
	    auth=KnackhqAuth(
	        application_id="your app id",
	        api_key="your api key",
	    ),
	)
	print(client)

	Out: KnackhqClient(application='Application('your app name')')

Example 2, put your credential in a json file:

Create a file ``auth.json``::

.. code-block:: json

	{"application_id": "your app id", "api_key": "your api key"}

Read credential from it::

	client = KnackhqClient(auth=KnackhqAuth.from_json("auth.json"))
	print(client)

	Out: KnackhqClient(application='Application('your app name')')


.. _connect:

Connect your Client and Collection
---------------------------------------------------------------------------------------------------

Once your client is connected, the schema information has been read from remote server. You can browse all object name you have defined like this (I use my personal apitest application just for demonstration reason)::

	print(client.all_object_name)

	Out: ['test_object', 'short_text_object', 'paragraph_text_object', 'yes_no_object', 'multiple_choice_object', 'date_time_object', 'date_time_from_to_object', 'number_object', 'image_object', 'file_object', 'address_object', 'name_object', 'link_object', 'email_object', 'phone_object', 'rich_text_object', 'currency_object', 'timer_object', 'rating_object']

So you can get ``Collection`` instance using::

	test_object = client.get_collection("test_object")
	print(test_object)

	Out: Collection('test_object')

Similarly, you can get all field name defined in Object like this::

	print(test_object.all_field_name)

	Out: ['short text field', 'paragraph text field', 'yes no field', 'multiple choice field', 'date time field', 'number field', 'image field', 'file field', 'address field', 'name field', 'link field', 'email field', 'phone field', 'rich text field', 'currency field', 'auto increment field', 'timer field', 'rating field', 'signature field']

Get ``Field`` instance using::

	short_text_field = test_object.get_field("short text field")
	print(short_text_field)

	Out: print(short_text_field)

All ``Object`` level CRUD operation has to be performed via ``Collection``. Let's take a look at how to it.


.. _manipulate:

Manipulate database via API
---------------------------------------------------------------------------------------------------

Create (insert)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

insert one record::

	from pprint import pprint # pretty printer

	record = {
	    "short text field": "Hello World",
	    "paragraph text field": "This is a paragraph text",
	    "yes no field": True,
	    "multiple choice field": ["First Choice", "Second Choice"],
	}
	response = test_object.insert_one(record)
	pprint(response) # if success, pretty print response, otherwise, response would be "error"

pyknackhq provide a convenient method :meth:`~pyknackhq.client.insert` takes single python dict record or list of records. If a record is failed to insert, it will be automatically skipped.

insert many::

	records = [
	    {"short text field": "a"},
	    {"short text field": "b"},
	]
	test_object.insert(records)


Read (find)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

find one record:

.. code-block:: python

	record = employee.find(id_="564020bd465539a51dede83f")
	pprint(record)

	Out:
	{'address field': {'city': 'Washington',
	                   'latitude': '38.8976989',
	                   'longitude': '-77.036553192281',
	                   'state': 'DC',
	                   'street': '1600 Pennsylvania Ave NW',
	                   'street2': '',
	                   'zip': '20500'},
	 'auto increment field': 1,
	 'currency field': '123.45',
	 'date time field': {'am_pm': 'AM',
	                     'date': '11/01/2015',
	                     'date_formatted': '11/01/2015',
	                     'hours': '12',
	                     'minutes': '00',
	                     'timestamp': '11/01/15Y 12:00 am',
	                     'unix_timestamp': 1446336000000},
	 'email field': {'email': 'example@gmail.com'},
	 'file field': {'application_id': '56325e4a5839b2486913f542',
	                'filename': 'readme.txt',
	                'id': '56401ffbdb53de555f7e40c0',
	                's3': True,
	                'size': 346,
	                'thumb_url': 'http://assets.knackhq.com/assets/56325e4a5839b2486913f542/56401ffbdb53de555f7e40c0/thumb/readme.txt',
	                'type': 'file',
	                'url': 'http://assets.knackhq.com/assets/56325e4a5839b2486913f542/56401ffbdb53de555f7e40c0/original/readme.txt'},
	 'id': '564020bd465539a51dede83f',
	 'image field': {'application_id': '56325e4a5839b2486913f542',
	                 'filename': 'sanheprojectlogo.jpg',
	                 'id': '56401fafefbc736c4aff457c',
	                 's3': True,
	                 'size': 2586,
	                 'thumb_url': 'http://assets.knackhq.com/assets/56325e4a5839b2486913f542/56401fafefbc736c4aff457c/thumb/sanheprojectlogo.jpg',
	                 'type': 'image',
	                 'url': 'http://assets.knackhq.com/assets/56325e4a5839b2486913f542/56401fafefbc736c4aff457c/original/sanheprojectlogo.jpg'},
	 'link field': {'url': 'http://www.google.com'},
	 'multiple choice field': ['First Choice', 'Second Choice'],
	 'name field': {'first': 'Obama', 'last': 'Barrack'},
	 'number field': 3,
	 'paragraph text field': 'a paragraph text',
	 'phone field': {'area': '123',
	                 'formatted': '(123) 456-7890',
	                 'full': '1234567890',
	                 'number': '4567890'},
	 'rating field': 3,
	 'rich text field': '<strong>a rich text</strong>',
	 'short text field': 'a short text',
	 'signature field': {'base30': '5EZ44553534433220Y22222423Z3555555_pZ1100Y22232333363333333320Z10000_6DZ221212Y1_1W354344Z4_6L_1w_9zZ35544332110Y553332232000000Z1212121242332Y10324333434544544665_1FZ20Y122233445Z11222332Y355665644544344Z1322355243223122121211100_bC00Z111121Y112121223431100Z1Y1243333_1C56445534Z4444343331Y24455443Z12222',
	                     'svg': '<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="276" height="96"><path fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M 62 3 c -0.14 -0.04 -5.36 -1.71 -8 -2 c -3.21 -0.36 -7.27 -1.03 -10 0 c -5.98 2.27 -13.17 7.04 -19 11 c -2.25 1.53 -4.22 3.86 -6 6 c -1.51 1.82 -3.35 4.05 -4 6 c -0.54 1.62 -0.73 4.46 0 6 c 2.21 4.63 6.54 10.56 10 15 c 0.96 1.23 2.85 1.85 4 3 c 1.79 1.79 4.69 4.76 5 6 c 0.14 0.57 -1.99 1.97 -3 2 c -8.42 0.26 -30 -1 -30 -1"/><path fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M 91 36 c -0.17 0.4 -9.8 22.58 -10 23 c -0.03 0.07 1 -4 1 -4"/><path fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M 99 10 l 1 1"/><path fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M 177 19 c -0.05 -0.04 -2.02 -1.92 -3 -2 c -2.74 -0.21 -7.09 0.03 -10 1 c -3.63 1.21 -7.91 3.68 -11 6 c -1.92 1.44 -3.95 3.91 -5 6 c -1.11 2.21 -1.6 5.37 -2 8 c -0.25 1.59 -0.73 4.78 0 5 c 1.49 0.45 7.12 -0.79 10 -2 c 3.06 -1.29 6.57 -3.75 9 -6 c 1.62 -1.5 2.55 -4.34 4 -6 c 0.73 -0.83 2.38 -2.12 3 -2 c 0.62 0.12 1.94 1.98 2 3 c 0.52 9.37 0.91 22.59 0 33 c -0.37 4.29 -2.38 8.68 -4 13 c -2.45 6.54 -5.8 15.7 -8 19 c -0.44 0.66 -3.08 -0.39 -4 -1 c -0.8 -0.54 -1.17 -2.27 -2 -3 c -1.66 -1.45 -4.34 -2.55 -6 -4 c -0.83 -0.73 -1.92 -2.02 -2 -3 c -0.21 -2.74 0.2 -7.6 1 -10 c 0.29 -0.86 2.33 -1.19 3 -2 c 0.84 -1 1.02 -3.09 2 -4 c 3.59 -3.35 8.81 -7.29 13 -10 c 1.05 -0.68 2.8 -0.45 4 -1 c 2.34 -1.07 4.53 -3.1 7 -4 c 8.32 -3.03 17.39 -6.2 26 -8 l 17 -1"/><path fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M 240 16 c 0 0.19 0.49 7.45 0 11 c -0.82 5.95 -2.36 12.15 -4 18 c -0.68 2.41 -2.9 7.1 -3 7 c -0.1 -0.1 1.09 -5.39 2 -8 c 1.78 -5.11 3.55 -10.47 6 -15 c 1.73 -3.2 4.67 -6.88 7 -9 c 0.84 -0.77 2.95 -1.15 4 -1 c 0.92 0.13 2.57 1.14 3 2 c 0.99 1.98 1.71 5.36 2 8 c 0.36 3.21 0.23 6.78 0 10 c -0.09 1.33 -1.2 2.87 -1 4 c 0.38 2.08 1.89 6.04 3 7 c 0.6 0.52 2.88 -0.37 4 -1 c 3.92 -2.2 12 -8 12 -8"/></svg>'},
	 'timer field': {'times': [{'from': {'am_pm': 'AM',
	                                     'date': '01/01/2012',
	                                     'date_formatted': '01/01/2012',
	                                     'hours': '12',
	                                     'minutes': '00',
	                                     'timestamp': '01/01/12Y 12:00 am',
	                                     'unix_timestamp': 1325376000000},
	                            'to': {'am_pm': 'AM',
	                                   'date': '01/01/2012',
	                                   'date_formatted': '01/01/2012',
	                                   'hours': '12',
	                                   'minutes': '30',
	                                   'timestamp': '01/01/12Y 12:30 am',
	                                   'unix_timestamp': 1325377800000}}],
	                 'total_time': 1800000},
	 'yes no field': True}


find all records:

.. code-block:: python

	for record in test_object.find():
	    # do what every you want


Update (update)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

update one record::

	test_object.update_one(id_="564020bd465539a51dede83f", data={"short text field": "New short text"})


Delete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

delete one record::

	employee.delete_one(id_="564020bd465539a51dede83f")

delete all record of one object::
	
	# watch out! there's no way to get it back
	employee.delete_all()


Now, you basically is able to program knackhq. If you want to know more useful feature about ``pyknackhq``, please read: :ref:`Advance Feature <advance_feature>`.