
# 1. Folder Structure
```
automation_framework/  
|-- base/           # core modules of framework
|-- config/         # config files to run test, each environement of each project should have its own config file  
|-- main/           # run test case from main_pytest.py  
|-- projects/       # project folders
    |-- general/    
        |-- general_api_test.py     # Excel driven api test
    |-- project A/    
        |-- api/    
        |-- lib/    # libraries to be used within project
        |-- mobile/  
        |-- web/
            |-- case/
            |-- po/
    |-- project B
|-- testreport      # test reports will be generated here
|-- util            # utility
  
```




# 2. Usage
```
Set up:  
    Create a settings-XXX.ini file(XXX should not have space in it),  
    e.g. settings-automation_exercise_api.ini is for automation_exercise_api is for api test of automationexercise website  
    You can set up different files for each environment like qa,std,etc.  
Execute:  
    For Excel-driven api test cases:  
    (need to close the Excel file first)
    cd main  
    python main_pytest.py XXX
      XXX is the config file suffix
    For Code type api test cases and web/mobile tests, run them as pytest executes tests  
     
```


# 3. Excel Case Explanation
## 3.1 Sheets
You can have multiple sheets to better organize your test cases(e.g. one sheet per module).
It will execute test cases in sheet sequence.

## 3.2 Columns
```

|Requirement_ID|        # optional                  ID of the requirement
|Case_Name|	            # required                  Test Case Name(will be used in test report)
|Module|	            # optional                  name of module, for filtering test cases
|Summary|	            # required                  short description of test case
|Run|	                # optional(defaul to Y)     whether to run the case (filter cases in addition to case level)
|Case_Level|	        # required                  Smoke/Sanity/Regression
|New_Session|	        # optional(default to N)    whether to start a new session or retain session
|Set_Up|	            # optional                  function to execute as set up of test case
|Specify_Header|	    # optional(default to N)    whether to specify a header for request
|Header_Content|	    # required when Sepecify_Header is set to Y
                                                    either the json header, or a node in header file
|Root_URL|	
|relative_URL|	
|Request_Type|	        # GET/POST/PUT/DELETE
|Data_Type|	            # if data specified in "Request Data" column should be passed as json data, then put 'json', 
                          otherwise "Reqeust Data" will be converted to parameter like key1=value1&key2=value2 
|Request_Data|	         
|Expected_Code|	
|Expected_Text|	        # if response should be plain text, put the text here
|Compare_Method|        # method used to compare expected result with actual result, 
                          required when "Expected Text" is not empty: assertEqual/assertNotEqual/assertIn/assertNotIn
                          {Expected Text}	{Compare Method}  {Actual Result}
                          e.g. "Expected Text" column value is a, "Compare Method" is b, actual result the api returns is b, assertion is whether a==b
|Json_Result_Validation|	# assertions when response data is of json format  
|Set_Global_Variable|	# set global variable where needed 
|Tear_Down|	    # optional                  you can execute action defined in project libraries after test case execution
|Owner|                 # Owner of this test case, so when there're multiple persons working on the test cases, 
                          it's easy to find the owner to troubleshoot/maintain the test case when it fails

```
## 3.3 Detail Explanation
```
|Set_Up| |Tear_Down|
Example: use function defined in projects/automation_exercise/libs/
${projects.automation_exercise.libs.demo.py::function_used_by_setup()}
${projects.automation_exercise.libs.demo.py::function_used_by_teardown()}



|Header Content|
When |Specify Header| is set to 'Y', header content can either be the full header like 
{
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Authorization": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "username": "Automation"
  }
Or, you can have a header file in projects/automation_exercise/data/headers.json,
and put the file path as in config/settings-automation_exercise_api.ini,
and fill in 'header1' to refer to the 'header1' node in the headers file.

|Set Global Variable| 
For example: You need to extract a value(e.g. ) from the api response, you need to get the id value of first item in data node,
 to save to global variable "FresultId", then write as json:$.data[*].id:[0]:resultId
- json: process api response as json data
- $.data[*].id:[0]: the jsonpath used to extract id value of first item in data node
- resultId: name of the global variable
  

断言内容为比较jsonpath表示的列表中每一个元素，则正常添加断言表达式  
断言内容为比较jsonpath表示的列表，则在断言表达式末尾增加一个参数"list relation"
     
接口返回结果为仅一个空列表的情况：  
如果接口仅可能返回一个空列表，可在“期望响应文本”列填[]  
如果接口可能返回一个空列表，也可能为其他结果，则空列表的情况写为：["=","$response_plain_text","[]"]

表达式内包含表达式：
["in","$.data[*].id","${proj_spec.DEMO.mudule1.function_a('param1_value,param2='${proj_spec.DEMO.module2.function_b(param1=\"text_value\")}')}"]

Post_Case_Action基于响应结果设置全局变量：  
响应结果为文本类型：  
text:变量名  
响应结果为json格式：  
json:表达式:索引下标:变量名， 如json:$.newsId:[0]:newsId


	
```

