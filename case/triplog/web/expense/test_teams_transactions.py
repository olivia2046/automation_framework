# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/2 19:44
# @Author : Olivia
# Desc:
# **************************************
from case.triplog.web.expense.test_expense_transactions import TestExpenseTransactions


class TestTeamsTransactions(TestExpenseTransactions):
    user_identifier = "teams"
