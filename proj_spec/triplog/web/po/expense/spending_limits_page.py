# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/8 21:41
# @Author : Olivia
# Desc:
# **************************************
import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage


class SpendingLimitsPage(TriplogNavigablePage):
    url = glo.get_value("url1")+"/expense/expenseLimits"

