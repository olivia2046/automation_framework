# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 3/12/2026 17:27
desc: common hooks
used to be defined in top-level conftest.py, but since projects may need to have their own pytest.ini/pyproject.toml
which leads to top-level conftest.py not loaded, put these hook definitions here, and register in project conftest.py as:
pytest_plugins = ["base.pytest_plugins.common_hooks"]
'''

import os, subprocess, logging, sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path
import pytest
from urllib.parse import urlparse

import yaml

import base.globalvars as glo
import base.config as global_config

# add automation_framework/ to sys.path, so base/ and projects/ both can be imported as top level package
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# _FRAMEWORK_ROOT = os.path.dirname(os.path.abspath(__file__))
# print(f"[conftest] inserting into sys.path: {_FRAMEWORK_ROOT}")
# sys.path.insert(0, _FRAMEWORK_ROOT)

from util.clean_expired_files import delfile

_HOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_DIR = os.path.abspath(os.path.join(_HOOKS_DIR, "..", "..", "config"))


def pytest_addoption(parser):
    """ command line parameters

    :param parser:
    :return:
    """
    parser.addoption(
        "--config",  # to specify test cases of which project/environement is to be executed
        action="store",
        default="automation_exercise_web",
        help="test project name"
    )

    parser.addoption(
        "--webdriver",  # for Selenium cases: which webdriver to be used: Chrome/Firefox/Edge
        action="store",
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
        default=False,
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

    for item in items:  # 解决测试用例名乱码问题
        # item.name = item.name.encode("utf-8").decode("unicode_escape")
        # item.nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        # if item.cls.__bases__[0] is not unittest.case.TestCase: # unittest的用例，item.nodeid不能转码
        if item.parent.__class__.__name__ != 'UnitTestCase':  # unittest的用例，item.nodeid不能转码
            item._nodeid = item._nodeid.encode("utf-8").decode("unicode_escape")
        # else:
        #     item.name = item.name.encode("utf-8").decode("unicode_escape")

    limit = config.getoption("--limit")
    if limit >= 0:
        tests_by_name = {item.name: item for item in items}
        test_base_names = set(get_base_name(name) for name in tests_by_name.keys())

        tests_to_run = []
        for base_name in test_base_names:
            # to_skip = [t for n, t in tests_by_name.items() if base_name in n][limit:]
            to_skip = [t for n, t in tests_by_name.items() if (base_name + '[') in n][
                limit:]  # 对于多个testcase名有相同的substring的情况，防止被错误跳过
            for t in to_skip:
                t.add_marker("skip")


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")
    cells.insert(2, "<th>Test_nodeid</th>")
    # cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    if hasattr(report, 'description'):
        cells.insert(2, "<td>%s</td>" % report.description)
    else:
        cells.insert(2, "<td>no description</td>")
    # cells.insert(2, "<td>%s</td>"%report.description)
    cells.insert(2, "<td>%s</td>" % report.nodeid)
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
    get screenshot automatically when test fail, and display in html report
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    # if report.when == 'call' or report.when == "setup":
    #     xfail = hasattr(report, 'wasxfail')
    #     # if (report.skipped and xfail) or (report.failed and not xfail):
    #     #     file_name = report.nodeid.replace("::", "_")+".png"
    #     #     screen_img = _capture_screenshot()
    #     #     if file_name:
    #     #         html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
    #     #                'onclick="window.open(this.src)" align="right"/></div>' % screen_img
    #     #         extra.append(pytest_html.extras.html(html))
    report.extra = extra
    # report.description = str(item.function.__doc__)
    if item.function.__doc__ is not None:
        # report.description = str(item.function.__doc__.split('\n')[0]) #docstring仅取第一行内容
        setattr(report, 'description', str(item.function.__doc__.split('\n')[0]))  # take the first line of docstring
    else:
        # report.description = ""
        setattr(report, 'description', 'No description provided')

        # report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")


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
    # def _get_config():
    #
    #     glo.init()
    #     # set config name(indicate which configuration file to look for )
    #     glo.set_value("config_name", config.option.config)
    #
    #     logging.info("Now running case using config:%s" % glo.get_value("config_name"))
    #
    #
    #
    #     from base.get_config import get_and_set_global_vars, get_url_dict
    #
    #     # 获取并设置
    #     # GetConfig.get_and_set_global_vars()
    #     get_and_set_global_vars()
    #     # 获取ini文件中URLS的字典数据
    #     # url_dict = GetConfig.get_url_dict()
    #     url_dict = get_url_dict()
    #     # 判断ini文件中URLs不能为空字典
    #     if url_dict != {}:
    #         for item in url_dict.items():
    #             # 设置url
    #             glo.set_value(item[0], item[1])
    #             # 设置hosts
    #             glo.set_value("host" + item[0][-1], urlparse(item[1]).hostname)
    #
    #     glo.set_value("webdriver_arg", config.option.webdriver)
    #     glo.set_value("device_name", config.option.devicename)
    #     glo.set_value("platform_name", config.option.platformname)
    #     glo.set_value("platform_version", config.option.platformversion)
    #     glo.set_value("app_url", config.option.appurl)

    config_name = config.option.config
    # get configuration from yaml file
    # abspath = os.path.split(os.path.realpath(__file__))[0]
    # cfgfile = abspath + '/../config/' + f"{config_name}.yaml"
    # cfgfile = os.path.join('../config', f"{config_name}.yaml")
    yaml_path = os.path.join(_CONFIG_DIR, f"{config_name}.yaml")

    with open(f"{yaml_path}", "r") as file:
        yaml_data = yaml.safe_load(file)

    global_config.config.update(yaml_data)
    global_config.config['config_name'] = config_name

    # get environement variable from .env file



    #_get_config()
    # from base.get_config_class import GetConfig
    # config_name = glo.get_value("config_name")
    #from base.get_config import get_log_level
    logger = logging.getLogger(__name__)
    # logger.setLevel(level=logging.INFO)

    #root_path = os.path.split(os.path.realpath(__file__))[0]
    root_path = os.path.abspath(os.path.join(_HOOKS_DIR, "..",".."))
    report_root_path = root_path + os.sep + 'testreport'
    dir_path = Path(report_root_path)
    # create testreport foler if doesn't exist
    dir_path.mkdir(exist_ok=True, parents=True)
    handler = TimedRotatingFileHandler(report_root_path + os.sep + 'run.log', when='d', interval=1, backupCount=30,
                                       encoding='utf-8')
    # handler.setLevel(eval("logging." + GetConfig.get_log_level()))
    # Todo: comment the log level and format settings to see whether those in pytest.ini takes effect
    # handler.setLevel(eval("logging." + get_log_level()))
    #
    # formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)

    # set log level of specific libs, otherwise there's too many debug outputs
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("chardet.charsetprober").setLevel(logging.WARNING)
    logging.getLogger("faker.factory").setLevel(logging.WARNING)

    now = datetime.now()
    # create report target dir
    # reports_dir = Path('reports', now.strftime('%Y%m%d'))
    # from base.get_config import get_test_type
    # test_type = get_test_type()
    reports_dir = Path("%s/testreport" % root_path)
    raw_dir = Path("%s/xml" % reports_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    html_dir = Path("%s/html" % reports_dir)
    html_dir.mkdir(parents=True, exist_ok=True)
    # set custom options only if none are provided from command line
    if not hasattr(config.option, "htmlpath") or config.option.htmlpath is None:  # no --html argument specified
        # reports_dir.mkdir(parents=True, exist_ok=True)
        # # custom report file
        # environment_str = glo.get_value("device_name", "") + "_" + glo.get_value("platform_name",
        #                                                                          "") + "_" + glo.get_value(
        #     "platform_version", "")
        environment_str = (global_config.config.get('device_name','') + "_" + global_config.config.get('platform_name','')
                           + "_"+ global_config.config.get('platform_version',''))
        if environment_str != "__":  # run case by different device environment(mobile cases)
            report_file_path = reports_dir / f"pytest_{environment_str}_{config_name}_{now.strftime('%Y%m%d %H%M%S')}.html"
        else:
            report_file_path = reports_dir / f"pytest_{config_name}_{now.strftime('%Y%m%d %H%M%S')}.html"
        # adjust plugin options
        config.option.htmlpath = report_file_path
        config.option.self_contained_html = True

    if not hasattr(config.option, "allure_report_dir") or config.option.allure_report_dir is None:
        config.option.allure_report_dir = raw_dir

    config.option.clean_alluredir = True

    #glo.set_value("report_file_path", config.option.htmlpath)
    global_config.config['report_file_path'] = config.option.htmlpath


def pytest_unconfigure(config):

    report_file_path = global_config.config['report_file_path']
    report_root_dir = os.path.dirname(report_file_path)

    xml_report_path = f'{report_root_dir}/xml/'
    html_report_path = f'{report_root_dir}/html/'
    delfile(report_root_dir, 30)

    cmd = "allure generate %s -o %s --clean" % (xml_report_path, html_report_path)

    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # cmd="allure serve testreport/xml"
    # subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # report_file_path = glo.get_value("report_file_path")
    # config_name = glo.get_value("config_name")
    # from base.get_config import get_test_type
    # # test_type = GetConfig.get_test_type()
    # test_type = get_test_type()

    config_name = global_config.config["config_name"]
    test_type = global_config.config['test_type']

    if config.option.email:
        from base.email_pytest_report import Email_Pytest_Report
        email_obj = Email_Pytest_Report()
        # 1. Send html formatted email body message with pytest report as an attachment
        # Here log/pytest_report.html is a default file. To generate pytest_report.html file use following command to the test e.g. py.test --html = log/pytest_report.html
        # report_file_path=os.path.abspath(os.path.join(os.path.dirname(__file__),report_file_path))
        email_obj.send_test_report_email(html_body_flag=True, attachment_flag=True,
                                         report_file_path=str(report_file_path),
                                         subject_prefix="%s test %s" % (test_type, config_name))
