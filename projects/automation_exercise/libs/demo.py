# -*- coding: utf-8 -*-
# **************************************
# @Time : 2026/3/6 15:21
# @Author : Olivia
# Desc: use as demo for functions used in Set_Up and Tear_Down
# **************************************
import logging

def function_used_by_setup():
    logging.info("Function used by Set_Up")

def function_used_by_teardown():
    logging.info("Function used by Tear_Down")