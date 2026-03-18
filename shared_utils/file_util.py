# -*- coding: utf-8 -*-
'''
| @author: olivia.dou
| Created on: 2018/10/16 17:24
| desc: 和文件操作相关的常用库
'''
import logging,os,shutil,urllib,re
from functools import reduce

def clear_folder(folderpath):
    """清理文件夹

    :param folderpath: 文件夹路径

    :return: 无
    """
    contents =  os.listdir(folderpath)
    if contents!=[]:
        for item in contents:
            item_path = os.path.join(folderpath, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)


def download_file(url,local_path):
    """Todo

    :param url: 文件url
    :param local_path: 文件存储本地路径

    :return:
    """


def get_legal_filename(raw_filename):
    """去除字符串中不能被文件名使用的非法字符

    :param raw_filename: 输入的raw文件名
    :return: 合法的文件名
    """

    #return raw_filename.translate(None, r"|\\?*<\":>+[]/'")
    pattern = r'[\\/:*?"<>|\r\n]+'
    return re.sub(pattern,'',raw_filename)




 