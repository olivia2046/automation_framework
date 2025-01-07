# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/17 20:25
# @Author : Olivia
# Desc: test access of paid users, including premium, teams and enterprise
# **************************************
from case.triplog.web.access.test_access_base import TestWebAccessBase
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.web.po.mileage.trips_page import TripsPage


class TestPremiumWebAccess(TestWebAccessBase):
    user_identifier = "premium"


