# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/5 9:49
# @Author : Olivia
# Desc:
# **************************************
from base.getdata import GetData
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.po.login.login_page import TriplogLoginPage


class TestLogin(TestTriplogWebBase):
    def test_login(self):
        login_page = TriplogLoginPage()
        email, password = GetData.get_user_credential('single_paid')
        overview_page = login_page.login(email,password)

        assert overview_page.get_title()=='Overview'

