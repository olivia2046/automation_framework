# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/5 14:31
# @Author : Olivia
# Desc:
# **************************************
from proj_spec.triplog.playwright.triplog_navigable_page import TriplogNavigablePage
import base.globalvars as glo

class OverviewPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/dashboard/overview"
