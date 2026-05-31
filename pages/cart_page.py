"""
pages/cart_page.py - Cart Page Object
"""
import allure
from playwright.sync_api import Page


class CartPage:

    # Locators
    CART_ITEMS        = ".cart_item"
    ITEM_NAME         = ".inventory_item_name"
    ITEM_PRICE        = ".inventory_item_price"
    CHECKOUT_BUTTON   = "[data-test='checkout']"
    CONTINUE_SHOPPING = "[data-test='continue-shopping']"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Wait for Cart page to load")
    def wait_for_page(self):
        self.page.wait_for_selector(".cart_list", timeout=10000)

    def get_cart_item_names(self) -> list:
        return [el.text_content().strip()
                for el in self.page.query_selector_all(self.ITEM_NAME)]

    def get_cart_item_prices(self) -> list:
        prices = []
        for el in self.page.query_selector_all(self.ITEM_PRICE):
            price_text = el.text_content().strip().replace("$", "")
            prices.append(float(price_text))
        return prices

    @allure.step("Proceed to Checkout")
    def proceed_to_checkout(self):
        self.page.click(self.CHECKOUT_BUTTON)
        self.page.wait_for_selector("#checkout_info_container")
