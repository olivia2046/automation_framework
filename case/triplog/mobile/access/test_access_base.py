# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:19
# @Author : Olivia
# Desc:
# **************************************
import pandas as pd
import pytest
from base.get_config import GetConfig
from case.triplog.mobile.test_triplog_mobile_base import TestTriplogMobileBase



class TestMobileAccessBase(TestTriplogMobileBase):
    user_identifier = None
    #user_identifier = "trial_end"
    #user_identifier = "single_paid"


    @classmethod
    def setup_class(cls):
        user_file = GetConfig.get_user_file_path()
        df = pd.read_csv(user_file,index_col='loc')
        df = df.fillna('')
        #cls.user_row = df.loc[df['loc'] == cls.user_identifier] # cls.user_identifier will be replaced by value in concrete class
        cls.user_data = df[cls.user_identifier]

    # def test_bottom_trips_access(self):
    #     """test access of bottom trips tab
    #
    #     :return:
    #     """
    @pytest.mark.skip("")
    def test_left_panel_submission_access(self):
        """

        :return:
        """
        self.page.show_left_panel()
        from proj_spec.triplog.mobile.po.tabs.submission_page import SubmissionPage

        page = SubmissionPage(self.driver)
        accessibility = self.user_data['Mobile Left->Submission']

        if accessibility.lower()=='y':
            assert page.left_panel.is_submission_accessible()
        else:
            # todo: assertion when no access
            assert not page.left_panel.is_submission_accessible()


    @pytest.mark.skip("")
    def test_bottom_tab_submission_access(self):
        from proj_spec.triplog.mobile.po.tabs.submission_page import SubmissionPage

        page = SubmissionPage(self.driver)
        accessibility = self.user_data['Mobile Bottom->Submission']

        if accessibility.lower()=='y':
            assert page.bottom_nav.is_submission_accessible()
        else:
            # todo: assertion when no access
            assert not page.bottom_nav.is_submission_accessible()


    def test_bottom_tab_reports_access(self):
        from proj_spec.triplog.mobile.po.tabs.submission_page import SubmissionPage

        page = SubmissionPage(self.driver)
        accessibility = self.user_data['Mobile Bottom->Reports']

        if accessibility.lower()=='y':
            assert page.bottom_nav.is_reports_accessible()
        else:
            # todo: assertion when no access
            assert not page.bottom_nav.is_reports_accessible()