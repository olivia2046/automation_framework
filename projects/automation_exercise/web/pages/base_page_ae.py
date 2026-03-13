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

    # # ------------------------------------------------------------------
    # # Ad / Overlay Handling (site-specific)
    # # ------------------------------------------------------------------
    #
    # def dismiss_ad_overlay(self) -> None:
    #     """
    #     Dismiss third-party ad overlays that appear on this site.
    #
    #     Silently does nothing if no overlay is present.
    #     """
    #     try:
    #         close_btn = self.page.locator(
    #             "button:has-text('×'), .fc-close, [id*='dismiss'], [aria-label='Close'], iframe>>"
    #         )
    #         if close_btn.count() > 0:
    #             close_btn.first.click(timeout=3_000)
    #             logger.debug("Dismissed ad overlay")
    #     except Exception:
    #         pass

    _AD_CLOSE_SELECTORS = [
        # "#dismiss-button",
        "[id*='dismiss']",
        "//*[@id='image-square']/div/div/a",
        "[aria-label='Close ad']",
        "[aria-label='Close']",
        ".btn.skip",
        ".fc-close",
        "button:has-text('×')",
        "button:has-text('Close')",

    ]

    def dismiss_ad_overlay(self) -> None:
        """
        Dismiss ad overlays that may appear in the main page or inside any iframe.

        Strategy
        --------
        1. Try each close-button selector in the main page DOM.
        2. If not found, iterate over every iframe and try each selector inside it.
        3. Stop as soon as one close button is successfully clicked.
        4. Silently do nothing if no overlay is found.

        This is intentionally generic — it does not assume a specific iframe id
        or ad network, so it works across different sites and ad providers.
        """
        # 1. Try main page first
        # if self._try_dismiss_in_frame(self.page):
        #     return

        # 2. Try every iframe on the page
        iframe_count = self.page.locator("iframe").count()
        for i in range(iframe_count):
            iframe = self.page.locator("iframe").nth(i)

            try:
                src = iframe.get_attribute("src") or ""
                id_ = iframe.get_attribute("id") or ""
                print(id)
                frame = self.page.frame_locator(f"iframe >> nth={i}")
                if self._try_dismiss_in_frame(frame):
                    logger.debug(f"Dismissed ad overlay in iframe[{i}] id={id_!r} src={src[:60]!r}")
                    return
            except Exception:
                continue

    def _try_dismiss_in_frame(self, frame) -> bool:
        """
        Try each ad close-button selector inside the given frame or page.

        Args:
            frame: A Playwright Page or FrameLocator to search within.

        Returns:
            True if a close button was found and clicked, False otherwise.
        """
        for selector in self._AD_CLOSE_SELECTORS:
            try:
                if frame.locator(selector).count() > 0: # need to click when there's element matched, otherwise it will pend forever
                    btn = frame.locator(selector).first
                    # btn.click(timeout=1_000)
                    btn.click()
                    logger.debug(f"Dismissed ad overlay using selector: {selector!r}")
                    return True
                else:
                    continue
            except Exception:
                continue
        return False

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
