# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/6 18:23
# @Author : Olivia
# Desc: test access of user as basic plan without 7 day pass activated
# **************************************
from case.triplog.web.access.test_access_base import TestWebAccessBase


class TestBasicPlanWithoutPassActivated(TestWebAccessBase):
    user_identifier = "abasic@3973-2.com"