# -*- coding: utf-8 -*-
# **************************************
# @Time : 2026/3/16 15:27
# @Author : Olivia
# Desc:
# **************************************
import logging, os, shutil, subprocess
from pathlib import Path

def allure_pre_process(report_rootdir_path):
    """ pre-process for allure report, saving history data for trend chart
    :param report_rootdir_path: absolute path of report rootdir
    """
    allure_resultdir_path = f'{report_rootdir_path}/allure-results/'
    allure_reportdir_path = f'{report_rootdir_path}/allure-report/'
    history_storage_path = f'{report_rootdir_path}/allure-history-storage/'
    # if there's old report, extract history data for trend chart
    # if os.path.exists(os.path.join(allure_reportdir_path, "history")):
    #     shutil.copytree(
    #         os.path.join(allure_reportdir_path, "history"),
    #         os.path.join(allure_resultdir_path, "history"),
    #         dirs_exist_ok=True
    #     )

    if os.path.exists(history_storage_path):
        shutil.copytree(history_storage_path, os.path.join(allure_resultdir_path, "history"), dirs_exist_ok=True)


def make_allure_report(report_rootdir_path):
    """
    :param report_rootdir_path: absolute path of report rootdir
    """
    allure_resultdir_path = f'{report_rootdir_path}/allure-results/'
    allure_reportdir_path = f'{report_rootdir_path}/allure-report/'
    temp_report_path = f'{report_rootdir_path}/allure-report-temp/'
    history_storage_path = f'{report_rootdir_path}/allure-history-storage/'

    # first, generate standard report(not single file), to get history folder
    cmd = f"allure generate {allure_resultdir_path} --clean -o  {temp_report_path}"
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # next, save history data for usage in next run
    if not os.path.exists(os.path.join(history_storage_path, "history")):
        Path(os.path.join(history_storage_path, "history")).mkdir(parents=True, exist_ok=True)
    shutil.copytree(os.path.join(temp_report_path, "history"), history_storage_path, dirs_exist_ok=True)

    # finally, generate single file to view report
    cmd = f"allure generate {allure_resultdir_path} --clean --single-file -o  {allure_reportdir_path}"

    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    # # clean temp report folder
    # if os.path.exists(temp_report_path):
    #     shutil.rmtree(temp_report_path)

    logging.info(f"Completed！Allure single file report generated: {allure_reportdir_path}/index.html")

