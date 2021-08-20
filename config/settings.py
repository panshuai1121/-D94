#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：-D94
@File    ：settings.py
@Author  ：ld_949253@163.com,lucas0099999@gmail.com
@Date    ：2021/8/18 3:46 下午
"""

"""
等待页面元素出现的默认最长时间（以秒为单位）
"""
MINI_TIMEOUT = 2
SMALL_TIMEOUT = 6
LARGE_TIMEOUT = 10
EXTREME_TIMEOUT = 30

"""
设置各浏览器使用wait_for_ready_state_complete 等待资源加载结束后操作
"""
# Called after self.open(url) or self.open_url(url), NOT self.driver.open(url)
WAIT_FOR_RSC_ON_PAGE_LOADS = True
# Called after self.click(selector), NOT element.click()
WAIT_FOR_RSC_ON_CLICKS = True

"""
验证有限时间配置
"""
time_limit = 10
start_time_ms = 5
time_limit_ms = 10

"""
默认模块加载时间
"""
DEFAULT_MODE_TIMEOUT = 0.5

"""
ANGULARJS 配置项
"""
WAIT_FOR_ANGULARJS = True
