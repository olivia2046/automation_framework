# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 6/23/2021 17:27
desc: 顶层的fixture
'''

import os, subprocess, logging, unittest
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path
import pytest
from urllib.parse import urlparse
import base.globalvars as glo
from py.xml import html

from util.clean_expired_files import delfile


def pytest_addoption(parser):
    '''增加命令行参数 --config'''
    parser.addoption(
        "--config",
        action="store",
        # default: 默认值，命令行没有指定host时，默认用该参数值
        default="DEMO",       
        help="test project name"
    )

    parser.addoption(
        "--webdriver",
        action="store",
        # default: 默认值，命令行没有指定host时，默认用该参数值
        default="Chrome",
        help="web driver used for ui automation"
    )

    parser.addoption(
        "--limit",
        action="store",
        default=-1,
        type=int,
        help="Maximum number of permutations of parametrised tests to run",
    )

    parser.addoption(
        "--devicename",
        action="store",
        help="app automation device name"
    )

    parser.addoption(
        "--platformversion",
        action="store",
        help="app automation platform version"
    )

    parser.addoption(
        "--platformname",
        action="store",
        help="app automation platform name"
    )

    parser.addoption(
        "--appurl",
        action="store",
        help="app automation app url"
    )

   
    parser.addoption(
        "--email",
        action="store_true",
        default = False,
        help="whether to send email for pytest report(not allure report generated from jenkins)"
    )


def pytest_collection_modifyitems(session, config, items):
    """根据命令行参数传入的limit数，在执行参数化的一组用例时，仅执行前limit个用例（适用场景如一组用例中若干个为高优先级用例/Smoke test用例，执行全组用例太耗时时）

    :param session:
    :param config:
    :param items:
    :return:
    """
    def get_base_name(test_name):
        """
        Get name of test without parameters

        Parametrised tests have the [ character after the base test name, followed by
        the parameter values. This removes the [ and all that follows from test names.
        """
        try:
            return test_name[: test_name.index("[")]
        except ValueError:
            return test_name

    for item in items: #解决测试用例名乱码问题
        #item.name = item.name.encode("utf-8").decode("unicode_escape")
        #item.nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        # if item.cls.__bases__[0] is not unittest.case.TestCase: # unittest的用例，item.nodeid不能转码
        if item.parent.__class__.__name__!='UnitTestCase': # unittest的用例，item.nodeid不能转码
            item._nodeid = item._nodeid.encode("utf-8").decode("unicode_escape")
        # else:
        #     item.name = item.name.encode("utf-8").decode("unicode_escape")



    limit = config.getoption("--limit")
    if limit >= 0:
        tests_by_name = {item.name: item for item in items}
        test_base_names = set(get_base_name(name) for name in tests_by_name.keys())

        tests_to_run = []
        for base_name in test_base_names:
            #to_skip = [t for n, t in tests_by_name.items() if base_name in n][limit:]
            to_skip = [t for n, t in tests_by_name.items() if (base_name + '[') in n][limit:]  #对于多个testcase名有相同的substring的情况，防止被错误跳过
            for t in to_skip:
                t.add_marker("skip")



@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(2, html.th('Test_nodeid'))
    # cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop(2)

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    # cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop(2)

# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     report.description = str(item.function.__doc__)

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        # if (report.skipped and xfail) or (report.failed and not xfail):
        #     file_name = report.nodeid.replace("::", "_")+".png"
        #     screen_img = _capture_screenshot()
        #     if file_name:
        #         html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
        #                'onclick="window.open(this.src)" align="right"/></div>' % screen_img
        #         extra.append(pytest_html.extras.html(html))
        report.extra = extra
        #report.description = str(item.function.__doc__)
        if item.function.__doc__ is not None:
            report.description = str(item.function.__doc__.split('\n')[0]) #docstring仅取第一行内容
        else:
            report.description = ""
        #report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")


# @pytest.fixture(scope="session", autouse=True)  # autouse=True自动执行该前置操作
# def get_config(request):
#     glo.init()
#     glo.set_value("config_name",request.config.getoption("--config"))
#     print("当前用例运行环境配置:%s"%glo.get_value("config_name"))
#
#     from base.get_config import get_and_set_global_vars,get_url_dict
#     get_and_set_global_vars()
#     url_dict = get_url_dict()
#     if url_dict != {}:
#         for item in url_dict.items():
#             glo.set_value(item[0], item[1])
#             glo.set_value("host" + item[0][-1], urlparse(item[1]).hostname)

# hooks钩子函数 调用方式:收集完所有测试项目后调用
# 该钩子函数实现的功能有获取url地址 生成html和allure测试报告
'''
先执行标有tryfirst=True的钩子函数
再执行标有trylast=True的钩子函数
再执行标有hookwrapper=True的钩子函数
'''


@pytest.hookimpl(tryfirst=True)  # trylast=True  hookwrapper=True
# pytest_configure(config)允许插件和conftest文件执行初始配置。
# 通过config.pluginmanager.register（）这个函数可以实现注册插件的功能，后续pytest这个框架在运行过程中就会调用你注册的插件
def pytest_configure(config):
    def _get_config():
        glo.init()
        # 设置运行环境名:{'config_name':BMV_QA}
        glo.set_value("config_name", config.option.config)
        print("当前用例运行环境配置:%s" % glo.get_value("config_name"))

        from base.get_config import get_and_set_global_vars, get_url_dict
        #from util import db_util

        # 获取并设置
        get_and_set_global_vars()
        # 获取ini文件中URLS的字典数据
        url_dict = get_url_dict()
        # 判断ini文件中URLs不能为空字典
        if url_dict != {}:
            for item in url_dict.items():
                # 设置url
                glo.set_value(item[0], item[1])
                # 设置hosts
                glo.set_value("host" + item[0][-1], urlparse(item[1]).hostname)

        glo.set_value("webdriver_arg",config.option.webdriver)
        glo.set_value("device_name",config.option.devicename)
        glo.set_value("platform_name",config.option.platformname)
        glo.set_value("platform_version",config.option.platformversion)
        glo.set_value("app_url", config.option.appurl)
        # if config.option.check_std_entity=='1':
        #     glo.set_value("check_std_entity", True)
        # else:
        #     glo.set_value("check_std_entity", False)

    _get_config()

    config_name = glo.get_value("config_name")

    from base.get_config import get_log_level
    logger = logging.getLogger(__name__)
    # logger.setLevel(level=logging.INFO)
    abspath = os.path.split(os.path.realpath(__file__))[0]
    root_path = abspath + os.sep + 'testreport'
    dir_path = Path(root_path)
    # 不存在就新增testreport目录
    dir_path.mkdir(exist_ok=True, parents=True)
    handler = TimedRotatingFileHandler(root_path + os.sep + 'run.log', when='d', interval=1, backupCount=30,
                                       encoding='utf-8')
    handler.setLevel(eval("logging." + get_log_level()))
    formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)

    # 设置特定库的log level(否则有大量debug输出)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("chardet.charsetprober").setLevel(logging.WARNING)  # 客户端查询时自动输出的日志
    logging.getLogger("faker.factory").setLevel(logging.WARNING)

    now = datetime.now()
    # create report target dir
    # reports_dir = Path('reports', now.strftime('%Y%m%d'))
    # from base.get_config import get_test_type
    # test_type = get_test_type()
    reports_dir = Path("%s/testreport" % abspath)
    raw_dir = Path("%s/xml" % reports_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    html_dir = Path("%s/html" % reports_dir)
    html_dir.mkdir(parents=True, exist_ok=True)
    # set custom options only if none are provided from command line
    if not hasattr(config.option,"htmlpath") or config.option.htmlpath is None:  # 未指定--html
        # reports_dir.mkdir(parents=True, exist_ok=True)
        # # custom report file
        environment_str = glo.get_value("device_name","") + "_" + glo.get_value("platform_name","") + "_" + glo.get_value("platform_version","")
        if environment_str!="": #分环境执行
            report_file_path = reports_dir / f"pytest_{environment_str}_{config_name}_{now.strftime('%Y%m%d %H%M%S')}.html"
        else:
            report_file_path = reports_dir / f"pytest_{config_name}_{now.strftime('%Y%m%d %H%M%S')}.html"
        # adjust plugin options
        config.option.htmlpath = report_file_path
        config.option.self_contained_html = True

    if not hasattr(config.option,"allure_report_dir") or config.option.allure_report_dir is None:
        config.option.allure_report_dir = raw_dir

    config.option.clean_alluredir = True

    glo.set_value("report_file_path",config.option.htmlpath)





def pytest_unconfigure(config):

    abspath = os.path.split(os.path.realpath(__file__))[0]
    xml_report_path = '%s/testreport/xml/' % abspath
    html_report_path = '%s/testreport/html/' % abspath
    delfile(abspath + os.sep + '/testreport', 30)

    cmd = "allure generate %s -o %s --clean" % (xml_report_path, html_report_path)

    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # cmd="allure serve testreport/xml"
    # subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    report_file_path = glo.get_value("report_file_path")
    config_name = glo.get_value("config_name")
    from base.get_config import get_test_type
    test_type = get_test_type()

    if config.option.email:
        from base.email_pytest_report import Email_Pytest_Report
        email_obj = Email_Pytest_Report()
        # 1. Send html formatted email body message with pytest report as an attachment
        # Here log/pytest_report.html is a default file. To generate pytest_report.html file use following command to the test e.g. py.test --html = log/pytest_report.html
        # report_file_path=os.path.abspath(os.path.join(os.path.dirname(__file__),report_file_path))
        email_obj.send_test_report_email(html_body_flag=True, attachment_flag=True, report_file_path=str(report_file_path),
                                         subject_prefix="%s test %s" % (test_type, config_name))
