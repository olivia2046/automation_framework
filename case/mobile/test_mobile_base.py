# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2023/3/7 9:52
desc: 移动端测试用例基类
'''
import base.globalvars as glo
from case.test_base import TestBase


class TestMobileBase(TestBase):
    pass
    # def mark_case(self, status, reason=""):
    #     if "browserstack" in glo.get_value("config_name"):
    #         self.driver.execute_script(
    #             'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": ""}}')