# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/26 20:45
# @Author : Olivia
# Desc: test the access of enterprise user without time product
#
# **************************************
from case.triplog.web.access.test_access_base import TestWebAccessBase


class TestEnterpriseWebAccess(TestWebAccessBase):
    user_identifier = "enterprise"
