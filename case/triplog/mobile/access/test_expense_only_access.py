# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2024/12/22 11:16
desc: 
'''
from case.triplog.mobile.access.test_mobile_access_base import TestMobileAccessBase
import pytest

#@pytest.mark.skip("")
class TestExpenseOnlyMobileAccess(TestMobileAccessBase):
    user_identifier = "expense_only"