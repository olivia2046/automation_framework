# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2022/10/20 18:11
desc: 移动端Page基类
'''
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from base.po.base_page import BasePage

class MobileBasePage(BasePage):
    def __init__(self, driver: WebDriver):
        self.driver=driver
        self.os = str(self.driver.capabilities['platformName']).lower()

    def swipe_up(self, frame_locator, height_rate=1, duration = 400):
        """ 向上滑动整个纵向长度*height_rate，用于UiScrollable的scrollIntoView不工作的情况

        :param frame_locator: 滑动区域的定位
        :param height_rate: 滑动的纵向比例，1为滑动到底
        :param n_times: 滑动次数

        :return:
        """
        # frame = self.driver.find_element(*frame_locator)
        # startx = frame.location['x'] + (frame.size['width'] / 2)
        # starty = frame.location['y'] + ((frame.size['height']) - 5) * height_rate
        # endx = startx
        # endy = frame.location['y']  + 5
        # self.driver.swipe(startx, starty, endx, endy, duration)

        frame = self.driver.find_element(*frame_locator)
        startx = frame.location['x'] + (frame.size['width'] / 2)
        while height_rate>0:
            rate = height_rate if height_rate<=1 else 1
            starty = frame.location['y'] + ((frame.size['height']) - 5) * rate
            endx = startx
            endy = frame.location['y'] + 5
            self.driver.swipe(startx, starty, endx, endy, duration)
            height_rate -= 1




    def swipe_by_element(self, locator, x_offset, y_offset, duration):
        """根据指定元素滑动（以元素中心为起点，滑动指定距离）
        :param locator: webdriver locator
        :param x_offset: x的偏移距离，负数表示往左移动
        :param y_offset: y的偏移距离，负数表示往上移动
        :param duration:
        :return:
        """
        ele_rect = self.get_element_rect(locator)
        ele_center = {'x': ele_rect['x']+ele_rect['width']/2, 'y': ele_rect['y']+ele_rect['height']/2}
        self.driver.swipe(ele_center['x'], ele_center['y'], ele_center['x']+x_offset, ele_center['y']+y_offset, duration)

    def scroll_into_view(self, locator, target_locator, text):
        """
        在指定组件中下拉滑动，查找匹配的元素（用于下拉框组件）
        locator: 下拉框组件
        target_locator: 需要查找的text的定位，基于下拉框的元素定位
        text: 需要寻找的文本，精准匹配
        return: 找到的元素/False
        """
        component = self.find_element(locator)
        component_rect = {'x_middle': component.rect['x']+(component.rect['width']/2), 'y_top': component.rect['y'], 'y_floor': component.rect['y']+component.rect['height']}

        last_text = None
        not_in_rect = True
        while not_in_rect:
            page_texts = []
            elements = component.find_elements(*target_locator)
            for i in elements:
                page_texts.append(i.text)

            if text in page_texts:
                # 判断是否在页面内并且在可视范围内
                text_rect = component.find_element(AppiumBy.XPATH, f"//*[@text='{text}']").rect
                if text_rect['y']+text_rect['height'] >= component_rect['y_floor']:
                    # 页面内但不在可见范围内，向上滑动
                    self.driver.swipe(component_rect['x_middle'], component_rect['y_floor']-20, component_rect['x_middle'], component_rect['y_top'], duration=500)
                    last_text = elements[-1]
                    continue
                else:
                    # 页面内并且在可见范围内，返回元素
                    return component.find_element(AppiumBy.XPATH, f"//*[@text='{text}']")

            # 判断是否到达底部,到达底部仍没有找到，返回false
            if not last_text or (last_text.text != elements[-1].text or
                (last_text.rect['y']+last_text.rect['height'] >= component_rect['y_floor'])):
                self.driver.swipe(component_rect['x_middle'], component_rect['y_floor']-20, component_rect['x_middle'], component_rect['y_top'], duration=500)
                last_text = elements[-1]
            else:
                return False

    def get_locator(self, prefix):
        """获取指定os上的locator

        :param prefix: locator前缀
        :param os: 系统 ios/android，默认ios

        :return: 指定os对应的locator
        """

        return getattr(self, prefix + self.os)

    def update_location_permission(self, os='ios', permission='Always'):
        """

        :param os: 系统类型，ios/android，默认ios
        :param permission: 权限-‘Always/While Using the App’

        :return:
        """
        # set Location Access to Always
        if os.lower()=='ios':
            self.driver.execute_script('browserstack_executor: {\"action\": \"updateAppSettings\", \"arguments\": '
                                       '{\"Permission Settings\": {\"Location\": {\"ALLOW LOCATION ACCESS\": \"%s\"}}} }'%permission)


    def allow_invisible_elements(self, flag = True):
        """启用/禁用允许不可见元素

        :param flag: True/False

        :return:
        """
        self.driver.update_settings({"allowInvisibleElements": flag})


    def swipe_golden_position(self, n_col, start_index, end_index, loc_golden, duration=0):
        """ 滑动金刚位

        :param n_col: 一行有几个金刚位
        :param start_index: 从第几个金刚位开始滑动
        :param end_index: 滑动到第几个金刚位
        :param loc_golden: 金刚位定位符
        :param duration: 以ms计的滑动速度（webdriver的swipe方法参数）

        :return:
        """

        # 获取屏幕尺寸
        screen_size = self.driver.get_window_size()
        width = screen_size['width']

        # 将屏幕横向大致分为n_col份，滑动时从start_index指定的区块中间点开始滑动
        start_x = width *  ((start_index)*2+1)/(n_col*2)
        end_x = width * ((end_index)*2+1)/(n_col*2)

        golden_position_ele = self.find_element(loc_golden)
        rect = golden_position_ele.rect
        y = rect['y'] + 0.5 * rect['height']
        self.driver.swipe(start_x, y, end_x, y, duration)








