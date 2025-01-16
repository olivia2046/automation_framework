# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/6 18:23
# @Author : Olivia
# Desc: test access of user as basic plan without 7 day pass activated
# **************************************
import pytest
from case.triplog.web.access.test_access_base import TestWebAccessBase


@pytest.mark.skip("not ready")
class TestBasicPlanWithoutPassActivated(TestWebAccessBase):
    user_identifier = "basicplan_without_pass"