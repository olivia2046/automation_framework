# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/20 16:44
# @Author : Olivia
# Desc:
# **************************************
import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage


class HeatMapPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/fleet/heatmap"