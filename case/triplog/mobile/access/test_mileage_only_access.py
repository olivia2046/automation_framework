# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/21 10:51
# @Author : Olivia
# Desc:
# **************************************
from case.triplog.mobile.access.test_mobile_access_base import TestMobileAccessBase
import pytest

#@pytest.mark.skip("")
class TestMileageOnlyMobileAccess(TestMobileAccessBase):
    user_identifier = "mileage_only"
