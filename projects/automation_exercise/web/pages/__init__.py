# pages package — Page Object Model classes
from pages.base_page_ae import BasePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.contact_page import ContactPage

__all__ = [
    "BasePage",
    "HomePage",
    "LoginPage",
    "ProductsPage",
    "ProductDetailPage",
    "CartPage",
    "CheckoutPage",
    "ContactPage",
]
