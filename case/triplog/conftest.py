# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/20 7:02
# @Author : Olivia
# Desc:
# **************************************

import pytest
import pandas as pd




@pytest.fixture(scope="class",autouse=True)
def get_login_info(request):
    from base.get_config import GetConfig
    user_file = GetConfig.get_user_file_path()
    df = pd.read_csv(user_file,index_col='loc')
    df = df.fillna('')
    if request.cls.user_identifier in df.columns:
        user_data = df[request.cls.user_identifier]
        #email, password = user_data[['email'],['password']]
        email, password = tuple(user_data[['email', 'password']])
        return email,password
    else:
        return None