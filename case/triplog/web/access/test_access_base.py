# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/18 20:05
# @Author : Olivia
# Desc:
# **************************************
import pandas as pd
from base.get_config import GetConfig
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.web.po.mileage.trips_page import TripsPage


class TestAccessBase(TestTriplogWebBase):
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

    # def test_accessibility_by_navigation(self):
    #     """check access of each page from navigation bar
    #
    #     :return:
    #     """


        # for column in df.columns[4:]:
        #     menu_texts = column.split('->')
        #     first_level = menu_texts[0]
        #     second_level = menu_texts[1]
        #
        #     accessibility = user_row[column].item()

    def test_trips_page_accessibility(self):
        trips_page = TripsPage(self.driver,accessible=False)
        accessibility = self.user_row['Mileage->Trips'].item()

        if accessibility.lower()=='y':
            assert not trips_page.is_layer_popup_visible()
        else:
            assert trips_page.is_layer_popup_visible(expected=True)







