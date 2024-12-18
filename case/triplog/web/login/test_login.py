# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/5 9:49
# @Author : Olivia
# Desc:
# **************************************
import pytest

from case.triplog.web.test_triplog_web_base import TestTriplogWebBase


@pytest.mark.skip()
class TestLogin(TestTriplogWebBase):
    user_identifier = "single_paid"
    def test_login(self):
        # login_page = TriplogLoginPage(self.driver)
        # email, password = GetData.get_user_credential(self.user_identifier)
        # overview_page = login_page.login(email,password)

        assert self.overview_page.get_title()=='Overview'

