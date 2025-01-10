# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/16 19:55
# @Author : Olivia
# Desc:
# **************************************
# def pytest_ignore_collect(path, config):
#     """
#     return True to prevent considering this path for collection.
#     This hook is consulted for all files and directories prior to calling more specific hooks.
#
#     :param path:
#     :param config:
#     :return:
#     """
#     if "test_trips" in str(path):
#         return True  # ignore
#     return False

def pytest_collection_modifyitems(config, items):
    # skip parent test class
    items[:] = [item for item in items if "TestWebAccessBase" not in item.nodeid]