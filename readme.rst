Welcome to pyknackhq documentation
================================================================================

`Knackhq <https://www.knackhq.com/>`_ is an awesome developer tools. It allows developer to build a user friendly, database backed web application in few clicks. So the non-developer can enjoy the power and convenience of non-sql database with no Pain. However, the developer may still want to manipulate it via programming, that's how knackhq API for. Python is the easiest powerful general purpose programming language. Most of new technique put supporting Python API in their top 3 list. I don't know why there's no official Python API for this great app - Knackhq.

Highlight:

By default, the naive api using object_key to `construct encoded endpoint url <https://api.knackhq.com/v1/objects/object_key/records>`_. If you want to `insert a record <http://helpdesk.knackhq.com/support/solutions/articles/5000446111-api-reference-root-access#create>`_, data key has to be field_key, which is not convenient and straightforward. And when you `execute a query <http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api#response>`_, it returns data with field_key only. I have to say, that's sucks.

Fortunately, pyknackhq support both object_key/object_name, field_key/field_name for all kinds of API operation. And the syntax is super friendly like human language. With preserving the convenience, pyknackhq also provides rich features and options for developer to customize the behavior of API call.

Quick Link:

- `Github <https://github.com/MacHu-GWU/pyknackhq-project>`_
- `pyknackhq PyPI Homepage <https://pypi.python.org/pypi/pyknackhq>`_
- `Online Documentation <http://www.wbh-doc.com.s3.amazonaws.com/pyknackhq/index.html>`_
- `Naive knackhq API <http://helpdesk.knackhq.com/support/solutions/articles/5000444173-working-with-the-api>`_ 
- `Class method reference <http://www.wbh-doc.com.s3.amazonaws.com/pyknackhq/pyknackhq/__init__.html#module-pyknackhq>`_

.. _install:

Install
----------------------------------------------------------------------------------------------------

``pyknackhq`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install pyknackhq

To upgrade to latest version:

.. code-block:: console
	
	$ pip install --upgrade pyknackhq