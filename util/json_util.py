# -*- coding: utf-8 -*-
"""
| Created on Wed Aug 22 06:20:19 2018
| @author: olivia
"""

import json,logging

from util.os.os_tool import get_root_path


class JsonUtil:
    def __init__(self, file_path=None):
        if file_path == None:
            self.file_path = './data/data.json'
        else:
            self.file_path = file_path
        self.data = self.read_data()
        

    def read_data(self):
        """读取json文件

        :return: 文件中获取的json数据
        """

        with open(self.file_path,encoding='utf8') as fp:
            data = json.load(fp)
            return data  
        

    def get_data(self, key):
        """根据键名获取数据

        :param key: 键名

        :return: 指定键名下的数据
        """
        #print type(self.data)
        return self.data[key]

#    #写json
#    def write_data(self,data):
#        #with open('../dataconfig/cookie.json','w') as fp:
#        with open(cookie_file,'w') as fp:
#            fp.write(json.dumps(data))

if __name__ == '__main__':
    json_data=JsonUtil("company_type.json")
    d = json_data.get_data("T01")
    print(d)
    i = json_data.read_data()
    print(i.keys())
    print(list(i.values()))

