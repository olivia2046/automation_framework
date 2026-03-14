"""
pages/components/navbar.py
--------------------------
Component Object for the navigation bar shared across every page of
automationexercise.com.

Usage (inside any page object):
    self.navbar.go_to_cart()
    assert self.navbar.is_logged_in()
"""

import logging
from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


class Navbar:
    """
    Encapsulates all interactions with the top navigation bar.

    This component is present on every page of automationexercise.com.
    It is instantiated once inside BasePage and exposed as `self.navbar`
    so every page object can use it without duplicating locators.

    Args:
        page: The Playwright Page instance passed down from the parent page.
    """

    def __init__(self, page: Page) -> None:
        self._page = page

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    @property
    def home_link(self) -> Locator:
        return self._page.locator("a[href='/']").first

    @property
    def products_link(self) -> Locator:
        return self._page.locator("a[href='/products']")

    @property
    def cart_link(self) -> Locator:
        return self._page.locator("a[href='/view_cart']")

    @property
    def login_link(self) -> Locator:
        return self._page.locator("a[href='/login']")

    @property
    def logout_link(self) -> Locator:
        return self._page.locator("a[href='/logout']")

    @property
    def contact_link(self) -> Locator:
        return self._page.locator("a[href='/contact_us']")

    @property
    def about_link(self) -> Locator:
        return self._page.locator("a[href='/about_us']")

    @property
    def logged_in_as(self) -> Locator:
        """'Logged in as <username>' indicator."""
        return self._page.locator("li:has-text('Logged in as')")

    @property
    def username_text(self) -> Locator:
        """The <b> tag inside the logged-in indicator that holds the username."""
        return self._page.locator("li:has-text('Logged in as') b")

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def is_logged_in(self) -> bool:
        """Return True if a user is currently authenticated."""
        return self.logged_in_as.is_visible()

    def get_logged_in_username(self) -> str:
        """
        Return the username shown in the navbar.

        Returns:
            str: The username text, or empty string if not logged in.
        """
        if self.is_logged_in():
            return self.username_text.inner_text().strip()
        return ""

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def go_to_home(self) -> None:
        logger.info("Navbar: navigating to Home")
        self.home_link.click()

    def go_to_products(self) -> None:
        logger.info("Navbar: navigating to Products")
        self.products_link.click()

    def go_to_cart(self) -> None:
        logger.info("Navbar: navigating to Cart")
        self.cart_link.click()

    def go_to_login(self) -> None:
        logger.info("Navbar: navigating to Login")
        self.login_link.click()

    def go_to_contact(self) -> None:
        logger.info("Navbar: navigating to Contact Us")
        self.contact_link.click()

    def go_to_about(self) -> None:
        logger.info("Navbar: navigating to About Us")
        self.about_link.click()

    def logout(self) -> None:
        logger.info("Navbar: clicking Logout")
        self.logout_link.click()
