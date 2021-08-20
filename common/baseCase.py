#!/usr/bin/env
# python-*- coding: UTF-8 -*-
"""
@Project ：-D94
@File    ：baseCase.py
@Author  ：ld_949253@163.com,lucas0099999@gmail.com
@Date    ：2021/8/18 2:55 下午
"""
import re
import sys
from time import sleep, time
from urllib.error import URLError

from common.exceptions import OutOfScopeException
from config import settings
from utils import js_utils
from utils import worlds
from selenium.common.exceptions import WebDriverException

class BaseCase(object):

    def __init__(self):
        self.slow_mode = None
        self.demo_sleep = None
        self.demo_mode = None
        self.js_checking_on = None
        self.driver = None
        self.browser = None
        self.timeout_multiplier = None
        self._language = "Chinese"

    def open(self, url):
        self.__check_scope()
        if type(url) is str:
            url = url.strip()
        if (type(url) is not str) or not self.__looks_like_a_page_url(url):
            msg = '是否忘记输入了前缀 "http:" or "https:"?'
            raise Exception('Invalid URL: "%s"\n%s' % (url, msg))
        if url.startswith("://"):
            url = "https" + url
        if self.browser == "safari" and url.startswith("data:"):
            url = re.escape(url)
            url = self.__escape_quotes_if_needed(url)
            self.execute_script("window.location.href='%s';" % url)
        else:
            self.driver.get(url)
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def __check_scope(self):
        if hasattr(self, "browser"):
            return
        else:
            message = (
                "\n It looks like you are trying to call a SeleniumBase method"
                "\n from outside the scope of your test class's `self` object,"
                "\n which is initialized by calling BaseCase's setUp() method."
                "\n The `self` object is where all test variables are defined."
                "\n If you created a custom setUp() method (that overrided the"
                "\n the default one), make sure to call super().setUp() in it."
                "\n When using page objects, be sure to pass the `self` object"
                "\n from your test class into your page object methods so that"
                "\n they can call BaseCase class methods with all the required"
                "\n variables, which are initialized during the setUp() method"
                "\n that runs automatically before all tests called by pytest."
            )
            raise OutOfScopeException(message)

    def __looks_like_a_page_url(self, url):
        """
        匹配url相似度
        :param url:
        :return:
        """
        if (
                url.startswith("http:")
                or url.startswith("https:")
                or url.startswith("://")
                or url.startswith("chrome:")
                or url.startswith("about:")
                or url.startswith("data:")
                or url.startswith("file:")
                or url.startswith("edge:")
                or url.startswith("opera:")
        ):
            return True
        else:
            return False

    def __escape_quotes_if_needed(self, string):
        """
        检查是否存在需要转义的引号
        :param string:
        :return:
        """
        return js_utils.escape_quotes_if_needed(string)

    def execute_script(self, script, *args, **kwargs):
        """
        执行script语句，操作元素
        :param script:
        :param args:
        :param kwargs:
        :return:
        """
        self.__check_scope()
        return self.driver.execute_script(script, *args, **kwargs)

    def wait_for_ready_state_complete(self, timeout=None):
        """
        等待状态加载完成
        :param timeout:
        :return:
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.EXTREME_TIMEOUT
        if self.timeout_multiplier and timeout == settings.EXTREME_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        is_ready = js_utils.wait_for_ready_state_complete(self.driver, timeout)
        js_utils.wait_for_angularjs(self.driver, timeout=settings.MINI_TIMEOUT)
        if self.js_checking_on:
            self.assert_no_js_errors()
        if self.ad_block_on:
            # If the ad_block feature is enabled, then block ads for new URLs
            current_url = self.get_current_url()
            if not current_url == self.__last_page_load_url:
                sleep(0.02)
                self.ad_block()
                sleep(0.02)
                if self.is_element_present("iframe"):
                    sleep(0.1)  # iframe ads take slightly longer to load
                    self.ad_block()  # Do ad_block on slower-loading iframes
                self.__last_page_load_url = current_url
        return is_ready

    def __get_new_timeout(self, timeout):
        """
        创建新的超时时间
        :param timeout:
        :return:
        """
        import math
        self.__check_scope()
        try:
            timeout_multiplier = float(self.timeout_multiplier)
            if timeout_multiplier <= 0.5:
                timeout_multiplier = 0.5
            timeout = int(math.ceil(timeout_multiplier * timeout))
            return timeout
        except TimeoutError:
            return timeout

    def __demo_mode_pause_if_active(self, tiny=False):
        if self.demo_mode:
            wait_time = settings.MODE_TIMEOUT
            if self.demo_sleep:
                wait_time = float(self.demo_sleep)
            if not tiny:
                sleep(wait_time)
            else:
                sleep(wait_time / 3.4)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def __slow_mode_pause_if_active(self):
        if self.slow_mode:
            wait_time = settings.DEFAULT_DEMO_MODE_TIMEOUT
            if self.demo_sleep:
                wait_time = float(self.demo_sleep)
            sleep(wait_time)

    def get_current_url(self):
        """
        获取当前url地址
        :return:
        """
        self.__check_scope()
        current_url = self.driver.current_url
        if "%" in current_url and sys.version_info[0] >= 3:
            try:
                from urllib.parse import unquote
                current_url = unquote(current_url, errors="strict")
            except URLError:
                pass
        return current_url


def assert_no_js_errors(self, seleniumbase=None):
    """
    断言不存在javascript SEVERE"-level 级别的错误
    该方法只支持Chrome (non-headless) and Chrome-based 浏览器
    不支持运行在 Firefox, Edge, IE，和一些其他浏览器
    :param self:
    :param seleniumbase:
    :return:
    """
    self.__check_scope()
    sleep(0.1)
    try:
        browser_logs = self.driver.get_log("browser")
    except (ValueError, WebDriverException):
        # If unable to get browser logs, skip the assert and return.
        return
    errors = []
    for entry in browser_logs:
        if entry["level"] == "SEVERE":
            errors.append(entry['message'])
    if len(errors) > 0:
        current_url = self.get_current_url()
        raise Exception(
            "JavaScript errors found on %s => %s" % (current_url, errors)
        )
    if self.demo_mode:
        if self.browser == "chrome" or self.browser == "edge":
            a_t = "ASSERT NO JS ERRORS"
            if self._language != "English":
                a_t = worlds.SD.translate_assert_no_js_errors(self._language)
            messenger_post = "%s" % a_t
            self.__highlight_with_assert_success(messenger_post, "html")