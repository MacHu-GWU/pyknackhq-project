#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is re-pack of some json utility functions.

- :func:`load_js`: Load Json from file. If file are not exists, returns 
  user defined ``default value``.
        
- :func:`dump_js`: Dump Json serializable object to file.
        
- :func:`safe_dump_js`: An atomic write version of dump_js, silently overwrite 
  existing file.
        
- :func:`js2str`: Encode js to nicely formatted human readable string.
    
- :func:`prt_js`: Print Json in pretty format.


Highlight
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- :func:`load_js`, :func:`dump_js`, :func:`safe_dump_js` support gzip compress, 
  size is **10 - 20 times** smaller in average.


Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python2: Yes
- Python3: Yes


Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- None


Class, method, function, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import print_function, unicode_literals
import json, gzip
import os, shutil
import time

def load_js(abspath, default=dict(), compress=False, enable_verbose=True):
    """Load Json from file. If file are not exists, returns ``default``.

    :param abspath: File path. Use absolute path as much as you can. File 
        extension has to be ``.json`` or ``.gz``. (for compressed Json)
    :type abspath: string

    :param default: (default dict()) If ``abspath`` not exists, return the 
        default Python object instead.

    :param compress: (default False) Load from a gzip compressed Json file.
        Check :func:`dump_js()<dump_js>` function for more information.
    :type compress: boolean
    
    :param enable_verbose: (default True) Trigger for message.
    :type enable_verbose: boolean

    Usage::

        >>> from weatherlab.lib.dataIO.js import load_js
        >>> load_js("test.json") # if you have a json file
        Loading from test.json...
            Complete! Elapse 0.000432 sec.
        {'a': 1, 'b': 2}

    **中文文档**

    从Json文件中读取数据

    参数列表
    
    :param abspath: 文件路径, 扩展名需为 ``.json`` 或 ``.gz``
    :type abspath: ``字符串``

    :param default: (默认 dict()) 如果文件路径不存在, 则会返回一个默认的Python对象。
    
    :param compress: (默认 False) 是否从一个gzip压缩过的Json文件中读取数据。 请
        参考 :func:`dump_js()<dump_js>` 获得更多信息.
    :type compress: ``布尔值``

    :param enable_verbose: (默认 True) 是否打开信息提示开关, 批处理时建议关闭.
    :type enable_verbose: ``布尔值``
    """
    abspath = str(abspath) # try stringlize
    
    if compress: # check extension name
        if os.path.splitext(abspath)[1] != ".gz":
            raise Exception("compressed json has to use extension '.gz'!")
    else:
        if os.path.splitext(abspath)[1] != ".json":
            raise Exception("file extension are not '.json'!")

    if enable_verbose:
        print("\nLoading from %s..." % abspath)
        st = time.clock()
        
    if os.path.exists(abspath): # exists, then load
        if compress:
            with gzip.open(abspath, "rb") as f:
                js = json.loads(f.read().decode("utf-8"))
        else:
            with open(abspath, "r") as f:
                js = json.load(f)
        if enable_verbose:
            print("\tComplete! Elapse %.6f sec." % (time.clock() - st) )
        return js
    
    else:
        if enable_verbose:
            print("\t%s not exists! cannot load! Create an default object "
                  "instead" % abspath)
        return default

def dump_js(js, abspath, 
            fastmode=False, replace=False, compress=False, enable_verbose=True):
    """Dump Json serializable object to file.
    Provides multiple choice to customize the behavior.
    
    :param js: Serializable python object.
    :type js: dict or list
    
    :param abspath: ``save as`` path, file extension has to be ``.json`` or ``.gz`` 
        (for compressed json).
    :type abspath: string
    
    :param fastmode: (default False) If ``True``, then dumping json without 
        sorted keys and pretty indent, and it's faster and smaller in size.
    :type fastmode: boolean
    
    :param replace: (default False) If ``True``, when you dump json to a existing 
        path, it silently overwrite it. If False, an exception will be raised.
        Default False setting is to prevent overwrite file by mistake.
    :type replace: boolean
    
    :param compress: (default False) If ``True``, use GNU program gzip to 
        compress the json file. Disk usage can be greatly reduced. But you have 
        to use :func:`load_js(abspath, compress=True)<load_js>` in loading.
    :type compress: boolean
    
    :param enable_verbose: (default True) Trigger for message.
    :type enable_verbose: boolean

    Usage::

        >>> from weatherlab.lib.dataIO.js import dump_js
        >>> js = {"a": 1, "b": 2}
        >>> dump_js(js, "test.json", replace=True)
        Dumping to test.json...
            Complete! Elapse 0.002432 sec

    **中文文档**
    
    将Python中可被序列化的"字典", "列表"以及他们的组合, 按照Json的编码方式写入文件
    文件
    
    参数列表
    
    :param js: 可Json化的Python对象
    :type js: ``字典`` 或 ``列表``
    
    :param abspath: 写入文件的路径。扩展名必须为``.json``或``.gz``, 其中gz用于被压
        缩的Json
    :type abspath: ``字符串``
    
    :param fastmode: (默认 False) 当为``True``时, Json编码时不对Key进行排序, 也不
        进行缩进排版。这样做写入的速度更快, 文件的大小也更小。
    :type fastmode: "布尔值"
    
    :param replace: (默认 False) 当为``True``时, 如果写入路径已经存在, 则会自动覆盖
        原文件。而为``False``时, 则会抛出异常。防止误操作覆盖源文件。
    :type replace: "布尔值"
    
    :param compress: (默认 False) 当为``True``时, 使用开源压缩标准gzip压缩Json文件。
        通常能让文件大小缩小10-20倍不等。如要读取文件, 则需要使用函数
        :func:`load_js(abspath, compress=True)<load_js>`.
    :type compress: "布尔值"
    
    :param enable_verbose: (默认 True) 是否打开信息提示开关, 批处理时建议关闭.
    :type enable_verbose: "布尔值"
    """
    abspath = str(abspath) # try stringlize
    
    if compress: # check extension name
        root, ext = os.path.splitext(abspath)
        if ext != ".gz":
            if ext != ".tmp":
                raise Exception("compressed json has to use extension '.gz'!")
            else:
                _, ext = os.path.splitext(root)
                if ext != ".gz":
                    raise Exception("compressed json has to use extension '.gz'!")
    else:
        root, ext = os.path.splitext(abspath)
        if ext != ".json":
            if ext != ".tmp":
                raise Exception("file extension are not '.json'!")
            else:
                _, ext = os.path.splitext(root)
                if ext != ".json":
                    raise Exception("file extension are not '.json'!")
    
    if enable_verbose:
        print("\nDumping to %s..." % abspath)
        st = time.clock()
    
    if os.path.exists(abspath): # if exists, check replace option
        if replace: # replace existing file
            if fastmode: # no sort and indent, do the fastest dumping
                if compress:
                    with gzip.open(abspath, "wb") as f:
                        f.write(json.dumps(js).encode("utf-8"))
                else:
                    with open(abspath, "w") as f:
                        json.dump(js, f)
            else:
                if compress:
                    with gzip.open(abspath, "wb") as f:
                        f.write(json.dumps(js, sort_keys=True,
                            indent=4, separators=("," , ": ")).encode("utf-8"))
                else:
                    with open(abspath, "w") as f:
                        json.dump(js, f, sort_keys=True, 
                                  indent=4, separators=("," , ": ") )
        else: # stop, print error message
            raise Exception("\tCANNOT WRITE to %s, it's already "
                            "exists" % abspath)
                
    else: # if not exists, just write to it
        if fastmode: # no sort and indent, do the fastest dumping
            if compress:
                with gzip.open(abspath, "wb") as f:
                    f.write(json.dumps(js).encode("utf-8"))
            else:
                with open(abspath, "w") as f:
                    json.dump(js, f)
        else:
            if compress:
                with gzip.open(abspath, "wb") as f:
                    f.write(json.dumps(js, sort_keys=True,
                        indent=4, separators=("," , ": ")).encode("utf-8"))
            else:
                with open(abspath, "w") as f:
                    json.dump(js, f, sort_keys=True, 
                              indent=4, separators=("," , ": ") )
            
    if enable_verbose:
        print("\tComplete! Elapse %.6f sec" % (time.clock() - st) )

def safe_dump_js(js, abspath, 
                 fastmode=False, compress=False, enable_verbose=True):
    """A stable version of dump_js, silently overwrite existing file.

    When your program been interrupted, you lose nothing. Typically if your
    program is interrupted by any reason, it only leaves a incomplete file.
    If you use replace=True, then you also lose your old file.
    
    So a bettr way is to:
    
    1. dump json to a temp file.
    2. when it's done, rename it to #abspath, overwrite the old one.

    This way guarantee atomic write.

    :param js: Serializable python object.
    :type js: dict or list
    
    :param abspath: ``save as`` path, file extension has to be ``.json`` or ``.gz`` 
        (for compressed json).
    :type abspath: string
    
    :param fastmode: (default False) If ``True``, then dumping json without 
        sorted keys and pretty indent, and it's faster and smaller in size.
    :type fastmode: boolean
    
    :param compress: (default False) If ``True``, use GNU program gzip to 
        compress the json file. Disk usage can be greatly reduced. But you have 
        to use :func:`load_js(abspath, compress=True)<load_js>` in loading.
    :type compress: boolean
    
    :param enable_verbose: (default True) Trigger for message.
    :type enable_verbose: boolean

    Usage::

        >>> from weatherlab.lib.dataIO.js import dump_js
        >>> js = {"a": 1, "b": 2}
        >>> safe_dump_js(js, "test.json")
        Dumping to test.json...
            Complete! Elapse 0.002432 sec

    **中文文档**

    在对文件进行写入时, 如果程序中断, 则会留下一个不完整的文件。如果你使用了覆盖式
    写入, 则你同时也丢失了原文件。所以为了保证写操作的原子性(要么全部完成, 要么全部
    都不完成), 更好的方法是: 首先将文件写入一个临时文件中, 完成后再讲文件重命名, 
    覆盖旧文件。这样即使中途程序被中断, 也仅仅是留下了一个未完成的临时文件而已, 不会
    影响原文件。

    参数列表

    :param js: 可Json化的Python对象
    :type js: ``字典`` 或 ``列表``
    
    :param abspath: 写入文件的路径。扩展名必须为 ``.json`` 或 ``.gz``, 其中gz用于被压
        缩的Json
    :type abspath: ``字符串``
    
    :param replace: (默认 False) 当为``True``时, 如果写入路径已经存在, 则会自动覆盖
        原文件。而为``False``时, 则会抛出异常。防止误操作覆盖源文件。
    :type replace: ``布尔值``
    
    :param compress: (默认 False) 当为``True``时, 使用开源压缩标准gzip压缩Json文件。
        通常能让文件大小缩小10-20倍不等。如要读取文件, 则需要使用函数
        :func:`load_js(abspath, compress=True)<load_js>`.
    :type compress: ``布尔值``
    
    :param enable_verbose: (默认 True) 是否打开信息提示开关, 批处理时建议关闭.
    :type enable_verbose: ``布尔值``
    """
    abspath = str(abspath) # try stringlize
    temp_abspath = "%s.tmp" % abspath
    dump_js(js, temp_abspath, fastmode=fastmode, 
            replace=True, compress=compress, enable_verbose=enable_verbose)
    shutil.move(temp_abspath, abspath)
    
def js2str(js, sort_keys=True, indent=4):
    """Encode js to nicely formatted human readable string. (utf-8 encoding)

    Usage::

        >>> from weatherlab.lib.dataIO.js import js2str
        >>> s = js2str({"a": 1, "b": 2})
        >>> print(s)
        {
            "a": 1,
            "b": 2
        }

    **中文文档**

    将可Json化的Python对象转化成格式化的字符串。
    """
    return json.dumps(js, sort_keys=sort_keys, 
                      indent=indent, separators=("," , ": "))

def prt_js(js, sort_keys=True, indent=4):
    """Print Json in pretty format.
    There's a standard module pprint, can pretty print python dict and list.
    But it doesn't support sorted key. That why we need this func.

    Usage::

        >>> from weatherlab.lib.dataIO.js import prt_js
        >>> prt_js({"a": 1, "b": 2})
        {
            "a": 1,
            "b": 2
        }

    **中文文档**

    以人类可读的方式打印可Json化的Python对象。
    """
    print(js2str(js, sort_keys, indent) )
    
############
# Unittest #
############

if __name__ == "__main__":
    import unittest
    
    class JSUnittest(unittest.TestCase):
        def test_write_and_read(self):
            data = {"a": [1, 2], "b": ["是", "否"]} 
            safe_dump_js(data, "data.json")
            data = load_js("data.json")
            self.assertEqual(data["a"][0], 1)
            self.assertEqual(data["b"][0], "是")
             
        def test_js2str(self):
            data = {"a": [1, 2], "b": ["是", "否"]} 
            prt_js(data)
        
        def test_compress(self):
            data = {"a": list(range(32)),
                    "b": list(range(32)),}
            safe_dump_js(data, "data.gz", compress=True)
            prt_js(load_js("data.gz", compress=True))
            
        def tearDown(self):
            for path in ["data.json", "data.gz"]:
                try:
                    os.remove(path)
                except:
                    pass
            
    unittest.main()