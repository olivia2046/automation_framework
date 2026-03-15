# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:59:53 2018

@author: olivia
"""
import sys,re,logging,json
from jsonpath import jsonpath
sys.path.append('..')
from base.runmethod import RunMethod
from util.json_util import JsonUtil
from base.getdata import GetData
#from base.get_config import get_header_file,get_data_file, get_verify_cert
#@Todo:get_header_file,get_data_file,get_root_url,get_verify不需要执行每个case时调用一次，用全局变量即可
from base.expression_evaluation import eval_from_string
import base.config as global_config


# class DependentData:
#     def __init__(self,case_id):
#         self.case_id = case_id
#         self.depend_case_data = None
#         self.data = None
#
#     #执行依赖测试，获取结果
#     def run_dependent(self):
#
#         #通过case_id去获取该case_id的整行数据
#         self.depend_case_data = GetData().get_case_data(self.case_id)
#         res = ExecuteStep().execute(self.depend_case_data)
#         return res
#
#
#     #根据依赖的key去获取执行依赖测试case的响应,然后返回
#     def get_data_for_case(self,case_data):
#         depend_data = case_data['Post Data依赖的返回数据']
#         response_data = self.run_dependent()
#
#         #获取依赖数据的key
#         if depend_data.startswith('json:'):
#             return jsonpath(response_data,depend_data.replace('json:'),'')
#
#         elif depend_data.startswith('html:'):
#             pattern = re.compile(depend_data.split(':')[1])#取中间的字符串
#             matches = re.findall(pattern,response_data.text)
#             indice = int(depend_data.split(':')[2])
#             dependent_value = matches[indice] #到底应该取第一个还是第二个？
#             return dependent_value

class ExecuteStep():
    
    def execute(self,casedata):
        #logging.debug(casedata.keys())
        if 'Specify_Header' in casedata.keys() and casedata['Specify_Header'].upper()=='Y':
            if 'Header_Content' in casedata.keys():
                header_value = casedata['Header_Content']
            else:
                header_value = {}
            # if header content is of {...} format then parse as json, otherwise use tag in header_file to extract as json header
            # supports expression evaluation for header written directly in Excel
            if re.findall("^{.+}$", header_value.replace("\n", "")) != []:  # todo: why match is None when contains \n
                header = json.loads(header_value)
            else:
                jutil = JsonUtil(global_config.get_header_file())
                header = jutil.get_data(header_value)
                #header_str = eval_from_string(repr(header),return_str=True,json_str=True)
                #header = json.loads(json.dumps(eval(header_str))) #直接用json.loads(header_str)会报json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
                header = eval_from_string(repr(header))
        else:
            header = None

        data = []
        if 'Request_Data' in casedata.keys() and casedata['Request_Data']!='':
            request_data = casedata['Request_Data'].strip()
            # if post data is of {...} format then parse as json, otherwise use tag in data_file to extract as json
            #if re.findall("^{.+}$",request_data.replace("\n",""))!=[]:
            try:
                data = json.loads(request_data)
                data_str = request_data
            except Exception as e:
                if ';' in request_data: # equation separated by ';', used when function called in json format data returns non-text
                    items = request_data.split(';')
                    data = {}
                    for item in items:
                        key,value = tuple(ele.strip('\n') for ele in item.split('=',1))
                        data[key] = eval(eval_from_string(value))
                    data_str = repr(data)

                elif request_data.startswith('data_label:'): #request_data is data label in data file
                    jutil = JsonUtil(global_config.get_data_file())
                    data = jutil.get_data(request_data) #json format data
                    data_str = repr(data)

                elif '=' in request_data: #api with url like /xxx&type=POST&params={"id":"123","type":"1","paths":{}}&contentType=1
                    data_str = request_data.strip()

                else: #post data is pure text
                    data_str = request_data

            # result = eval_from_string(data_str,return_str=True,json_str=True)
            # if not isinstance(result,str):
            #     result = repr(result)
            # #logging.debug("data_str: %s"%data_str)
            # #将函数执行后的结果再重新构造成json对象
            # data = json.loads(json.dumps(eval(result))) #json.dumps(eval(data_str))的作用是兼容单引号内容
            # 解析表达式
            data = eval_from_string(data_str)
            if isinstance(data,str):
                try:
                    # if dta is of json format then convert to json object
                    data = json.loads(data)
                except:
                    pass


        # #获取case依赖数据
        # if 'case依赖' in casedata.keys() and casedata['case依赖'] !='':#casedata已先期将nan替换为''
        #     depend_data = DependentData(casedata['case依赖'])
        #     #依赖的返回数据可能不止一处，返回的json数据，返回的html页面的一部分(authenticity_token， 如果要动态操作repository，则url也依赖返回的html页面元素)
        #     value = depend_data.get_data_for_case(casedata)
        #     if '数据依赖字段' in casedata.keys():
        #         field = casedata['数据依赖字段']
        #         data[field] = value
        #     else:
        #         return "未指定数据依赖字段"

        if 'Root_URL' in casedata:
            root_url = casedata['Root_URL']
        else:
            root_url = ""
        #root_url = eval_from_string(root_url, return_str=True, json_str=False)
        #root_url = eval_from_string(root_url)
        root_url = global_config.config.get(root_url)
        if 'relative_URL' in casedata.keys():
            #relative_url = eval_from_string(casedata['relative_URL'], return_str=True, json_str=False)
            relative_url = eval_from_string(casedata['relative_URL'])
        else:
            relative_url = ""

        # if 'encode_URL' in casedata.keys() and casedata['encode_URL'].upper()=='Y':
        #     relative_url = quote(relative_url, 'utf-8')


        url = root_url + relative_url


        if 'New_Session' in casedata.keys() and casedata['New_Session'].upper()=='N':
            # print("Retain Session~~~~~~~~~~~~~~~~~~~~~~")
            new_session=False
        else :
            # print("New Session~~~~~~~~~~~~~~~~~~~~~~~~")
            new_session=True

        if '+' in data:
            data = data.replace("+","%2B")
        #logging.debug("data:" + repr(data))
        self.data = data
        #glo.set_value("post_data",data)

        #verify = get_verify_str()
        # if verify.upper()=='FALSE':
        #     # logging.debug("no need to vefify certification.")
        #     #verify = eval("False")
        #     verify = False
        #     cert = None
        # else:
        #     verify=True
        #     cert = sys.path[0] + '/../' + get_certfile_path()
        #cert = get_cert()
        #verify,cert = get_verify_cert()
        verify = global_config.config.get("verify",False)
        cert = global_config.config.get("cert",None)

        if isinstance(header,str):
            logging.debug("headers:%s"%header)
            header = None

        if not 'Request_Type' in casedata.keys():
            return "Request_Type Not Specified!"

        arguments = {"method": casedata['Request_Type'], "url": url, "headers": header, "verify": verify,
                     "new_session": new_session}
        if 'Data_Type' in casedata.keys() and casedata['Data_Type'].lower()=='json':
            # res = RunMethod().run_main(method=casedata['Request_Type'], url=url, json=data, headers=header, verify=verify, cert = cert,
            #                            new_session=new_session)
            arguments["json"] = data
        else:
            # res = RunMethod().run_main(method=casedata['Request_Type'], url=url, data=data, headers = header, verify = verify, cert = cert, new_session=new_session)
            arguments["data"] = data

        if cert is not None:
            arguments["cert"] = cert

        res = RunMethod().run_main(**arguments)


        return res