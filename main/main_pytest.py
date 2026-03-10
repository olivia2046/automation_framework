#!/usr/bin/env python
# encoding:utf-8
"""# -*- coding: utf-8 -*-

Created on Tue Aug 21 20:55:06 2018

@author: olivia
description: entrance to run test cases
"""
#import platform
#print(platform.python_version())
import unittest,pytest,time
import os,sys, logging,argparse
import pandas as pd
from urllib.parse import urlparse
sys.path.append('..')
sys.path.append('../base') # pypom
import base.globalvars as glo
glo.init()  # need to initialize in main module(and only once)
# retrieve project config name and set global variables. Must be imported before imported APITest(get_config imported in APITest need to get config file)
if len(sys.argv)==1: # no config name specified
    sys.argv.append("automation_exercise_api")
glo.set_value("config_name", sys.argv[1])

def main():

    from base.get_config import get_log_level, get_run_case_folder, get_run_case_type
    # from base import HTMLTestRunner

    # logging.basicConfig(stream=HTMLTestRunner.stdout_redirector, level=eval("logging." + get_log_level())
    #                     # logging.basicConfig(stream=sys.stdout, level=eval("logging." + get_log_level())
    #                     # , format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #                     # datefmt='%a, %d %b %Y %H:%M:%S'
    #                     )
    logging.basicConfig(stream=sys.stdout, level=eval("logging." + get_log_level())
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

    from base.get_config import get_and_set_global_vars, get_url_dict, get_tc_rootdir
    #from util import db_util
    from base.get_config import get_test_type
    # test_type = get_test_type().lower()

    # use argparse to handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config_name")
    #parser.add_argument("-a", "--algorithm", help="specify target algorithm name")
    #parser.add_argument("--host", help="specify target algorithm host")
    #parser.add_argument("-p", "--port", help="specify target algorithm port")
    parser.add_argument("-r", "--report", help="specify report name")
    parser.add_argument("-e", "--email", help="specify condition to send email:fail/any")
    parser.add_argument("--webdriver", help="specify webdriver for gui automation")
    # parser.add_argument("--enable_proxy", help="whether to enable browsermob-proxy")
    parser.add_argument("--tests_per_worker", help="pytest-parallel argument: specify number of tests per worker")
    parser.add_argument("--reruns", help="specify maximum rerun times")
    # parser.add_argument("-e", action='store_true', default=False, dest='send_email', help="switch whether to send email")
    #args = parser.parse_args()
    args,unknown = parser.parse_known_args()

    # get global variables from config file and set
    get_and_set_global_vars()

    test_type = get_test_type()
    if test_type == 'api' or test_type == 'gui':
        # get url list from config file and set corresponding global variables
        url_dict = get_url_dict()
        if url_dict != {}:
            for item in url_dict.items():
                glo.set_value(item[0], item[1])
                glo.set_value("host" + item[0][-1], urlparse(item[1]).hostname)


    general_case_class_mapping = {"db": "projects.general.general_db_test.DBTest",
                                  "api": "projects.general.general_api_test.APITest"}

    if test_type in ['db', 'api']:
        classname = general_case_class_mapping[test_type].split('.')[-1]
        classpath = general_case_class_mapping[test_type].replace("." + classname, "")
    else:
        classname = None
        classpath = None

    run_case_types = get_run_case_type()

    if run_case_types == ["Excel"]:  # only when Excel driver general api test
        exec("from %s import %s" % (classpath, classname))
        #run_testsuite = unittest.TestLoader().loadTestsFromTestCase(eval(classname))
        tc_folders = os.path.abspath('../projects/general')
    else:
        # if run_case_types == ["Code"]:  # 仅运行独立的Python代码test case
        #     run_testsuite = unittest.TestSuite()
        # else:  # 两种都运行
        #     exec("from %s import %s" % (classpath, classname))
        #     run_testsuite = unittest.TestLoader().loadTestsFromTestCase(eval(classname))

        run_case_folders = get_run_case_folder()

        if len(run_case_folders) == 0:  # 未指定运行case的level,则运行根目录下case（包括所有子目录）
            run_case_folders = ['.']


        if test_type == 'algorithm' and args.algorithm:
            run_case_folders = [args.algorithm]

        # gui automation
        if test_type == 'gui' and args.webdriver:
            glo.set_value("webdriver_arg",args.webdriver)

        if args.enable_proxy:
            glo.set_value("enable_proxy",True)

        tc_rootdir = get_tc_rootdir()
        #tc_folders_str = '"' + '","'.join([os.path.abspath(tc_rootdir + '/' + folder) for folder in run_case_folders]) + '"'
        #tc_folders_str = ','.join([os.path.abspath(tc_rootdir + '/' + folder) for folder in run_case_folders])
        tc_folders = tuple([os.path.abspath(tc_rootdir + '/' + folder) for folder in run_case_folders])

    now = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())  # 时分秒中间不能用:连接，无效的文件名

    current_work_dir = os.getcwd()
    if not os.path.exists('../testreport'):
        os.makedirs('../testreport')
    if args.report:
        report_file_path = r'../testreport/%s.html' % args.report
    else:
        report_file_path = r'../testreport/pytest_report-%s-%s.html' % (args.config_name, now)

    #pytest.main(['-s','-v',tc_folders_str,'--clean-alluredir Report/raw'])
    #pytest.main(['-s', '-v', tc_folders_str, "--tests-per-worker","4","--alluredir","../testreport/xml","--html=%s"%report_file_path,"--self-contained-html"])

    cmd_list = []
    # if args.tests_per_worker:
    #     cmd_list=['-s', '-v', tc_folders,"--tests-per-worker", args.tests_per_worker , "--html=%s" % report_file_path, "--self-contained-html"]
    #
    # else:
    #     cmd_list=['-s', '-v', tc_folders,"--html=%s" % report_file_path, "--self-contained-html"]
    #
    # if args.reruns:
    #     #n_rerun = int(args.reruns)
    #     cmd_list.extend(["--reruns",args.reruns])


    cmd_list.extend(unknown)
    cmd_list.append(f"--html={report_file_path}")

    cmd_list.append(tc_folders)

    missing = list(set(['-s','-v','--self-contained-html'])-set(cmd_list))
    if missing:
        cmd_list.extend(missing) # add these arguments if not provided

    cmd_list.extend(["-c", "pytest.ini"])  # to skip outer layer conftest.py

    pytest.main(cmd_list)
    # time.sleep(5)
    # os.system('allure generate ../testreport/xml -o ../testreport/html --clean')
    logging.shutdown()

    if args.email:
        from base.email_pytest_report import Email_Pytest_Report
        email_obj = Email_Pytest_Report()
        # 1. Send html formatted email body message with pytest report as an attachment
        # Here log/pytest_report.html is a default file. To generate pytest_report.html file use following command to the test e.g. py.test --html = log/pytest_report.html
        #report_file_path=os.path.abspath(os.path.join(os.path.dirname(__file__),report_file_path))
        email_obj.send_test_report_email(html_body_flag=True, attachment_flag=True, report_file_path=report_file_path, subject_prefix = "%s test %s"%(test_type, args.config_name))



# # clean the outdated reports
# delfile('../testreport', 30)

if __name__=='__main__':
    main()


