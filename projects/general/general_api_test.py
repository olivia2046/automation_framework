# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 08:00:48 2018
@author: olivia
Description: General Test Class of API
"""


import pandas as pd
import numpy as np
import sys,logging, re, os
import json
import unittest

import pytest
from jsonpath import jsonpath # used in eval. DON'T REMOVE THIS LINE
sys.path.append('../../case/interface')
from base import ddt
from util.jsonmatch import jsonmatch
from base.executestep import ExecuteStep
#from base.get_config import get_testcase_file,get_run_specific_case,get_tc_rootdir
from base.expression_evaluation import eval_from_string
import base.globalvars as glo
from base.ruleparser import RuleParser
from base.decorators import retry
import base.config as global_config


# Read from Excel test case, to drive api test
#sheets_dict = pd.read_excel(get_testcase_file(),dtype='str',sheet_name=None)
sheets_dict = pd.read_excel(global_config.get_testcase_file(),dtype='str',sheet_name=None)

datafrm = pd.concat([sheets_dict[key] for key in sheets_dict],axis=0)
datafrm = datafrm.fillna('') #replace null value with empty string
testdata = []
datafrm.apply(lambda x:testdata.append(x.to_dict()),axis=1) #convert each row to dictionary, and make a list of all rows

#run_specific_case = get_run_specific_case()
run_specific_case = global_config.config.get('run_specific_case',False)
if run_specific_case:
    with open(global_config.get_tc_rootdir() + os.sep + 'run_cases.txt') as f:
        content = f.readlines()
        case_list = [line.strip('\n') for line in content]
else:
    case_list = list(datafrm['Case_Name'])


@ddt.ddt
class APITest(unittest.TestCase):
    #from base.get_config import get_retry_times, get_retry_wait_time
    retry_times = global_config.config.get("retry_times")
    retry_wait_time = global_config.config.get("retry_wait_time")

    @ddt.data(*testdata)
    def setUp(self,casedata):
        # cannot be data-driven so just leave it, and set up actions will be implemented in test case
        # if casedata['Set_Up'] != "":
        #     eval_from_string(casedata['Set_Up'])
        # global test_case_data
        # test_case_data= []
        pass


    @ddt.data(*testdata)
    #@ddt.data(*test_case_data)
    @retry(retry_times, retry_wait_time)
    def test_api(self, casedata):
        ''' general test case for api testing, data driven using excel file

        :param casedata: data that represents a test case from Excel file

        :return:  None
        '''

        #from base.get_config import get_run_case_level
        run_case_level = global_config.config.get("run_case_level")
        # Skip the case if not in specified case level or not marked as Run
        if (casedata['Case_Level'] in run_case_level or run_case_level==[]) and casedata['Case_Name'] in case_list and casedata['Run'].upper()=='Y':
            # Execute content in 'Set_Up' Column
            if 'Set_Up' in casedata.keys() and casedata['Set_Up']!="":
                #eval_from_string(casedata['Set_Up'], return_str=False, json_str = True)
                for content in casedata['Set_Up'].split(';'):
                    if content!='':
                        eval_from_string(content)

            # Execute Test Step
            exec_step = ExecuteStep()
            res = exec_step.execute(casedata)
            
            # debug to output resonse text
            '''
            if not os.path.exists('../testreport'):
                os.makedirs('../testreport')
            now=time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
            with open(r"../testreport/ResponsePage-%s-%s.html"%(casedata['Case_Name'],now),'w',encoding='utf-8-sig') as f: # 中文即使用utf-8也还是乱码
                f.write(res.text)
            '''

            expected_status_code = casedata['Expected_Code']

            #logging.debug(res.status_code)


            #try:
            if expected_status_code!='':#
                self.assertEqual(str(res.status_code),expected_status_code, f"Status Code not as expected! Expected:{expected_status_code}, Actual: {res.status_code}, {res.text}\nurl:{casedata['relative_URL']}\ndata:{casedata['Request_Data']}")
            #except:
            #    raise

            # res.raise_for_status()

            expected_res_txt = casedata['Expected_Text']
            if expected_res_txt!="":
                if casedata['Compare_Method']=="" or casedata['Compare_Method'] is np.nan:
                    self.fail("Need to input Compare_Method！")
                else:
                    #logging.debug("casedata['Compare_Method']：%s"%casedata['Compare_Method'])
                    #logging.debug("Expected text:%s"%expected_res_txt)
                    expected_res_txt = eval_from_string(expected_res_txt)
                    eval("self."+ casedata['Compare_Method'])(str(expected_res_txt),res.text, f"Response text not as expected! Compare_Method： {casedata['Compare_Method']} Expected: {expected_res_txt}, Actual: {res.text}")

            json_validation = casedata['Json_Result_Validation']

            if json_validation!="":
                # Validate the Json content get
                try:
                    if 'Content-Type' in res.headers.keys() and 'application/json' in res.headers['Content-Type']:
                        actual_json_obj = res.json()
                    else:
                        actual_json_obj = {}
                    if re.compile("^\${.+}$").match(json_validation) is not None: # only contains function expression with ${...}
                        #eval_result = eval_from_string(json_validation,return_str=True,json_str=True)
                        #json_validation = eval_from_string(json_validation, return_str=True, json_str=True)
                        json_validation = eval_from_string(json_validation)
                        # since eval_result contains single quote, need to use json.dumps(eval(xxx)) to do replacement
                        eval_result = json.loads(json.dumps(eval(json_validation)))
                        logging.debug("expected Json string: %s"%repr(eval_result))
                        logging.debug("Json string in response:%s"%repr(actual_json_obj))
                        self.assertTrue(jsonmatch(eval_result, actual_json_obj))

                    elif re.compile("^{.+}$").match(json_validation) is not None: # only contains {} json content
                        logging.debug("expected Json string: %s" % repr(json_validation))
                        logging.debug("Json string in response:%s" % repr(actual_json_obj))
                        self.assertTrue(jsonmatch(json.loads(json_validation),actual_json_obj))

                    else: #process as json_path
                        json_validation=json_validation.rstrip(";")
                        for element in json_validation.split(';\n'):
                            if element.strip()=="": # common case is there's an extra ';' the last element in json_validation
                                #logging.warning("json expression is empty")
                                continue

                            #rparser = RuleParser(element.strip(),actual_json_obj)
                            rparser = RuleParser(element.strip(), res)
                            if 'Content-Type' in res.headers.keys()  and 'application/json' in res.headers['Content-Type']:
                                actual_result = res.json()
                            else:
                                actual_result = res.text

                            assert rparser.evaluate() is True, f"Test Fail：url {casedata['relative_URL']}\ndata {casedata['Request_Data']}\nrule {element}\nactual response:\n{actual_result}"


                except Exception as e:
                    #self.assertEqual(1,0,"Exception occured: %s"%e) # fails the test
                    self.fail("Exception occured: %s" % e)  # fails the test


            # if '结果验证方法名' in casedata.keys() and casedata['结果验证方法名']!="":
            #     # 本地变量无法传递到expression_evaluation模块，需要使用全局变量
            #     glo.set_value('post_data', exec_step.data)
            #     #glo.set_value('response', res)
            #     glo.set_value('res_json', res.json())
            #     logging.debug("res.json(): %s"%repr(res.json()))
            #
            #     #eval_from_string(casedata['结果验证方法名'].rstrip('}') + '(${post_data},${response})}')
            #     # validation_result = eval_from_string(casedata['结果验证方法名'].rstrip('}') +
            #     #                                      #'(base.globalvars.getvalue("post_data"),base.globalvars.getvalue("response"))}',return_str=False,json_str=False)
            #     #                                     '(${post_data},${res_json})}', return_str = False, json_str = False)
            #     validation_result = eval_from_string(casedata['结果验证方法名'].rstrip('}') +
            #                                         '(${post_data},${res_json})}')
            #     self.assertTrue(validation_result,'验证不通过')

            if 'Set_Global_Variable' in casedata.keys() and casedata['Set_Global_Variable']!="":
                if casedata['Set_Global_Variable'].startswith("text:"): #text: variable_name
                    var_name=casedata['Set_Global_Variable'].replace("text:","")
                    glo.set_value(var_name,res.text)
                # json: expression-index:variable_name, e.g: json:$.newsId:[0]:newsId，setting multiple variables in one request is supported(serapate by ';')
                elif casedata['Set_Global_Variable'].startswith("json:"):
                    set_glo_value_json = casedata['Set_Global_Variable'].rstrip(";")
                    for json_item in set_glo_value_json.split(';\n'):
                        values = json_item.split(':')
                        var_name=values[-1]
                        jp_exp = values[1] #jsonpath
                        # if values[2]!="":
                        #     index = values[2]
                        result = eval("jsonpath(res.json(),jp_exp)")
                        glo.set_value(var_name,eval("jsonpath(res.json(),jp_exp)"+values[2]))

                else:
                    self.fail("Incorrect format in Set Global Variable")


            if 'Tear_Down' in casedata.keys() and casedata['Tear_Down']!="":
                # execute post case action
                #eval_from_string(casedata['Tear_Down'],return_str=False,json_str=True)
                eval_from_string(casedata['Tear_Down'])
        else:
            # raise unittest.SkipTest("case set not to run") # case skipped and won't be calculated as pass
            pytest.skip("case set not to run")

    def tearDown(self):
        pass