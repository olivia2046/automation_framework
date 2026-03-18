# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2019/8/9 16:52
desc: https://www.cnblogs.com/changbo/p/5595030.html
'''

import os,datetime,time,logging
import pathlib


# def remove_old_files(folder, days):
#     """
#
#     :param folder: folder that needs to be cleaned
#     :param days: number of days. files older than it will get cleaned.
#
#     :return:
#     """
#     f = list(os.listdir(folder))
#     logging.info(f"Start to clean folders under {folder} older than {days} days.....")
#     try:
#         for i in range(len(f)):
#             filedate = os.path.getmtime(folder + os.sep+ f[i])
#             time1 = datetime.datetime.fromtimestamp(filedate).strftime('%Y-%m-%d')
#             date1 = time.time()
#             num1 = (date1 - filedate) / 60 / 60 / 24
#             if num1 >= days:
#
#                 os.remove(folder +os.sep + f[i])
#                 logging.info(u"Files cleaned: %s ： %s" % (time1, f[i]))
#     except Exception as e:
#         logging.error(e)

def remove_old_files(target_dir, days=30):
    """

    :param target_dir: folder that needs to be cleaned
    :param days: number of days. files older than it will get cleaned.

    :return:
    """
    #convert to Path object
    base_path = pathlib.Path(target_dir)

    # calculate time
    seconds_in_day = 24 * 60 * 60
    cutoff_time = time.time() - (days * seconds_in_day)

    count = 0

    # rglob("*") recursively visit all file and sub folders
    for item in base_path.rglob("*"):
        # only check files, skip folder itself
        if item.is_file():
            # get last modified time
            file_mtime = item.stat().st_mtime

            if file_mtime < cutoff_time:
                try:
                    logging.info(f"Cleaning file {item}")
                    item.unlink()  # delete file
                    count += 1
                except Exception as e:
                    print(f"delete failed for {item} : {e}")

    logging.info(f"Finished cleaning. Deleted {count} files.")


 