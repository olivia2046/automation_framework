# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:42
# @Author : Olivia
# Desc:
# **************************************
import pytest
from base.getdata import GetData
from case.triplog.web.mileage.test_trips import TestTrips
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.po.login.login_page import TriplogLoginPage


class TestEnterpriseTrips(TestTrips):
    user_identifier = "enterprise_paid"







