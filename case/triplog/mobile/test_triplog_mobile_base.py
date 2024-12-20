# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:21
# @Author : Olivia
# Desc:
# **************************************
import pytest

from case.mobile.test_mobile_base import TestMobileBase


@pytest.mark.usefixtures("driver_init")
class TestTriplogMobileBase(TestMobileBase):
    @classmethod
    def setup_class(cls):
        pass