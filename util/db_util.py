# -*- coding: utf-8 -*-
'''
| @author: olivia.dou
| Created on: 2018/9/26 13:53
| desc:数据库相关的工具函数
'''
import sys, logging, re, inspect
import os


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # cx_Oracle 中文乱码问题
import pymysql
# need to install DBUtils==1.4
from DBUtils.PooledDB import PooledDB
sys.path.append('..')
#import base.globalvars as glo
import base.config as global_config



def init_conn_pool(db_section_name='DB'):
    """根据不同数据库选择不同驱动初始化连接池，存入全局变量

    :param db_section_name: 数据库配置在配置文件中的section名

    :return: 无
    """

    #from base.get_config import get_db_type, get_db_host, get_db_user, get_db_pwd, get_db_database, get_db_port, \
    #    get_db_service_name

    #if get_db_type(db_section_name).upper() == "MYSQL":
    db_type = global_config.config.get(db_section_name).get("db_type","MySQL").upper()
    host = global_config.config[db_section_name]["host"]
    username = global_config.config[db_section_name]["username"]
    password = global_config.config[db_section_name]["password"]
    database = global_config.config[db_section_name]["database"]
    port = int(global_config.config[db_section_name]["port"])
    if db_type == "MYSQL":
        pool = PooledDB(pymysql, 5, 16, host=host, user=username, passwd=password, db=database, port=port,
                        cursorclass=pymysql.cursors.DictCursor, charset="utf8")

    elif db_type == "ORACLE":
        import cx_Oracle
        '''oracle_cx need to use service name instead of sid
            check Oracle service name:select value from v$parameter where name like '%service_name%
        '''
        pool = PooledDB(cx_Oracle, user=username, password=password,
                        dsn=f"{host}:{port}/{global_config.config.get(db_section_name).get('service_name')}" , mincached=5, maxcached=16)
    elif db_type == "DM": #dameng db https://eco.dameng.com/document/dm/zh-cn/pm/dbutils-package.html
        import dmPython
        # pool = PooledDB(dmPython, maxconnections=6, mincached=2, maxcached=5, maxshared=3, setsession=[], ping=0,
        #                 host=get_db_host(db_section_name), port=int(get_db_port(db_section_name)),
        #                 user=get_db_user(db_section_name), password=get_db_pwd(db_section_name)) #SystemError: <class 'dmPython.Connection'> returned a result with an error set
        pool = PooledDB(dmPython, host=host, port=port, user=username, password=password)
    else:
        pool = None
    poolname = (db_section_name + '_pool').lower()
    global_config[poolname]=pool
    #glo.set_value(poolname, pool)


def get_conn_pool(db_section_name='DB'):
    """获取连接池

    :param db_section_name:  数据库配置在配置文件中的section名

    :return: 全局变量中存储的连接池
    """
    poolname = (db_section_name + '_pool').lower()
    #return glo.get_value(poolname)
    return global_config.config.get(poolname)

def get_connection(db_section_name='DB'):
    """ get connection separately, when it fails to get connection from connection pool

    :param db_section_name: section name for db configuration

    :return:
    """
    #from base.get_config import get_db_type, get_db_host, get_db_user, get_db_pwd, get_db_port
    db_type = global_config.config.get(db_section_name).get("db_type", "MySQL").upper()
    host = global_config.config[db_section_name]["host"]
    username = global_config.config[db_section_name]["username"]
    password = global_config.config[db_section_name]["password"]
    port = int(global_config.config[db_section_name]["port"])
    if db_type == "DM":
        import dmPython
        # conn = dmPython.connect(user=get_db_user(db_section_name), password=get_db_pwd(db_section_name),
        #                         server=get_db_host(db_section_name), port=int(get_db_port(db_section_name)))
        conn = dmPython.connect(username, password, f"{host}:{port}")

        return conn


def execute_query(sql, *args, db_section_name='DB', result_type=None):  # when using default value of an argument, it should be placed before keyword arguments
    """

    :param sql: sql
    :param db_section_name: db section in configuration file
    :param args: tuple, list? or dict?，to resolve issue of inserting None when executed
    :param result_type: by default is None,return list of tuples, if "dict"，then return list of dictionary

    :return:
    """

    """
    https://blog.csdn.net/legendary_Dragon/article/details/81254386
    Call ：
    sql = "INSERT INTO test VALUES (%s,%s)"
    test_tuple=(3,None)
    execute_query(sql,*test_tuple,dbname="DB_XXX")
    """
    try:
        pool = get_conn_pool(db_section_name)
        if pool is None:
            init_conn_pool(db_section_name)
            pool = get_conn_pool(db_section_name)

        conn = pool.connection()  # use connection() to get connection when needed
    except Exception: # fails to get connection by connection pool
        conn = get_connection(db_section_name)


    cursor = conn.cursor()

    try:

        # logging.debug("sql: %s"%sql)
        cursor.execute(sql, *args)
        conn.commit()  # need to commit after dml

        if result_type == "dict":  # query result is list of dictionary
            results = cursor.fetchall()
            # logging.debug(results)
            if results == ():  # when query result is empty, return empty tuple
                results = []
            return results
        else:
            # When `type` defaults to `None`, the result of a MySQL query—originally a list of dictionaries—is converted into a list of dictionaries where the values are tuples;
            # for Oracle, the query result is inherently a list of tuples.
            res = cursor.fetchall()
            results = []
            for i in range(len(res)):
                if isinstance(res[i], dict):
                    results.append(tuple(res[i].values()))
                else:
                    results.append(res[i])
            return results

    except Exception as e:
        logging.error("Error: unable to execute query, %s" % e)
        raise
    finally:
        cursor.close()
        conn.close()


def get_query_string(input_str):
    """ Extract the query string from the input text.

    :param input_str: input string

    :return: query string
    """
    pattern = 'select.+?;'
    # result = re.search(pattern,input_str)
    result = re.compile(pattern, re.S | re.I).search(input_str)
    if result is None:  # If a semicolon is not matched, match until the end
        pattern = 'select.+'
        # result = re.search(pattern,input_str)
        result = re.compile(pattern, re.S).search(input_str)
    if result is not None:
        return result.group()
    else:
        return ""


def get_neo4j_driver():
    """Retrieve the Neo4j driver based on the configuration information in the configuration file

    :return: neo4j驱动
    """
    from neo4j.v1 import GraphDatabase, basic_auth
    #from base.get_config import get_neo4j_uri, get_neo4j_username, get_neo4j_pwd
    logging.getLogger("GraphDatabase").setLevel(logging.WARNING)
    uri = global_config.config["NEO4J"]["uri"]
    username = global_config.config["NEO4J"]["uri"]
    password = global_config.config["NEO4J"]["password"]
    if uri is not None:
        # return GraphDatabase.driver(uri, auth=(get_neo4j_username(), get_neo4j_pwd()))
        return GraphDatabase.driver(uri, auth=basic_auth(username, password))
    else:
        return None


def get_mongodb_connection():
    """Obtain a MongoDB connection based on the configuration information in the configuration file.

    :return: MongoDB connection
    """
    from pymongo import MongoClient
    #from base.get_config import get_mongodb_host, get_mongodb_port, get_mongodb_username, get_mongodb_password, \
    #    get_mongodb_mechanism
    host = global_config.config["MongoDB"]["host"]
    port = global_config.config["MongoDB"]["port"]
    username = global_config.config["MongoDB"]["username"]
    password = global_config.config["MongoDB"]["password"]
    mechanism = global_config.config["MongoDB"]["mechanism"]

    try:
        conn = MongoClient(host, int(port))
        db_auth = conn.admin
        db_auth.authenticate(username, password, mechanism=mechanism)
        return conn
    except Exception as e:
        return None


def get_redis_connection():
    """ Obtain a Redis connection based on the information in the configuration file.

    :return: Redis connection
    """
    from rediscluster import StrictRedisCluster
    #from base.get_config import get_redis_host, get_redis_port
    host = global_config.config["Redis"]["host"]
    port = global_config.config["Redis"]["port"]

    startup_nodes = [{"host": host, "port": port}]
    try:
        conn = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        return conn
    except Exception as e:
        logging.error("Get Redis connection failed")
        return None


# def get_query_result(sql,func_name,fetch_one=True,result_type="dict"):
def get_query_result(sql, fetch_one=True, result_type="dict", dbname='DB'):
    """return one or more results by sql

    :param sql: sql
    :param func_name: function_name
    :param fetch_one: whether to fetch one result
    :param result_type: type of returned result:dict (by default)-return list of dictionary, tuple-return list of tuples

    :return: 结果值
    """
    try:
        res = execute_query(sql, result_type=result_type, db_section_name=dbname)
        if fetch_one is True:
            return res[0] if len(res) > 0 else None
            # return res[0]
        else:
            return res
    except Exception as e:
        # logging.error("%s:%s"%(func_name, e))
        logging.error("%s:%s" % (inspect.getouterframes(inspect.currentframe(), 2)[1][3], e))
        raise Exception  # raise exception, 否则出错时用例仍为pass



# if __name__ == '__main__':
#     """
#      https://blog.csdn.net/legendary_Dragon/article/details/81254386
#      # Call by：
#      sql = "INSERT INTO test VALUES (%s,%s)"
#      test_tuple=(3,None)
#      execute_query(sql,*test_tuple,dbname="DB_XXX")
#      """
#     body1={
#   "query": {
#    "match_phrase": {
#      "regionCodes": "CSF_CN_360700"
#    }
#   }
# }
#
#     data = get_es_query_result(body=body1)
#     print(data)
