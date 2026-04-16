# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 3/12/2026 17:27
desc: common hooks
used to be defined in top-level conftest.py, but since projects may need to have their own pytest.ini/pyproject.toml
which leads to top-level conftest.py not loaded, put these hook definitions here, and register in project conftest.py as:
pytest_plugins = ["base.pytest_plugins.common_hooks"]
'''

import os, logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path
import pytest
from urllib.parse import urlparse
import yaml
from playwright.sync_api import Page

import base.globalvars as glo
import base.config as global_config
from base.allure_report_handler import allure_pre_process, make_allure_report


# add automation_framework/ to sys.path, so base/ and projects/ both can be imported as top level package
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# _FRAMEWORK_ROOT = os.path.dirname(os.path.abspath(__file__))
# print(f"[conftest] inserting into sys.path: {_FRAMEWORK_ROOT}")
# sys.path.insert(0, _FRAMEWORK_ROOT)

from shared_utils.clean_expired_files import remove_old_files
from shared_utils.helpers import take_screenshot

#from base.pwpo.base_page import BasePage

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
        #default="automation_exercise_web",
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
    """Based on the `limit` value passed via command-line arguments, when executing a parameterized set of test cases,
    only the first `limit` cases are executed. (This is applicable in scenarios where, for instance,
    a subset of the cases consists of high-priority or Smoke Test cases, and executing the entire set would be too time-consuming.)


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


@pytest.fixture(autouse=True)
def auto_trace(context):
    """
    Start Playwright tracing before each test and stop it after.

    Strategy: retain-on-failure
      - Tracing is started for every Playwright test (detected via 'context' fixture).
      - On failure: pytest_runtest_makereport stops tracing and saves the trace file.
      - On success: tracing is stopped here without saving, discarding the data.

    Defined in common_hooks.py so all projects inherit it automatically
    via pytest_plugins = ["base.pytest_plugins.common_hooks"].

    to view trace: playwright show-trace xxx.zip, or python -m playwright show-trace xxx.zip
    """
    trace_on_failure = os.getenv("TRACE_ON_FAILURE", "true").lower() == "true"
    if trace_on_failure:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    # On success: stop tracing without saving (discard trace data).
    # On failure: already stopped by pytest_runtest_makereport — ignore the error.
    if trace_on_failure:
        try:
            context.tracing.stop()
        except Exception:
            pass


#@pytest.mark.optionalhook
pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")
    cells.insert(2, "<th>Test_nodeid</th>")
    # cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop(2)


#@pytest.mark.optionalhook
pytest.hookimpl(optionalhook=True)
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
def pytest_runtest_makereport(item,call):
    """
    Hook that runs after each test phase (setup / call / teardown).

    On test failure:
      1. Takes a screenshot (Playwright tests only, detected via 'page' fixture).
      2. Attaches the screenshot to the Allure report via allure.attach().
      3. Embeds the screenshot as a Base64 inline image in the pytest-html report.
      4. Sets the test description from the first line of the docstring.

    Screenshot is only taken when SCREENSHOT_ON_FAILURE env var is 'true' (default).
    """
    # Must yield first so that report object is available before we attach extras.
    # Screenshot is captured before yield so page is still in the failure state.
    screenshot_bytes = None

    if call.when == "call" and call.excinfo is not None:
        scr_on_failure = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
        if scr_on_failure:
            page: Page = item.funcargs.get("page")
            if page:  # 'page' fixture is pytest-playwright specific — indicates a Playwright test
                test_name = item.nodeid.replace("/", "_").replace("::", "_")

                # Save screenshot to disk for reference
                path = take_screenshot(page, f"FAILED_{test_name}")
                logging.info(f"Failure screenshot saved: {path}")

                # Capture raw bytes for embedding in reports
                try:
                    screenshot_bytes = page.screenshot(full_page=True)
                except Exception as e:
                    logging.warning(f"Failed to capture screenshot bytes: {e}")

            # todo: add Selenium / Appium screenshot support here

    # --- Allure: attach screenshot before yield so it is associated with the correct test ---
    if screenshot_bytes:
        try:
            import allure
            allure.attach(
                screenshot_bytes,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except ImportError:
            logging.debug("allure-pytest not installed — skipping Allure screenshot attachment")
        except Exception as e:
            logging.warning(f"Failed to attach screenshot to Allure report: {e}")

    # Yield to let pytest collect the test result
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        # --- Save and attach Playwright trace on failure ---
        # trace_on_failure = os.getenv("TRACE_ON_FAILURE", "true").lower() == "true"
        # if trace_on_failure:
        #     context = item.funcargs.get("context")
        #     if context:  # 'context' fixture is pytest-playwright specific
        #         test_name = item.nodeid.replace("/", "_").replace("::", "_")
        #         trace_dir = global_config.config.get("trace_dir", "traces")
        #         trace_path = os.path.join(
        #             trace_dir,
        #             f"FAILED_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        #         )
        #         try:
        #             # Stop tracing and save the trace file
        #             context.tracing.stop(path=trace_path)
        #             logging.info(f"Trace saved: {trace_path}")
        #
        #             # Attach trace file to Allure report
        #             try:
        #                 import allure
        #                 with open(trace_path, "rb") as f:
        #                     allure.attach(
        #                         f.read(),
        #                         name="Playwright Trace",
        #                         attachment_type=allure.attachment_type.ZIP,
        #                     )
        #             except ImportError:
        #                 logging.debug("allure-pytest not installed — skipping Allure trace attachment")
        #             except Exception as e:
        #                 logging.warning(f"Failed to attach trace to Allure report: {e}")
        #
        #             # Add trace link to pytest-html report
        #             try:
        #                 pytest_html = item.config.pluginmanager.getplugin("html")
        #                 if pytest_html:
        #                     trace_link = (
        #                         f'<div>Playwright Trace: '
        #                         f'<a href="{trace_path}" target="_blank">{os.path.basename(trace_path)}</a>'
        #                         f' — open with <code>playwright show-trace {os.path.basename(trace_path)}</code>'
        #                         f'</div>'
        #                     )
        #                     extra.append(pytest_html.extras.html(trace_link))
        #             except Exception as e:
        #                 logging.warning(f"Failed to add trace link to pytest-html report: {e}")
        #
        #         except Exception as e:
        #             logging.warning(f"Failed to save Playwright trace: {e}")

        # --- pytest-html: embed screenshot as
        # Base64 inline image ---
        if screenshot_bytes:
            try:
                import base64
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    img_b64 = base64.b64encode(screenshot_bytes).decode()
                    html_img = (
                        '<div>'
                        '<img src="data:image/png;base64,{}" '
                        'alt="Failure Screenshot" '
                        'style="width:800px; height:auto; cursor:pointer;" '
                        'onclick="window.open(this.src)" />'
                        '</div>'
                    ).format(img_b64)
                    extra.append(pytest_html.extras.html(html_img))
            except Exception as e:
                logging.warning(f"Failed to attach screenshot to pytest-html report: {e}")

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
    # root_path = os.path.abspath(os.path.join(_HOOKS_DIR, "..",".."))
    #root_path = str(config.rootdir)
    report_dir = config.option.reportdir
    if os.path.isabs(report_dir):
        report_root_path = report_dir
    else:
        report_root_path = os.path.join(os.getcwd(), report_dir)
    #report_root_path = root_path + os.sep + config.option.reportdir
    report_root_dir = Path(report_root_path)
    # create testreport foler if doesn't exist
    report_root_dir.mkdir(exist_ok=True, parents=True)
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
            report_file_path = report_root_dir / f"pytest_{environment_str}_{config_name}_{now.strftime('%Y%m%d %H%M%S')}.html"
        else:
            report_file_path = report_root_dir / f"pytest_{config_name}_{now.strftime('%Y%m%d %H%M%S')}.html"
        # adjust plugin options
        config.option.htmlpath = report_file_path
        config.option.self_contained_html = True

    # if not hasattr(config.option, "allure_report_dir") or config.option.allure_report_dir is None:
    #     config.option.allure_report_dir = raw_dir

    # config.option.clean_alluredir = True

    global_config.config['report_file_path'] = config.option.htmlpath
    #allure_pre_process(report_root_dir)
    allure_pre_process(report_root_path)
    # Ensure the screenshots output directory exists before tests run.
    screenshot_dir = os.path.join(report_root_path, "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    global_config.config['screenshot_dir'] = screenshot_dir

    # Ensure the traces output directory exists before tests run.
    # Traces are only saved for failed tests (retain-on-failure strategy).
    trace_dir = os.path.join(report_root_path, "traces")
    os.makedirs(trace_dir, exist_ok=True)
    global_config.config['trace_dir'] = trace_dir


def pytest_unconfigure(config):
    """
    """
    html_report_file_path = global_config.config['report_file_path']
    report_root_path = os.path.dirname(html_report_file_path)

    # root_path = os.path.abspath(os.path.join(_HOOKS_DIR, "..",".."))
    # report_root_path = root_path + os.sep + config.option.reportdir

    # allure_resultdir_path = f'{report_root_dir}/allure-result/'
    # allure_reportdir_path = f'{report_root_dir}/allure-report/'
    remove_old_files(report_root_path, 30)

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




