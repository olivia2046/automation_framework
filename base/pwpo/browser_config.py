# -*- coding: utf-8 -*-
# **************************************
# @Time : 2026/3/18 10:09
# @Author : Olivia
# Desc:
# **************************************
import os
from dataclasses import dataclass, field
from base import config as global_config

# BrowserConfig is of dataclass, so code will be executed when importing,
    # while code in default_factory will be delayed when BrowserConfig is instantiated
def get_headless_value():
    """ get headless browser launch options
    """
    # if not called in default_factory of BrowserConfig, get_env_filepath() will return None
    from dotenv import load_dotenv
    env_file_path = global_config.get_env_filepath()
    load_dotenv(env_file_path)
    return os.getenv("HEADLESS", "true").lower()

def get_slowmo_value():
    """ get slowmo launch options
    """
    # if not called in default_factory of BrowserConfig, get_env_filep1ath() will return None
    from dotenv import load_dotenv
    env_file_path = global_config.get_env_filepath()
    load_dotenv(env_file_path)
    return os.getenv("SLOW_MO", "0")

@dataclass
class BrowserConfig:
    """Playwright browser launch options."""
    # # Load environment variables from .env file if present
    # from dotenv import load_dotenv
    # env_file_path = global_config.get_env_filepath()
    #
    # if env_file_path:
    #     load_dotenv(env_file_path)
    # else:
    #     load_dotenv()
    #
    #
    # headless: bool = field(default_factory=lambda: os.getenv("HEADLESS", "true").lower() == "true")
    # slow_mo: int = field(default_factory=lambda: int(os.getenv("SLOW_MO", "0")))
    headless: bool = field(default_factory=lambda: get_headless_value() == "true")
    slow_mo: int = field(default_factory=lambda: int(get_slowmo_value()))
    viewport_width: int = 1920
    viewport_height: int = 1080
    locale: str = "en-US"
    timezone: str = "America/Los_Angeles"
