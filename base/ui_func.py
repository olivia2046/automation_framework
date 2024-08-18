# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2020/9/14 9:24
desc:
'''
import logging,time
from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.firefox.options import Options
import base.globalvars as glo


class readiness_of_document(object):
    """使用javascript的document.readyState检查页面是否加载完成，定制wait condition
    参考：https://selenium-python.readthedocs.io/waits.html

    """
    def __init__(self):
        #self.driver = driver
        pass

    def __call__(self,driver):
        """

        :param driver: web driver

        :return: javascript返回的页面是否ready
        """
        ready_state =  driver.execute_script("return document.readyState;")
        return ready_state == "complete"

def initialize_web_driver():
    """获取web driver, 当前主要支持Chrome和Chrome_headless方式
    python selenium 获取接口数据: https://blog.csdn.net/mxdzchallpp/article/details/106475193


    :return: web driver
    """
    #web_driver_cfg = get_webdriver_cfg()
    web_driver_cfg = glo.get_value("webdriver_arg")
    web_driver_cfg = web_driver_cfg.split('_')


    if web_driver_cfg[0]=='Chrome':
        options = webdriver.ChromeOptions()

        if glo.get_value("enable_proxy") is True:
            from browsermobproxy import Server

            server_options = {"port":8090} #默认端口号为8080，一般会有冲突
            server = Server(options = server_options)
            server.start()

            proxy = server.create_proxy()
            if proxy is not None:
                logging.info("Browserweb-Proxy created!")
            else:
                logging.error("Browserweb-Proxy not created: cannot record HAR!")


            options.add_argument('--proxy-server={0}'.format(proxy.proxy))
        else:
            server = None
            proxy = None

        if len(web_driver_cfg) == 2 and web_driver_cfg[1] == 'headless': # Chrome headless
            options.add_argument("--headless")
            # https://github.com/SeleniumHQ/selenium/issues/4961
            # for unknown error: Chrome failed to start: exited abnormally, 添加两个argument
            options.add_argument("window-size=1024,768")
            options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(chrome_options=options,desired_capabilities=caps)
        driver = webdriver.Chrome(options=options)
        #return driver,proxy

    elif web_driver_cfg[0] == 'Firefox':
        if len(web_driver_cfg) == 2 and web_driver_cfg[1] == 'headless':  # Firefox headless
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument("-headless")
            driver = webdriver.Firefox(options = firefox_options)
        else:
            driver = webdriver.Firefox()
        server = None
        proxy = None
    elif web_driver_cfg[0] in ["Ie","Edge"]:
        driver = eval("webdriver.%s()"%web_driver_cfg[0])
        server = None
        proxy = None
    else:
        logging.error("web driver config should be Chrome/Chrome_headless/Firefox/Firefox_headless/Ie")
        driver = None
        server = None
        proxy = None
    if driver is not None:
        driver.implicitly_wait(3)
    return driver, server, proxy

#def close_driver(driver)

# def prepare_jquery(driver):
#     driver.execute_script("""var jquery_script = document.createElement('script');
#     jquery_script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js';
#     jquery_script.onload = function(){var $ = window.jQuery;};
#     document.getElementsByTagName('head')[0].appendChild(jquery_script);""")
#
#     time.sleep(0.5)  # time to load jQuery library


def scroll_to_window_top(driver):
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    # prepare_jquery(driver)
    # driver.execute_script('$(window).scrollTop(0)')



def scroll_to_window_bottom(driver):
    # # Chrome/Firefox/IE各自有适用的JS方法
    # if driver.name=='chrome':
    #     js = "var q=document.documentElement.scrollTop=10000"
    # elif driver.name=='firefox':
    #     #js = "var q=document.body.scrollTop = 10000"
    #     #js = "scroll(0, -250);"
    #     #js = "window.scrollTo(0,document.body.scrollHeight)"
    #js = "var q=document.documentElement.scrollTop=10000"
    js = "window.scrollTo(0,document.body.scrollHeight);"
    driver.execute_script(js)
    # # 统一用jQuery执行
    # prepare_jquery(driver)
    # driver.execute_script('$(window).scrollTop(10000)')