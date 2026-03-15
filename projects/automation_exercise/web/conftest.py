"""
conftest.py
-----------


sys.path note
-------------
This file lives at projects/automation_exercise/conftest.py.
Inserting its own directory into sys.path ensures that sibling packages
(pages/, utils/, fixtures/) are always importable regardless of which
working directory pytest is invoked from — repo root, projects/, or here.
"""

import sys
import os

# Make THIS project's root (automation_exercise/web) importable as a source root,
# regardless of from which directory pytest or the IDE launches.
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# add automation_framework to sys.path（base/ importable）
# need to add explicitly here, and not dependent on loading sequence in  root conftest.py
_FRAMEWORK_ROOT = os.path.abspath(os.path.join(_PROJECT_ROOT, "..", "..", ".."))
if _FRAMEWORK_ROOT not in sys.path:
    sys.path.insert(0, _FRAMEWORK_ROOT)

# register public hooks
pytest_plugins = ["base.pytest_plugins.common_hooks"]


import logging
import pytest
from playwright.sync_api import Page, Browser, BrowserContext

from pages import (
    HomePage,
    LoginPage,
    ProductsPage,
    ProductDetailPage,
    CartPage,
    CheckoutPage,
    ContactPage,
)
from utils.config import BROWSER_CONFIG, TIMEOUTS, SCREENSHOT_ON_FAILURE, SCREENSHOTS_DIR
from utils.helpers import take_screenshot, generate_registration_data, generate_card_data

logger = logging.getLogger(__name__)


# ===========================================================================
# Pytest Hooks
# ===========================================================================

def pytest_configure(config):
    """Ensure the screenshots output directory exists before tests run."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def pytest_runtest_makereport(item, call):
    """
    Hook that runs after each test phase (setup / call / teardown).

    Attaches a failure screenshot to the HTML report when a test fails,
    if SCREENSHOT_ON_FAILURE is enabled in config.
    """
    if call.when == "call" and call.excinfo is not None:
        if SCREENSHOT_ON_FAILURE:
            page: Page = item.funcargs.get("page")
            if page:
                test_name = item.nodeid.replace("/", "_").replace("::", "_")
                path = take_screenshot(page, f"FAILED_{test_name}")
                logger.info(f"Failure screenshot saved: {path}")


# ===========================================================================
# Browser-Level Fixtures
# ===========================================================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Override default browser context arguments with framework settings.

    Applies viewport size, locale, and timezone from BrowserConfig.
    This fixture is recognized and merged by pytest-playwright automatically.
    """
    return {
        **browser_context_args,
        "viewport": {
            "width": BROWSER_CONFIG.viewport_width,
            "height": BROWSER_CONFIG.viewport_height,
        },
        "locale": BROWSER_CONFIG.locale,
        "timezone_id": BROWSER_CONFIG.timezone,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Override browser launch arguments with framework settings.

    Controls headless mode and slow-motion playback speed.
    """
    return {
        **browser_type_launch_args,
        "headless": BROWSER_CONFIG.headless,
        "slow_mo": BROWSER_CONFIG.slow_mo,

    }

# @pytest.fixture(autouse=True)
# def stealth_context(context):
#     """
#     Inject a stealth script into every page before any other script runs.
#
#     automationexercise.com reads navigator.webdriver to detect automated
#     browsers and injects ad/interference scripts specifically for them.
#     This fixture masks the webdriver flag so the site treats Playwright
#     like a regular browser — matching the behaviour seen in manual testing.
#
#     The script is added via add_init_script() which runs before ANY page
#     script, so the site's detection code never sees webdriver = true.
#     """
#     context.add_init_script("""
#         // Hide the webdriver flag that identifies Playwright/Selenium
#         Object.defineProperty(navigator, 'webdriver', {
#             get: () => undefined,
#         });
#
#         // Remove the automation-specific chrome runtime marker
#         if (window.chrome) {
#             window.chrome.runtime = {};
#         }
#
#         // Spoof plugins array (empty in headless browsers, populated in real ones)
#         Object.defineProperty(navigator, 'plugins', {
#             get: () => [1, 2, 3, 4, 5],
#         });
#
#         // Spoof languages (headless often returns empty)
#         Object.defineProperty(navigator, 'languages', {
#             get: () => ['en-US', 'en'],
#         });
#     """)
#     yield

# ===========================================================================
# Page Object Fixtures (function-scoped — fresh instance per test)
# ===========================================================================

@pytest.fixture
def home_page(page: Page) -> HomePage:
    """Provide a ready-to-use HomePage instance."""
    return HomePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Provide a ready-to-use LoginPage instance."""
    return LoginPage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    """Provide a ready-to-use ProductsPage instance."""
    return ProductsPage(page)


@pytest.fixture
def product_detail_page(page: Page) -> ProductDetailPage:
    """Provide a ready-to-use ProductDetailPage instance."""
    return ProductDetailPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Provide a ready-to-use CartPage instance."""
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    """Provide a ready-to-use CheckoutPage instance."""
    return CheckoutPage(page)


@pytest.fixture
def contact_page(page: Page) -> ContactPage:
    """Provide a ready-to-use ContactPage instance."""
    return ContactPage(page)


# ===========================================================================
# State / Data Fixtures
# ===========================================================================

@pytest.fixture
def new_user_data() -> dict:
    """
    Generate a fresh set of registration form data for each test.

    Returns:
        dict: All fields required to register a new account.
    """
    return generate_registration_data()


@pytest.fixture
def test_card_data() -> dict:
    """
    Provide test credit card details for the payment form.

    Returns:
        dict: Card name, number, CVC, and expiry.
    """
    return generate_card_data()


@pytest.fixture
def logged_in_page(page: Page):
    """
    Fixture that logs in an existing test user before the test runs.

    Uses EXISTING_USER credentials from config. Tests using this fixture
    start with an authenticated session.

    Yields:
        Page: The Playwright Page object with an active user session.
    """
    from utils.config import get_existing_user
    login = LoginPage(page)
    login.open()
    EXISTING_USER = get_existing_user()
    login.login(EXISTING_USER.email, EXISTING_USER.password)
    # Verify login succeeded by waiting for the navbar indicator,
    # not a URL pattern — the URL check was unreliable when CSRF
    # caused the server to return 200 (stay on login page) instead of 302.
    #login.wait_for_visible(login.nav_logged_in_as)
    login.wait_for_visible(login.navbar.logged_in_as)
    yield page


@pytest.fixture
def product_in_cart(page: Page):
    """
    Fixture that adds a product to the cart before the test runs.

    Opens the products page, adds the first product to the cart,
    and dismisses the modal. Tests using this fixture start with
    at least one item already in the shopping cart.

    Yields:
        Page: The Playwright Page object with a product in the cart.
    """
    products = ProductsPage(page)
    products.open()
    products.add_product_to_cart(index=0)
    products.dismiss_modal_and_continue()
    yield page
