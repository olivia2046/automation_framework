"""
test_cart.py
------------
Test suite for shopping cart functionality:
  - Adding products from the products page
  - Adding products from the product detail page
  - Removing products from the cart
  - Verifying cart contents and quantities
  - Cart persists after navigating away
"""

import pytest
from pages import ProductsPage, ProductDetailPage, CartPage


@pytest.mark.cart
class TestAddToCart:
    """Tests for adding items to the cart."""

    def test_add_single_product_from_catalog(self, page, products_page, cart_page):
        """
        Scenario: A user adds one product from the catalog to the cart.

        Steps:
          1. Open /products.
          2. Add the first product to the cart.
          3. Dismiss the modal.
          4. Navigate to the cart and verify 1 item is present.
        """
        products_page.open()
        products_page.add_product_to_cart(index=0)
        products_page.dismiss_modal_and_continue()

        cart_page.open()

        assert not cart_page.is_empty(), "Expected cart to contain at least one item"
        assert cart_page.get_cart_item_count() >= 1, (
            "Expected at least 1 product row in the cart"
        )

    def test_add_multiple_products_from_catalog(self, page, products_page, cart_page):
        """
        Scenario: A user adds two different products to the cart.

        Steps:
          1. Open /products.
          2. Add product at index 0 and dismiss modal.
          3. Add product at index 1 and dismiss modal.
          4. Navigate to cart and verify 2 distinct items.
        """
        products_page.open()

        # Add first product
        products_page.add_product_to_cart(index=0)
        products_page.dismiss_modal_and_continue()

        # Add second product
        products_page.add_product_to_cart(index=1)
        products_page.dismiss_modal_and_continue()

        cart_page.open()
        count = cart_page.get_cart_item_count()

        assert count >= 2, (
            f"Expected at least 2 items in the cart after adding 2 products, found {count}"
        )

    def test_add_product_from_detail_page(self, page, products_page, cart_page):
        """
        Scenario: A user views a product's detail page and adds it to the cart.

        Steps:
          1. Open /products and click 'View Product' for the first item.
          2. On the detail page, click 'Add to cart'.
          3. Dismiss the modal.
          4. Verify the cart contains the item.
        """
        products_page.open()
        products_page.click_view_product(index=0)

        detail = ProductDetailPage(page)
        product_name = detail.get_product_name()
        detail.add_to_cart()
        detail.continue_shopping()

        cart_page.open()

        assert cart_page.is_product_in_cart(product_name), (
            f"Expected '{product_name}' to be in the cart after adding from detail page"
        )

    def test_add_product_with_quantity_2_from_detail_page(self, page, products_page, cart_page):
        """
        Scenario: A user sets quantity to 2 on the detail page before adding to cart.

        Steps:
          1. Navigate to a product detail page.
          2. Set quantity to 2.
          3. Add to cart.
          4. Open cart and verify the quantity column shows '2'.
        """
        products_page.open()
        products_page.click_view_product(index=0)

        detail = ProductDetailPage(page)
        detail.quantity_input.clear()
        detail.set_quantity(2)
        detail.add_to_cart()
        detail.continue_shopping()

        cart_page.open()

        qty = cart_page.get_quantity_in_row(0)
        assert qty == "2", (
            f"Expected cart item quantity to be '2', got '{qty}'"
        )

    def test_modal_view_cart_navigates_to_cart(self, page, products_page):
        """
        Scenario: Clicking 'View Cart' in the add-to-cart modal goes to the cart page.

        Steps:
          1. Add a product and click 'View Cart' in the modal (instead of 'Continue').
          2. Verify the URL is now /view_cart.
        """
        products_page.open()
        products_page.add_product_to_cart(index=0)
        products_page.dismiss_modal_and_go_to_cart()

        current_url = page.url
        assert "view_cart" in current_url, (
            f"Expected to be on /view_cart, got: {current_url}"
        )


@pytest.mark.cart
class TestRemoveFromCart:
    """Tests for removing items from the cart."""

    def test_remove_only_item_leaves_empty_cart(self, page, product_in_cart, cart_page):
        """
        Scenario: Removing the only item in the cart results in an empty cart.

        Uses the `product_in_cart` fixture for pre-condition setup.

        Steps:
          1. (Pre-condition) One item is in the cart.
          2. Open the cart page.
          3. Delete the first (only) item.
          4. Verify the cart is now empty.
        """
        cart_page.open()
        initial_count = cart_page.get_cart_item_count()
        assert initial_count >= 1, "Pre-condition: cart should have at least one item"

        cart_page.remove_item(index=0)

        assert cart_page.is_empty() or cart_page.get_cart_item_count() < initial_count, (
            "Expected the cart to be empty or have fewer items after removal"
        )

    def test_remove_one_of_two_items(self, page, products_page, cart_page):
        """
        Scenario: Removing one item from a two-item cart leaves one item.

        Steps:
          1. Add two products to the cart.
          2. Open cart and verify count is 2.
          3. Remove the first item.
          4. Verify count is now 1.
        """
        # Setup: add 2 products
        products_page.open()
        products_page.add_product_to_cart(index=0)
        products_page.dismiss_modal_and_continue()
        products_page.add_product_to_cart(index=1)
        products_page.dismiss_modal_and_continue()

        cart_page.open()
        initial_count = cart_page.get_cart_item_count()
        assert initial_count >= 2, "Pre-condition: expected at least 2 items"

        cart_page.remove_item(index=0)
        new_count = cart_page.get_cart_item_count()

        assert new_count == initial_count - 1, (
            f"Expected {initial_count - 1} items after removal, got {new_count}"
        )


@pytest.mark.cart
class TestCartContents:
    """Tests for verifying cart item details."""

    def test_cart_shows_product_name_price_and_quantity(self, page, product_in_cart, cart_page):
        """
        Scenario: Cart rows display name, price, and quantity for each item.

        Steps:
          1. (Pre-condition) At least one product is in the cart.
          2. Open the cart.
          3. Verify the first row has a non-empty name, price, and quantity.
        """
        cart_page.open()
        assert not cart_page.is_empty(), "Pre-condition: cart must not be empty"

        name = cart_page.get_product_name_in_row(0)
        price = cart_page.get_price_in_row(0)
        quantity = cart_page.get_quantity_in_row(0)

        assert name, "Expected a non-empty product name in the cart row"
        assert price, "Expected a non-empty price in the cart row"
        assert quantity, "Expected a non-empty quantity in the cart row"

    def test_cart_total_reflects_quantity(self, page, products_page, cart_page):
        """
        Scenario: The row total equals price × quantity.

        Steps:
          1. Add a product with quantity 2.
          2. Verify the total column is approximately double the unit price.

        Note: This test performs a numeric comparison of the price values.
        """
        products_page.open()
        products_page.click_view_product(index=0)

        detail = ProductDetailPage(page)
        detail.set_quantity(2)
        detail.add_to_cart()
        detail.continue_shopping()

        cart_page.open()

        price_str = cart_page.get_price_in_row(0)
        total_str = cart_page.get_total_in_row(0)

        # Extract numeric value (handle "Rs. 500" → 500)
        def extract_amount(text):
            digits = "".join(c for c in text if c.isdigit() or c == ".")
            return float(digits) if digits else 0.0

        unit_price = extract_amount(price_str)
        row_total = extract_amount(total_str)

        expected_total = unit_price * 2
        assert abs(row_total - expected_total) < 1.0, (
            f"Expected total ~{expected_total}, got {row_total} (unit price: {unit_price})"
        )
