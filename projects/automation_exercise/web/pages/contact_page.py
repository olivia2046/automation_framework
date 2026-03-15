"""
contact_page.py
---------------
Page Object for the Contact Us page (/contact_us).

Covers filling out and submitting the contact form.
"""

import logging
from playwright.sync_api import Page, Locator

from pages.base_page_ae import BasePage
from utils.config import get_urls


logger = logging.getLogger(__name__)


class ContactPage(BasePage):
    """
    Page Object for /contact_us — the contact form.

    Usage:
        contact = ContactPage(page)
        contact.open()
        contact.submit_form("John", "john@example.com", "Hello!", "Need help")
        assert contact.is_submission_successful()
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    @property
    def page_heading(self) -> Locator:
        """'Get In Touch' heading at the top of the page."""
        return self.page.locator(".contact-form h2", has_text="Get In Touch")

    @property
    def name_input(self) -> Locator:
        return self.page.locator("input[data-qa='name']")

    @property
    def email_input(self) -> Locator:
        return self.page.locator("input[data-qa='email']")

    @property
    def subject_input(self) -> Locator:
        return self.page.locator("input[data-qa='subject']")

    @property
    def message_textarea(self) -> Locator:
        return self.page.locator("textarea[data-qa='message']")

    @property
    def file_upload_input(self) -> Locator:
        """File attachment input (optional)."""
        return self.page.locator("input[name='upload_file']")

    @property
    def submit_button(self) -> Locator:
        return self.page.locator("input[data-qa='submit-button']")

    @property
    def success_alert(self) -> Locator:
        """Success alert shown after the form is submitted."""
        return self.page.locator(".contact-form>.alert-success")

    @property
    def home_button(self) -> Locator:
        """'Home' button that appears after a successful submission."""
        return self.page.locator("a.btn:has-text('Home')")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self) -> "ContactPage":
        """Navigate to the contact page."""
        URLS = get_urls()
        self.navigate_to(URLS["contact"])
        return self

    def is_loaded(self) -> bool:
        """
        Verify the contact page has loaded.

        Returns:
            bool: True if the 'Get In Touch' heading is visible.
        """
        return self.page_heading.is_visible()

    def submit_form(
        self,
        name: str,
        email: str,
        subject: str,
        message: str,
    ) -> None:
        """
        Fill in and submit the contact form.

        Args:
            name: Sender's full name.
            email: Sender's email address.
            subject: Message subject.
            message: Body of the message.
        """
        logger.info(f"Submitting contact form from: {name} <{email}>")
        self.fill(self.name_input, name)
        self.fill(self.email_input, email)
        self.fill(self.subject_input, subject)
        self.fill(self.message_textarea, message)

        # Handle browser confirm dialog that fires on submit
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self.submit_button)

    def is_submission_successful(self) -> bool:
        """
        Check whether the form submission succeeded.

        Returns:
            bool: True if the success alert is visible after submission.
        """
        return self.success_alert.is_visible()

    def go_home_after_submission(self) -> None:
        """
        Click the 'Home' button on the post-submission confirmation page
        and wait until the homepage is fully loaded.

        On automationexercise.com, clicking Home triggers a Google ad overlay
        (google_vignette) before the navigation completes, changing the URL to
        /contact_us#google_vignette. The ad must be dismissed first, then we
        wait for the actual navigation to the homepage to complete.
        """
        self.click(self.home_button)

        # Dismiss the Google vignette ad that appears before navigation
        self.dismiss_ad_overlay()

        #self.page.pause()
        # Wait for navigation to homepage to complete
        self.page.wait_for_url("**/", timeout=30_000)
