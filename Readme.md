# 环境处理
因框架用到pytest-timestamps，当前服务器自动化运行环境python版本为3.7，只能安装pytest-timestamps 0.1.4，在同时使用pytest.mark.skip/skipif等的时候会因为未从跳过的用例获取到时间戳而出错，需要在pytest-timestamps的plugin.py里做如下修改
https://gy1hkk14ia.feishu.cn/wiki/DK5DwEMuriq22eklQijcfrx5nZg

# 目录结构  
base:此框架的构成要素  
case:测试用例  
--algo：算法测试用例
--db: 数据库测试用例  
--interface：接口测试用例  
----proj_a：项目A接口测试用例  
config:配置文件  
data：数据文件，包含headers数据和post数据  
main: 主程序入口  
proj_spec: 基于项目的函数库  
testreport：测试报告  
util: 工具函数库  

# 使用方法
运行：在config目录下新建settings - XXXX.ini文件（XXXX部分不能有空格），内容可参照DEMO项目测试配置文件  
      cd main  
      python main_test.py XXXX  [-e any/fail] [-r reportname] [ -a algorithm_name] [--host algorithm_host] [-p/--port algorithm_port]  
      XXXX为配置文件名的后缀, -e为发送email, fail为仅当有失败或错误时发送，any为任意情况都发送  
      使用pytest执行 增加--tests_per_worker参数，即pytest的--tests-per-worker参数


# 配置文件参数说明
[Framework]     
run_case_type: Excel-Excel格式的用例, Code-Python代码的用例，用逗号连接

指定运行部分用例：  
运行Excel格式的用例时，可设置run_specific_case = true，并在配置文件[FilePath]/tc_rootdir所指定的目录下创建run_cases.txt文件，
该文件内容每一行为一个测试用例名称(Excel文件中的Case_Name列)，则仅运行Excel文件中“是否运行”列为Y/y，且Case_Name在run_cases.txt中列出的用例

运行Python代码用例，可在run_case_folder下设置需要运行的文件夹名称，以逗号分隔

# Excel用例说明
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

# 文档生成
命令行下执行doc/regen_doc.bat（需pip安装sphinx_rtd_theme）  
注意代码中涉及获取配置信息的导入，需要放到具体函数中，若放在文件根部，生成文档时会出错  
如：from base.get_config import get_header_file  
    from base.getdata import get_header
	


