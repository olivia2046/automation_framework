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
from util.db_util import execute_query

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

def get_user_credential(role_name,channel='person'):
    """从指定文件中获取指定角色的用户登录信息,默认渠道为个人版"""
    abs_file_path = get_user_file_path()
    user_data = pd.read_csv(abs_file_path)
    row = user_data[(user_data['rolename']==role_name) & (user_data['channel']==channel)]
    return tuple(row.iloc[0][['username','password']])

def get_user_id_from_file(user_name):
    abs_file_path = get_user_file_path()
    user_data = pd.read_csv(abs_file_path)
    row = user_data[user_data['username']==user_name]
    try:
        return row.iloc[0][['user_id']]
    except Exception as e:
        logging.error(e)

def get_user_id_from_db(user_name, db_section='DB_auth', account_type=2):
    """从数据库获取用户id

    :param user_name:
    :param db_section:
    :param account_type: 账号类型1-LDAP, 2-Standard， 默认使用2-Standard标准账号
    :return:
    """
    sql = """select id from t_permission_user where username='%s' and account_type=%s"""%(user_name, account_type)
    res = execute_query(sql, dbname=db_section)
    try:
        return res[0][0]
    except Exception as e:
        logging.error(e)
