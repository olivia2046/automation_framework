# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:19
# @Author : Olivia
# Desc:
# **************************************
import logging

import pandas as pd
import pytest
from case.triplog.mobile.test_triplog_mobile_base import TestTriplogMobileBase



class TestMobileAccessBase(TestTriplogMobileBase):
    user_identifier = None
    #user_identifier = "trial_end"
    #user_identifier = "single_paid"


    @classmethod
    def setup_class(cls):
        logging.info("Test access of %s"%cls.user_identifier)
        access_matrix_file = "../../accessbility-matrix.csv"
        df = pd.read_csv(access_matrix_file,index_col='loc')
        df = df.fillna('')
        #cls.user_row = df.loc[df['loc'] == cls.user_identifier] # cls.user_identifier will be replaced by value in concrete class
        cls.user_data = df[cls.user_identifier]

    #@pytest.mark.skip("")
    # @pytest.mark.parametrize('menu_name',['Auto Start on','Work Schedule','Vehicles','Send to Concur','Locations',
    #     'State Mileage','Submission','Navigate/Route Planning','Frequent Trip Rules','Adjust Odometer',
    #     'Mileage Rates','Business Activities','Last Known Parking','Banks & Credit Cards','Invite Accountant','Approval Management'])
    # @pytest.mark.parametrize('menu_name', ['Business Activities'])
    @pytest.mark.parametrize('menu_name',['Auto Start on','Work Schedule','State Mileage','Approval Management'])
    def test_left_panel_menus_access(self,menu_name):
        """

        :return:
        """

        logging.info("Testing access of Left Panel-%s"%menu_name)
        self.page.show_left_panel()

        accessibility = self.user_data['Mobile Left->%s'%menu_name]

        if accessibility.lower()=='y':
            assert self.page.left_panel.is_left_menu_accessible(menu_name),"should have access to left panel %s"%menu_name
        else:
            # todo: assertion when no access

            assert not self.page.left_panel.is_left_menu_accessible(menu_name),"should not have access to left panel %s"%menu_name


    # Todo: Time on android
    #@pytest.mark.skip("")
    #@pytest.mark.parametrize('tab_name',['Trips','Fuel','Submission','Reports','Transactions','Time','Schedule','Time off'])
    @pytest.mark.parametrize('tab_name',['Trips', 'Fuel', 'Submission', 'Reports', 'Transactions', 'Schedule', 'Time off'])
    # @pytest.mark.parametrize('tab_name',['Submission'])
    def test_bottom_tabs_access(self, tab_name):
        from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage

        logging.info("checking bottom tab access of %s"%tab_name)
        page = TabsBasePage(self.driver)
        accessibility = self.user_data['Mobile Bottom->%s'%tab_name]

        if accessibility.lower()=='y':
            assert page.bottom_nav.is_tab_page_accessible(tab_name),"should have access to bottom %s"%tab_name
        else:
            # todo: assertion when no access
            assert not page.bottom_nav.is_tab_page_accessible(tab_name,expected=False),"should not have access to bottom %s"%tab_name




