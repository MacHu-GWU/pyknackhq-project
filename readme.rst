pyknackhq API documentation
================================================================================

.. image:: http://sqlite4dummy-project.readthedocs.org/_static/sqlite4dummy-logo.jpg
	:width: 500px
	:height: 500px

Quick links:

- `Home page <https://github.com/MacHu-GWU/sqlite4dummy-project>`_
- `Online Documentation <http://sqlite4dummy-project.readthedocs.org/>`_
- `PyPI download <https://pypi.python.org/pypi/sqlite4dummy>`_
- `Install <install_>`_


English Introduction
--------------------------------------------------------------------------------

``sqlite4dummy`` is a high level Python sqlite3 database API. 


- What ``sqlite4dummy`` can do?

	1. Provide an OOD database syntax, allow developer doing regular CRUD and DB level operation **without writing any SQL**.
	2. Extend ability of SQL with Python, so seamlessly combine benefits of these two.
	3. Provide a feasible way to **save/read any Python pickable type to/from database.** Once the column is defined, no extra code is needed.
	4. **Ultra fast speed** that beat MySql, Postgres, Oracle, MSSQL...

- Intended audience:

	1. developer
	2. **data analyst deal with large volumn data**
	3. **data scientist**
	4. test engineer
	5. non-dba developer

- Highlights:

	1. Faster than the Top Database Project in Python Community - ``sqlalchemy``.
	2. Human language like syntax, minimal code is needed.
	3. A lots of vanilla method are provided for frequent-used work and data manipulation.

- Why sqlite?

	One of a common complain I heard for R/Matlab is that: It is too slow with large amount of data! sqlite is a database that:

	1. single file (no software install needed) portable
	2. ultra fast, (C implementation), high speed I/O

	Although sqlite doens't provide features like ``user group``, ``transaction``, ``failure over and backup``, but in non-production environment, we don't need it at all! But **we can always take the benefit of high I/O performance and "out of box, no setup needed" in development and data analysis!**

- why ``sqlite4dummy`` beat ``sqlalchemy`` in sqlite?

	1. In bulk insert operation, sometime we meet primary key conflict. In this scenario, we have to insert records one by one, catch the exception and handle it. Because Sqlalchemy is created to be compatible with most of database system, the way Sqlalchemy handle the exception is rollback. But, sqlite is so special. In sqlite, there's only one writer is allowed at one time, and there's no transaction. That's why sqlite don't need the rollback mechanism. In the sqlite Python generic API, we can simple pass that exception. As result, **the generic API is 50-100 times faster than Sqlalchemy** when there's conflict in bulk insert.

	2. Sqlalchemy use Rowproxy to preprocess the data that cursor returns. After that, we can visit value by the column name. But sometime, we actually don't need this feature. A better way is to activate this feature when we need it. That makes **Sqlalchemy is 1.5 to 3 times slower generic API**.

One final comment, you can use ``Sqlite3Engine.execute("any sql...")`` to execute any SQL with generic sqlite3 Python API for those features ``sqlite4dummy`` doesn't have (such as foreign key, left joint).

Thank you for using ``sqlite4dummy``, for installation, click `here <install_>`_.


Chinese Introduction (中文介绍)
--------------------------------------------------------------------------------

``sqlite4dummy`` 是一个 ``sqlite`` 数据库的简单API库。 目的是 **为数据分析人员, 和非数据库专业的开发者** 使用数据提供一套: 类似人类的语言, 没有冗余代码, 不用写纯SQL语句的数据库解决方案。 让非计算机背景的数据分析人员也能轻松愉快的使用sqlite数据库带来的极大便利。

- ``sqlite4dummy`` 能做什么?

	``sqlite4dummy`` 是一个建造于Python原生 ``sqlite3`` 模块之上的 ``sqlite`` 数据库的一套面向对象API。 其特点是能让用户在不写一行SQL语句的情况下, 对数据库进行常规的 "增删查改" 以及数据库维护的工作。 并且由于使用的是数据库中抽象概念的对象作为接口, 所以让数据库进行批量复杂操作变得可编程化。 使得能做许多SQL所不能做的事情。

- ``sqlite4dummy`` 适合什么人用?

	开发者, 利用数据库的高吞吐性能进行数据分析的人, 数据科学家, 测试人员和非数据库管理员开发者。

- ``sqlite4dummy`` 有什么亮点?

	1. 速度超快, 快于Python社区第一的关系数据库项目 ``sqlalchemy``
	2. 语法类似人类语言, 易读, 使开发时需要写的代码量大量减少
	3. 提供了很多额外的快捷方法(vanilla method)

- 为什么要用 ``sqlite`` 数据库?

	sqlite由于并没有很多其他关系数据库在运维方面的复杂功能, 所以使得 **性能非常优异**。 这一特性 **非常适合科学学科的工作者进行大容量的数据分析**。 例如在处理大于1G以上的csv文件时, 将所有数据放入数据库, 建立索引, 进行查找的速度要远远快于直接对数据文件进行处理。 

	而R, Matlab等语言都需要将数据全部放入内存中才能进行处理。 而使用数据库作为中间件储存数据, 然后利用其高吞吐性能进行处理数据, 使得人们能掌控的数据量上限大大增加。

- 相比 ``sqlalchemy``, ``sqlite4dummy`` 有什么优势?

	SA为了能够兼容所有主流关系数据库, 所以牺牲了一些性能。 SA在数据库运维, 以及ORM的情况下有很多功能非常有用, 但是在许多情况下, 例如数据分析中, 并不能给我们带来多少便利。

	对于数据科学家而言, sqlite是一个非常适合加速IO的数据库。单文件, C实现, 简单高速, 
	这些特性都非常适合分析中等大小(1GB - 1TB)的数据集。而Transaction, Session, User Group这些功能, 我们并不需要。

	此外, SA在性能上有两个致命的弱点:

	1. SA在执行 ``Select`` 的时候, 调用了一种叫做 ``Rowproxy`` 的机制, 将所有的行打包成字典, 方便我们进行读取。这一特性我们并不是100%的需要, 而我们完全可以在需要的时候, 再打包成字典。 这使得SA **在Select返回大量数据的情况下, 要比 ``sqlite4dummy`` 慢50%左右。**

	2. SA在执行 ``Insert`` 的时候, 如果发生了 ``primary key conflict``, 由于SA需要兼容所有的数据库,所以SA使用了 ``rollback`` 机制。 而由于sqlite3只支持单线程的write, 所以在处理冲突的时候要比多线程简单很多, 导致SA的速度在 **当写入的数据与数据表中的数据有冲突的时候, 速度要比原生sqliteAPI慢几十倍甚至百倍。**

目前 ``sqlite4dummy`` 没有提供定义 ``foreign key`` 的语法, 但是你可以使用: ``Sqlite3Engine.execute("any sql...")`` 进行定义。 换言之, 所有 ``sqlite4dummy`` 没有的功能, 都可以通过这一方法调用原生的SQL语句完成。


.. _install:

Install
---------------------------------------------------------------------------------------------------

``sqlite4dummy`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install sqlite4dummy

To upgrade to latest version:

.. code-block:: console
	
	$ pip install --upgrade sqlite4dummy