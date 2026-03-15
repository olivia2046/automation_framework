"""
home_page.py
------------
Page Object for the automationexercise.com homepage.

Covers the hero section, featured products carousel, category sidebar,
and the subscription / newsletter widget at the bottom of the page.
"""

import logging
from playwright.sync_api import Page, Locator

from pages.base_page_ae import BasePage
from utils.config import get_urls


logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """
    Encapsulates all interactions with the application's homepage.

    Usage:
        home = HomePage(page)
        home.open()
        assert home.is_loaded()
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    @property
    def slider_section(self) -> Locator:
        """Main hero/carousel slider."""
        return self.page.locator("#slider")

    @property
    def featured_items(self) -> Locator:
        """Featured product cards on the homepage."""
        return self.page.locator(".features_items .product-image-wrapper")

    @property
    def category_sidebar(self) -> Locator:
        """Left-hand category panel."""
        return self.page.locator(".left-sidebar")

    @property
    def women_category_link(self) -> Locator:
        """'Women' category accordion toggle in the sidebar."""
        return self.page.locator("a[href='#Women']")

    @property
    def men_category_link(self) -> Locator:
        """'Men' category accordion toggle in the sidebar."""
        return self.page.locator("a[href='#Men']")

    @property
    def kids_category_link(self) -> Locator:
        """'Kids' category accordion toggle in the sidebar."""
        return self.page.locator("a[href='#Kids']")

    def get_subcategory_link(self, category: str, subcategory: str) -> Locator:
        """
        Return the locator for a specific subcategory link inside a category.

        Args:
            category: Parent category name, e.g. 'Women'.
            subcategory: Subcategory name, e.g. 'Dress'.

        Returns:
            Locator: Playwright locator for the subcategory anchor.
        """
        return self.page.locator(f"#{category} a", has_text=subcategory)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self) -> "HomePage":
        """Navigate to the homepage."""
        URLS = get_urls()
        self.navigate_to(URLS["home"])
        return self

    def is_loaded(self) -> bool:
        """
        Verify the homepage has fully loaded by checking for key UI elements.

        Returns:
            bool: True if the slider and featured items are visible.
        """
        return self.slider_section.is_visible() and self.featured_items.count() > 0

    def subscribe_to_newsletter(self, email: str) -> None:
        """
        Submit the newsletter subscription form via the footer component.

        Args:
            email: Email address to subscribe with.
        """
        logger.info(f"Subscribing to newsletter with: {email}")
        self.footer.subscribe(email)

    def is_subscription_successful(self) -> bool:
        """
        Check whether the newsletter subscription succeeded.

        Returns:
            bool: True if the success alert is visible after submission.
        """
        return self.footer.is_subscription_successful()

    def expand_category(self, category: str) -> None:
        """
        Click a top-level category in the sidebar to expand its subcategories.

        Args:
            category: Category name, e.g. 'Women', 'Men', 'Kids'.
        """
        link = self.page.locator(f"a[href='#{category}']")
        self.click(link)
        self.page.wait_for_timeout(500)  # wait for accordion animation

    def click_subcategory(self, category: str, subcategory: str) -> None:
        """
        Expand a category and click one of its subcategory links.

        Args:
            category: Parent category name, e.g. 'Women'.
            subcategory: Subcategory name, e.g. 'Dress'.
        """
        logger.info(f"Navigating to category: {category} > {subcategory}")
        self.expand_category(category)
        self.click(self.get_subcategory_link(category, subcategory))

    def get_featured_product_count(self) -> int:
        """
        Count how many featured product cards are rendered on the homepage.

        Returns:
            int: Number of featured product cards.
        """
        return self.featured_items.count()

    def click_first_featured_product(self) -> None:
        """Click the 'View Product' link of the first featured product card."""
        first_product = self.featured_items.first
        view_btn = first_product.locator("a:has-text('View Product')")
        self.click(view_btn)

    def add_first_featured_product_to_cart(self) -> None:
        """
        Hover over the first featured product and click 'Add to cart'.

        Note:
            The 'Add to cart' button only becomes visible on hover.
        """
        first_product = self.featured_items.first
        first_product.hover()
        add_btn = first_product.locator(".add-to-cart").first
        self.click(add_btn)
