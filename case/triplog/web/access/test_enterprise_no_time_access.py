# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/26 20:45
# @Author : Olivia
# Desc: test the access of enterprise user without time product
# current design is when user don't have time access, the Time navigation menu won't show
# Todo: expect to have access but actually not: Maps->Current Locations,Maps->Location Stay Time,Maps->Heat Map
#  Mileage->State Mileage,Expense->Spending Limits
# **************************************
from case.triplog.web.access.test_access_base import TestWebAccessBase


class TestEnterpriseNoTimeWebAccess(TestWebAccessBase):
    user_identifier = "enterprise_no_time"

    # def test_time_clock_page_accessibility(self):
    #     from proj_spec.triplog.web.po.time.time_calendar_page import TimeClockCalendarPage
    #     page = TimeClockCalendarPage(self.driver)
    #     accessibility = self.user_data['Time->Time Clock Calendar']
    #
    #     if accessibility.lower() == 'y':
    #         assert not page.is_layer_popup_visible()
    #         assert page.get_title() == 'Time Clock Calendar'
    #     else:
    #         assert page.jumped_to_billing()