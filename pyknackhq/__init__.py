#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pyknackhq is the most elegant way to access and manipulate knackhq API.

Full documentation is at http://www.wbh-doc.com.s3.amazonaws.com/pyknackhq/index.html

Quick start guide is at http://www.wbh-doc.com.s3.amazonaws.com/pyknackhq/quick%20start.html

:copyright: 2015 by Sanhe Hu.
:license: MIT, see LICENSE for more details.
"""

from .client import KnackhqAuth, KnackhqClient
from .schema import Application
from .datatype import (dtype, 
    ShortTextType, ParagraphTextType, YesNoType, 
    SingleChoiceType, MultipleChoiceType, 
    DateTimeType, DateTimeFromToType, NumberType, 
    AddressType, NameType, LinkType, EmailType, 
    PhoneType, RichTextType, TimerType, CurrencyType, RatingType,
)

__version__ = "0.0.2"
__short_description__ = "knackhq root access Python API."