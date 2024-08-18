#!/usr/bin/env python
# encoding:utf-8
"""# -*- coding: utf-8 -*-

Created on Tue Aug 21 20:55:06 2018

@author: olivia
description: 测试框架入口
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
glo.init()  # 先必须在主模块初始化（只在Main模块需要一次即可）
# 获取项目名并设置全局变量,必须在import InterfaceTest之前导入，因InterfaceTest导入的get_config需要在import阶段就获取配置文件
if len(sys.argv)==1: #没有指定配置名
    sys.argv.append("Demo")
glo.set_value("config_name", sys.argv[1])

def main():

    from base.get_config import get_log_level, get_run_case_folder, get_run_case_type
    from base import HTMLTestRunner

    # logging.basicConfig(stream=HTMLTestRunner.stdout_redirector, level=eval("logging." + get_log_level())
    #                     # logging.basicConfig(stream=sys.stdout, level=eval("logging." + get_log_level())
    #                     # , format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #                     # datefmt='%a, %d %b %Y %H:%M:%S'
    #                     )
    logging.basicConfig(stream=sys.stdout, level=eval("logging." + get_log_level())
                        ,format='%(levelname)s: %(asctime)s - %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # 输出到结果报告文件的同时，在控制台打印日志
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger('').addHandler(ch)

    from base.get_config import get_neo4j_uri, get_and_set_global_vars, get_url_dict, get_tc_rootdir
    from util import db_util
    from base.get_config import get_test_type
    # test_type = get_test_type().lower()

    # 使用argparse模块处理命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("config_name")
    parser.add_argument("-a", "--algorithm", help="specify target algorithm name")
    parser.add_argument("--host", help="specify target algorithm host")
    parser.add_argument("-p", "--port", help="specify target algorithm port")
    parser.add_argument("-r", "--report", help="specify report name")
    parser.add_argument("-e", "--email", help="specify condition to send email:fail/any")
    parser.add_argument("--webdriver", help="specify webdriver for gui automation")
    parser.add_argument("--enable_proxy", help="whether to enable browsermob-proxy")
    parser.add_argument("--tests_per_worker", help="pytest-parallel argument: specify number of tests per worker")
    parser.add_argument("--reruns", help="specify maximum rerun times")
    #Todo: parser仅解析自定义参数，非自定义参数直接传递给pytestmain
    # parser.add_argument("-e", action='store_true', default=False, dest='send_email', help="switch whether to send email")
    args = parser.parse_args()

    # 从配置文件中获取全局变量值并设置
    get_and_set_global_vars()

    test_type = get_test_type()
    if test_type == 'interface' or test_type == 'gui':
        # 获取配置文件中的url列表并依次设置对应的全局变量
        url_dict = get_url_dict()
        if url_dict != {}:
            for item in url_dict.items():
                glo.set_value(item[0], item[1])
                glo.set_value("host" + item[0][-1], urlparse(item[1]).hostname)
    elif test_type == 'algorithm':
        # 读入算法地址文件
        paths = pd.read_excel(sys.path[0] + os.sep + '..' + os.sep + glo.get_value("algo_path_file"))

        # 命令行参数指定算法的host,port overwrite文件中的配置
        if args.host:
            if not args.algorithm:
                sys.exit("请指定需要测试的算法(文件夹名，非实际接口名)：-a/--algorithm algorithm_folder")
            else:
                # paths.loc[paths.Algo_Name==args.algorithm,'Host']=args.host
                paths.loc[paths.Test_Folder == args.algorithm, 'Host'] = args.host
        if args.port:
            if not args.algorithm:
                sys.exit("请指定需要测试的算法(文件夹名，非实际接口名)：-a/--algorithm algorithm_folder")
            else:
                paths.loc[paths.Test_Folder == args.algorithm, 'Port'] = args.port

        paths_map = {}
        # glo.set_value("algo_paths",paths)
        # {"match_company":{"Host":"xxx.xxx.xxx.xxx","Port":"xxxxx"},...}
        for i in range(len(paths)):
            paths_map[paths.iloc[i]['Test_Folder']] = {"Algo_Name": paths.iloc[i]['Algo_Name'],
                                                       "Host": paths.iloc[i]['Host'],
                                                       "Port": paths.iloc[i]['Port'],
                                                       "Data_File": paths.iloc[i]['Data_File'],
                                                       "Schema_File": paths.iloc[i]['Schema_File']}
        glo.set_value("algo_paths_map", paths_map)

    general_case_class_mapping = {"db": "case.db.general_db_test.DBTest",
                                  "interface": "case.interface.general.general_interface_test.InterfaceTest"}

    if test_type in ['db', 'interface']:
        classname = general_case_class_mapping[test_type].split('.')[-1]
        classpath = general_case_class_mapping[test_type].replace("." + classname, "")

    run_case_types = get_run_case_type()

    if run_case_types == ["Excel"]:  # 仅运行Excel驱动的general case
        exec("from %s import %s" % (classpath, classname))
        run_testsuite = unittest.TestLoader().loadTestsFromTestCase(eval(classname))
        tc_folders = os.path.abspath('../case/interface')
    else:
        if run_case_types == ["Code"]:  # 仅运行独立的Python代码test case
            run_testsuite = unittest.TestSuite()
        else:  # 两种都运行
            exec("from %s import %s" % (classpath, classname))
            run_testsuite = unittest.TestLoader().loadTestsFromTestCase(eval(classname))

        run_case_folders = get_run_case_folder()

        if len(run_case_folders) == 0:  # 未指定运行case的level,则运行根目录下case（包括所有子目录）
            run_case_folders = ['.']

        # 算法测试可在命令行制定需要测试的算法
        # if test_type=='algorithm' and len(sys.argv)>2:
        #     run_case_levels = [sys.argv[2]]
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

    if not os.path.exists('../testreport'):
        os.makedirs('../testreport')
    if args.report:
        report_file_path = r'../testreport/%s.html' % args.report
    else:
        report_file_path = r'../testreport/pytest_report-%s-%s.html' % (args.config_name, now)
    #pytest.main(['-s','-v',tc_folders_str,'--clean-alluredir Report/raw'])
    #pytest.main(['-s', '-v', tc_folders_str, "--tests-per-worker","4","--alluredir","../testreport/xml","--html=%s"%report_file_path,"--self-contained-html"])

    cmd_list = []
    if args.tests_per_worker:
        cmd_list=['-s', '-v', *tc_folders,"--tests-per-worker", args.tests_per_worker , "--html=%s" % report_file_path, "--self-contained-html"]

    else:
        cmd_list=['-s', '-v', *tc_folders,"--html=%s" % report_file_path, "--self-contained-html"]

    if args.reruns:
        #n_rerun = int(args.reruns)
        cmd_list.extend(["--reruns",args.reruns])

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



# # 清理过期报告
# delfile('../testreport', 30)

if __name__=='__main__':
    main()


