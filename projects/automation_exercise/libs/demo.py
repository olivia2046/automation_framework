# -*- coding: utf-8 -*-
# **************************************
# @Time : 2026/3/6 15:21
# @Author : Olivia
# Desc: use as demo for functions used in Set_Up and Tear_Down
# **************************************
import logging

def function_used_by_setup():
    """ Demo function used in Set_Up column of Excel API test case, which will be executed as setup of test case.

    :return:
    """
    logging.info("Function used by Set_Up")

def function_used_by_teardown():
    """ Demo function used in Tear_Down column of Excel API test case, which will be executed as test case tear down

    :return:
    """
    logging.info("Function used by Tear_Down")