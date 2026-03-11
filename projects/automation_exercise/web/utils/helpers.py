"""
helpers.py
----------
Reusable utility functions for the Automation Exercise test framework.

Contains helper methods for generating test data, handling screenshots,
file operations, and other common testing utilities.
"""

import os
import re
import logging
import random
import string
from datetime import datetime
from faker import Faker

from utils.config import SCREENSHOTS_DIR

logger = logging.getLogger(__name__)
fake = Faker()


# ---------------------------------------------------------------------------
# Test Data Generators
# ---------------------------------------------------------------------------

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


def generate_registration_data() -> dict:
    """
    Generate a complete set of registration form data.

    Returns:
        dict: Dictionary with all fields required for account registration.
    """
    return {
        "name": fake.first_name() + " " + fake.last_name(),
        "email": generate_unique_email(),
        "password": "TestPassword@123",
        "title": random.choice(["Mr", "Mrs"]),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": fake.street_address(),
        "country": "United States",
        "state": fake.state(),
        "city": fake.city(),
        "zipcode": fake.zipcode(),
        "mobile": fake.numerify("##########"),
    }


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
# Screenshot Utilities
# ---------------------------------------------------------------------------

def take_screenshot(page, name: str) -> str:
    """
    Capture a screenshot and save it to the screenshots directory.

    Args:
        page: Playwright Page object.
        name: Descriptive name for the screenshot file.

    Returns:
        str: Absolute path to the saved screenshot.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r"[^\w\-_]", "_", name)
    filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_{timestamp}.png")

    try:
        page.screenshot(path=filepath, full_page=True)
        logger.info(f"Screenshot saved: {filepath}")
    except Exception as e:
        logger.warning(f"Failed to take screenshot '{name}': {e}")

    return filepath


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


# ---------------------------------------------------------------------------
# Wait Utilities
# ---------------------------------------------------------------------------

def wait_and_dismiss_ad(page) -> None:
    """
    Dismiss common ad overlays that may appear on automationexercise.com.

    The site serves third-party ads that can block interactions.
    This helper closes any visible ad iframes or overlay buttons.

    Args:
        page: Playwright Page object.
    """
    try:
        # Close button that appears with some ad overlays
        close_btn = page.locator("button:has-text('×'), .fc-close, [id*='dismiss'], [aria-label='Close']")
        if close_btn.count() > 0:
            close_btn.first.click(timeout=3000)
            logger.debug("Dismissed ad overlay")
    except Exception:
        pass  # No overlay present — continue normally
