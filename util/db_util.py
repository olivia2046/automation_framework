# -*- coding: utf-8 -*-
'''
| @author: olivia.dou
| Created on: 2018/9/26 13:53
| desc:数据库相关的工具函数
'''
import sys, logging, re, inspect
import os
from base.get_config import get_es_dict

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # cx_Oracle 中文乱码问题
import pymysql
from DBUtils.PooledDB import PooledDB
sys.path.append('..')
import base.globalvars as glo


def init_conn_pool(db_section_name='DB'):
    """根据不同数据库选择不同驱动初始化连接池，存入全局变量

    :param db_section_name: 数据库配置在配置文件中的section名

    :return: 无
    """

    from base.get_config import get_db_type, get_db_host, get_db_user, get_db_pwd, get_db_database, get_db_port, \
        get_db_service_name

    if get_db_type(db_section_name).upper() == "MYSQL":
        pool = PooledDB(pymysql, 5, 16, host=get_db_host(db_section_name), user=get_db_user(db_section_name),
                        passwd=get_db_pwd(db_section_name), db=get_db_database(db_section_name),
                        port=int(get_db_port(db_section_name)), cursorclass=pymysql.cursors.DictCursor, charset="utf8")
        # glo.set_value("db_pool",pool)
    elif get_db_type(db_section_name).upper() == "ORACLE":
        import cx_Oracle
        pool = PooledDB(cx_Oracle, user=get_db_user(db_section_name), password=get_db_pwd(db_section_name),
                        dsn="%s:%s/%s" % (get_db_host(db_section_name), get_db_port(db_section_name),
                                          get_db_service_name(db_section_name)), mincached=5, maxcached=16)
    elif get_db_type(db_section_name).upper() == "DM": #达梦数据库 https://eco.dameng.com/document/dm/zh-cn/pm/dbutils-package.html
        import dmPython
        # pool = PooledDB(dmPython, maxconnections=6, mincached=2, maxcached=5, maxshared=3, setsession=[], ping=0,
        #                 host=get_db_host(db_section_name), port=int(get_db_port(db_section_name)),
        #                 user=get_db_user(db_section_name), password=get_db_pwd(db_section_name)) #SystemError: <class 'dmPython.Connection'> returned a result with an error set
        pool = PooledDB(dmPython, host=get_db_host(db_section_name), port=int(get_db_port(db_section_name)), user=get_db_user(db_section_name), password=get_db_pwd(db_section_name))
    else:
        pool = None
    poolname = (db_section_name + '_pool').lower()
    glo.set_value(poolname, pool)


def get_conn_pool(db_section_name='DB'):
    """获取连接池

    :param db_section_name:  数据库配置在配置文件中的section名

    :return: 全局变量中存储的连接池
    """
    poolname = (db_section_name + '_pool').lower()
    return glo.get_value(poolname)

def get_connection(db_section_name='DB'):
    """ 通过连接池获取连接失败的情况下，单独获取连接

    :param db_section_name: 数据库配置section名

    :return:
    """
    from base.get_config import get_db_type, get_db_host, get_db_user, get_db_pwd, get_db_port

    if get_db_type(db_section_name).upper() == "DM":
        import dmPython
        # conn = dmPython.connect(user=get_db_user(db_section_name), password=get_db_pwd(db_section_name),
        #                         server=get_db_host(db_section_name), port=int(get_db_port(db_section_name)))
        conn = dmPython.connect('bdc_qcc', 'chinascope1234', '192.168.100.17:5236')
        return conn


def execute_query(sql, *args, dbname='DB', result_type=None):  # 使用默认参数时，默认参数的位置要在args之后kwargs之前
    """执行sql

    :param sql: 待执行的sql
    :param dbname: 执行sql的数据库名，为测试框架配置文件中'DB'开头的section名
    :param args: tuple, list? or dict?，为解决执行插入None值的问题
    :param result_type: 默认为None,返回元组的列表，如为"dict"，则返回字典的列表

    :return: 查询的结果
    """

    """
    https://blog.csdn.net/legendary_Dragon/article/details/81254386
    调用方法：
    sql = "INSERT INTO test VALUES (%s,%s)"
    test_tuple=(3,None)
    execute_query(sql,*test_tuple,dbname="DB_XXX")
    """
    try:
        pool = get_conn_pool(dbname)
        if pool is None:
            init_conn_pool(dbname)
            pool = get_conn_pool(dbname)

        conn = pool.connection()  # 每次需要数据库连接就是用connection（）函数获取连接就好了
    except Exception: #通过连接池获取连接失败
        conn = get_connection(dbname)


    cursor = conn.cursor()

    try:
        # 执行SQL语句
        # logging.debug("sql: %s"%sql)
        cursor.execute(sql, *args)
        conn.commit()  # 对于增删改操作必须提交commit

        if result_type == "dict":  # type为dict时，MySql query执行结果为dict的list
            results = cursor.fetchall()
            # logging.debug(results)
            if results == ():  # 查询结果为空时，返回为空元组，统一格式
                results = []
            return results
        else:  # type默认为None时，将MySql query执行结果为dict的list转换为dict的values为tuple的list;oracle则执行结果本身就为tuple的list
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
    """从输入的文本中获取查询字符串

    :param input_str: 输入字符串

    :return: 查询字符串
    """
    pattern = 'select.+?;'
    # result = re.search(pattern,input_str)
    result = re.compile(pattern, re.S | re.I).search(input_str)
    if result is None:  # 如果不能匹配到分号，则匹配到结尾
        pattern = 'select.+'
        # result = re.search(pattern,input_str)
        result = re.compile(pattern, re.S).search(input_str)
    if result is not None:
        return result.group()
    else:
        return ""


def get_neo4j_driver():
    """根据配置文件中的配置信息获取neo4j驱动

    :return: neo4j驱动
    """
    from neo4j.v1 import GraphDatabase, basic_auth
    from base.get_config import get_neo4j_uri, get_neo4j_username, get_neo4j_pwd
    logging.getLogger("GraphDatabase").setLevel(logging.WARNING)
    uri = get_neo4j_uri()
    if uri is not None:
        # return GraphDatabase.driver(uri, auth=(get_neo4j_username(), get_neo4j_pwd()))
        return GraphDatabase.driver(uri, auth=basic_auth(get_neo4j_username(), get_neo4j_pwd()))
    else:
        return None


def get_mongodb_connection():
    """根据配置文件中的配置信息获取MongoDB的连接

    :return: MongoDB连接
    """
    from pymongo import MongoClient
    from base.get_config import get_mongodb_host, get_mongodb_port, get_mongodb_username, get_mongodb_password, \
        get_mongodb_mechanism
    host = get_mongodb_host()
    port = get_mongodb_port()
    username = get_mongodb_username()
    password = get_mongodb_password()
    mechanism = get_mongodb_mechanism()
    try:
        conn = MongoClient(host, int(port))
        db_auth = conn.admin
        db_auth.authenticate(username, password, mechanism=mechanism)
        return conn
    except Exception as e:
        return None


def get_redis_connection():
    """根据配置文件中的信息获取redis连接

    :return: Redis连接
    """
    from rediscluster import StrictRedisCluster
    from base.get_config import get_redis_host, get_redis_port
    host = get_redis_host()
    port = get_redis_port()

    startup_nodes = [{"host": host, "port": port}]
    try:
        conn = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        return conn
    except Exception as e:
        logging.error("Get Redis connection failed")
        return None


# def get_query_result(sql,func_name,fetch_one=True,result_type="dict"):
def get_query_result(sql, fetch_one=True, result_type="dict", dbname='DB'):
    """根据传入的sql返回一条或多条结果

    :param sql: 查询sql
    :param func_name: 函数名
    :param fetch_one: 是否仅获取一条
    :param result_type: 返回的结果类型，dict（默认）：返回字典的列表，tuple：返回元组的列表

    :return: 结果值
    """
    try:
        res = execute_query(sql, result_type=result_type, dbname=dbname)
        if fetch_one is True:
            return res[0] if len(res) > 0 else None
            # return res[0]
        else:
            return res
    except Exception as e:
        # logging.error("%s:%s"%(func_name, e))
        logging.error("%s:%s" % (inspect.getouterframes(inspect.currentframe(), 2)[1][3], e))
        raise Exception  # raise exception, 否则出错时用例仍为pass


def get_es_connection(**kwargs):
    """
    根据配置文件中的配置信息获取es的连接
    :param hosts: ip 传入的是一个列表或者单个ip 例如:["192.168.250.213", "192.168.250.210", "192.168.250.216"] or ["192.168.250.213"]
    :param cluster: 集群名
    :param timeout: 超时时间
    :param kwargs: Elasticsearch可支持的参数
    :return:
    """
    from elasticsearch import Elasticsearch
    try:
        es_dict = get_es_dict()
        es = Elasticsearch(es_dict["hosts"], cluster=es_dict["cluster"], timeout=int(es_dict["sniff_timeout"]), **kwargs)
        return es
    except Exception as e:
        logging.error("Get ES connection failed")
        logging.error(e)
        return None


def get_es_query_result(body=None,fetch_one=True):
    """
    查询es语句,获取>=1条的数据
    :param body: 查询语法
    :param fetch_one: 默认取一条:True
    :return: 返回指定路径下的es数据
    """
    try:
        es_dict = get_es_dict()
        es = get_es_connection(
                               http_auth=es_dict["http_auth"],  # 设置用户名和密码
                               sniff_timeout=es_dict["sniff_timeout"]  # 设置超时时间
                               )
        # 查询es语句
        result = es.search(index=es_dict["index"], body=body)
        if fetch_one is True:
            return result["hits"]["hits"][0] if len(result["hits"]["hits"]) > 0 else None
        else:
            return result["hits"]["hits"]
    except Exception as e:
        logging.error("查询es失败:%s" % e)
        logging.error(e)
        return None

if __name__ == '__main__':
    """
     https://blog.csdn.net/legendary_Dragon/article/details/81254386
     调用方法：
     sql = "INSERT INTO test VALUES (%s,%s)"
     test_tuple=(3,None)
     execute_query(sql,*test_tuple,dbname="DB_XXX")
     """
    body1={
  "query": {
   "match_phrase": {
     "regionCodes": "CSF_CN_360700"
   }
  }
}

    data = get_es_query_result(body=body1)
    print(data)
