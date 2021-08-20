#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：-D94
@File    ：exceptions.py
@Author  ：ld_949253@163.com,lucas0099999@gmail.com
@Date    ：2021/8/18 3:27 下午
"""

""" common Exceptions
    NoSuchFileException => Used by self.assert_downloaded_file(...)
    NotUsingChromeException => Used by Chrome-only methods if not using Chrome
    OutOfScopeException => Used by BaseCase methods when setUp() is skipped
    TimeLimitExceededException => Used by "--time-limit=SECONDS"
"""


class NoSuchFileException(Exception):
    pass


class NotUsingChromeException(Exception):
    pass


class OutOfScopeException(Exception):
    pass


class TimeLimitExceededException(Exception):
    pass
