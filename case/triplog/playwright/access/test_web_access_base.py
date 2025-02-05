# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/5 13:44
# @Author : Olivia
# Desc:
# **************************************
import logging,pytest
import pandas as pd

from case.triplog.playwright.test_triplog_pw_base import TestTriplogPWBase


class TestWebAccessBase(TestTriplogPWBase):
    user_identifier = None

    @classmethod
    def setup_class(cls):
        logging.info("Testing access of %s" % cls.user_identifier)
        access_matrix_file = "../../accessbility-matrix.csv"
        df = pd.read_csv(access_matrix_file,index_col='loc')
        df = df.fillna('')
        cls.user_data = df[cls.user_identifier]

    # @pytest.mark.parametrize('menu_path',['Dashboard->Overview','Dashboard->Performance','Dashboard->Trends',
    #                                       'Reports->Mileage Reports','Reports->Business Expenses','Reports->Time Clock',
    #                                       'Maps->Current Locations','Maps->Heat Map','Maps->Frequent Locations','Maps->Driving Safety',
    #                                       'Maps->Location Stay Time', 'Maps->Time Clock',
    #                                       'Mileage->Trips','Mileage->State Mileage','Mileage->Fuel','Mileage->Locations','Mileage->Vehicles',
    #                                       'Expense->Transactions','Expense->Categories','Expense->Spending Limits','Expense->Tax Groups','Expense->Bank Accounts',
    #                                       'Time->Time Clock Calendar','Time->Time Clock List','Time->Scheduling','Time->Job Activities'])
    @pytest.mark.parametrize('menu_path',
                             ['Maps->Current Locations', 'Maps->Frequent Locations', 'Maps->Location Stay Time',
                              'Maps->Time Clock',
                              'Mileage->State Mileage', 'Expense->Tax Groups'])
    def test_page_navigatability(self, menu_path):
        logging.info("Testing page navigation of %s" % menu_path)

        accessibility = self.user_data[menu_path]
        if "->" in menu_path:
            first_level, second_level = menu_path.split("->")
            expected_title = second_level
            page = self.default_page.navigation_bar.navigate(first_level, second_level)
        else:
            first_level = menu_path
            expected_title = first_level
            page = self.default_page.navigation_bar.navigate(first_level)

        if accessibility.lower() == 'y':
            assert page is not None
            assert not page.is_layer_popup_visible()
            assert page.get_title() == expected_title
        else:
            assert page is None