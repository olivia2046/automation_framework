"""
test_contact.py
---------------
Test suite for the Contact Us page (/contact_us):
  - Page loads correctly
  - Successful form submission shows success message
  - Navigating home after submission works
"""

import pytest
from pages import ContactPage, HomePage


@pytest.mark.contact
class TestContactPage:
    """Tests covering the Contact Us form."""

    def test_contact_page_loads_correctly(self, contact_page):
        """
        Scenario: Opening /contact_us displays the 'Get In Touch' form.

        Expected: The page heading is visible.
        """
        contact_page.open()

        assert contact_page.is_loaded(), (
            "Expected 'Get In Touch' heading to be visible on the contact page"
        )

    def test_submit_contact_form_shows_success(self, contact_page):
        """
        Scenario: A user fills out and submits the contact form successfully.

        Steps:
          1. Open /contact_us.
          2. Fill in name, email, subject, and message.
          3. Submit the form (accept the browser confirmation dialog).
          4. Verify the success alert is shown.
        """
        contact_page.open()
        contact_page.submit_form(
            name="Test Automation User",
            email="testuser@example.com",
            subject="Automated Test Inquiry",
            message="This is a test message submitted by the automation framework. "
                    "Please disregard this message.",
        )
        #contact_page.page.pause()
        assert contact_page.is_submission_successful(), (
            "Expected a success alert after submitting the contact form"
        )

    def test_home_button_after_submission_navigates_home(self, page, contact_page):
        """
        Scenario: Clicking 'Home' after a successful submission goes to the homepage.

        Steps:
          1. Submit the contact form.
          2. Click the 'Home' button.
          3. Verify navigation to the homepage URL.
        """
        contact_page.open()
        contact_page.submit_form(
            name="Navigator Test",
            email="nav@example.com",
            subject="Navigation Test",
            message="Testing the post-submission Home navigation button.",
        )

        assert contact_page.is_submission_successful(), "Pre-condition: form must submit successfully"

        contact_page.go_home_after_submission()

        # Navigation to homepage is awaited inside go_home_after_submission().
        # Strip any fragment (e.g. #google_vignette) before asserting.
        current_url = page.url.split("#")[0].rstrip("/")
        # Todo: remove hardcode
        assert current_url.endswith("automationexercise.com"), (
            f"Expected to be on the homepage after clicking 'Home', got: {page.url}"
        )

    def test_contact_page_reachable_from_navbar(self, page, home_page):
        """
        Scenario: The Contact Us page is accessible via the 'Contact Us' navbar link.

        Steps:
          1. Open the homepage.
          2. Click 'Contact Us' in the navbar.
          3. Verify navigation to /contact_us.
        """
        home_page.open()

        contact_link = page.locator("a[href='/contact_us']")
        contact_link.click()

        assert "/contact_us" in page.url, (
            f"Expected URL to contain '/contact_us', got: {page.url}"
        )

        contact_page = ContactPage(page)
        assert contact_page.is_loaded(), (
            "Expected the contact page to load correctly after clicking navbar link"
        )
