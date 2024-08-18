# -*- coding: utf-8 -*-
'''
| @author: olivia.dou
| Created on: 2019/4/15 9:46
| desc:
'''

import re,logging,traceback,random, string
import urllib.parse
import uuid


def url_encode_special_char(string):
    """将后面两个字符不是数字，也不是字母的'%'字符串encode成%25?

    :param string: 输入字符串

    :return: encode后的字符串
    """

    # 模式(?!pattern), 零宽负向先行断言(zero-widthnegative lookahead assertion),代表字符串中的一个位置，紧接该位置之后的字符序列不能匹配pattern
    #'%'开始，但是后面两个字符不是数字，也不是字母
    string = re.sub("%(?![0-9a-fA-F]{2})","%25",string)
    string = string.replace("\\+", "%2B")

    return string


def encode_url_parameter(param_dict):
    """将参数字典作url encode

    :param param_dict: 参数字典

    :return: url
    """
    for key,value in param_dict.items():
        value = url_encode_special_char(value)
        param_dict[key]=value

    encoded_url = urllib.parse.urlencode(param_dict)
    return encoded_url

def hit_string(target_str,str_list):
    """目标字符串是否在指定的字符串列表中匹配到（字符串patial匹配）
    | 如：指定字符串列表["abcd","efg"],则"abc"匹配到

    :param target_str: 目标字符串
    :param str_list: 字符串列表

    :return: True: 匹配到， False: 未匹配到
    """

    hit = False
    for str in str_list:
        if target_str in str:
            hit = True
            break
    return hit

def convert_to_float_from_str(input_str):
    """将输入的字符串(可含千分位表示)转换为浮点数

    :param input_str: 输入字符串

    :return: 浮点数
    """

    try:
        if input_str is None:
            return None
        input_str = input_str.replace(',', '')
        matched = re.match('(-)?\((\d.+)\)', input_str)
        if matched is not None: #添加符号
            if matched.group(1) is not None:
                input_str = matched.group(2)
            else:
                input_str = '-' + matched.group(2)
        return float(input_str)
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        return 0

def convert_number_to_chinese(keyword):
    """将数字转换为中文数字

    :param keyword: 输入的数字

    :return: 与输入数字对应的中文数字
    """
    num_to_ch_dict = {'1':'一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '0': '零'}
    for char in keyword:
        if char in num_to_ch_dict.keys():
            keyword = keyword.replace(char, num_to_ch_dict[char])
    return keyword

def random_partial_string(input_str):
    """返回指定字符串中随机位置的部分字符串（如股票代码的部分）

    :param input_str: 输入字符串

    :return: 随机位置的部分字符串，如输入"600690"，可能返回"0690","6006"等
    """
    length = len(input_str)
    start = random.randint(0,length - 2)
    end = random.randint(start + 1, length - 1)
    return input_str[start:end]

def random_char(i):
    """随机生成类型（a-z,A-Z,0-9）指定长度的字符串"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for j in range(i))


def get_random_uuid():
    random_uuid = str(uuid.uuid4()).replace("-", "")
    return random_uuid

def get_list_from_str(input_str):
    return input_str.split(',') if input_str != "" and input_str is not None else []


def format_parse_thousandth(input_str):
    """格式化str的千分位表示（因内置format()函数进行千分位转换时，会将str转为float造成精度丢失，
    无法对某些六位小数位准确表示，如65.165408）

    :param input_str: 输入字符串

    :return: 千分位格式字符串
    """
    #  拼接结果字符串
    sum_str = ''
    count = 0
    # 是否含小数位，含有则分割小数左边字符串
    format_str = input_str.split('.')[0] if input_str.count('.') != 0 else input_str
    # 是否含负号位，含负号则去除负号
    final_format_str = format_str[::-1] if input_str.count('-') == 0 else format_str[:0:-1]  # 循环需从后向前输出
    final_format_str_len = len(format_str) if input_str.count('-') == 0 else len(format_str) - 1

    for str in final_format_str:
        count += 1
        if count % 3 == 0 and count != final_format_str_len:
            # count等于3或3的倍数并且不等于总长度，在前加','
            str = ',' + str
            sum_str = str + sum_str
        else:
            sum_str = str + sum_str

    # 最终拼接还原字符串，还原负号/小数位等
    sum_str = '-' + sum_str + '.' + input_str.split('.')[1] if input_str.count('-') != 0 and input_str.count('.') != 0 \
        else '-' + sum_str if input_str.count('-') != 0 and input_str.count('.') == 0 \
        else sum_str + '.' + input_str.split('.')[1] if input_str.count('-') == 0 and input_str.count('.') != 0 \
        else sum_str

    return sum_str

def dic_to_str(dic):
    s = ''
    for key in dic:
        s+="{0}: {1}\n".format(key,dic[key])
    return s



def extract_string(input_str, separators):
    """从input_str中获取被separators包含的字符串

    :param input_str: 输入字符串
    :param separators: 分隔符，需要为一对字符，如括号"()"

    :return:
    """
    start_index = input_str.find(separators[0]) + 1
    end_index = input_str.find(separators[1], start_index)
    if start_index != -1 and end_index != -1:
        return input_str[start_index:end_index]
    else:
        return ""