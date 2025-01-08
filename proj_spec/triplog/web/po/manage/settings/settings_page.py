# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/7 19:29
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By

import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage


class SettingsListPage(TriplogNavigablePage):
    url = glo.get_value("url1")+"/setting/list"


    def access_detail_setting(self, setting_name):
        setting_loc = (By.XPATH, '//label[contains(text(),"%s")]'%setting_name)
        self.find_element_and_click(setting_loc)
        from proj_spec.triplog.web.po.manage.settings.detail_setting_base_page import DetailSettingBasePage
        return DetailSettingBasePage(self.driver)


    def is_detail_setting_accessible(self, setting_name):
        detail_page = self.access_detail_setting(setting_name)
        #return not detail_page.get_title()==""
        return not detail_page.is_upgrade_visible()
