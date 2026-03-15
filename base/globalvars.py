# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 08:23:02 2018
https://www.cnblogs.com/suwings/p/6358061.html

to be used in Excel api test only. For other tests, use base.config.config for global variable settings
"""


def init():
    global _global_dict
    _global_dict = {}


def set_value(key,value):
    """ Define a global variable. """
    _global_dict[key] = value


def get_value(key,defValue=None):
    """ Retrieve a global variable; return a default value if it does not exist. """
    try:
        result = _global_dict[key]
        if result is None:
            return defValue
        else:
            return result
    except Exception as e:
        #logging.error("get_value: %s"%e)
        return defValue
    
