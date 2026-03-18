"""
helpers.py
----------
Reusable utility functions for the Automation Exercise test framework.

Contains helper methods for generating test data, handling screenshots,
file operations, and other common testing utilities.
"""

import logging
import random
from faker import Faker
from shared_utils.helpers import generate_unique_email

logger = logging.getLogger(__name__)
fake = Faker()


# ---------------------------------------------------------------------------
# Test Data Generators
# ---------------------------------------------------------------------------

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
            logging.debug("Dismissed ad overlay")
    except Exception:
        pass  # No overlay present — continue normally
