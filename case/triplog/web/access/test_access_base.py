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
from proj_spec.triplog.web.po.dashboard.overview_page import OverviewPage
from proj_spec.triplog.web.po.expense.transactions_page import TransactionPage
from proj_spec.triplog.web.po.maps.heat_map_page import HeatMapPage
from proj_spec.triplog.web.po.mileage.trips_page import TripsPage
from proj_spec.triplog.web.po.reports.mileage_reports_page import MileageReportsPage
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
    #@pytest.mark.skip("")
    def test_overview_page_accessibility(self):
        page = OverviewPage(self.driver)
        accessibility = self.user_data['Dashboard->Overview']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Overview'
        else:
            assert page.is_layer_popup_visible(expected=True)


    def test_mileage_report_page_accessibility(self):
        page = MileageReportsPage(self.driver)
        accessibility = self.user_data['Reports->Mileage Reports']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title()=='Mileage Reports'
        else:
            assert page.is_layer_popup_visible(expected=True)


    def test_heat_map_page_accessibility(self):
        page = HeatMapPage(self.driver)
        accessibility = self.user_data['Maps->Heat Map']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Heat Map'
        else:
            assert page.is_layer_popup_visible(expected=True)

    #@pytest.mark.skip("")
    def test_trips_page_accessibility(self):
        page = TripsPage(self.driver,accessible=False)
        #accessibility = self.user_row['Mileage->Trips'].item()
        accessibility = self.user_data['Mileage->Trips']

        if accessibility.lower()=='y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Trips'
        else:
            assert page.is_layer_popup_visible(expected=True)

    #@pytest.mark.skip("")
    def test_transactions_page_accessibility(self):
        page = TransactionPage(self.driver)
        accessibility = self.user_data['Expense->Transactions']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Transactions'
        else:
            assert page.is_layer_popup_visible(expected=True)


    #@pytest.mark.skip("")
    def test_time_clock_page_accessibility(self):
        page = TimeClockPage(self.driver)
        accessibility = self.user_data['Time->Time Clock Calendar']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Time Clock Calendar'
        else:
            assert page.is_layer_popup_visible(expected=True)



