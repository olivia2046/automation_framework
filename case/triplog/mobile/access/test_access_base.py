# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:19
# @Author : Olivia
# Desc:
# **************************************
import pandas as pd
from base.get_config import GetConfig
from case.triplog.mobile.test_triplog_mobile_base import TestTriplogMobileBase


class TestMobileAccessBase(TestTriplogMobileBase):
    user_identifier = None
    #user_identifier = "trial_end"
    #user_identifier = "single_paid"


    @classmethod
    def setup_class(cls):
        user_file = GetConfig.get_user_file_path()
        df = pd.read_csv(user_file)
        df = df.fillna('')
        cls.user_row = df.loc[df['loc'] == cls.user_identifier] # cls.user_identifier will be replaced by value in concrete class
        pass
    def test_bottom_menu_access(self):
        """test access of bottom menu

        :return:
        """
