"""
test_checkout.py
----------------
Test suite for the checkout flow:
  - Logged-in user can complete checkout and place an order
  - Checkout page displays correct delivery address
  - Order summary shows the cart items
  - Guest user is prompted to login before checkout
  - Payment form accepts and submits card details
  - Order confirmation is shown after payment
"""
import time

import pytest
from playwright.sync_api import expect
from pages import ProductsPage, CartPage, CheckoutPage, LoginPage
from utils.config import EXISTING_USER


@pytest.mark.checkout
class TestCheckoutAsLoggedInUser:
    """End-to-end checkout tests for authenticated users."""

    def test_checkout_page_shows_delivery_address(self, page, product_in_cart):
        """
        Scenario: After login and proceeding to checkout, the delivery address
        is shown from the user's account.

        Steps:
          1. (Pre-condition) Product is in cart.
          2. Log in.
          3. Navigate to cart and proceed to checkout.
          4. Verify the delivery address section is visible.
        """
        # Login
        login_page = LoginPage(page)
        login_page.open()
        #time.sleep(30)
        home_page = login_page.login(EXISTING_USER.email, EXISTING_USER.password)



        #page.wait_for_url("**/", timeout=30000)
        #page.wait_for_url("**/automationexercise.com/*", timeout=30000)
        #page.wait_for_selector("li:has-text('Logged in as')", timeout=30000)
        #page.wait_for_selector("get_by_text('Logged in as TestAutomation')", timeout=30000)
        page.wait_for_selector("li:has-text('Logged in as')", timeout=30000)
        expect(home_page.navbar.logout_link).to_be_visible(timeout=30000)


        # Go to cart and checkout
        cart_page = CartPage(page)

        cart_page.open()

        #cart_page.pause()
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(page)

        assert checkout_page.is_on_checkout_page(), (
            "Expected to be on the checkout/address summary page"
        )
        address_text = checkout_page.get_delivery_address_text()
        assert address_text, "Expected delivery address section to contain text"

    def test_checkout_order_summary_contains_items(self, page, product_in_cart):
        """
        Scenario: The order summary at checkout shows the products from the cart.

        Steps:
          1. (Pre-condition) Product is in cart.
          2. Login, then proceed to checkout.
          3. Verify at least one item appears in the order summary table.
        """
        # Login
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(EXISTING_USER.email, EXISTING_USER.password)
        #page.wait_for_url("**/", timeout=30000)
        page.wait_for_selector("li:has-text('Logged in as')", timeout=30000)

        # Proceed to checkout
        cart_page = CartPage(page)
        cart_page.open()
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(page)
        item_count = checkout_page.get_order_item_count()

        assert item_count >= 1, (
            f"Expected at least 1 item in the order summary, found {item_count}"
        )

    def test_place_order_with_valid_payment(self, page, product_in_cart, test_card_data):
        """
        Scenario: A logged-in user completes a full checkout including payment.

        This is the primary end-to-end happy-path test.

        Steps:
          1. (Pre-condition) Product is in cart.
          2. Login as existing user.
          3. Go to cart → Proceed to Checkout.
          4. Enter an optional order comment.
          5. Click 'Place Order'.
          6. Fill in payment details.
          7. Confirm payment.
          8. Verify 'Order Placed!' success message.
        """
        # Step 1: Login
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(EXISTING_USER.email, EXISTING_USER.password)
        #page.wait_for_url("**/", timeout=30000)
        page.wait_for_selector("li:has-text('Logged in as')", timeout=30000)

        # Step 2: Go to cart
        cart_page = CartPage(page)
        cart_page.open()

        assert not cart_page.is_empty(), "Pre-condition: cart must not be empty"

        # Step 3: Proceed to checkout
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(page)
        assert checkout_page.is_on_checkout_page(), "Expected to reach checkout/address page"

        # Step 4: Add comment and place order
        checkout_page.enter_order_comment("Please deliver between 9am and 6pm.")
        checkout_page.click_place_order()

        # Step 5: Fill payment details
        checkout_page.fill_payment_details(test_card_data)

        # Step 6: Confirm
        checkout_page.confirm_payment()

        # Step 7: Verify success
        assert checkout_page.is_order_placed_successfully(), (
            "Expected 'Order Placed!' confirmation message after successful payment"
        )

    def test_checkout_with_comment_proceeds_normally(self, page, product_in_cart, test_card_data):
        """
        Scenario: Order comments do not interfere with the checkout flow.

        Steps:
          1. Login and proceed to checkout.
          2. Enter a long order comment.
          3. Complete the order.
          4. Verify success.
        """
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(EXISTING_USER.email, EXISTING_USER.password)

        #page.wait_for_url("**/", timeout=30000)
        page.wait_for_selector("li:has-text('Logged in as')", timeout=30000)

        cart_page = CartPage(page)
        cart_page.open()
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(page)
        long_comment = "This is a test order comment. " * 5  # ~150 chars
        checkout_page.enter_order_comment(long_comment)
        checkout_page.click_place_order()

        checkout_page.fill_payment_details(test_card_data)
        checkout_page.confirm_payment()

        assert checkout_page.is_order_placed_successfully(), (
            "Expected successful order placement even with a long order comment"
        )


@pytest.mark.checkout
class TestCheckoutAsGuestUser:
    """Tests for the checkout flow when the user is not logged in."""

    def test_guest_checkout_prompts_login_modal(self, page, product_in_cart):
        """
        Scenario: A guest user clicking 'Proceed To Checkout' sees a login modal.

        Steps:
          1. (Pre-condition) Product is in cart, user is NOT logged in.
          2. Open cart and click 'Proceed To Checkout'.
          3. Verify the login/register modal appears.
        """
        cart_page = CartPage(page)
        cart_page.open()
        cart_page.proceed_to_checkout()

        # The modal should appear for guests
        modal = page.locator("#checkoutModal")
        assert modal.is_visible(), (
            "Expected the 'Register / Login to proceed' modal for a guest user"
        )

    def test_guest_can_navigate_to_login_from_checkout_modal(self, page, product_in_cart):
        """
        Scenario: From the checkout modal, clicking 'Login' takes the guest to /login.

        Steps:
          1. (Pre-condition) Product in cart, user not logged in.
          2. Proceed to checkout.
          3. Click 'Login' inside the modal.
          4. Verify navigation to /login.
        """
        cart_page = CartPage(page)
        cart_page.open()
        cart_page.proceed_to_checkout()
        cart_page.click_login_from_checkout_modal()

        assert "/login" in page.url, (
            f"Expected to be navigated to /login, got: {page.url}"
        )
