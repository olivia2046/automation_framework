# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2020/9/19 20:30
desc: UI自动化时基于分层自动化的考量，需验证页面请求时前端调用的接口参数是否符合预期，使用Browsermob-Proxy实现该功能
| 本模块为与UI自动化时使用的proxy相关的功能
'''

def get_full_request_url(proxy, requese_base_url):
    """获取请求的完整Url(页面请求时的完整url

    :param proxy: browsermobproxy代理
    :param requese_base_url: 页面请求的基本url(指定不带参的部分)

    :return: 请求的完整url
    """
    result = proxy.har

    for entry in result['log']['entries']:
        _url = entry['request']['url']
        # 根据URL找到数据接口
        if requese_base_url in _url:
            return _url

def start_new_har(proxy,ref=None, options=None, title=None):
    """封装browsermobproxy的new_har方法:sets a new HAR to be recorded

    :param proxy: browsermobproxy
    :param ref: (str) – A reference for the HAR. Defaults to None
    :param options: (dict) – A dictionary that will be passed to BrowserMob Proxy with specific keywords. Keywords are:
    |    captureHeaders: Boolean, capture headers
    |    captureContent: Boolean, capture content bodies
    |    captureBinaryContent: Boolean, capture binary content
    :param title:  (str) – the title of first har page. Defaults to ref.

    :return: none
    """

    if proxy is not None:
        if options is None:
            options = {'captureHeaders': True, 'captureContent': True}
        proxy.new_har(ref, options=options,title=title)


def parameter_in_full_url(proxy, base_url, param_str):
    # 获取接口请求中的参数
    if proxy is not None:
        request_url = get_full_request_url(proxy, base_url)
        return param_str in request_url
    else: #不支持代理的webdriver,不做校验
        return True