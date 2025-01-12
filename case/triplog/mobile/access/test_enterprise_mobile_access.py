# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2024/12/29 8:11
desc: 
'''
import pytest
from case.triplog.mobile.access.test_mobile_access_base import TestMobileAccessBase

#@pytest.mark.skip("")
class TestEnterpriseMobileAccess(TestMobileAccessBase):
    user_identifier = "enterprise"