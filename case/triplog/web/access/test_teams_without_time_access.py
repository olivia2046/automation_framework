# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/7 21:12
# @Author : Olivia
# Desc:
# **************************************
from case.triplog.web.access.test_access_base import TestWebAccessBase


class TestTeamsWithoutTimeAccess(TestWebAccessBase):
    user_identifier = "teams_no_time"