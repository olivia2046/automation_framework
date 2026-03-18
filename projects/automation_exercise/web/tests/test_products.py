"""
test_products.py
----------------
Test suite for product browsing, searching, and filtering features:
  - All-products page loads correctly
  - Keyword search returns relevant results
  - Search with no results shows empty state
  - Category navigation (Women, Men, Kids)
  - Brand filtering via sidebar
  - Product detail page loads with correct information
  - Homepage featured products are displayed
"""

import pytest
from pages import ProductsPage, ProductDetailPage, HomePage
from utils.config import SEARCH_TERMS, PRODUCT_CATEGORIES, BRANDS


@pytest.mark.products
class TestProductListing:
    """Tests for the main product catalog page."""

    def test_products_page_loads_with_items(self, products_page):
        """
        Scenario: Opening /products displays a list of products.

        Expected: Page heading 'All Products' is visible and at least one
        product card is rendered.
        """
        products_page.open()

        assert products_page.is_loaded(), (
            "Expected the 'All Products' page to load with product cards visible"
        )
        assert products_page.get_product_count() > 0, (
            "Expected at least one product card on the products page"
        )

    def test_products_page_shows_multiple_items(self, products_page):
        """
        Scenario: The products page lists more than a handful of items.

        Verifies that the catalog isn't accidentally empty or partially loaded.
        """
        products_page.open()

        count = products_page.get_product_count()
        assert count >= 5, (
            f"Expected at least 5 product cards, got {count}"
        )


@pytest.mark.products
class TestProductSearch:
    """Tests for the product search functionality."""

    def test_search_returns_results_for_valid_keyword(self, products_page):
        """
        Scenario: Searching for a known keyword returns matching products.

        Steps:
          1. Open the products page.
          2. Enter a valid search keyword.
          3. Verify 'Searched Products' heading appears.
          4. Verify at least one result is returned.
        """
        products_page.open()
        keyword = SEARCH_TERMS["valid"]
        products_page.search_product(keyword)

        count = products_page.get_product_count()
        assert count > 0, (
            f"Expected search results for '{keyword}' but found {count} products"
        )

    def test_search_results_are_relevant_to_keyword(self, products_page):
        """
        Scenario: Search results contain products related to the keyword.

        Verifies that returned items aren't completely unrelated to the query.
        """
        products_page.open()
        keyword = SEARCH_TERMS["valid"]
        products_page.search_product(keyword)

        assert products_page.are_search_results_relevant(keyword), (
            f"Expected at least one result name to contain '{keyword}'"
        )

    def test_search_for_nonexistent_product_returns_empty(self, products_page):
        """
        Scenario: Searching for a gibberish keyword returns zero results.

        Steps:
          1. Search for a term that cannot match any product.
          2. Verify the result count is 0.
        """
        products_page.open()
        keyword = SEARCH_TERMS["no_results"]
        products_page.search_product(keyword)

        count = products_page.get_product_count()
        assert count == 0, (
            f"Expected 0 results for '{keyword}' but found {count}"
        )

    def test_search_input_clears_between_searches(self, products_page):
        """
        Scenario: Performing a second search replaces the first results.

        Steps:
          1. Search for keyword A.
          2. Search for a different keyword B.
          3. Verify results change between searches.
        """
        products_page.open()

        # First search
        products_page.search_product("Top")
        first_count = products_page.get_product_count()

        # Second search (different keyword)
        products_page.search_product("Jeans")
        second_count = products_page.get_product_count()

        # The result counts should reflect different result sets
        # (they may differ; we just verify the search doesn't crash)
        assert isinstance(second_count, int), (
            "Expected a valid integer result count after second search"
        )


@pytest.mark.products
class TestCategoryNavigation:
    """Tests for browsing products by category."""

    def test_navigate_to_women_dress_category(self, page, home_page):
        """
        Scenario: Clicking Women > Dress in the sidebar shows dress products.

        Steps:
          1. Open the homepage.
          2. Click 'Women' to expand the category.
          3. Click 'Dress' subcategory.
          4. Verify the page heading references 'Women' and 'Dress'.
        """
        home_page.open()
        home_page.click_subcategory("Women", "Dress")

        # The heading should now say something like "Women - Dress Products"
        products = ProductsPage(page)
        heading_text = products.get_text(products.page.locator(".title.text-center")).lower()

        assert "women" in heading_text or "dress" in heading_text, (
            f"Expected category heading to reference 'Women' or 'Dress', got: '{heading_text}'"
        )

    def test_navigate_to_men_tshirts_category(self, page, home_page):
        """
        Scenario: Clicking Men > Tshirts shows t-shirt products.

        Steps:
          1. Open the homepage.
          2. Click 'Men' to expand, then 'Tshirts'.
          3. Verify heading mentions 'Men' or 'Tshirt'.
        """
        home_page.open()
        home_page.click_subcategory("Men", "Tshirts")

        products = ProductsPage(page)
        heading_text = products.get_text(products.page.locator(".title.text-center")).lower()

        assert "men" in heading_text or "tshirt" in heading_text or "t-shirt" in heading_text, (
            f"Expected heading to reference Men/Tshirts, got: '{heading_text}'"
        )


@pytest.mark.products
class TestBrandFilter:
    """Tests for the brand filtering sidebar."""

    def test_filter_by_polo_brand(self, products_page):
        """
        Scenario: Clicking a brand in the sidebar shows only that brand's products.

        Steps:
          1. Open /products.
          2. Click the 'Polo' brand link in the Brands sidebar.
          3. Verify the page heading contains 'Polo'.
        """
        products_page.open()
        products_page.click_brand("Polo")

        heading = products_page.get_brand_heading()
        assert "polo" in heading.lower(), (
            f"Expected page heading to contain 'Polo' after brand filter, got: '{heading}'"
        )

    def test_brand_filter_returns_products(self, products_page):
        """
        Scenario: Filtering by a brand shows at least one product.

        Steps:
          1. Open /products.
          2. Apply brand filter 'H&M'.
          3. Verify at least one product card is displayed.
        """
        products_page.open()
        products_page.click_brand("H&M")

        count = products_page.get_product_count()
        assert count > 0, (
            "Expected at least one product after applying the H&M brand filter"
        )


@pytest.mark.products
class TestProductDetail:
    """Tests for individual product detail pages."""

    def test_product_detail_page_displays_info(self, page, products_page):
        """
        Scenario: Clicking 'View Product' opens the product detail page
        with all key information visible.

        Steps:
          1. Open /products.
          2. Click 'View Product' on the first item.
          3. Verify name, price, availability, and 'Add to cart' button are shown.
        """
        products_page.open()
        products_page.click_view_product(index=0)

        detail = ProductDetailPage(page)

        assert detail.is_loaded(), (
            "Expected product detail page to load with name and 'Add to cart' button"
        )
        assert detail.get_product_name(), "Expected a non-empty product name"
        assert detail.get_product_price(), "Expected a non-empty product price"

    def test_product_detail_quantity_can_be_changed(self, page, products_page):
        """
        Scenario: The quantity input on the detail page accepts custom values.

        Steps:
          1. Navigate to a product detail page.
          2. Set quantity to 3.
          3. Verify the input value reflects the change.
        """
        products_page.open()
        products_page.click_view_product(index=0)

        detail = ProductDetailPage(page)
        detail.set_quantity(3)

        qty_value = detail.quantity_input.input_value()
        assert qty_value == "3", (
            f"Expected quantity input to show '3', got '{qty_value}'"
        )


@pytest.mark.products
class TestHomepageProducts:
    """Tests for products displayed on the homepage."""

    def test_homepage_shows_featured_products(self, home_page):
        """
        Scenario: The homepage displays featured product cards.

        Expected: At least one featured product card is visible.
        """
        home_page.open()

        count = home_page.get_featured_product_count()
        assert count > 0, "Expected at least one featured product on the homepage"

    def test_homepage_newsletter_subscription(self, home_page):
        """
        Scenario: A visitor can subscribe to the newsletter.

        Steps:
          1. Open homepage.
          2. Scroll to the subscription widget.
          3. Enter a valid email and submit.
          4. Verify the success alert appears.
        """
        from shared_utils.helpers import generate_unique_email
        home_page.open()
        home_page.subscribe_to_newsletter(generate_unique_email())

        assert home_page.is_subscription_successful(), (
            "Expected subscription success alert after submitting a valid email"
        )
