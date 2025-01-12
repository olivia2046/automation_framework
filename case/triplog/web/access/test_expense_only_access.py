# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/11 10:10
desc: 
'''
from case.triplog.web.access.test_access_base import TestWebAccessBase


class TestExpenseOnlyAccess(TestWebAccessBase):
    user_identifier = "expense_only"