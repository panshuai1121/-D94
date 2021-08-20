#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：-D94
@File    ：shared_utils.py
@Author  ：ld_949253@163.com,lucas0099999@gmail.com
@Date    ：2021/8/18 4:02 下午
"""
from datetime import time
from config import settings

"""
This module contains shared utility methods.
"""
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException
from common.exceptions import NoSuchFileException
from common.exceptions import TimeLimitExceededException


def format_exc(exception, message):
    """
    Formats an exception message to make the output cleaner.
    """
    if exception == Exception:
        exc = Exception
        return exc, message
    elif exception == ElementNotVisibleException:
        exc = ElementNotVisibleException
    elif exception == "ElementNotVisibleException":
        exc = ElementNotVisibleException
    elif exception == NoSuchElementException:
        exc = NoSuchElementException
    elif exception == "NoSuchElementException":
        exc = NoSuchElementException
    elif exception == NoAlertPresentException:
        exc = NoAlertPresentException
    elif exception == "NoAlertPresentException":
        exc = NoAlertPresentException
    elif exception == NoSuchAttributeException:
        exc = NoSuchAttributeException
    elif exception == "NoSuchAttributeException":
        exc = NoSuchAttributeException
    elif exception == NoSuchFrameException:
        exc = NoSuchFrameException
    elif exception == "NoSuchFrameException":
        exc = NoSuchFrameException
    elif exception == NoSuchWindowException:
        exc = NoSuchWindowException
    elif exception == "NoSuchWindowException":
        exc = NoSuchWindowException
    elif exception == NoSuchFileException:
        exc = NoSuchFileException
    elif exception == "NoSuchFileException":
        exc = NoSuchFileException
    elif type(exception) is str:
        exc = Exception
        message = "%s: %s" % (exception, message)
        return exc, message
    else:
        exc = Exception
        return exc, message
    message = _format_message(message)
    return exc, message


def _format_message(message):
    message = "\n " + message
    return message


def __time_limit_exceeded(message):
    raise TimeLimitExceededException(message)


def check_if_time_limit_exceeded():
    if settings.time_limit:
        time_limit = settings.time_limit
        now_ms = int(time.time() * 1000)
        if now_ms > settings.start_time_ms + settings.time_limit_ms:
            display_time_limit = time_limit
            plural = "s"
            if float(int(time_limit)) == float(time_limit):
                display_time_limit = int(time_limit)
                if display_time_limit == 1:
                    plural = ""
            message = (
                    "This test has exceeded the time limit of %s second%s!"
                    % (display_time_limit, plural)
            )
            message = _format_message(message)
            __time_limit_exceeded(message)
