# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 8:52
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By

from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage
import base.globalvars as glo

class TransactionsPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/expense"

    _add_btn_loc = (By.ID,'add_button')
    _amount_input_loc = (By.ID, 'cost')
    _category_combo_loc = (By.XPATH, '//tbody[@id="expense_table_body"]//div[contains(@id, "expense_category_div_expense_row")]'
                                     '//input[contains(@id,"_easyui_textbox_input")]')
    # there're 2 inputs with value of 'Create', so use 'Add Receipt' to locate 'Create'
    _create_transaction_btn_loc = (By.XPATH, '//input[@type="submit" and @value="Add Receipt"]/../input[1]')
    # use Copy button to locate Save button
    _save_transaction_btn_loc = (By.XPATH, '//input[@type="button" and @value="Copy"]/../input[1]')
    _delete_one_btn_loc = (By.XPATH, '//input[@type="button" and @value="Delete"]')
    nth_transaction_loc = (By.XPATH, '//td[@class="mlarge"][index_placeholder]')

    def _input_transaction_arguments(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.find_element_and_input(self._amount_input_loc,kwargs['amount'])
        self.choose_category_from_combobox(kwargs['category'])

    def _get_nth_transaction_locator(self, row_index):
        loc_str = self.nth_transaction_loc[1]
        loc_str = loc_str.replace('index_placeholder',str(row_index+1))
        return (self.nth_transaction_loc[0],loc_str)

    def choose_category_from_combobox(self, category_name):
        """choose category from combobox, when creating/editing transaction

        :return:
        """
        self.find_element_and_input(self._category_combo_loc, category_name)
        item_loc = (By.XPATH, '//div[contains(@id, "easyui_combobox") and text()="%s"]'%category_name)
        item_element = self.find_element(item_loc)
        if item_element is not None:
            item_element.click()
        # else there's no need to choose


    def create_transaction(self, **kwargs):
        """

        :return:
        """
        self.driver.get(self.url) # make sure page loads completely before finding the add button
        self.find_element_and_click(self._add_btn_loc)
        assert 'amount' in kwargs.keys()
        assert 'category' in kwargs.keys()
        self._input_transaction_arguments(**kwargs)
        # self.find_element_and_input(self._amount_input_loc,kwargs['amount'])
        # self.choose_category_from_combobox(kwargs['category'])
        self.find_element_and_click(self._create_transaction_btn_loc)

        #self.find_element(self._add_btn_loc,condition="element_to_be_clickable")


    def edit_transaction(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.driver.get(self.url)
        row_index = kwargs['row_index']

        #transaction_loc = (By.XPATH, '//tr[contains(@id, "expense_row")][%s]'%(row_index+1))
        #transaction_loc = (By.XPATH, '//td[@class="mlarge"][%s]'%(row_index+1))
        transaction_loc = self._get_nth_transaction_locator(row_index)
        self.find_element_and_click(transaction_loc)
        self.find_element(self._save_transaction_btn_loc) # wait for row expanded
        self._input_transaction_arguments(**kwargs)
        self.find_element_and_click(self._save_transaction_btn_loc)


    def delete_one_transaction(self, row_index=0):
        """Expand a transaction and delete it

        :param row_index:
        :return:
        """
        self.driver.get(self.url)
        transaction_loc = self._get_nth_transaction_locator(row_index)
        self.find_element_and_click(transaction_loc)
        delete_one_btn =self.find_element(self._delete_one_btn_loc)
        delete_one_btn.click()
        # confirm the pop up
        alert = self.driver.switch_to.alert
        alert.accept()













