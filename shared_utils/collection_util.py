# -*- coding: utf-8 -*-
'''
| @author: olivia.dou
| Created on: 2018/11/23 15:20
| desc: 和集合有关的util function
'''
import random


def random_select_from_list(input_list,n=0):
    """从列表中随机选取指定个数的元素

    :param input_list: 输入列表
    :param n: 指定返回元素的个数

    :return: 随机选取的指定个数的元素
    """
    if len(input_list)==1:
        return input_list
    else:
        #result = []
        if n==0: #未指定需返回的元素个数
            n = random.randint(1,len(input_list))  #随机选定返回结果的元素个数
        elif n>len(input_list): #指定个数超过列表元素个数
            n=len(input_list)
        # for i in range(n):
        #     result.append(input_list[random.randint(0, len(input_list)-1)])
        result = random.sample(input_list,n)
        return result

def random_select_one_from_list(input_list):
    """从输入列表中随机选取一个元素

    :param input_list: 输入列表

    :return: 随机选取的一个元素
    """
    select_list = random_select_from_list(input_list,1)
    return select_list[0]

def is_list(obj):
    if isinstance(obj, list):
        return True
    else:
        return False