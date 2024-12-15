# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/5 10:01
# @Author : Olivia
# Desc:
# **************************************
import pytest

from case.test_web_base import TestWebBase

@pytest.mark.usefixtures("driver_init")
class TestTriplogWebBase(TestWebBase):
    @classmethod
    def setup_class(cls):
        pass

