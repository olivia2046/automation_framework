# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2022/10/20 18:01
desc:
'''
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base.globalvars as glo


class BasePage:

    _black_list = [] # 异常弹窗黑名单，如果有多个异常弹窗会同时出现，尽量按可能出现的顺序定义。例如：[(By.ID, "XXXX"),(By.ID, "YYYY")]

    def __int__(self, driver: WebDriver):
        self.driver = driver

    def find_element(self, locator, timeout=5, condition='visibility_of_element_located', skip_error_handle=False):
        """查找元素

        :param locator: 元素定位元组
        :param timeout: 超时时间，单位为秒
        :param condition: 预期的expected_conditions条件，默认为visibility_of_element_located
        :param skip_error_handle: 是否跳过需要handle_exception
                                正常情况预期找到元素时，可能由于黑名单上一些元素遮挡导致找不到元素，需要handle_exception;
                                正常情况预期找不到元素时（如成功登录后找不到验证码错误的提示、有权限时找不到无权限提示框等）

        :return:
        """
        try:
            #return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return WebDriverWait(self.driver, timeout).until(eval("EC." + condition)(locator))
        except Exception as e:
            if not skip_error_handle:
                self.handle_exception()
                # 处理完异常（异常弹窗等）后，再次查找指定的元素
                # self.find_element(locator) # 可处理未按指定顺序处理的多个异常弹窗，但需要添加逻辑避免死循环

                try:
                    return WebDriverWait(self.driver, timeout).until(eval("EC." + condition)(locator))
                except Exception as e:
                    logging.error("e: %s"%str(locator))
                    raise e
            else:
                raise e


    def find_elements(self, locator):
        """查找多个元素 Todo: 超时：

        :param locator: 元素定位元组

        :return:
        """
        try:
            return self.driver.find_elements(*locator)
        except Exception as e:
            logging.error(e)
            self.handle_exception()
        return self.driver.find_elements(*locator)


    def find_element_and_click(self, locator, timeout=5, condition='element_to_be_clickable',skip_error_handle=False):
        """查找元素并点击

        :param locator: 元素定位元组
        :param timeout: 超时时间，单位为秒

        :return:
        """
        self.find_element(locator, timeout, condition, skip_error_handle).click()

    def find_element_and_input(self, locator, text, timeout=10):
        """查找元素并输入文本

        :param locator: 元素定位元组
        :param text:  输入的文本
        :param timeout: 超时时间，单位为秒

        :return:
        """
        element = self.find_element(locator, timeout, condition='element_to_be_clickable')
        element.click()
        element.clear().send_keys(text)



    def handle_exception(self):
        #设置隐式等待时间为0（黑名单上元素找不到不长时间等待）
        self.driver.implicitly_wait(0)
        for locator in self._black_list:
            elements = self.driver.find_elements(*locator)
            if len(elements)>=1:
                elements[0].click()
            else:
                logging.info("%s not found") %str(locator)
        # 恢复隐式等待时间
        self.driver.implicitly_wait(glo.get_value("implicit_wait", 10))

    def get_element_rect(self, locator, condition='visibility_of_element_located'):
        element = self.find_element(locator, condition=condition)
        return element.rect



    def press_enter_key(self):
        self.driver.press_keycode(66)


    def hide_keyboard(self):
        self.driver.hide_keyboard()
        #self.driver.press_keycode(66)  # 发送Enter键
        #android
        #self.driver.execute_script('mobile: performEditorAction', {'action': 'done'})
        #self.driver.execute_script("if (window.android) { window.android.hideKeyboard() }")
