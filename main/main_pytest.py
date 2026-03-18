#!/usr/bin/env python
# encoding:utf-8
"""# -*- coding: utf-8 -*-

Created on Tue Aug 21 20:55:06 2018

@author: olivia
description: entrance to run test cases
"""

import pytest,time,yaml, os,sys, logging,argparse
#from urllib.parse import urlparse
_MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
_FRAMEWORK_ROOT = os.path.abspath(os.path.join(_MAIN_DIR, ".."))
if _FRAMEWORK_ROOT not in sys.path:
    sys.path.insert(0, _FRAMEWORK_ROOT)

import base.config as global_config
from base.allure_report_handler import allure_pre_process, make_allure_report
from shared_utils.clean_expired_files import remove_old_files

#import base.globalvars as glo


sys.path.append('..')
sys.path.append('../base')
import base.globalvars as glo
glo.init()  # need to initialize in main module(and only once)
# retrieve project config name and set global variables. Must be imported before imported APITest(get_config imported in APITest need to get config file)
# if len(sys.argv)==1: # no config name specified
#     sys.argv.append("automation_exercise_api")
# glo.set_value("config_name", sys.argv[1])

def main():
    glo.init()
    _CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    _CONFIG_DIR = os.path.abspath(os.path.join(_CURRENT_DIR, "..", "config"))
    # use argparse to handle command line arguments, executed before pytest.ini
    parser = argparse.ArgumentParser()
    #parser.add_argument("config_name")
    parser.add_argument("--config",help="locate the config file for testing")
    parser.add_argument("--reportdir",help="locate the report file for testing",default='../testreport')
    #parser.add_argument("-e", "--email", help="specify condition to send email:fail/any")
    # parser.add_argument("--enable_proxy", help="whether to enable browsermob-proxy")
    #parser.add_argument("--reruns", help="specify maximum rerun times")
    # parser.add_argument("-e", action='store_true', default=False, dest='send_email', help="switch whether to send email")
    #args = parser.parse_args()
    args,unknown = parser.parse_known_args()
    config_name = args.config
    # get configuration from yaml file
    # abspath = os.path.split(os.path.realpath(__file__))[0]
    # cfgfile = abspath + '/../config/' + f"{config_name}.yaml"
    # cfgfile = os.path.join('../config', f"{config_name}.yaml")
    yaml_path = os.path.join(_CONFIG_DIR, f"{config_name}.yaml")

    with open(f"{yaml_path}", "r") as file:
        yaml_data = yaml.safe_load(file)

    global_config.config.update(yaml_data)
    global_config.config['config_name'] = config_name
    #from base.get_config import get_log_level, get_run_case_folder, get_run_case_type
    # from base import HTMLTestRunner

    # logging.basicConfig(stream=HTMLTestRunner.stdout_redirector, level=eval("logging." + get_log_level())
    #                     # logging.basicConfig(stream=sys.stdout, level=eval("logging." + get_log_level())
    #                     # , format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #                     # datefmt='%a, %d %b %Y %H:%M:%S'
    #                     )
    log_level = global_config.config.get("log_level", "INFO")
    logging.basicConfig(stream=sys.stdout, level=eval("logging." + log_level)
                        ,format='%(levelname)s: %(asctime)s - %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("chardet.charsetprober").setLevel(logging.WARNING)
    logging.getLogger("faker.factory").setLevel(logging.WARNING)
    #logging.info("---------------conftest.py---------------------------------")

    # # logging.info printed as red, so remove this part
    # # print log on console as well when outputting to test report
    # ch = logging.StreamHandler()
    # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # ch.setFormatter(formatter)
    # logging.getLogger('').addHandler(ch)
    # logging.info("---------------conftest.py---------------------------------")

    #from util import db_util

    # get global variables from config file and set
    # get_and_set_global_vars()

    test_type = global_config.config.get("test_type", "api").lower()
    general_case_class_mapping = {"api": "projects.general.general_api_test.APITest"}

    if test_type in ['api']: # can be extended for other specific tests
        classname = general_case_class_mapping[test_type].split('.')[-1]
        classpath = general_case_class_mapping[test_type].replace("." + classname, "")
    else:
        classname = None
        classpath = None

    run_case_types = global_config.config.get("run_case_types", ["Excel,Code"])


    if run_case_types == ["Excel"]:  # only when Excel driver general api test
        exec("from %s import %s" % (classpath, classname))
        #run_testsuite = unittest.TestLoader().loadTestsFromTestCase(eval(classname))
        tc_folders = os.path.abspath('../projects/general')
    else:
        # if run_case_types == ["Code"]:  # only execute python code test case
        #     run_testsuite = unittest.TestSuite()
        # else:  # excute both python code test case and excel test case
        #     exec("from %s import %s" % (classpath, classname))
        #     run_testsuite = unittest.TestLoader().loadTestsFromTestCase(eval(classname))

        #run_case_folders = get_run_case_folder()
        run_case_folders = global_config.config.get("run_case_folders",[])

        if len(run_case_folders) == 0:  # if no folders specified, then run all cases under current folder
            run_case_folders = ['.']

        project_rootdir_str = global_config.config.get("file_path", {}).get("project_rootdir")
        tc_rootdir_str = global_config.config.get("file_path",{}).get("tc_rootdir","api/tests")
        tc_rootdir = project_rootdir_str + os.sep + tc_rootdir_str
        #tc_folders_str = '"' + '","'.join([os.path.abspath(tc_rootdir + '/' + folder) for folder in run_case_folders]) + '"'
        #tc_folders_str = ','.join([os.path.abspath(tc_rootdir + '/' + folder) for folder in run_case_folders])
        tc_folders = tuple([os.path.abspath(tc_rootdir + '/' + folder) for folder in run_case_folders])

    now = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())  # cannot include ':', invalid file name

    current_work_dir = os.getcwd()
    reportdir = args.reportdir
    if not os.path.exists(reportdir):
        os.makedirs(reportdir)
    # # clean the outdated reports
    remove_old_files(reportdir, 30)


    report_file_path = f'{reportdir}/pytest_report-{args.config}-{now}.html'

    #pytest.main(['-s','-v',tc_folders_str,'--clean-alluredir Report/raw'])
    #pytest.main(['-s', '-v', tc_folders_str, "--tests-per-worker","4","--alluredir","../testreport/xml","--html=%s"%report_file_path,"--self-contained-html"])

    cmd_list = []


    cmd_list.extend(unknown)
    cmd_list.append(f"--html={report_file_path}")


    cmd_list.append(tc_folders)

    missing = list(set(['-s','-v','--self-contained-html'])-set(cmd_list))
    if missing:
        cmd_list.extend(missing) # add these arguments if not provided

    cmd_list.extend(["-c", "pytest.ini"])  # to skip outer layer conftest.py
    #cmd_list.extend(["-p", "base.pytest_plugins.common_hooks"]),  # explicitly register hooks

    allure_pre_process(reportdir)
    pytest.main(cmd_list)
    make_allure_report(reportdir)
    # time.sleep(5)
    # os.system('allure generate ../testreport/xml -o ../testreport/html --clean')
    logging.shutdown()

    # if args.email:
    #     from base.email_pytest_report import Email_Pytest_Report
    #     email_obj = Email_Pytest_Report()
    #     # 1. Send html formatted email body message with pytest report as an attachment
    #     # Here log/pytest_report.html is a default file. To generate pytest_report.html file use following command to the test e.g. py.test --html = log/pytest_report.html
    #     #report_file_path=os.path.abspath(os.path.join(os.path.dirname(__file__),report_file_path))
    #     email_obj.send_test_report_email(html_body_flag=True, attachment_flag=True, report_file_path=report_file_path, subject_prefix = "%s test %s"%(test_type, args.config_name))


if __name__=='__main__':
    main()


