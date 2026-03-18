# -*- coding: utf-8 -*-
'''
| @author: olivia.dou
| Created on: 2018/10/18 17:37
| desc: 和日期相关的util function
'''

import base.globalvars as glo
from datetime import datetime
from dateutil.relativedelta import *
import time,logging


def get_datetime_from_now(floor_time = False, format="%Y-%m-%d %H:%M:%S", **kwargs):
    """获取距离今天给定时间段的日期，to be called in excel test case, like in the parameter
    part of URL as below:
        | start=${get_date_from_today(-7)}&end=${get_date_from_today(0)}

    :param floor_time: 时间向下取整到零时
    :param format: 返回的时间字符串格式
    :param kwargs: 可变参数，支持years, months, days, leapdays, weeks, hours, minutes, seconds, microseconds
        | （与dateutil中的relativedelta类的构造函数参数对应）正数代表当前时间之后的时间，负数代表当前时间之前的时间

    :return: 指定format的日期时间
    """

    for key in kwargs.keys():
        if key not in ['years', 'months', 'days', 'leapdays', 'weeks',
                 'hours', 'minutes', 'seconds', 'microseconds']:
            logging.error("params error! %s not a legal parameter"%key)
            return
    date_time = datetime.now() + relativedelta(**kwargs)
    if floor_time:
        time_tuple = date_time.timetuple()
        time_obj =  time.mktime(time_tuple)
        timestamp = time_obj - time_obj % 86400 # 用时间戳减去时间戳对24小时取的余数，即时间戳的整数
        result = datetime.utcfromtimestamp(timestamp).strftime(format) #fromtimestamp转换为Local time，此处需要的是0时的字符串，因此用utcfromtimestamp
    else:
        result = date_time.strftime(format)

    return result

def wait(seconds=5):
    """等待指定的时间（提供给Excel case调用）

    :param seconds: 等待的秒数

    :return: 无
    """
    time.sleep(seconds)

def get_current_timestamp(n=0,convert_str=False,get_round=False):
    """获取当前时间戳

    :param n: 需乘以10的n次方
    :param convert_str: 是否需要转换为字符串
    :param get_round: 是否需要取整

    :return: cenvert_str为True时，返回转换的字符串，否则返回浮点数
    """
    result = time.time()*pow(10,n)
    if get_round:
        result = round(result)

    if convert_str:
        result =  str('{:.0f}'.format(result)) #大整数取消科学计数法显示

    glo.set_value("timestamp",result) #可用于在用例的setup部分获取时间，设置全局变量供数据部分使用
    return result


def get_current_datetime(date_time_format='%Y-%m-%d %H:%M:%S'):
    """

    :param date_time_format: 日期时间格式

    :return:
    """
    return timestamp_to_str(get_current_timestamp())


def str_to_timestamp(datetime_str,format="%Y-%m-%d %H:%M:%S"):
    """将字符串类型的日期时间转换为时间戳

    :param datetime_str: 字符串类型的日期时间
    :param format: 日期时间格式

    :return: 时间戳
    """
    try:
        timearray = time.strptime(datetime_str, format)
        timestamp = time.mktime(timearray)
        return timestamp
    except Exception as e:
        logging.error("date_util.str_to_timestramp error:")
        return None

def timestamp_to_str(timestamp,format="%Y-%m-%d %H:%M:%S"):
    """时间戳转换为字符串

    :param timestamp: 输入的时间戳
    :param format: 日期时间格式

    :return: 日期时间字符串
    """

    timearray = time.localtime(timestamp)
    result = time.strftime(format, timearray)
    return result

def datetime_roundly_equal(datetime1, datetime2, format_str):
    """判断两个日期是否近似？

    :param datetime1: 接口输入的日期时间字符串
    :param datetime2: 接口返回的日期时间字符串
    :format_str: 日期时间的格式字符串，如‘%Y-%m-%dT%H:%M:%S.%f%z’

    :return: datetime1四舍五入是否等于datetime2
    """
    inbound_datetime = datetime.strptime(datetime1, format_str)
    outbound_datetime= datetime.strptime(datetime2, format_str)
    inbound_timestamp = inbound_datetime.timestamp()
    outbound_timestamp = outbound_datetime.timestamp()

    return round(inbound_timestamp==outbound_timestamp)


def convert_fq_to_fp(financial_quarter):
    """
    将财季转换成季末月份字符串（报告期）

    :param financial_quarter: 财季，Q1/Q2/Q3/Q4

    :return: 季末月份字符串，即报告期
    """
    fq_fp_mapping = {"Q1":"03","Q2":"06","Q3":"09","Q4":"12"}
    try:
        return fq_fp_mapping[financial_quarter]
    except Exception as e:
        logging.error("convert_fq_to_fp:%s"%e)


def get_fyfq_of_date(input_date):
    """获取指定日期所在的财年、财季

    :param input_date: 输入日期，格式yyyy-mm-dd

    :return: 日期所在的财年财季，如2018Q4
    """

    try:
        fy = input_date[:4]
        month = input_date[5:7]
        fq = "Q"+ str((int(month)-1)//3+1)
        return fy+fq
    except Exception as e:
        logging.error("get_fyfq_of_date:%s"%e)
        return ""

def get_fyfp_of_date(input_date):
    """获取指定日期所在的财年、报告期,日期是yyyy-mm-dd的格式

    :param input_date: 输入日期，格式yyyy-mm-dd

    :return: 日期所在的财年报告期，如201812
    """
    """"""
    fyfq=get_fyfq_of_date(input_date)
    fy = fyfq[:4]
    fq = fyfq[4:]
    fp = convert_fq_to_fp(fq)
    return fy+fp

# def convert_datetime_str(input_str,input_format,output_format,timezone_delta):
#     """将一种格式的日期时间字符串转为另一种格式
#
#     :param input_str: 输入字符串
#     :param input_format: 输入格式
#     :param output_format: 目标格式
#     :param timezone_delta: 需要叠加的时区delta
#
#     :return: 指定格式的字符串
#     """
#     timestamp = str_to_timestamp(input_str, input_format)
#     return timestamp_to_str(output_format, timestamp + timezone_delta*60*60)






