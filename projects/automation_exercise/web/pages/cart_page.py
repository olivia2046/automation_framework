"""
cart_page.py
------------
Page Object for the Shopping Cart page (/view_cart).

Handles viewing cart items, removing products, verifying quantities,
and proceeding to checkout.
"""

import logging
from playwright.sync_api import Page, Locator

from pages.base_page_ae import BasePage
from utils.config import get_urls


logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """
    Page Object for /view_cart — the shopping cart.

    Usage:
        cart = CartPage(page)
        cart.open()
        assert cart.get_cart_item_count() > 0
        cart.proceed_to_checkout()
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    @property
    def cart_table(self) -> Locator:
        """The main cart items table."""
        return self.page.locator("#cart_info_table")

    @property
    def cart_rows(self) -> Locator:
        """Each product row inside the cart table body."""
        return self.page.locator("#cart_info_table tbody tr")

    @property
    def empty_cart_message(self) -> Locator:
        """Message shown when the cart contains no items."""
        return self.page.locator("#empty_cart")

    @property
    def proceed_to_checkout_btn(self) -> Locator:
        """'Proceed To Checkout' button at the bottom of the cart."""
        return self.page.locator("a.btn:has-text('Proceed To Checkout')")

    @property
    def login_to_checkout_modal(self) -> Locator:
        """Modal that appears when guest users click checkout."""
        return self.page.locator("#checkoutModal")

    @property
    def modal_login_link(self) -> Locator:
        """'Login' link inside the checkout modal for guest users."""
        return self.page.locator("#checkoutModal a:has-text('Login')")

    @property
    def modal_guest_checkout_btn(self) -> Locator:
        """'Continue On Cart' / 'Register / Login' button inside the checkout modal."""
        return self.page.locator("#checkoutModal .modal-footer a")

    # ------------------------------------------------------------------
    # Per-Row Locator Helpers
    # ------------------------------------------------------------------

    def get_row_by_index(self, index: int) -> Locator:
        """Return a cart row locator by its zero-based index."""
        return self.cart_rows.nth(index)

    def get_product_name_in_row(self, index: int) -> str:
        """
        Return the product name text for a specific cart row.

        Args:
            index: Zero-based row index.

        Returns:
            str: Product name string.
        """
        row = self.get_row_by_index(index)
        return row.locator("td.cart_description h4 a").inner_text().strip()

    def get_quantity_in_row(self, index: int) -> str:
        """
        Return the quantity text for a specific cart row.

        Args:
            index: Zero-based row index.

        Returns:
            str: Quantity as a string, e.g. '2'.
        """
        row = self.get_row_by_index(index)
        return row.locator("td.cart_quantity button").inner_text().strip()

    def get_price_in_row(self, index: int) -> str:
        """
        Return the unit price text for a specific cart row.

        Args:
            index: Zero-based row index.

        Returns:
            str: Price string, e.g. 'Rs. 500'.
        """
        row = self.get_row_by_index(index)
        return row.locator("td.cart_price p").inner_text().strip()

    def get_total_in_row(self, index: int) -> str:
        """
        Return the total price text for a specific cart row.

        Args:
            index: Zero-based row index.

        Returns:
            str: Total price string.
        """
        row = self.get_row_by_index(index)
        return row.locator("td.cart_total p").inner_text().strip()

    def get_delete_button_in_row(self, index: int) -> Locator:
        """Return the delete (×) button locator for a specific cart row."""
        row = self.get_row_by_index(index)
        return row.locator("td.cart_delete a")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self) -> "CartPage":
        """Navigate directly to the cart page."""
        URLS = get_urls()
        self.navigate_to(URLS["cart"])
        return self

    def is_loaded(self) -> bool:
        """
        Verify the cart page is loaded.

        Returns:
            bool: True if the cart table or empty cart message is visible.
        """
        return (self.cart_table.is_visible() or self.empty_cart_message.is_visible())

    def is_empty(self) -> bool:
        """
        Check if the cart is currently empty.

        Returns:
            bool: True when no cart rows are present.
        """
        return self.cart_rows.count() == 0

    def get_cart_item_count(self) -> int:
        """
        Count how many distinct items (rows) are in the cart.

        Returns:
            int: Number of cart rows.
        """
        return self.cart_rows.count()

    def remove_item(self, index: int = 0) -> None:
        """
        Remove a product from the cart by clicking its delete button.

        Args:
            index: Zero-based row index of the item to remove (default: 0).
        """
        logger.info(f"Removing cart item at index: {index}")
        delete_btn = self.get_delete_button_in_row(index)
        self.click(delete_btn)
        # Wait briefly for the row to disappear
        self.page.wait_for_timeout(1000)

    def proceed_to_checkout(self) -> None:
        """Click 'Proceed To Checkout' to initiate the checkout flow."""
        logger.info("Proceeding to checkout")
        self.click(self.proceed_to_checkout_btn)

    def click_login_from_checkout_modal(self) -> None:
        """
        When the 'Register / Login' modal appears during checkout (guest user),
        click the 'Login' link to go to the login page.
        """
        if self.login_to_checkout_modal.is_visible():
            self.click(self.modal_login_link)

    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Check whether a product with a given name exists in the cart.

        Args:
            product_name: The product name to look for (case-insensitive).

        Returns:
            bool: True if the product is found in any cart row.
        """
        for i in range(self.get_cart_item_count()):
            if product_name.lower() in self.get_product_name_in_row(i).lower():
                return True
        return False
