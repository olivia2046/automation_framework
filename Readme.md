
# 1. Folder Structure
```
automation_framework/  
├── base/           # core modules of framework
├── config/         # config files to run test, each environement of each project should have its own config file  
├── main/           # run test case from main_pytest.py  
├── projects/       # project folders
    ├── general/    
        ├── general_api_test.py     # Excel driven api test
    ├── project A/    
        ├── api/    
        ├── lib/    # libraries to be used within project
        ├── mobile/  
        ├── web/
            ├── case/
            ├── po/
    ├── project B
├── testreport      # test reports will be generated here
├── util            # utility
  
```




# 2. Usage
```
⚙️ Set up:  
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


# 💡3. Excel API Case Explanation
📌 Example of Excel API Test Case can be found under projects/automation_exercise/api
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
|Request_Data|	        # optional                  json format post data 
|Expected_Code|	        # required                  expect reponse status code
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


💡|Json_Result_Validation|
Rule based valiation on json response using jsonpath.
e.g. Search for "tshort" in product list, verify that all items returned are of category 'Tshirts', then validate as:
["=","$.products[*].category.category","Tshirts"]
where the first item in the [] is operator, the second one is the jsonpath to extract data, the third is the value to be compared to
🔹 use ';' to seperate multiple rules, and each rule functions together as 'and' relationship  
🔹 supported operators:
    '=',
    '!=',
    '>',
    '>=',
    '<',
    '<=',
    'and',
    'in',
    'not in',
    'contains',
    'not contains',
    'or',
    'not'
🔹 You can use operator "and", "or" to link rules  
🔹 default rule is to check on each item of list get from jsonpath expression. 
E.g. for ["=","$.products[*].category.category","Tshirts"], $.products[*].category.category returns a list of categories, it will check whether each item in this list equals to "Tshirts"
🔹 to check against the list itself, add "list relation" to the end of the rule, e.g.
["length","$.brands[*]","list relation"] gets the length of list retrieved by "$.brands[*]",
and then you can use ["=",["length","$.brands[*]","list relation"],34] to check whether the length equals to 34
🔹 value to be compared to can contain function call, just like that used in Set_Up and Tear_Down 


|Set Global Variable|
Extract data from API response to set to global variable
🔹 response is text
For example: API response is "Tshirts" and you want to set to global variable "category",then write as:
text:category 
🔹 resonse it json
For example: You need to extract a value(e.g. ) from the api response, you need to get the id value of first item in data node,
 to save to global variable "resultId", then write as: 
 json:$.data[*].id:[0]:resultId
- json: process api response as json data
- $.data[*].id:[0]: the jsonpath used to extract id value of first item in data node
- resultId: name of the global variable
```

