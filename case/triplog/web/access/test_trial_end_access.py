# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/17 20:16
# @Author : Olivia
# Desc: test the access of team paid user
# **************************************
from case.triplog.web.access.test_access_base import TestAccessBase


class TestTrialEndAccess(TestAccessBase):
    user_identifier = "trial_end"


