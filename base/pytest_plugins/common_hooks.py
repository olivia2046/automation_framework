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
from base.allure_report_handler import allure_pre_process, make_allure_report

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
        help="locate the config file for testing"
    )

    parser.addoption(
        "--reportdir",
        action="store",
        default="testreport",
        help="locate the test report folder"
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

    # parser.addoption(
    #     "--email",
    #     action="store_true",
    #     default=False,
    #     help="whether to send email for pytest report(not allure report generated from jenkins)"
    # )


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

    for item in items:  # resolve encoding issue for Chinese in test case name
        # item.name = item.name.encode("utf-8").decode("unicode_escape")
        # item.nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        # if item.cls.__bases__[0] is not unittest.case.TestCase: # unittest test case, item.nodeid cannot encode
        if item.parent.__class__.__name__ != 'UnitTestCase':  # unittest test case, item.nodeid cannot encode
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
                limit:]  # for cases where multiple test cases have save substring, to prevent test case skipped by mistake
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
        # report.description = str(item.function.__doc__.split('\n')[0]) #docstring only pck the first line
        setattr(report, 'description', str(item.function.__doc__.split('\n')[0]))  # take the first line of docstring
    else:
        # report.description = ""
        setattr(report, 'description', 'No description provided')

        # report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")


"""
First, execute hooks marked with tryfirst=True
Second, execute hooks marked with trylast=True
Then execute hooks marked with hookwrapper=True
"""


@pytest.hookimpl(tryfirst=True)  # trylast=True  hookwrapper=True
def pytest_configure(config):
    """ hook function, called when all test items are collected
    execute initial configurations: get url and report path

    """

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

    logger = logging.getLogger(__name__)
    # logger.setLevel(level=logging.INFO)

    #root_path = os.path.split(os.path.realpath(__file__))[0]
    root_path = os.path.abspath(os.path.join(_HOOKS_DIR, "..",".."))
    report_root_path = root_path + os.sep + config.option.reportdir
    reports_dir = Path(report_root_path)
    # create testreport foler if doesn't exist
    reports_dir.mkdir(exist_ok=True, parents=True)
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
    #reports_dir = Path("%s/testreport" % root_path)
    # raw_dir = Path("%s/xml" % reports_dir)
    # raw_dir.mkdir(parents=True, exist_ok=True)
    # html_dir = Path("%s/html" % reports_dir)
    # html_dir.mkdir(parents=True, exist_ok=True)
    # set custom options only if none are provided from command line
    if not hasattr(config.option, "htmlpath") or config.option.htmlpath is None:  # no --html argument specified
        # reports_dir.mkdir(parents=True, exist_ok=True)
        # custom report file
        environment_str = (global_config.config.get('device_name','') + "_" + global_config.config.get('platform_name','')
                           + "_"+ global_config.config.get('platform_version',''))
        if environment_str != "__":  # run case by different device environment(mobile cases)
            report_file_path = reports_dir / f"pytest_{environment_str}_{config_name}_{now.strftime('%Y%m%d %H%M%S')}.html"
        else:
            report_file_path = reports_dir / f"pytest_{config_name}_{now.strftime('%Y%m%d %H%M%S')}.html"
        # adjust plugin options
        config.option.htmlpath = report_file_path
        config.option.self_contained_html = True

    # if not hasattr(config.option, "allure_report_dir") or config.option.allure_report_dir is None:
    #     config.option.allure_report_dir = raw_dir

    # config.option.clean_alluredir = True

    global_config.config['report_file_path'] = config.option.htmlpath
    allure_pre_process(reports_dir)


def pytest_unconfigure(config):


    # html_report_file_path = global_config.config['report_file_path']
    # report_root_dir = os.path.dirname(html_report_file_path)
    root_path = os.path.abspath(os.path.join(_HOOKS_DIR, "..",".."))
    report_root_path = root_path + os.sep + config.option.reportdir

    # allure_resultdir_path = f'{report_root_dir}/allure-result/'
    # allure_reportdir_path = f'{report_root_dir}/allure-report/'
    delfile(report_root_path, 30)

    # cmd = "allure generate %s -o %s --clean" % (allure_resultdir_path, allure_reportdir_path)
    #
    # subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    make_allure_report(report_root_path)

    # cmd="allure serve testreport/xml"
    # subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # report_file_path = glo.get_value("report_file_path")
    # config_name = glo.get_value("config_name")
    # from base.get_config import get_test_type
    # # test_type = GetConfig.get_test_type()
    # test_type = get_test_type()

    # config_name = global_config.config["config_name"]
    # test_type = global_config.config['test_type']

    # if config.option.email:
    #     from base.email_pytest_report import Email_Pytest_Report
    #     email_obj = Email_Pytest_Report()
    #     # 1. Send html formatted email body message with pytest report as an attachment
    #     # Here log/pytest_report.html is a default file. To generate pytest_report.html file use following command to the test e.g. py.test --html = log/pytest_report.html
    #     # report_file_path=os.path.abspath(os.path.join(os.path.dirname(__file__),report_file_path))
    #     email_obj.send_test_report_email(html_body_flag=True, attachment_flag=True,
    #                                      report_file_path=str(html_report_file_path),
    #                                      subject_prefix="%s test %s" % (test_type, config_name))
