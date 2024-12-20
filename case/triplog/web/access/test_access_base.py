# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/18 20:05
# @Author : Olivia
# Desc: Todo: parameterize these page access tests??? no, each page should have its own specific assertion
# **************************************
import pandas as pd
import pytest

from base.get_config import GetConfig
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.web.po.expense.transactions_page import TransactionPage
from proj_spec.triplog.web.po.mileage.trips_page import TripsPage
from proj_spec.triplog.web.po.time.time_clock_page import TimeClockPage


class TestAccessBase(TestTriplogWebBase):
    user_identifier = None
    #user_identifier = "trial_end"
    #user_identifier = "single_paid"


    @classmethod
    def setup_class(cls):
        user_file = GetConfig.get_user_file_path()
        df = pd.read_csv(user_file,index_col='loc')
        df = df.fillna('')
        #cls.user_row = df.loc[df['loc'] == cls.user_identifier] # cls.user_identifier will be replaced by value in concrete class
        cls.user_data = df[cls.user_identifier]
        pass

    # def test_accessibility_by_navigation(self):
    #     """check access of each page from navigation bar
    #
    #     :return:
    #     """


        # for column in df.columns[4:]:
        #     menu_texts = column.split('->')
        #     first_level = menu_texts[0]
        #     second_level = menu_texts[1]
        #
        #     accessibility = user_row[column].item()
    def test_overview_page_accessibility(self):
        overview_page = TimeClockPage(self.driver)
        accessibility = self.user_data['Dashboard->Overview']

        if accessibility.lower() == 'y':
            assert not overview_page.is_layer_popup_visible()
            # todo: other assertion to test against trips page itself
        else:
            assert overview_page.is_layer_popup_visible(expected=True)


    #@pytest.mark.skip("")
    def test_trips_page_accessibility(self):
        trips_page = TripsPage(self.driver,accessible=False)
        #accessibility = self.user_row['Mileage->Trips'].item()
        accessibility = self.user_data['Mileage->Trips']

        if accessibility.lower()=='y':
            assert not trips_page.is_layer_popup_visible()
        else:
            assert trips_page.is_layer_popup_visible(expected=True)

    #@pytest.mark.skip("")
    def test_transactions_page_accessibility(self):
        transaction_page = TransactionPage(self.driver)
        accessibility = self.user_data['Expense->Transactions']

        if accessibility.lower() == 'y':
            assert not transaction_page.is_layer_popup_visible()
            # todo: other assertion to test against trips page itself
        else:
            assert transaction_page.is_layer_popup_visible(expected=True)


    #@pytest.mark.skip("")
    def test_time_clock_page_accessibility(self):
        time_clock_page = TimeClockPage(self.driver)
        accessibility = self.user_data['Time->Time Clock Calendar']

        if accessibility.lower() == 'y':
            assert not time_clock_page.is_layer_popup_visible()
            # todo: other assertion to test against trips page itself
        else:
            assert time_clock_page.is_layer_popup_visible(expected=True)



