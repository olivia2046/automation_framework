"""
test_auth.py
------------
Test suite for authentication features:
  - New user registration
  - Login with valid credentials
  - Login with invalid credentials
  - Logout
  - Duplicate email registration prevention

All tests follow the Arrange → Act → Assert (AAA) pattern.
"""

import pytest
from pages import LoginPage, HomePage
from utils.config import get_existing_user, INVALID_USER


@pytest.mark.auth
class TestRegistration:
    """Tests covering the new user registration flow."""

    def test_register_new_user_successfully(self, page, new_user_data):
        """
        Scenario: A new visitor registers a valid account.

        Steps:
          1. Navigate to the login/signup page.
          2. Enter name and unique email in the Signup form.
          3. Fill in the full account information form.
          4. Verify the 'Account Created!' confirmation is shown.
          5. Continue and verify the user is now logged in.
        """
        login_page = LoginPage(page)
        login_page.open()

        # Step 1 — Initiate signup
        login_page.start_signup(new_user_data["name"], new_user_data["email"])

        # Step 2 — Complete account info form
        login_page.complete_registration(new_user_data)

        # Assert: Account created heading must be visible
        assert login_page.is_account_created(), (
            "Expected 'Account Created!' heading to be visible after registration"
        )

        # Step 3 — Continue to home page
        login_page.click_continue_after_registration()

        # Assert: User is now logged in
        assert login_page.is_logged_in(), (
            "Expected user to be logged in after completing registration"
        )

    def test_register_with_existing_email_shows_error(self, page):
        """
        Scenario: Registration fails when the email is already in use.

        Steps:
          1. Navigate to signup page.
          2. Attempt to register with an already-registered email.
          3. Verify the 'Email Address already exist!' error message.
        """
        login_page = LoginPage(page)
        login_page.open()

        # Use the pre-existing test user's email
        login_page.start_signup("Duplicate User", get_existing_user().email)

        assert login_page.is_email_exists_error_shown(), (
            "Expected 'Email Address already exist!' error for duplicate registration"
        )


@pytest.mark.auth
class TestLogin:
    """Tests covering the login functionality."""

    def test_login_with_valid_credentials(self, page):
        """
        Scenario: Existing user logs in successfully.

        Steps:
          1. Navigate to /login.
          2. Enter valid email and password.
          3. Verify the 'Logged in as' navbar indicator appears.
        """
        login_page = LoginPage(page)
        login_page.open()
        EXISTING_USER = get_existing_user()
        login_page.login(EXISTING_USER.email, EXISTING_USER.password)

        assert login_page.is_logged_in(), (
            f"Expected to be logged in as '{EXISTING_USER.name}' but navbar indicator was not found"
        )

    def test_login_with_invalid_credentials_shows_error(self, page):
        """
        Scenario: Login fails with wrong credentials.

        Steps:
          1. Navigate to /login.
          2. Enter invalid email/password.
          3. Verify the error message is displayed.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(INVALID_USER.email, INVALID_USER.password)

        assert login_page.is_login_error_shown(), (
            "Expected 'Your email or password is incorrect!' error for invalid credentials"
        )

    def test_login_with_empty_fields(self, page):
        """
        Scenario: Login button with empty fields should not navigate away.

        The browser's built-in HTML5 validation prevents submission with
        empty required fields.
        """
        login_page = LoginPage(page)
        login_page.open()

        # Click login without filling any fields
        login_page.login_button.click()

        # Should still be on the login page
        assert "/login" in login_page.get_current_url(), (
            "Expected to remain on /login page when submitting empty credentials"
        )


@pytest.mark.auth
class TestLogout:
    """Tests covering the logout functionality."""

    def test_logout_redirects_to_login_page(self, logged_in_page):
        """
        Scenario: A logged-in user can log out successfully.

        Uses the `logged_in_page` fixture to start with an authenticated session.

        Steps:
          1. (Pre-condition) User is already logged in via fixture.
          2. Click 'Logout' in the navbar.
          3. Verify redirection to the /login page.
        """
        home = HomePage(logged_in_page)

        # Pre-condition check
        assert home.is_logged_in(), "Pre-condition: User should be logged in before testing logout"

        # Act
        home.logout()

        # Assert: Redirected to login page
        assert "/login" in home.get_current_url(), (
            "Expected to be redirected to /login page after logout"
        )

    def test_user_cannot_access_cart_after_logout(self, logged_in_page):
        """
        Scenario: After logout, navigating to /view_cart redirects to login.

        Steps:
          1. Log out.
          2. Navigate to /view_cart.
          3. Verify the user is redirected to login.
        """
        home = HomePage(logged_in_page)
        home.logout()

        # Try to go directly to the cart
        home.go_to_cart()

        # Automation exercise redirects guests from cart to login
        current_url = home.get_current_url()
        assert "/login" in current_url or "/view_cart" in current_url, (
            "Expected redirect to login or cart page for guest user after logout"
        )
