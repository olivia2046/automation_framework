# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2019/8/9 16:52
desc: https://www.cnblogs.com/changbo/p/5595030.html
'''

import os,datetime,time,logging

def delfile(folder,days):
    """

    :param folder: folder that needs to be cleaned
    :param days: number of days. files older than it will get cleaned.

    :return:
    """
    f = list(os.listdir(folder))
    logging.info(f"Start to clean folders under {folder} older than {days} days.....")
    try:
        for i in range(len(f)):
            filedate = os.path.getmtime(folder + os.sep+ f[i])
            time1 = datetime.datetime.fromtimestamp(filedate).strftime('%Y-%m-%d')
            date1 = time.time()
            num1 = (date1 - filedate) / 60 / 60 / 24
            if num1 >= days:

                os.remove(folder +os.sep + f[i])
                logging.info(u"Files cleaned: %s ： %s" % (time1, f[i]))
    except Exception as e:
        logging.error(e)


 