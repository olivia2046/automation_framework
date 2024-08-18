# -*- coding: utf-8 -*-
'''
| @author: olivia.dou
| Created on: 2019/12/6 16:16
| desc: 和数字相关的util function
'''
import logging,random, math

def get_number_from_string(input):
    """从输入字符串中获取数字，如输入"343,333,232.43"，返回343333232.43
    | Todo: 可以被string_util.convert_to_float_from_str包含？

    :param input: 输入的字符串

    :return: 输入字符串转换的浮点数
    """
    if input is None:
        return None
    if type(input) is not str:
        return input
    else:
        return float(input.replace(',', ''))


def get_random_amount(n=12):
    """获取指定有效位数的随机金额数

    :param n: 生成的有效数字位数

    :return: 包含n位有效数字的随机金额
    """

    return round(random.randint(0,math.pow(10,n))/100,2)



def approx_Equal(x, y, tolerance=0.001): #http://www.it1352.com/538183.html correct?
    """近似比较两个数字

    :param x: 数字1
    :param y: 数字2
    :param tolerance: 容错

    :return: True-容错率内近似，False-非近似
    """

    return abs(x-y) <= abs(0.5 * tolerance * (x + y))