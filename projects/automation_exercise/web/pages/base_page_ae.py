"""
pages/base_page_ae.py
------------------
Site-level base Page Object for automationexercise.com.

Inherits all generic Playwright helpers from core.BasePage and adds
elements and behaviours that are SHARED ACROSS EVERY PAGE of this site
(the navigation bar, login state indicator, ad dismissal, etc.).

Individual page classes (HomePage, LoginPage, …) inherit from THIS class,
not from core.BasePage directly.

Inheritance chain:
    core.BasePage                          (generic Playwright wrappers)
        └── pages.base_page.BasePage       (this file — site-wide shared UI)
                └── pages.home_page.HomePage  etc.
"""

import logging
from playwright.sync_api import Page, Locator

from base.pwpo.base_page import BasePage as CoreBasePage
from utils.config import TIMEOUTS, BASE_URL

logger = logging.getLogger(__name__)


class BasePage(CoreBasePage):
    """
    automationexercise.com — site-level base page.

    Adds:
    - Site base URL from project config.
    - Navbar locators (Home, Products, Cart, Login, Logout, Logged-in indicator).
    - Convenience navigation methods that use the navbar.
    - Ad/overlay dismissal helper specific to this site.
    """

    def __init__(self, page: Page) -> None:
        # Pass this site's configured timeout to the generic parent.
        super().__init__(page, timeout=TIMEOUTS.element)
        self.base_url = BASE_URL

    # ------------------------------------------------------------------
    # Ad / Overlay Handling (site-specific)
    # ------------------------------------------------------------------

    def dismiss_ad_overlay(self) -> None:
        """
        Dismiss the third-party ad overlays that appear on this site.

        automationexercise.com serves ads that can intercept clicks.
        This method silently closes any visible overlay — if none is
        present, it does nothing.
        """
        try:
            close_btn = self.page.locator(
                "button:has-text('×'), .fc-close, [id*='dismiss'], [aria-label='Close']"
            )
            if close_btn.count() > 0:
                close_btn.first.click(timeout=3_000)
                logger.debug("Dismissed ad overlay")
        except Exception:
            pass  # No overlay present — continue normally

    def navigate_to(self, url: str, wait_until: str = "domcontentloaded") -> None:
        """
        Navigate to a URL and automatically dismiss any ad overlay afterwards.

        Overrides core.BasePage.navigate_to to inject the site-specific
        ad-dismissal step without requiring every page object to call it
        manually.
        """
        super().navigate_to(url, wait_until)
        self.dismiss_ad_overlay()

    # ------------------------------------------------------------------
    # Navbar Locators
    # ------------------------------------------------------------------

    @property
    def nav_home(self) -> Locator:
        """Navbar 'Home' link."""
        return self.page.locator("a[href='/']").first

    @property
    def nav_products(self) -> Locator:
        """Navbar 'Products' link."""
        return self.page.locator("a[href='/products']")

    @property
    def nav_cart(self) -> Locator:
        """Navbar 'Cart' link."""
        return self.page.locator("a[href='/view_cart']")

    @property
    def nav_login(self) -> Locator:
        """Navbar 'Signup / Login' link."""
        return self.page.locator("a[href='/login']")

    @property
    def nav_logout(self) -> Locator:
        """Navbar 'Logout' link."""
        return self.page.locator("a[href='/logout']")

    @property
    def nav_contact(self) -> Locator:
        """Navbar 'Contact Us' link."""
        return self.page.locator("a[href='/contact_us']")

    @property
    def nav_logged_in_as(self) -> Locator:
        """'Logged in as <username>' indicator in the navbar."""
        return self.page.locator("li:has-text('Logged in as')")

    # ------------------------------------------------------------------
    # Auth State
    # ------------------------------------------------------------------

    def is_logged_in(self) -> bool:
        """
        Return True if the current session has an authenticated user.

        Detected via the 'Logged in as …' text that this site renders
        in the navbar when a user is signed in.
        """
        return self.nav_logged_in_as.is_visible()

    # ------------------------------------------------------------------
    # Navbar Navigation Helpers
    # ------------------------------------------------------------------

    def go_to_home(self) -> None:
        """Click the Home link in the navbar."""
        self.click(self.nav_home)

    def go_to_products(self) -> None:
        """Click the Products link in the navbar."""
        self.click(self.nav_products)

    def go_to_cart(self) -> None:
        """Click the Cart link in the navbar."""
        self.click(self.nav_cart)

    def go_to_login(self) -> None:
        """Click the Signup / Login link in the navbar."""
        self.click(self.nav_login)

    def go_to_contact(self) -> None:
        """Click the Contact Us link in the navbar."""
        self.click(self.nav_contact)

    def logout(self) -> None:
        """Click the Logout link in the navbar."""
        self.click(self.nav_logout)
