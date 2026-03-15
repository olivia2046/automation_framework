"""
product_detail_page.py
----------------------
Page Object for the individual Product Detail page (/product_details/<id>).

Covers viewing product info, selecting quantity, and adding the item to cart.
"""

import logging
from playwright.sync_api import Page, Locator

from pages.base_page_ae import BasePage

logger = logging.getLogger(__name__)


class ProductDetailPage(BasePage):
    """
    Page Object for a single product's detail view.

    Usage:
        detail = ProductDetailPage(page)
        detail.set_quantity(2)
        detail.add_to_cart()
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    @property
    def product_name(self) -> Locator:
        """The product name heading."""
        return self.page.locator(".product-information h2")

    @property
    def product_category(self) -> Locator:
        """Category label, e.g. 'Women > Dress'."""
        return self.page.locator(".product-information p", has_text="Category:")

    @property
    def product_price(self) -> Locator:
        """Price display element."""
        return self.page.locator(".product-information span span")

    @property
    def product_availability(self) -> Locator:
        """Availability text, e.g. 'In Stock'."""
        return self.page.locator(".product-information p", has_text="Availability:")

    @property
    def product_condition(self) -> Locator:
        """Condition text, e.g. 'New'."""
        return self.page.locator(".product-information p", has_text="Condition:")

    @property
    def product_brand(self) -> Locator:
        """Brand text, e.g. 'Polo'."""
        return self.page.locator(".product-information p", has_text="Brand:")

    @property
    def quantity_input(self) -> Locator:
        """Numeric quantity input field."""
        return self.page.locator("input#quantity")

    @property
    def add_to_cart_button(self) -> Locator:
        """'Add to cart' button on the detail page."""
        return self.page.locator("button:has-text('Add to cart')")

    @property
    def modal_added_heading(self) -> Locator:
        """'Added!' modal heading that confirms the item was added to the cart."""
        return self.page.locator(".modal-title", has_text="Added!")

    @property
    def modal_continue_btn(self) -> Locator:
        """'Continue Shopping' button inside the confirmation modal."""
        return self.page.locator("button:has-text('Continue Shopping')")

    @property
    def modal_view_cart_btn(self) -> Locator:
        """'View Cart' link inside the confirmation modal."""
        return self.page.locator(".modal-footer a:has-text('View Cart')")

    @property
    def product_image(self) -> Locator:
        """Main product image element."""
        return self.page.locator(".view-product img").first

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def is_loaded(self) -> bool:
        """
        Verify the product detail page has loaded correctly.

        Returns:
            bool: True if the product name and add-to-cart button are visible.
        """
        return self.product_name.is_visible() and self.add_to_cart_button.is_visible()

    def get_product_name(self) -> str:
        """Return the displayed product name text."""
        return self.get_text(self.product_name)

    def get_product_price(self) -> str:
        """Return the displayed product price text (e.g. 'Rs. 500')."""
        return self.get_text(self.product_price)

    def set_quantity(self, qty: int) -> None:
        """
        Set the product quantity in the numeric input.

        Args:
            qty: Desired quantity (positive integer).
        """
        logger.info(f"Setting quantity to: {qty}")
        #self.quantity_input.triple_click()
        self.quantity_input.clear()
        self.quantity_input.type(str(qty))

    def add_to_cart(self) -> None:
        """Click the 'Add to cart' button and wait for the modal to appear."""
        logger.info("Clicking 'Add to cart'")
        self.click(self.add_to_cart_button)
        self.wait_for_visible(self.modal_added_heading)

    def continue_shopping(self) -> None:
        """Dismiss the added-to-cart modal by clicking 'Continue Shopping'."""
        self.click(self.modal_continue_btn)

    def go_to_cart_from_modal(self) -> None:
        """Click 'View Cart' in the added-to-cart modal to navigate to the cart."""
        self.click(self.modal_view_cart_btn)

    def is_modal_visible(self) -> bool:
        """
        Check whether the 'Added!' confirmation modal is currently visible.

        Returns:
            bool: True if the modal heading is visible.
        """
        return self.modal_added_heading.is_visible()
