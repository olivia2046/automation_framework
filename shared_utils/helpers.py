# -*- coding: utf-8 -*-
# **************************************
# @Time : 2026/3/18 16:29
# @Author : Olivia
# Desc:
# **************************************
import logging
import os
import random, string
import re
from datetime import datetime
from faker import Faker
from playwright.sync_api import Page

import base.config as global_config

fake = Faker()
# from utils.config import SCREENSHOTS_DIR
# from utils.helpers import fake, logger


def generate_unique_email() -> str:
    """
    Generate a unique email address for registration tests.

    Returns:
        str: A unique email like 'testuser_abc12345@example.com'
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = "".join(random.choices(string.ascii_lowercase, k=4))
    return f"testuser_{suffix}{timestamp}@example.com"


def generate_random_name() -> str:
    """
    Generate a random full name.

    Returns:
        str: A random name string.
    """
    return fake.name()


def generate_card_data() -> dict:
    """
    Generate test credit card data (for test environments only).

    Returns:
        dict: Dictionary with card name, number, CVC, and expiry.
    """
    return {
        "name": fake.name(),
        "number": "4111111111111111",   # Standard Visa test number
        "cvc": "123",
        "expiry_month": "12",
        "expiry_year": "2027",
    }

# ---------------------------------------------------------------------------
# String / Assertion Helpers
# ---------------------------------------------------------------------------


def normalize_text(text: str) -> str:
    """
    Normalize a string by stripping whitespace and converting to lowercase.

    Args:
        text: The input string.

    Returns:
        str: Normalized string for case-insensitive comparisons.
    """
    return text.strip().lower()


def contains_text(haystack: str, needle: str, case_sensitive: bool = False) -> bool:
    """
    Check if one string contains another.

    Args:
        haystack: The string to search within.
        needle: The substring to search for.
        case_sensitive: Whether to perform a case-sensitive search.

    Returns:
        bool: True if needle is found in haystack.
    """
    if not case_sensitive:
        return needle.lower() in haystack.lower()
    return needle in haystack


def take_screenshot(page: Page, name: str, full_page: bool = True) -> str:
    """
    Capture a screenshot and save it to the screenshots directory

    Args:
        page:      Page to take screenshot.
        name:      Descriptive name for the screenshot file.
        full_page: When True, captures the entire scrollable page (default).
    """

    screenshot_dir = global_config.config['screenshot_dir']
    os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r"[^\w\-_]", "_", name)
    filepath = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")

    # self.page.screenshot(path=filepath, full_page=full_page)
    # logger.info(f"Screenshot saved: {filepath}")

    try:
        page.screenshot(path=filepath, full_page=full_page)
        logging.info(f"Screenshot saved: {filepath}")
    except Exception as e:
        logging.warning(f"Failed to take screenshot '{name}': {e}")

    return filepath