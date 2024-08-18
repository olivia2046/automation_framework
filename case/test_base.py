# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2023/4/10 17:47
desc:
'''
import os
import base.globalvars as glo

class TestBase:
    """测试基类

    """
    def setup(self):
        self.add_contextual_info("测试用例开始：%s"%os.environ.get('PYTEST_CURRENT_TEST').split('::')[-1].split(' ')[0],"info")


    def add_contextual_info(self, text, level):
        """添加上下文相关信息，主要为browserstack运行时向browserstack发送定制化log以便debug和track

        :param text: annotation log文本
        :param level: log level, info/warn/debug/error

        :return:
        """
        if "browserstack" in glo.get_value("config_name") and self.driver is not None:
            self.driver.execute_script(
                'browserstack_executor: {"action": "annotate", "arguments": {"data":"%s", "level": "%s"}}'%(text,level))

    def teardown(self):
        self.add_contextual_info("测试用例结束：%s" % os.environ.get('PYTEST_CURRENT_TEST').split('::')[-1].split(' ')[0],
                                 "info")
