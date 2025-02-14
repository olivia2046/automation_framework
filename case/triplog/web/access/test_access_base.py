# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/18 20:05
# @Author : Olivia
# Desc: Todo: parameterize these page access tests??? no, each page should have its own specific assertion
# **************************************
import logging

import pandas as pd
import pytest

from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.web.po.dashboard.overview_page import OverviewPage



class TestWebAccessBase(TestTriplogWebBase):
    user_identifier = None
    #user_identifier = "trial_end"
    #user_identifier = "single_paid"


    @classmethod
    def setup_class(cls):
        logging.info("Testing access of %s" % cls.user_identifier)
        access_matrix_file = "../../accessbility-matrix.csv"
        df = pd.read_csv(access_matrix_file,index_col='loc')
        df = df.fillna('')
        #cls.user_row = df.loc[df['loc'] == cls.user_identifier] # cls.user_identifier will be replaced by value in concrete class
        cls.user_data = df[cls.user_identifier]


    @pytest.mark.skip("no need")
    def test_overview_page_accessibility(self):
        page = OverviewPage(self.driver)
        accessibility = self.user_data['Dashboard->Overview']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Overview'
        else:
            assert page.is_layer_popup_visible(expected=True)

    @pytest.mark.skip("no need")
    def test_mileage_report_page_url_accessibility(self):
        from proj_spec.triplog.web.po.reports.mileage_reports_page import MileageReportsPage
        page = MileageReportsPage(self.driver)
        accessibility = self.user_data['Reports->Mileage Reports']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title()=='Mileage Reports'
        else:
            assert page.is_layer_popup_visible(expected=True)




    @pytest.mark.skip("no need")
    def test_heat_map_page_accessibility(self):
        from proj_spec.triplog.web.po.maps.heat_map_page import HeatMapPage
        page = HeatMapPage(self.driver)
        accessibility = self.user_data['Maps->Heat Map']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Heat Map'
        else:
            assert page.is_layer_popup_visible(expected=True)

    @pytest.mark.skip("no need")
    def test_trips_page_url_accessibility(self):
        from proj_spec.triplog.web.po.mileage.trips_page import TripsPage
        page = TripsPage(self.driver,accessible=False)
        #accessibility = self.user_row['Mileage->Trips'].item()
        accessibility = self.user_data['Mileage->Trips']

        if accessibility.lower()=='y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Trips'
        else:
            assert page.is_layer_popup_visible(expected=True)

    @pytest.mark.skip("no need")
    def test_trip_page_navigatability(self):
        from proj_spec.triplog.web.po.mileage.trips_page import TripsPage
        #page = TripsPage(self.driver, method="navigation")
        accessibility = self.user_data['Mileage->Trips']

        page = self.default_page.navigation_bar.navigate("Mileage", "Trips")
        if accessibility.lower()=='y':
            assert page is not None
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Trips'
        else:
            assert page is None


    @pytest.mark.parametrize('menu_path',['Dashboard->Overview','Dashboard->Performance','Dashboard->Trends',
                                          'Reports->Mileage Reports','Reports->Business Expenses','Reports->Time Clock',
                                          'Maps->Current Locations','Maps->Heat Map','Maps->Frequent Locations','Maps->Driving Safety',
                                          'Maps->Location Stay Time', 'Maps->Time Clock',
                                          'Mileage->Trips','Mileage->State Mileage','Mileage->Fuel','Mileage->Locations','Mileage->Vehicles',
                                          'Expense->Transactions','Expense->Categories','Expense->Spending Limits','Expense->Tax Groups','Expense->Bank Accounts',
                                          'Time->Time Clock Calendar','Time->Time Clock List','Time->Scheduling','Time->Job Activities'])
    # @pytest.mark.parametrize('menu_path', ['Maps->Current Locations', 'Maps->Frequent Locations','Maps->Location Stay Time', 'Maps->Time Clock',
    #                                        'Mileage->State Mileage', 'Expense->Tax Groups'])
    def test_page_navigatability(self,menu_path):
        logging.info("Testing page navigation of %s"%menu_path)

        accessibility = self.user_data[menu_path]
        if "->" in menu_path:
            first_level, second_level = menu_path.split("->")
            expected_title = second_level
            page = self.default_page.navigation_bar.navigate(first_level, second_level)
        else:
            first_level = menu_path
            expected_title = first_level
            page = self.default_page.navigation_bar.navigate(first_level)


        if accessibility.lower()=='y':
            assert page is not None
            assert not page.is_layer_popup_visible()
            assert page.get_title() == expected_title
        else:
            assert page is None


    @pytest.mark.skip("no need")
    def test_transactions_page_accessibility(self):
        from proj_spec.triplog.web.po.expense.transactions_page import TransactionsPage
        page = TransactionsPage(self.driver)
        accessibility = self.user_data['Expense->Transactions']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Transactions'
        else:
            assert page.is_layer_popup_visible(expected=True)



    @pytest.mark.skip("use navigation")
    def test_spending_limits_page_accessibility(self):
        from proj_spec.triplog.web.po.expense.spending_limits_page import SpendingLimitsPage
        page = SpendingLimitsPage(self.driver)
        accessibility = self.user_data['Expense->Spending Limits']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Spending Limits'
        else:
            assert page.is_layer_popup_visible(expected=True)


    @pytest.mark.skip("no need")
    def test_time_clock_page_accessibility(self):
        from proj_spec.triplog.web.po.time.time_calendar_page import TimeClockCalendarPage
        page = TimeClockCalendarPage(self.driver)
        accessibility = self.user_data['Time->Time Clock Calendar']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Time Clock Calendar'
        else:

            #assert page.is_layer_popup_visible(expected=True) or page.jumped_to_billing()
            # 强制由具体子类决定判断准则
            assert False

    @pytest.mark.skip("debug")
    @pytest.mark.parametrize('path', ['Integrations->ADP','Integrations->Paychex','Integrations->Paylocity',
                            'Integrations->UKG Pro','Integrations->UKG Ready','Integrations->SAP Concur',
                                                  'Integrations->QuickBooks Online', 'Integrations->Xero', 'Integrations->Sage Intacct'])
    def test_integrations_item_accessibility(self, path):
        from proj_spec.triplog.web.po.integrations.integrations_page import IntegrationsPage
        accessibility = self.user_data[path]
        integration_item = path.split("->")[-1]
        page = IntegrationsPage(self.driver)
        if accessibility.lower()=='y':
            assert page.is_integration_item_accessible(integration_item)
        else:
            assert not page.is_integration_item_accessible(integration_item)

    @pytest.mark.skip("debug")
    @pytest.mark.parametrize('setting_path', ['Settings->Account Settings','Settings->Components','Settings->Notifications',
                                              'Settings->Activities','Settings->Mileage Rates','Settings->Mileage Policies',
                                              'Settings->Time Policies','Settings->Tags & Notes','Settings->Custom Tags',
                                              'Settings->Custom Fields','Settings->Advanced Settings'])
    def test_settings_accessibility(self, setting_path):
        logging.info("Testing access of %s" % setting_path)
        accessibility = self.user_data[setting_path]
        from proj_spec.triplog.web.po.manage.settings.settings_page import SettingsListPage
        page = SettingsListPage(self.driver)
        detail_setting = setting_path.split('->')[-1]
        if accessibility.lower()=='y':
            #assert page.is_detail_setting_accessible(detail_setting)
            assert page.has_entrance_to_detail_setting(detail_setting)
        else:
            #assert not page.is_detail_setting_accessible(detail_setting)
            assert not page.has_entrance_to_detail_setting(detail_setting)


    @pytest.mark.skip("debug: 需要实例化具体页面类并赋值url")
    @pytest.mark.parametrize('menu_path', ['Time->Time Clock Calendar'])
    def test_url_access(self,menu_path):
        """

        :return:
        """
        from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage
        page = TriplogNavigablePage(self.driver)
        accessibility = self.user_data[menu_path]
        expected_title = menu_path.split('->')[-1]

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == expected_title
        else:

            # assert page.is_layer_popup_visible(expected=True) or page.jumped_to_billing()
            # 强制由具体子类决定判断准则
            assert False

