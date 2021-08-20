#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：-D94
@File    ：js_utils.py
@Author  ：ld_949253@163.com,lucas0099999@gmail.com
@Date    ：2021/8/18 3:54 下午
"""
from selenium.common.exceptions import WebDriverException

from config import settings
from utils import shared_utils
import time


def wait_for_ready_state_complete(driver, timeout=settings.LARGE_TIMEOUT):
    """
    DOM（文档对象模型),有一个名为readyState的属性,当 this 的值变为complete时，页面资源
    加载准备完成
    :param driver:
    :param timeout:
    :return:
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        shared_utils.check_if_time_limit_exceeded()
        try:
            ready_state = driver.execute_script("return document.readyState")
        except WebDriverException:
            time.sleep(0.03)
            return True
        if ready_state == "complete":
            time.sleep(0.01)
            return True
        else:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    return False


def escape_quotes_if_needed(string):
    """
    Javascript 调用转义正确的引号，在每一个'中增加转义符号
    :param string:
    :return:
    """
    if are_quotes_escaped(string):
        if string.count("'") != string.count("\\'"):
            string = string.replace("'", "\\'")
        if string.count('"') != string.count('\\"'):
            string = string.replace('"', '\\"')
    return string


def are_quotes_escaped(string):
    """
    校验转义符号是否不匹配，如不匹配时进行可进行转义
    :param string:
    :return:
    """
    if string.count("\\'") != string.count("'") or (
            string.count('\\"') != string.count('"')
    ):
        return True
    return False


def wait_for_angularjs(driver, timeout=settings.LARGE_TIMEOUT, **kwargs):
    if not settings.WAIT_FOR_ANGULARJS:
        return