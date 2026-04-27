"""
Created on Mar 12 08:23:02 2026
@author: Olivia
Description: Global config singleton. Filled when test initiates(in common_hooks.py)
            usage in other modules:

            import base.config as global_config
            url = global_config.config["base_url"]

"""
import os,logging
config: dict = {}
abspath = os.path.split(os.path.realpath(__file__))[0]

def get_testcase_file():
    try:
        project_dir_name = config.get("file_path").get("project_rootdir")
        tc_dir_name = config.get("file_path").get("tc_rootdir")
        return (abspath + os.sep + '..' + os.sep + project_dir_name + os.sep + tc_dir_name + os.sep +
                config.get("file_path").get("testcase_file"))
    except Exception as e:
        logging.error("get_testcase_file:%s" % e)
        return ""

def get_tc_rootdir():
    try:
        project_dir_name = config.get("file_path").get("project_rootdir")
        tc_dir_name = config.get("file_path").get("tc_rootdir")
        return (abspath + os.sep + '..' + os.sep + project_dir_name + os.sep + tc_dir_name)
    except Exception as e:
        logging.error("get_tc_rootdir:%s" % e)
        return ""

def get_header_file():
    try:
        project_dir_name = config.get("file_path").get("project_rootdir")
        data_dir_name = config.get("file_path").get("data_rootdir")
        return (abspath + os.sep + '..' + os.sep + project_dir_name + os.sep + data_dir_name + os.sep +
                config.get("file_path").get("header_file"))
    except Exception as e:
        logging.error("get_header_file:%s" % e)
        return ""

def get_data_file():
    try:
        project_dir_name = config.get("file_path").get("project_rootdir")
        data_dir_name = config.get("file_path").get("data_rootdir")
        return (abspath + os.sep + '..' + os.sep + project_dir_name + os.sep + data_dir_name + os.sep +
                config.get("file_path").get("data_file"))
    except Exception as e:
        logging.error("get_data_file:%s" % e)
        return ""


def get_env_filepath():
    """ each environment may have more than one test type: api/web/mobile so --config name in command line has _api/_web/_mobile suffix
        but each environment only have one .env file(those insensitive configuration are put in .yaml file for each test type)

    """
    if 'config_name' in config:
        config_name = config['config_name']
        environment = config_name.rsplit("_",1)[0]
        return abspath + os.sep + '..' + os.sep + f"config/.env.{environment}"
    else:
        return None


