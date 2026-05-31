"""
pages/inventory_page.py - Inventory/Products Page Object
"""
import allure
from playwright.sync_api import Page


class InventoryPage:

    # Locators
    HAMBURGER_MENU       = "#react-burger-menu-btn"
    RESET_APP_STATE      = "#reset_sidebar_link"
    LOGOUT_LINK          = "#logout_sidebar_link"
    MENU_CLOSE_BTN       = "#react-burger-cross-btn"
    SORT_DROPDOWN        = "[data-test='product-sort-container']"
    INVENTORY_ITEMS      = ".inventory_item"
    ITEM_NAME            = ".inventory_item_name"
    ITEM_PRICE           = ".inventory_item_price"
    ADD_TO_CART_BTN      = "button[data-test^='add-to-cart']"
    CART_BADGE           = ".shopping_cart_badge"
    CART_LINK            = ".shopping_cart_link"
    INVENTORY_CONTAINER  = "#inventory_container"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Wait for Inventory page to load")
    def wait_for_page(self):
        self.page.wait_for_selector(self.INVENTORY_CONTAINER, timeout=15000)

    @allure.step("Open hamburger menu")
    def open_menu(self):
        self.page.click(self.HAMBURGER_MENU)
        self.page.wait_for_selector(self.RESET_APP_STATE, state="visible")

    @allure.step("Reset App State")
    def reset_app_state(self):
        self.open_menu()
        self.page.click(self.RESET_APP_STATE)
        self.page.wait_for_timeout(500)
        # Close menu after reset
        if self.page.is_visible(self.MENU_CLOSE_BTN):
            self.page.click(self.MENU_CLOSE_BTN)
            self.page.wait_for_timeout(300)

    @allure.step("Logout")
    def logout(self):
        self.open_menu()
        self.page.click(self.LOGOUT_LINK)
        self.page.wait_for_selector("#login-button")

    @allure.step("Sort products by: {sort_option}")
    def sort_by(self, sort_option: str):
        """
        sort_option values:
          'az' - Name (A to Z)
          'za' - Name (Z to A)
          'lohi' - Price (low to high)
          'hilo' - Price (high to low)
        """
        self.page.select_option(self.SORT_DROPDOWN, value=sort_option)
        self.page.wait_for_timeout(500)

    def get_all_item_names(self) -> list:
        """Return list of all product names currently displayed."""
        return [el.text_content().strip()
                for el in self.page.query_selector_all(self.ITEM_NAME)]

    def get_all_item_prices(self) -> list:
        """Return list of all product prices as floats."""
        prices = []
        for el in self.page.query_selector_all(self.ITEM_PRICE):
            price_text = el.text_content().strip().replace("$", "")
            prices.append(float(price_text))
        return prices

    @allure.step("Add product to cart by name: {product_name}")
    def add_to_cart_by_name(self, product_name: str):
        items = self.page.query_selector_all(self.INVENTORY_ITEMS)
        for item in items:
            name_el = item.query_selector(self.ITEM_NAME)
            if name_el and name_el.text_content().strip() == product_name:
                btn = item.query_selector("button[data-test^='add-to-cart']")
                if btn:
                    btn.click()
                    self.page.wait_for_timeout(300)
                    return
        raise ValueError(f"Product '{product_name}' not found on inventory page.")

    @allure.step("Add first {count} products to cart")
    def add_first_n_items_to_cart(self, count: int) -> list:
        """Add the first N visible products and return their names and prices."""
        added = []
        items = self.page.query_selector_all(self.INVENTORY_ITEMS)
        for item in items[:count]:
            name = item.query_selector(self.ITEM_NAME).text_content().strip()
            price_text = item.query_selector(self.ITEM_PRICE).text_content().strip().replace("$", "")
            price = float(price_text)
            btn = item.query_selector("button[data-test^='add-to-cart']")
            btn.click()
            self.page.wait_for_timeout(300)
            added.append({"name": name, "price": price})
        return added

    @allure.step("Add first product (after sort) to cart")
    def add_first_item_to_cart(self) -> dict:
        """Add the very first product displayed and return its name and price."""
        items = self.page.query_selector_all(self.INVENTORY_ITEMS)
        first = items[0]
        name = first.query_selector(self.ITEM_NAME).text_content().strip()
        price_text = first.query_selector(self.ITEM_PRICE).text_content().strip().replace("$", "")
        price = float(price_text)
        btn = first.query_selector("button[data-test^='add-to-cart']")
        btn.click()
        self.page.wait_for_timeout(300)
        return {"name": name, "price": price}

    @allure.step("Go to cart")
    def go_to_cart(self):
        self.page.click(self.CART_LINK)
        self.page.wait_for_selector(".cart_list")

    def get_cart_count(self) -> int:
        badge = self.page.query_selector(self.CART_BADGE)
        if badge:
            return int(badge.text_content().strip())
        return 0
