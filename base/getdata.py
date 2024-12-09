# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:53:07 2018
@author: olivia
"""
import logging

import pandas as pd
import sys
from base.get_config import get_user_file_path
sys.path.append('..')
from base.expression_evaluation import eval_from_string
from util.json_util import JsonUtil


class GetData:

    def get_case_data(self,caseid,file_path=None):
        '''根据test case id，以字典形式返回test case'''
        from base.get_config import get_testcase_file
        #print("caseid%s"%caseid)
        #print(file_path)

        if file_path is None:
            file_path = get_testcase_file()
        datafrm = pd.read_excel(file_path).fillna('') #把空值替换成空字符串
        #case_data = datafrm[datafrm['CaseId']==caseid]#取出一行仍为DataFrame类型，需要取Series
        #print("get case data")
        #print(case_data)
        if len(datafrm[datafrm['CaseId']==caseid])>0:
            case_data = datafrm[datafrm['CaseId']==caseid].iloc[0]#取出一行仍为DataFrame类型，需要取Series
            return case_data.to_dict()
        else:
            return {}

    @staticmethod
    def get_user_credential(user_loc):
        """
        get user credential from user file

        :param user_loc: location in the user list

        :return:
        """

        abs_file_path = get_user_file_path()
        user_data = pd.read_csv(abs_file_path)
        row = user_data[(user_data['loc'] == user_loc)]
        return tuple(row.iloc[0][['username', 'password']])

    def get_user_id_from_file(user_name):
        abs_file_path = get_user_file_path()
        user_data = pd.read_csv(abs_file_path)
        row = user_data[user_data['username'] == user_name]
        try:
            return row.iloc[0][['user_id']]
        except Exception as e:
            logging.error(e)
        
    
def get_header(header_file_path,label_name):
    from base.get_config import get_header_file

    jutil = JsonUtil(get_header_file())
    header_value = jutil.get_data(label_name)
    headers = eval_from_string(repr(header_value))
    return headers

def get_json_data(header_file_path,label_name):
    from base.get_config import get_header_file

    jutil = JsonUtil(get_header_file())
    header_value = jutil.get_data(label_name)
    headers = eval_from_string(repr(header_value))
    return headers




