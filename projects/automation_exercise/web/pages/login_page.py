"""
login_page.py
-------------
Page Object for the Login & Registration page (/login).

The automationexercise.com login page contains two distinct forms:
  1. Login form  — for existing users
  2. Signup form — to start the registration flow (step 1 of 2)

This class handles both forms and the account info step that follows signup.
"""

import logging
from playwright.sync_api import Page, Locator

from pages import HomePage
from pages.base_page_ae import BasePage
from utils.config import URLS

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Page Object for /login — covers login, signup initiation, and
    the detailed account information form that follows new user signup.

    Usage:
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("user@example.com", "password")
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Locators — Login Form
    # ------------------------------------------------------------------

    @property
    def login_email_input(self) -> Locator:
        return self.page.locator("input[data-qa='login-email']")

    @property
    def login_password_input(self) -> Locator:
        return self.page.locator("input[data-qa='login-password']")

    @property
    def login_button(self) -> Locator:
        return self.page.locator("button[data-qa='login-button']")

    @property
    def login_error_message(self) -> Locator:
        """Error text shown when credentials are incorrect."""
        return self.page.locator("p:has-text('Your email or password is incorrect!')")

    # ------------------------------------------------------------------
    # Locators — Signup Form (step 1)
    # ------------------------------------------------------------------

    @property
    def signup_name_input(self) -> Locator:
        return self.page.locator("input[data-qa='signup-name']")

    @property
    def signup_email_input(self) -> Locator:
        return self.page.locator("input[data-qa='signup-email']")

    @property
    def signup_button(self) -> Locator:
        return self.page.locator("button[data-qa='signup-button']")

    @property
    def signup_error_message(self) -> Locator:
        """Error shown when trying to register an already-used email."""
        return self.page.locator("p:has-text('Email Address already exist!')")

    # ------------------------------------------------------------------
    # Locators — Account Info Form (step 2, after clicking signup)
    # ------------------------------------------------------------------

    @property
    def title_mr(self) -> Locator:
        return self.page.locator("#id_gender1")

    @property
    def title_mrs(self) -> Locator:
        return self.page.locator("#id_gender2")

    @property
    def account_password_input(self) -> Locator:
        return self.page.locator("input[data-qa='password']")

    @property
    def days_select(self) -> Locator:
        return self.page.locator("select[data-qa='days']")

    @property
    def months_select(self) -> Locator:
        return self.page.locator("select[data-qa='months']")

    @property
    def years_select(self) -> Locator:
        return self.page.locator("select[data-qa='years']")

    @property
    def newsletter_checkbox(self) -> Locator:
        return self.page.locator("#newsletter")

    @property
    def special_offers_checkbox(self) -> Locator:
        return self.page.locator("#optin")

    @property
    def first_name_input(self) -> Locator:
        return self.page.locator("input[data-qa='first_name']")

    @property
    def last_name_input(self) -> Locator:
        return self.page.locator("input[data-qa='last_name']")

    @property
    def address_input(self) -> Locator:
        return self.page.locator("input[data-qa='address']")

    @property
    def country_select(self) -> Locator:
        return self.page.locator("select[data-qa='country']")

    @property
    def state_input(self) -> Locator:
        return self.page.locator("input[data-qa='state']")

    @property
    def city_input(self) -> Locator:
        return self.page.locator("input[data-qa='city']")

    @property
    def zipcode_input(self) -> Locator:
        return self.page.locator("input[data-qa='zipcode']")

    @property
    def mobile_number_input(self) -> Locator:
        return self.page.locator("input[data-qa='mobile_number']")

    @property
    def create_account_button(self) -> Locator:
        return self.page.locator("button[data-qa='create-account']")

    @property
    def account_created_header(self) -> Locator:
        """'Account Created!' heading shown on successful registration."""
        return self.page.locator("h2[data-qa='account-created']")

    @property
    def continue_button(self) -> Locator:
        """'Continue' button on the account created confirmation page."""
        return self.page.locator("a[data-qa='continue-button']")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self) -> "LoginPage":
        """Navigate to the login page and wait for the form to be ready."""
        from playwright_stealth import stealth_sync
        stealth_sync(self.page)
        self.navigate_to(URLS["login"])
        self.wait_for_visible(self.login_email_input)
        return self

    def login(self, email: str, password: str) -> BasePage:
        """
        Submit the login form with the provided credentials.

        Why dispatchEvent instead of Playwright's click()
        --------------------------------------------------
        Playwright's click() injects a _hitTargetInterceptor listener on
        window (capture phase) for actionability checks. On this site this
        interceptor interferes with the form's submit event chain, causing
        the button click to have no effect.

        Dispatching a native MouseEvent directly bypasses Playwright's
        interception layer entirely — the event is indistinguishable from
        a real user click as far as the page's JS is concerned.

        Args:
            email: User's email address.
            password: User's password.
        """
        logger.info(f"Logging in with: {email}")
        self.wait_for_visible(self.login_email_input)
        self.fill(self.login_email_input, email)
        self.fill(self.login_password_input, password)

        # self.click(self.login_button, force=True)
        #with self.page.expect_navigation(wait_until="domcontentloaded", timeout=30_000):
            # self.page.evaluate("""
            #     document.querySelector('button[data-qa="login-button"]')
            #         .dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}))
            # """)
        #self.page.locator('form[action="/login"]').evaluate("node => node.submit()")
            # self.login_button.hover()
        self.click(self.login_button)
        return HomePage(self.page)



    def start_signup(self, name: str, email: str) -> None:
        """
        Fill in Step 1 of the signup flow (name + email) and submit.

        Uses dispatchEvent for the same reason as login().

        Args:
            name: Full name for the new account.
            email: Unique email address (must not already be registered).
        """
        logger.info(f"Starting signup for: {email}")
        self.fill(self.signup_name_input, name)
        self.fill(self.signup_email_input, email)

        # with self.page.expect_navigation(wait_until="domcontentloaded", timeout=30_000):
        #     self.page.evaluate("""
        #         document.querySelector('button[data-qa="signup-button"]')
        #             .dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}))
        #     """)
        self.click(self.signup_button)

    def complete_registration(self, user_data: dict) -> None:
        """
        Fill in the full account information form (Step 2 of signup).

        Args:
            user_data: Dictionary with the following keys:
                - title (str): 'Mr' or 'Mrs'
                - password (str)
                - first_name (str)
                - last_name (str)
                - address (str)
                - country (str)
                - state (str)
                - city (str)
                - zipcode (str)
                - mobile (str)
        """
        logger.info("Completing account registration form")

        # Title radio button
        if user_data.get("title") == "Mrs":
            self.click(self.title_mrs)
        else:
            self.click(self.title_mr)

        # Password
        self.fill(self.account_password_input, user_data["password"])

        # Date of birth (pick static test values)
        self.select_option(self.days_select, "15")
        self.select_option(self.months_select, "6")
        self.select_option(self.years_select, "1990")

        # Optional checkboxes
        if not self.newsletter_checkbox.is_checked():
            self.click(self.newsletter_checkbox)

        # Address details
        self.fill(self.first_name_input, user_data["first_name"])
        self.fill(self.last_name_input, user_data["last_name"])
        self.fill(self.address_input, user_data["address"])
        self.select_option(self.country_select, user_data["country"])
        self.fill(self.state_input, user_data["state"])
        self.fill(self.city_input, user_data["city"])
        self.fill(self.zipcode_input, user_data["zipcode"])
        self.fill(self.mobile_number_input, user_data["mobile"])

        self.click(self.create_account_button)

    def is_account_created(self) -> bool:
        """
        Verify that the account creation was successful.

        Returns:
            bool: True if 'Account Created!' heading is visible.
        """
        return self.account_created_header.is_visible()

    def click_continue_after_registration(self) -> None:
        """Click 'Continue' on the account-created confirmation page."""
        self.click(self.continue_button)

    def is_login_error_shown(self) -> bool:
        """Return True if the invalid-credentials error message is visible."""
        return self.login_error_message.is_visible()

    def is_email_exists_error_shown(self) -> bool:
        """Return True if the 'email already exists' error is visible."""
        return self.signup_error_message.is_visible()
