"""
pages/base_page_ae.py
------------------
Site-level base Page Object for automationexercise.com.

Inherits generic Playwright helpers from base.pwpo.basepage.BasePage and adds
elements and behaviours that are SHARED ACROSS EVERY PAGE of this site
(the navigation bar, login state indicator, ad dismissal, etc.).
the two shared UI components that appear on every page:


  - Navbar  → self.navbar   (top navigation bar)
  - Footer  → self.footer   (bottom subscription widget)

Individual page classes (HomePage, LoginPage, …) inherit from THIS class,
not from core.BasePage directly.

Inheritance chain:
    base.pwpo.base_page.BasePage                          (generic Playwright wrappers)
        └── pages.base_page.BasePage       (this file — site-wide shared UI)
                └── pages.home_page.HomePage  etc.
"""

import logging
from playwright.sync_api import Page, Locator

from base.pwpo.base_page import BasePage as CoreBasePage
from pages.components.navbar import Navbar
from pages.components.footer import Footer
from utils.config import TIMEOUTS, BASE_URL

logger = logging.getLogger(__name__)


class BasePage(CoreBasePage):
    """
    automationexercise.com — site-level base page.

    Every page on this site has:
      - self.navbar : Navbar  — top navigation bar
      - self.footer : Footer  — bottom subscription widget

    Page objects should delegate all navbar/footer interactions to these
    components instead of defining their own locators for shared elements.

    Example:
        class HomePage(BasePage):
            def go_to_cart(self):
                self.navbar.go_to_cart()   # ✅ use component

            def subscribe(self, email):
                self.footer.subscribe(email)  # ✅ use component
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page, timeout=TIMEOUTS.element)
        self.base_url = BASE_URL

        # Shared UI components — available in every page object
        self.navbar = Navbar(page)
        self.footer = Footer(page)

    # ------------------------------------------------------------------
    # Ad / Overlay Handling (site-specific)
    # ------------------------------------------------------------------

    def dismiss_ad_overlay(self) -> None:
        """
        Dismiss third-party ad overlays that appear on this site.

        Silently does nothing if no overlay is present.
        """
        try:
            close_btn = self.page.locator(
                "button:has-text('×'), .fc-close, [id*='dismiss'], [aria-label='Close']"
            )
            if close_btn.count() > 0:
                close_btn.first.click(timeout=3_000)
                logger.debug("Dismissed ad overlay")
        except Exception:
            pass

    def navigate_to(self, url: str, wait_until: str = "domcontentloaded") -> None:
        """
        Navigate to a URL, wait for DOM to be ready, then dismiss any ad overlay.

        Note: domcontentloaded is used (not networkidle) because ad scripts on
        this site never fully settle. Pages that require ad scripts to finish
        before interaction (e.g. LoginPage) implement their own wait via
        _wait_for_ad_then_dismiss().
        """
        super().navigate_to(url, wait_until)
        self.dismiss_ad_overlay()

    # ------------------------------------------------------------------
    # Convenience pass-throughs (optional — keeps existing test code working)
    # ------------------------------------------------------------------

    def is_logged_in(self) -> bool:
        """Convenience wrapper — delegates to self.navbar.is_logged_in()."""
        return self.navbar.is_logged_in()

    def logout(self) -> None:
        """Convenience wrapper — delegates to self.navbar.logout()."""
        self.navbar.logout()

    def go_to_home(self) -> None:
        self.navbar.go_to_home()

    def go_to_products(self) -> None:
        self.navbar.go_to_products()

    def go_to_cart(self) -> None:
        self.navbar.go_to_cart()

    def go_to_login(self) -> None:
        self.navbar.go_to_login()

    def go_to_contact(self) -> None:
        self.navbar.go_to_contact()
