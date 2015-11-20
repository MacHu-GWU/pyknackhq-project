.. _advance_feature:

Advance Feature
===================================================================================================

``pyknackhq`` provides several features to allow developer write productive code.

- `Field key and name handling <key_>`_
- `Raw and Html data format handling <raw_>`_
- `Browse schema <schema_>`_
- `Query with filter, sort, pagination <query_>`_
- `Data type constructor <dtype_>`_


.. _key:

Field key and name handling
---------------------------------------------------------------------------------------------------

By default, knackhq API returns json data using field key (`What is field key? <http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#field_keys>`_), for example:

.. code-block:: json

	{
	    "field_1": 100,
	    "field_1_raw": 100,
	    "field_2": "abc",
	    "field_2_raw": "abc",
	}

That means, you have to lookup all field keys when you want insert data.

But the good news is, ``pyknackhq`` provides a optional parameter ``using_name`` for most of CRUD methods. By default, it is equal to ``True``, which means you can use the human readable field name as the key of the json data:

.. code-block:: python

	collection.insert({"employee id": "E001", "name": "Michael Jackson"})

	collection.find(filter={
	    "field": "date of birth",
	    "operator": "is after",
	    "value": "01/01/1970",
	})

	collection.update(id_="0000aaaa1111bbbb2222cccc", data={"name": "Barrack Obama"})

If you really want to use the naive field key, you can still do this::

 	collection.insert({"field_1": "E001", "name": Michael Jackson"}, using_name=False)


.. _raw:

Raw and Html data format handling
---------------------------------------------------------------------------------------------------

The original knackhq API provides 3 options(Raw, HTML, Both) for the response format (`What is response format? <http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#response>`_). A default http get response looks like:

.. code-block:: json
	
	{
	    "field_1": "<a href="mailto:obama@gmail.com">obama@gmail.com</a>",
	    "field_1_raw": {"email": "obama@gmail.com"},
	}

You can set the parameter ``raw`` to True/False to tell the API which format you want (By default ``raw=True``):

.. code-block:: python

	record = collection.find_one(id_="0000aaaa1111bbbb2222cccc")
	print(record)

	Out: {"email": {"email": "obama@gmail.com"}}


	record = collection.find_one(id_="0000aaaa1111bbbb2222cccc", raw=False)
	print(record)

	Out: {"email": "<a href="mailto:obama@gmail.com">obama@gmail.com</a>"}


.. _schema:

Browse schema
---------------------------------------------------------------------------------------------------

If you want to know every single detail about your knackhq applicatoin such as:

1. How many object you have?
2. How many field you have for each object?
3. How everything been organized?
4. Setting for each field, like default value, format?
5. Application metadata?
6. etc...

``pyknackhq`` provide a convenient method to export this into a nicely formatted json file:

.. code-block:: python

	client = KnackhqClient(auth=KnackhqAuth.from_json("auth.json"))
	client.export_schema("schema.json") 

You can download an example schema file here: www.wbh-doc.com.s3.amazonaws.com/pyknackhq/example_schema.json


.. _query:

Query with filter, sort, pagination
---------------------------------------------------------------------------------------------------

If you are familiar with `MongoDB <https://www.mongodb.com/>`_, you may notice that the syntax of pyknackhq API is very similar to `pymongo <https://api.mongodb.org/python/current/>`_. Using filter, sort, pagination is super simple with pyknackhq. For arguments reference, read :meth:`pyknackhq.client.Collection.find`.

Let's see how it works with a real example:

.. code-block:: python

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


.. _dtype:

Data type constructor
---------------------------------------------------------------------------------------------------

The data structure for some field type such as ``short text`` and ``number`` is pretty simple. But some not. The raw structure for each field type can be found `here <http://helpdesk.knackhq.com/support/solutions/articles/5000446405-api-reference-field-types>`_. 

However, ``pyknackhq`` provide a Object Oriented way to construct data for some complex field, such as ``Date/Time``, ``Address``, ``Phone``, ``Link``, ``Email``, ``Currency``. And the most of python idle has auto-complete feature to help you focus on the data itself.

For example:

.. code-block:: python

	from pyknackhq import dtype
	from pyknackhq import * # Import all data type

	# the naive way
	record1 = {"address field": {
	    "street": "123 St", "city": "My City", "state": "My State", "zipcode": "12345"}}
	
	# use data type constructor via dtype
	record1 = {"address field": dtype.AddressType(
	    street="123 St", city="My City", state="My State", zipcode="12345")}

	# or using the data type constructor class
	record2 = {"address field": AddressType(
	    street="123 St", city="My City", state="My State", zipcode="12345")}

	collection.insert([record1, record2])

OK, you just finished! For the source code and programming reference, please read :mod:`API Reference <pyknackhq>`.