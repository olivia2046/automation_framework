"""
config.py
---------
Central configuration module for the Automation Exercise test project.

All constants, URLs, credentials, and environment settings are defined here.
Import this module wherever configuration values are needed.
"""

import os
from dataclasses import dataclass

import base.config as global_config
from base.pwpo.base_page import Timeouts
from base.pwpo.browser_config import BrowserConfig


# ---------------------------------------------------------------------------
# URLs
# ---------------------------------------------------------------------------
#BASE_URL = os.getenv("BASE_URL", "https://www.automationexercise.com")




# ---------------------------------------------------------------------------
# Test User Credentials
# ---------------------------------------------------------------------------
@dataclass
class TestUser:
    """Represents a test user account."""
    name: str
    email: str
    password: str
    first_name: str = "Test"
    last_name: str = "User"
    address: str = "123 Test Street"
    country: str = "United States"
    state: str = "California"
    city: str = "Los Angeles"
    zipcode: str = "90001"
    mobile: str = "5551234567"

def get_existing_user():
    # lazy load
    # Load environment variables from .env file if present
    from dotenv import load_dotenv

    load_dotenv(global_config.get_env_filepath())
    # from dotenv import load_dotenv, find_dotenv
    #
    # load_dotenv(find_dotenv())
    # Pre-registered user for login tests (must exist in the app)
    EXISTING_USER = TestUser(
        name="TestAutomation",
        email=os.getenv("AE_TEST_EMAIL"),
        password=os.getenv("AE_TEST_PASSWORD"),
    )
    return EXISTING_USER

# Invalid credentials for negative tests
INVALID_USER = TestUser(
    name="Invalid",
    email="nonexistent_user_xyz@example.com",
    password="wrongpassword",
)


# ---------------------------------------------------------------------------
# Timeouts (milliseconds)
# ---------------------------------------------------------------------------


TIMEOUTS = Timeouts()


# ---------------------------------------------------------------------------
# Browser Configuration
# ---------------------------------------------------------------------------
def get_browser_config() -> BrowserConfig:
    return BrowserConfig()



#BROWSER_CONFIG = BrowserConfig(headless=False, slow_mo=500, viewport_width=1920, viewport_height=1080)



# ---------------------------------------------------------------------------
# Screenshot & Reporting
# ---------------------------------------------------------------------------
# SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
# SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
# REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")


# ---------------------------------------------------------------------------
# Product Data
# ---------------------------------------------------------------------------
SEARCH_TERMS = {
    "valid": "Top",
    "no_results": "xyzproductnotexist123",
    "category_women": "Dress",
}

PRODUCT_CATEGORIES = {
    "Women": ["Dress", "Tops", "Saree"],
    "Men": ["Tshirts", "Jeans"],
    "Kids": ["Dress", "Tops & Shirts"],
}

BRANDS = ["Polo", "H&M", "Madame", "Mast & Harbour", "Babyhug", "Allen Solly Junior"]


def get_base_url() -> str:
    return global_config.config["base_url"]

def get_urls() -> dict:
    BASE_URL = get_base_url()
    return  {
        "home": BASE_URL,
        "login": f"{BASE_URL}/login",
        "products": f"{BASE_URL}/products",
        "cart": f"{BASE_URL}/view_cart",
        "checkout": f"{BASE_URL}/checkout",
        "contact": f"{BASE_URL}/contact_us",
        "signup": f"{BASE_URL}/login",
    }