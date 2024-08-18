# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 13:46:36 2018
@author: olivia
Description: 获取配置文件各项内容，避免在需要相应内容的模块处分别调用configparser
"""

from configparser import ConfigParser
import os, sys, logging

sys.path.append('..')
import base.globalvars as glo
from util.crypt_util import decryption
from util.data.pandas_tool import data_conversion_list

# cf = ConfigParser(os.environ) #使用环境变量进行插值
cf = ConfigParser()
# 替换ConfigParser.optionxform()函数，因为它会将大小写的配置项Key转换为小写，而seleium/appium的capabilities里需要大小写
cf.optionxform = str
# cfgfile = os.path.abspath('.') + os.sep + "settings.ini" #会在运行时引用主程序的当前路径
# ConfigParser读取的配置文件必须是实际绝对路径！
abspath = os.path.split(os.path.realpath(__file__))[0]
cfgfile = abspath + '/../config/' + "settings - %s.ini" % glo.get_value("config_name")
# cfgfile = abspath + '/../config/' + "settings - Bank_app_QA.ini"
cf.read(cfgfile, encoding="utf-8-sig")


# print(cf.sections())

def get_url_dict():
    if "URLs" in cf:
        return cf['URLs']
    else:
        return {}


def get_test_type():
    try:
        return cf.get('AUT', 'test_type')
    except Exception as e:
        logging.error("e")
        return 'interface'


def get_testcase_file():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath', 'testcase_file')
    except Exception as e:
        logging.error("get_testcase_file:%s" % e)
        return ""


def get_header_file():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath', 'header_file')
    except Exception as e:
        logging.error("get_header_file:%s" % e)
        return ""


def get_data_file():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath', 'data_file')
    except Exception as e:
        logging.error("get_data_file:%s" % e)
        return ""


def get_tc_rootdir(absolute_path=True):
    try:
        if absolute_path is False:
            return cf.get('FilePath', 'tc_rootdir')
        else:
            return abspath + os.sep + '..' + os.sep + cf.get('FilePath', 'tc_rootdir')
    except Exception as e:
        logging.error("get_tc_rootdir:%s" % e)
        return ""


def get_data_rootdir():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath', 'data_rootdir')
    except Exception as e:
        logging.error("get_data_rootdir:%s" % e)
        return ""

def get_user_file_path():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath', 'user_file')
    except Exception as e:
        logging.error("get_user_file_path:%s" % e)
        return ""

def get_email_config():
    try:
        email_host = cf.get('Email', 'email_host')
        if cf.has_option('Email', 'email_port'):
            email_port = cf.get('Email', 'email_port')
        else:
            email_port = 25
        send_user = cf.get('Email', 'send_user')
        password = decryption(cf.get('Email', 'password')).decode()  # 解密再把byte解码成string
        user_list_str = cf.get('Email', 'user_list')
        user_list = user_list_str.split(',')
        cc_list_str = cf.get('Email', 'cc_list')
        cc_list = cc_list_str.split(',')

        if cf.has_option('Email','manual_testers'):
            manual_testers_str = cf.get('Email','manual_testers')
            manual_testers = manual_testers_str.split(',')
        else:
            manual_testers = []

        return ({'email_host': email_host, 'email_port': email_port, 'send_user': send_user,
                 'password': password, 'user_list': user_list, 'cc_list': cc_list, 'manual_testers': manual_testers})
    except Exception as e:
        logging.error("get_email_config:%s" % e)
        return {}


def get_account_url():
    try:
        return cf.get('AUT', 'account_url')
    except Exception as e:
        logging.error("get_account_url:%s" % e)
        return ''


def get_frontend_root_url():
    try:
        return cf.get('AUT', 'frontend_root_url')
    except Exception as e:
        logging.error("get_frontend_root_url:%s" % e)
        return ""


def get_backend_root_url():
    try:
        return cf.get('AUT', 'backend_root_url')
    except Exception as e:
        logging.debug("get_backend_root_url:%s" % e)
        return ""


def get_verify_str():
    try:
        return cf.get('AUT', 'verify')
    except Exception as e:
        logging.error("get_verify_str:%s" % e)
        return None


def get_certfile_path():
    try:
        return cf.get('AUT', 'cert')
    except Exception as e:
        logging.error("get_certfile_path:%s" % e)
        return ""


def get_verify_cert():
    try:
        verify = get_verify_str()
        if verify.upper() == 'FALSE':
            # logging.debug("no need to vefify certification.")
            # verify = eval("False")
            verify = False
            cert = None
        else:
            verify = True
            cert = sys.path[0] + '/../' + get_certfile_path()
        return verify, cert
    except Exception as e:
        logging.error("get_verify_cert:%s" % e)
        return ()


def get_log_level():
    try:
        level = cf.get('Framework', 'log_level')
        return level
    except Exception as e:
        logging.error("get_log_level:%s" % e)
        return "DEBUG"


def get_db_type(dbname='DB'):
    try:
        return cf.get(dbname, 'db_type')
    except Exception as e:
        logging.error("get_db_type:%s" % e)
        return ""


def get_db_host(dbname='DB'):
    try:
        return cf.get(dbname, 'host')
    except Exception as e:
        logging.error("get_db_host:%s" % e)
        return ""


def get_db_port(dbname='DB'):
    try:
        return cf.get(dbname, 'port')
    except Exception as e:
        logging.error("get_db_port:%s" % e)
        return ""


def get_db_user(dbname='DB'):
    try:
        return cf.get(dbname, 'username')
    except Exception as e:
        logging.error("get_db_user:%s" % e)
        return ""


def get_db_pwd(dbname='DB'):
    try:
        pwdstr = cf.get(dbname, 'password')
        return decryption(pwdstr).decode()  # 解密再把byte解码成string
    except Exception as e:
        logging.error("get_db_pwd:%s" % e)
        return ""


# def get_db_sid():
#    return cf.get('DB','sid')

def get_db_service_name(dbname='DB'):
    try:
        '''oracle_cx 需要使用service name而不是sid
        查看Oracle service name:select value from v$parameter where name like '%service_name%'''
        return cf.get(dbname, 'service_name')
    except Exception as e:
        logging.error("get_db_service_name:%s" % e)
        return ""


def get_db_database(dbname='DB'):
    '''MySQL连接的database'''
    try:
        return cf.get(dbname, 'database')
    except Exception as e:
        logging.error("cannot find DB->database section:%s" % e)
        return ""


def get_neo4j_uri():
    try:
        return cf.get('NEO4J', 'uri')
    except Exception as e:
        logging.error("cannot find NEO4J->uri section:%s" % e)
        return ""


def get_neo4j_username():
    try:
        return cf.get('NEO4J', 'username')
    except Exception as e:
        logging.error("cannot find NEO4J->username section:%s" % e)


def get_neo4j_pwd():
    try:
        pwdstr = cf.get('NEO4J', 'password')
        return decryption(pwdstr).decode()
    except Exception as e:
        logging.error("cannot find NEO4J->password section:%s" % e)


def get_run_case_level():
    try:
        # 返回需要运行的case level的列表
        case_level_str = cf.get('Framework', 'run_case_level').replace(" ", "")
        # if case_level_str=='':
        #     case_level_str='Smoke,Sanity,Regression'
    except Exception as e:
        # case_level_str = 'Smoke,Sanity,Regression'
        logging.error("get_run_case_level:%s" % e)
        case_level_str = ''
    case_levels = case_level_str.split(',')
    if case_levels == ['']:
        case_levels = []
    return case_levels


def get_run_case_folder():
    try:
        # 返回需要运行的case level的列表
        case_folder_str = cf.get('Framework', 'run_case_folder').replace(" ", "")
    except Exception as e:
        logging.error("get_run_case_folder:%s" % e)
        case_folder_str = ''
    case_folders = case_folder_str.split(',')
    if case_folders == ['']:
        case_folders = []
    return case_folders


def get_run_case_type():
    # 返回需要运行的case类型列表
    try:
        case_type_str = cf.get('Framework', 'run_case_type').replace(" ", "")
        if case_type_str == "":
            case_type_str = "Excel,Code"
    except Exception as e:
        logging.error("get_run_case_type:%s" % e)
        case_type_str = "Excel,Code"
    return case_type_str.split(',')


def get_and_set_global_vars():
    try:
        if cf.has_section('Globals'):
            '''从配置文件中读取需要设置的全局变量（不同于配置文件中在整个框架使用的其他变量，此处的全局变量只在特定项目中使用，因此不同配置文件做不同设置'''
            for key in cf['Globals']:
                glo.set_value(key, cf.get('Globals', key))

    except Exception as e:
        logging.error("get_and_set_global_vars:%s" % e)


def get_mongodb_host():
    if cf.has_section('MongoDB'):
        try:
            return cf.get('MongoDB', 'host')
        except Exception as e:
            logging.error("cannot find MongoDB->host section:%s" % e)
            return ""
    else:
        return ""


def get_mongodb_port():
    if cf.has_section('MongoDB'):
        try:
            return cf.get('MongoDB', 'port')
        except Exception as e:
            logging.error("cannot find MongoDB->port section: %s" % e)
            return ""
    else:
        return ""


def get_mongodb_username():
    if cf.has_section('MongoDB'):
        try:
            return cf.get('MongoDB', 'username')
        except Exception as e:
            logging.error("cannot find MongoDB->username section:%s" % e)
            return ""
    else:
        return ""


def get_mongodb_password():
    if cf.has_section('MongoDB'):
        try:
            password = cf.get('MongoDB', 'password')
            return decryption(password).decode()
        except Exception as e:
            logging.error("cannot find MongoDB->password section:%s" % e)
            return ""
    else:
        return ""


def get_mongodb_mechanism():
    if cf.has_section('MongoDB'):
        try:
            return cf.get('MongoDB', 'mechanism')
        except Exception as e:
            logging.error("cannot find MongoDB->mechanism section:%s" % e)
            return ""
    else:
        return ""


def get_redis_host():
    if cf.has_section('Redis'):
        try:
            return cf.get('Redis', 'host')
        except Exception as e:
            logging.error("cannot find Redis->host section:%s" % e)
            return ""
    else:
        return ""


def get_redis_port():
    if cf.has_section('Redis'):
        try:
            return cf.get('Redis', 'port')
        except Exception as e:
            logging.error("cannot find Redis->port section: %s" % e)
            return ""
    else:
        return ""


def get_environment():
    if cf.has_section('AUT'):
        try:
            return cf.get('AUT', 'environment')
        except Exception as e:
            logging.error("cannot find AUT->environment section:%s" % e)
            return ""
    else:
        return ""


def get_retry_times():
    try:
        # 返回需要运行的case level的列表
        retry_times = int(cf.get('Framework', 'retry_times').replace(" ", ""))
    except Exception as e:
        logging.warning("get_retry_times:%s" % e)
        retry_times = 0
    return retry_times


def get_retry_wait_time():
    try:
        # 返回需要运行的case level的列表
        retry_wait_time = int(cf.get('Framework', 'retry_wait_time').replace(" ", ""))
    except Exception as e:
        logging.warning("get_retry_wait_time:%s" % e)
        retry_wait_time = 10
    return retry_wait_time


def get_sync_server_time():
    if cf.has_section('AUT'):
        try:
            return cf.get('AUT', 'sync_server_time')
        except Exception as e:
            logging.error("cannot find AUT->sync_server_time:%s" % e)
            return "false"
    else:
        return "false"


def get_run_specific_case():
    if cf.has_section('Framework'):
        try:
            run_specific_case = cf.get('Framework', 'run_specific_case')
            if run_specific_case.lower() == 'true':
                return True
            else:
                return False
        except Exception as e:
            logging.error("cannot find Framework->run_case_folder:%s" % e)
            return False
    else:
        return False


def get_timeout():
    if cf.has_section('Framework'):
        try:
            timeout = int(cf.get('Framework', 'timeout'))
            return timeout
        except Exception as e:
            logging.error("cannot find Framework->timeout:%s" % e)
            return -1
    else:
        return -1

# 获取指定的ini文件指定的key数据
def get_value(section, key, default = ''):
    try:
        return cf.get(section, key)
    except Exception as e:
        logging.error(e)
        return default


# 获取capabilities
def get_capabilities():
    if cf.has_section('Caps'):
        caps={}
        try:
            for cap in cf['Caps'].keys():
                value = cf.get('Caps', cap)
                if value in ['True','False']:
                    value = eval(value)
                caps[cap] = value
            for appium_cap in cf['Caps_appium'].keys():
                value = cf.get('Caps_appium', appium_cap)
                if value in ['True','False']:
                    value = eval(value)
                caps["appium:%s"%appium_cap] = value
            if cf.has_section('Caps_bstack'): #browserstack capabilities
                caps["bstack:options"]={}
                for bstack_cap in cf['Caps_bstack'].keys():
                    value = cf.get('Caps_bstack', bstack_cap)
                    if value in ['True', 'False']:
                        value = eval(value)
                    caps["bstack:options"][bstack_cap]=value
            if cf.has_section('Caps_lt'): #lambdatest capabilities
                caps["lt:options"] = {}
                for lt_cap in cf['Caps_lt'].keys():
                    value = cf.get('Caps_lt', lt_cap)
                    if value in ['True', 'False']:
                        value = eval(value)
                    caps["lt:options"][lt_cap] = value
            return caps
        except Exception as e:
            logging.error("get capability: %s"%e)
            return {}
    else:
        logging.warning("no capabilities set")
        return {}

def get_cmd_executor():
    """获取command_executor配置，用于webdriver初始化参数command_executor。若获取失败，返回默认值http://127.0.0.1:4444/wd/hub

    :return: 配置文件中WebDriver section command_executor的值
    """
    if cf.has_section('WebDriver'):
        try:
            return cf.get('WebDriver', 'command_executor')
        except Exception as e:
            logging.error("获取command executor配置失败： %s"%e)
            return "http://127.0.0.1:4444/wd/hub"


def get_other_app_activity():
    """获取另一个app的包名（用户企业微信运行场景下通过微信登录）

    :return: 另一个app的包名，默认为com.tencent.mm
    """
    if cf.has_section('WebDriver'):
        try:
            values = cf.get('WebDriver', 'other_app_activity').split((':'))
            return values[0], values[1]
        except Exception as e:
            logging.error("获取other_app配置失败： %s"%e)
            return "com.tencent.mm","com.tencent.mm.ui.LauncherUI"


# 获取es连接配置信息
def get_es_dict(section='ES'):
    try:
        es_dict = {}
        for i in cf.options(section):
            if i == 'hosts':
                es_dict['hosts'] = data_conversion_list(cf.get(section, 'hosts'))
            es_dict[i] = cf.get(section, i)
        es_dict["http_auth"]=(es_dict.pop('Username'),es_dict.pop('Password'))
        return es_dict
    except Exception as e:
        logging.error("获取es配置信息失败:%s" % e)
        return None


def get_data_file_mode():
    """ 获取数据文件的模式：
    merge（默认）：项目的测试用例数据在基准测试数据
    standalone: 项目使用独立的测试用例数据，适用于项目使用独立数据（例如使用达梦数据库，外部数据源）

    :return:
    """
    return get_value('Globals','data_file_mode','merge')
