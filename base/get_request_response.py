#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Leiyh
# @File : get_request_response.py
import json

import allure
from base import globalvars as glo
from util.api import request_tool
from util.report import log_tool


def get_request_url(url,path):
    """
    :param url: 获取config/settings - BMV_QA.ini文件中指定的url1的数据 例如:url1
    :param path:路径地址,例如:'/api/bank/region/sector/topics/detail?regionCode=CSF_CN_110000&industryFilter=GB&_v=1628245529950'
    :return:返回拼接好的完整的url
    """
    api_url = glo.get_value(url)
    join_url = api_url + path
    allure.attach(join_url, '请求地址', allure.attachment_type.TEXT)
    # log_tool.info('\n请求地址：\n' + join_url)
    return join_url


def record_allure_log(comment, json_headers):
    """
    :param headers: 生成的具体接口数据,例如:json_headers=json.dumps(headers, ensure_ascii=False, indent=4)
    :param comment:备注信息 例如:'请求头'
    """
    allure.attach(json_headers, comment, allure.attachment_type.TEXT)
    # log_tool.info('\n{}：\n'.format(comment) + json_headers)


def allure_step_url(url, headers):
    """
    :param url: path 例如:/api/bank/region/sector/list?topicCode=TP0001&regionCode=CSF_CN_110000&industryFilter=GB&_v=1627007267703
    :param headers: 请求头信息
    :return:  返回完整的urls
    """
    with allure.step('第1步：准备请求报文'):
        urls = get_request_url("url1", url)
        record_allure_log('请求头', json.dumps(headers, ensure_ascii=False, indent=4))
        return urls

def allure_step_url_path(url,path,headers):
    """
    :param url: ini文件中指定的key 例如：url1
    :param path: 例如:/api/bank/region/sector/list?topicCode=TP0001&regionCode=CSF_CN_110000&industryFilter=GB&_v=1627007267703
    :param headers: 请求头信息
    :return: 返回完整的urls
    """
    with allure.step('第1步：准备请求报文'):
        urls = get_request_url(url, path)
        record_allure_log('请求头', json.dumps(headers, ensure_ascii=False, indent=4))
        return urls


def allure_step_url_data(url_path, headers, json_data=None, ip="url1"):
    """
    :param url_path: 接口路径地址:'/api/bank/news/stat/event'
    :param headers: 接口请求头信息
    :param json_data: 请求参数
    :param ip:获取config/settings - BMV_QA.ini文件中指定的url1的数据 例如:url1
    :return:返回完整的url链接
    """
    with allure.step('第1步：准备请求报文'):
        urls = get_request_url(ip, url_path)  # 拼接url
        record_allure_log('请求头', json.dumps(headers, ensure_ascii=False, indent=4))
        record_allure_log('请求正文', json.dumps(json_data, ensure_ascii=False, indent=4))
    return urls


def allure_step_request_tool_get(url, headers,params=None,cookies=None):
    """
    :param url: 完整的urls
    :param headers: 请求头信息
    :return: 返回接口响应数据
    """
    with allure.step('第2步：调用接口'):
        resp = request_tool.get(url, headers=headers,params=params,cookies=cookies)
    return resp


def allure_step_request_tool_post(url, headers, json_data=None,data=None,params=None,files=None,cookies=None):
    """
    :param url: 完整的urls
    :param headers: 请求头信息
    :param json_data: 传入json格式的数据
    :param data: 传入的格式的数据
    :return:  u
    """
    with allure.step('第2步：调用接口'):
        resp = request_tool.post(url, headers=headers, json=json_data,data=data,params=params,files=files,cookies=cookies)
    return resp


def allure_step_request_tool_delete(url, headers, json_data=None,data=None):
    with allure.step('第2步：调用接口'):
        resp = request_tool.delete(url=url, headers=headers, json=json_data,data=data)
    return resp


def allure_step_response_json(resp):
    """
    :param resp: 传入接口响应数据
    :return: 返回处理之后的json数据
    """
    with allure.step('第3步：接收响应'):
        data = resp.json()
        if resp.status_code != 200:
            record_allure_log(json.dumps(data, ensure_ascii=False, indent=4), '响应报文')
        else:
            record_allure_log('无', '响应报文')
    return data


def allure_step_response_text(resp):
    """
    :param resp: 传入接口响应数据
    :return: 返回处理之后的text数据
    """
    with allure.step('第3步：接收响应'):
        data = resp.text
        if resp.status_code != 200:
            record_allure_log(json.dumps(data, ensure_ascii=False, indent=4), '响应报文')
        else:
            record_allure_log('无', '响应报文')
    return data


def allure_step_assert_response(resp,error_description="接口查询失败,状态码不为200"):
    with allure.step('第4步：判断结果'):
        if resp.status_code == 200:
            record_allure_log('断言状态码是否为200', "{} == 200".format(resp.status_code))
        else:
            record_allure_log('断言状态码是否为200', "{} != 200".format(resp.status_code))
        assert resp.status_code == 200,error_description


def allure_step_extract_data(data='无'):
    with allure.step('第5步：提取数据'):
        allure.attach(data, '提取数据列表', allure.attachment_type.TEXT)
        # log_tool.info('\n提取数据列表：\n' + data)
        # log_tool.info('\n\n\n')
