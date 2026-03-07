# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2022/10/20 18:01
desc:
'''
import logging

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import base.globalvars as glo
from selenium.webdriver.support import expected_conditions as EC #don't remove this line as condition is evaluated dynamically


class BasePage:
    # black list of exceptional pop ups. It there're multiple popups together, try to define them in the order they are displayed
    # e.g. [(By.ID, "XXXX"),(By.ID, "YYYY")]
    _black_list = []

    def __int__(self, driver: WebDriver):
        self.driver = driver

    def find_element(self, locator, timeout=5, condition='visibility_of_element_located'):
        """find element by locator

        :param locator: tuple of element locator
        :param timeout: timeout in seconds
        :param condition: selenium.webdriver.support.expected_conditions，visibility_of_element_located by default
                        visibility_of_element_located
                        presence_of_element_located
                        element_located_to_be_selected
                        element_located_selection_state_to_be
                        element_to_be_clickable
                        invisibility_of_element
                        ...

        :return:
        """
        try:
            #return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return WebDriverWait(self.driver, timeout).until(eval("EC." + condition)(locator))
        except Exception as e:
            return None


    def find_elements(self, locator):
        """查找多个元素 Todo: 超时：

        :param locator: 元素定位元组

        :return:
        """
        try:
            return self.driver.find_elements(*locator)
        except Exception as e:
            logging.error(e)
            #self.handle_exception()
        return self.driver.find_elements(*locator)


    def find_element_and_click(self, locator, timeout=5, condition='element_to_be_clickable'):
        """查找元素并点击

        :param locator: 元素定位元组
        :param timeout: 超时时间，单位为秒

        :return:
        """
        self.find_element(locator, timeout, condition).click()

    def click(self, locator):
        """Alias for find_element_and_click"""
        # element = self.wait.until(EC.element_to_be_clickable(locator))
        # element.click()
        self.find_element_and_click(locator)

    def find_element_and_input(self, locator, text, timeout=10):
        """find element and input text

        :param locator: tuple of element locator
        :param text:  text input
        :param timeout: timeout time, in seconds

        :return:
        """
        element = self.find_element(locator, timeout, condition='element_to_be_clickable')
        element.click()
        element.clear()
        element.send_keys(text)



    def handle_exception(self):
        """set implicit wait time to 0(do not wait long time if elements on blacklist cannot be found)

        :return:
        """

        self.driver.implicitly_wait(0)
        for locator in self._black_list:
            elements = self.driver.find_elements(*locator)
            if len(elements)>=1:
                elements[0].click()
            else:
                logging.info("%s not found") %str(locator)
        # restore implicit wait time
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


    def hover_over_element(self, locator):
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()



