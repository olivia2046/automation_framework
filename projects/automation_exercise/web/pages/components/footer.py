"""
pages/components/footer.py
--------------------------
Component Object for the footer section shared across every page of
automationexercise.com.

The footer contains:
  - Newsletter subscription widget
  - Copyright text

Usage (inside any page object):
    self.footer.subscribe("user@example.com")
    assert self.footer.is_subscription_successful()
"""

import logging
from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


class Footer:
    """
    Encapsulates all interactions with the page footer.

    This component is present at the bottom of every page on
    automationexercise.com. It is instantiated once inside BasePage
    and exposed as `self.footer`.

    Args:
        page: The Playwright Page instance passed down from the parent page.
    """

    def __init__(self, page: Page) -> None:
        self._page = page

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    @property
    def subscription_heading(self) -> Locator:
        """'Subscription' heading above the email input."""
        return self._page.locator("#footer h2", has_text="Subscription")

    @property
    def email_input(self) -> Locator:
        """Newsletter email input field."""
        return self._page.locator("#susbscribe_email")

    @property
    def subscribe_button(self) -> Locator:
        """Newsletter submit (arrow) button."""
        return self._page.locator("#subscribe")

    @property
    def success_alert(self) -> Locator:
        """Success message shown after a successful subscription."""
        return self._page.locator(".alert-success")

    @property
    def copyright_text(self) -> Locator:
        """Copyright notice at the very bottom of the page."""
        return self._page.locator("#footer .pull-left")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def scroll_into_view(self) -> None:
        """Scroll the page until the footer is visible."""
        self._page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.subscription_heading.wait_for(state="visible", timeout=5_000)

    def subscribe(self, email: str) -> None:
        """
        Enter an email address and submit the newsletter subscription form.

        Automatically scrolls to the footer first.

        Args:
            email: The email address to subscribe with.
        """
        logger.info(f"Footer: subscribing with {email}")
        self.scroll_into_view()
        self.email_input.fill(email)
        self.subscribe_button.click()

    def is_subscription_successful(self) -> bool:
        """
        Return True if the subscription success alert is visible.

        Returns:
            bool: True when the green success alert appears after subscribing.
        """
        return self.success_alert.is_visible()

    def get_copyright_text(self) -> str:
        """
        Return the copyright notice text.

        Returns:
            str: The copyright string displayed in the footer.
        """
        return self.copyright_text.inner_text().strip()
