"""
checkout_page.py
----------------
Page Object for the Checkout page (/checkout).

Handles address verification, order comments, and the payment form.
The payment confirmation step is also handled here.
"""

import logging
from playwright.sync_api import Page, Locator

from pages.base_page_ae import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """
    Page Object for the /checkout flow.

    The checkout is split into two views in the application:
      1. Address & order summary — /checkout
      2. Payment — /payment

    Both are covered by this single class.

    Usage:
        checkout = CheckoutPage(page)
        checkout.enter_order_comment("Please deliver fast")
        checkout.click_place_order()
        checkout.fill_payment_details(card_data)
        checkout.confirm_payment()
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Locators — Address & Order Summary
    # ------------------------------------------------------------------

    @property
    def delivery_address_section(self) -> Locator:
        """Delivery address block shown at checkout."""
        return self.page.locator("#address_delivery")

    @property
    def billing_address_section(self) -> Locator:
        """Billing address block shown at checkout."""
        return self.page.locator("#address_invoice")

    @property
    def order_comment_textarea(self) -> Locator:
        """Text area for adding a note to the order."""
        return self.page.locator("textarea.form-control", has_text="")

    @property
    def place_order_btn(self) -> Locator:
        """'Place Order' button on the checkout summary page."""
        return self.page.locator("a:has-text('Place Order')")

    @property
    def cart_items_in_checkout(self) -> Locator:
        """Cart product rows listed in the order summary table."""
        return self.page.locator("#cart_info tbody tr")

    # ------------------------------------------------------------------
    # Locators — Payment Form
    # ------------------------------------------------------------------

    @property
    def card_name_input(self) -> Locator:
        """Name on card input."""
        return self.page.locator("input[data-qa='name-on-card']")

    @property
    def card_number_input(self) -> Locator:
        """Card number input."""
        return self.page.locator("input[data-qa='card-number']")

    @property
    def card_cvc_input(self) -> Locator:
        """CVC / CVV input."""
        return self.page.locator("input[data-qa='cvc']")

    @property
    def card_expiry_month_input(self) -> Locator:
        """Expiry month input (MM)."""
        return self.page.locator("input[data-qa='expiry-month']")

    @property
    def card_expiry_year_input(self) -> Locator:
        """Expiry year input (YYYY)."""
        return self.page.locator("input[data-qa='expiry-year']")

    @property
    def pay_and_confirm_btn(self) -> Locator:
        """'Pay and Confirm Order' submit button."""
        return self.page.locator("button[data-qa='pay-button']")

    # ------------------------------------------------------------------
    # Locators — Order Confirmation
    # ------------------------------------------------------------------

    @property
    def order_success_message(self) -> Locator:
        """Success message shown after an order is placed successfully."""
        return self.page.locator("[data-qa='order-placed'], .order-placed, h2.title:has-text('Order Placed!')")

    @property
    def continue_btn_after_order(self) -> Locator:
        """'Continue' button on the order confirmation page."""
        return self.page.locator("a[data-qa='continue-button']")

    @property
    def download_invoice_btn(self) -> Locator:
        """'Download Invoice' link on the order confirmation page."""
        return self.page.locator("a.btn:has-text('Download Invoice')")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def is_on_checkout_page(self) -> bool:
        """
        Verify the page is on the checkout/address summary step.

        Returns:
            bool: True if the delivery address section is visible.
        """
        return self.delivery_address_section.is_visible()

    def get_delivery_address_text(self) -> str:
        """
        Return the full text of the delivery address block.

        Returns:
            str: Delivery address lines as a single string.
        """
        return self.get_text(self.delivery_address_section)

    def get_order_item_count(self) -> int:
        """
        Count the number of product lines in the checkout order summary.

        Returns:
            int: Number of product rows.
        """
        return self.cart_items_in_checkout.count()

    def enter_order_comment(self, comment: str) -> None:
        """
        Type an optional message/note in the order comment textarea.

        Args:
            comment: The comment or delivery instruction text.
        """
        logger.info(f"Entering order comment: '{comment}'")
        self.fill(self.order_comment_textarea, comment)

    def click_place_order(self) -> None:
        """Click 'Place Order' to proceed from the summary to the payment form."""
        logger.info("Clicking 'Place Order'")
        self.click(self.place_order_btn)

    def fill_payment_details(self, card_data: dict) -> None:
        """
        Fill in the payment form fields.

        Args:
            card_data: Dictionary with keys:
                - name (str): Name on card.
                - number (str): Card number.
                - cvc (str): CVC/CVV code.
                - expiry_month (str): Expiry month (MM).
                - expiry_year (str): Expiry year (YYYY).
        """
        logger.info("Filling payment details")
        self.fill(self.card_name_input, card_data["name"])
        self.fill(self.card_number_input, card_data["number"])
        self.fill(self.card_cvc_input, card_data["cvc"])
        self.fill(self.card_expiry_month_input, card_data["expiry_month"])
        self.fill(self.card_expiry_year_input, card_data["expiry_year"])

    def confirm_payment(self) -> None:
        """Click 'Pay and Confirm Order' to submit the payment form."""
        logger.info("Confirming payment")
        self.click(self.pay_and_confirm_btn)

    def is_order_placed_successfully(self) -> bool:
        """
        Verify whether the order was placed successfully.

        Returns:
            bool: True if the order success confirmation is visible.
        """
        try:
            self.wait_for_visible(self.order_success_message)
            return self.order_success_message.is_visible()
        except Exception:
            return False

    def click_continue_after_order(self) -> None:
        """Click 'Continue' on the post-order confirmation screen."""
        self.click(self.continue_btn_after_order)

    def download_invoice(self) -> None:
        """Click 'Download Invoice' on the confirmation page."""
        self.click(self.download_invoice_btn)
