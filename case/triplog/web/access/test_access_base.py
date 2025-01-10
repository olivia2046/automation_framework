# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/18 20:05
# @Author : Olivia
# Desc: Todo: parameterize these page access tests??? no, each page should have its own specific assertion
# **************************************
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
        access_matrix_file = "../../accessbility-matrix.csv"
        df = pd.read_csv(access_matrix_file,index_col='loc')
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

    @pytest.mark.skip("")
    def test_overview_page_accessibility(self):
        page = OverviewPage(self.driver)
        accessibility = self.user_data['Dashboard->Overview']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Overview'
        else:
            assert page.is_layer_popup_visible(expected=True)

    @pytest.mark.skip("")
    def test_mileage_report_page_accessibility(self):
        from proj_spec.triplog.web.po.reports.mileage_reports_page import MileageReportsPage
        page = MileageReportsPage(self.driver)
        accessibility = self.user_data['Reports->Mileage Reports']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title()=='Mileage Reports'
        else:
            assert page.is_layer_popup_visible(expected=True)

    @pytest.mark.skip("")
    def test_heat_map_page_accessibility(self):
        from proj_spec.triplog.web.po.maps.heat_map_page import HeatMapPage
        page = HeatMapPage(self.driver)
        accessibility = self.user_data['Maps->Heat Map']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Heat Map'
        else:
            assert page.is_layer_popup_visible(expected=True)

    @pytest.mark.skip("")
    def test_trips_page_accessibility(self):
        from proj_spec.triplog.web.po.mileage.trips_page import TripsPage
        page = TripsPage(self.driver,accessible=False)
        #accessibility = self.user_row['Mileage->Trips'].item()
        accessibility = self.user_data['Mileage->Trips']

        if accessibility.lower()=='y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Trips'
        else:
            assert page.is_layer_popup_visible(expected=True)

    @pytest.mark.skip("")
    def test_transactions_page_accessibility(self):
        from proj_spec.triplog.web.po.expense.transactions_page import TransactionsPage
        page = TransactionsPage(self.driver)
        accessibility = self.user_data['Expense->Transactions']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Transactions'
        else:
            assert page.is_layer_popup_visible(expected=True)



    def test_spending_limits_page_accessibility(self):
        from proj_spec.triplog.web.po.expense.spending_limits_page import SpendingLimitsPage
        page = SpendingLimitsPage(self.driver)
        accessibility = self.user_data['Expense->Spending Limits']

        if accessibility.lower() == 'y':
            assert not page.is_layer_popup_visible()
            assert page.get_title() == 'Spending Limits'
        else:
            assert page.is_layer_popup_visible(expected=True)


    @pytest.mark.skip("")
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
        accessibility = self.user_data[setting_path]
        from proj_spec.triplog.web.po.manage.settings.settings_page import SettingsListPage
        page = SettingsListPage(self.driver)
        detail_setting = setting_path.split('->')[-1]
        if accessibility.lower()=='y':
            assert page.is_detail_setting_accessible(detail_setting)
        else:
            assert not page.is_detail_setting_accessible(detail_setting)


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

    @pytest.mark.skip("debug")
    @pytest.mark.parametrize('menu_path',
                             ['Dashboard->Overview','Reports->Mileage Reports','Maps->Heat Map','Mileage->Trips',
                              'Expense->Transactions','Time->Time Clock Calendar'])
    def test_navigation_access(self, menu_path):

        from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage
        page = TriplogNavigablePage(self.driver)
        menus = menu_path.split("->")
        page.navigation_bar.navigate(menus[0], menus[1])
        assert page.get_title()==menus[1]