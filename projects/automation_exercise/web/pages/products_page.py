"""
products_page.py
----------------
Page Object for the Products listing page (/products) and search results.

Handles product browsing, keyword search, category/brand filtering,
and navigating to individual product detail pages.
"""

import logging
from playwright.sync_api import Page, Locator

from pages.base_page_ae import BasePage
from utils.config import get_urls


logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    """
    Page Object for /products — product catalog, search, and filters.

    Usage:
        products_page = ProductsPage(page)
        products_page.open()
        products_page.search_product("Dress")
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Locators — Page Structure
    # ------------------------------------------------------------------

    @property
    def page_heading(self) -> Locator:
        """'All Products' heading at the top of the catalog."""
        return self.page.locator(".title.text-center", has_text="All Products")

    @property
    def search_input(self) -> Locator:
        """Keyword search input field."""
        return self.page.locator("input#search_product")

    @property
    def search_button(self) -> Locator:
        """Search submit button (magnifying glass icon)."""
        return self.page.locator("button#submit_search")

    @property
    def search_results_heading(self) -> Locator:
        """'Searched Products' heading that appears after a search."""
        return self.page.locator(".title.text-center", has_text="Searched Products")

    @property
    def product_cards(self) -> Locator:
        """All product-image-wrapper cards in the current listing."""
        return self.page.locator(".features_items .product-image-wrapper")

    @property
    def product_names(self) -> Locator:
        """The <p> name label inside each product card."""
        return self.page.locator(".features_items .productinfo p")

    @property
    def brand_sidebar(self) -> Locator:
        """The Brands panel in the left sidebar."""
        return self.page.locator(".brands_products")

    @property
    def category_women_link(self) -> Locator:
        """'Women' category toggle in the sidebar."""
        return self.page.locator("a[href='#Women']")

    @property
    def category_heading(self) -> Locator:
        """Heading that shows the active category name, e.g. 'Women - Dress Products'."""
        return self.page.locator(".title.text-center")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self) -> "ProductsPage":
        """Navigate to the all-products page."""
        URLS = get_urls()
        self.navigate_to(URLS["products"])
        return self

    def is_loaded(self) -> bool:
        """
        Verify the products page is fully loaded.

        Returns:
            bool: True if the heading and at least one product card are visible.
        """
        return self.page_heading.is_visible() and self.product_cards.count() > 0

    def search_product(self, keyword: str) -> None:
        """
        Enter a keyword in the search box and submit.

        Args:
            keyword: Search term to enter.
        """
        logger.info(f"Searching for product: '{keyword}'")
        self.fill(self.search_input, keyword)
        self.click(self.search_button)
        self.wait_for_visible(self.search_results_heading)

    def get_product_count(self) -> int:
        """
        Count the product cards currently visible.

        Returns:
            int: Number of product cards in the listing.
        """
        return self.product_cards.count()

    def get_all_product_names(self) -> list[str]:
        """
        Collect the name text from every product card in the listing.

        Returns:
            list[str]: List of product name strings.
        """
        return [self.product_names.nth(i).inner_text().strip()
                for i in range(self.product_names.count())]

    def click_view_product(self, index: int = 0) -> None:
        """
        Click the 'View Product' link for a product at the given index.

        Args:
            index: Zero-based index of the product card to click (default: 0).
        """
        logger.info(f"Opening product detail for index: {index}")
        card = self.product_cards.nth(index)
        view_link = card.locator("a[href*='product_details']")
        self.click(view_link)

    def add_product_to_cart(self, index: int = 0) -> None:
        """
        Hover a product card and click its 'Add to cart' button.

        Args:
            index: Zero-based index of the product card.
        """
        logger.info(f"Adding product at index {index} to cart")
        card = self.product_cards.nth(index)
        card.hover()
        add_btn = card.locator(".add-to-cart").first
        self.click(add_btn)

    def dismiss_modal_and_continue(self) -> None:
        """
        Click 'Continue Shopping' in the 'Added to cart' modal dialog.

        The modal appears after every 'Add to cart' action.
        """
        continue_btn = self.page.locator("button:has-text('Continue Shopping')")
        if continue_btn.is_visible():
            self.click(continue_btn)

    def dismiss_modal_and_go_to_cart(self) -> None:
        """
        Click 'View Cart' in the 'Added to cart' modal dialog to go straight
        to the cart page.
        """
        view_cart_btn = self.page.locator("a:has-text('View Cart')")
        if view_cart_btn.is_visible():
            self.click(view_cart_btn)

    def click_brand(self, brand_name: str) -> None:
        """
        Click a brand link in the Brands sidebar panel.

        Args:
            brand_name: Exact brand name text, e.g. 'Polo', 'H&M'.
        """
        logger.info(f"Filtering by brand: {brand_name}")
        brand_link = self.brand_sidebar.locator(f"a:has-text('{brand_name}')").first
        self.click(brand_link)

    def get_brand_heading(self) -> str:
        """
        Return the page heading text after a brand filter is applied.

        Returns:
            str: Heading text, e.g. 'Brand - Polo Products'.
        """
        return self.get_text(self.category_heading)

    def click_women_subcategory(self, subcategory: str) -> None:
        """
        Expand the Women category accordion and click a subcategory.

        Args:
            subcategory: Subcategory name, e.g. 'Dress', 'Tops'.
        """
        logger.info(f"Clicking Women > {subcategory}")
        self.click(self.category_women_link)
        sub_link = self.page.locator(f"#Women a:has-text('{subcategory}')").first
        self.click(sub_link)

    def are_search_results_relevant(self, keyword: str) -> bool:
        """
        Basic relevance check: verify at least one result name contains the keyword.

        Args:
            keyword: The term that was searched.

        Returns:
            bool: True if any product name contains the keyword (case-insensitive).
        """
        names = self.get_all_product_names()
        keyword_lower = keyword.lower()
        return any(keyword_lower in name.lower() for name in names)
