"""
pages/checkout_page.py - Checkout Step One & Step Two & Confirmation Page Objects
"""
import allure
from playwright.sync_api import Page


class CheckoutInfoPage:
    """Checkout Step One: Customer information form."""

    FIRST_NAME   = "[data-test='firstName']"
    LAST_NAME    = "[data-test='lastName']"
    POSTAL_CODE  = "[data-test='postalCode']"
    CONTINUE_BTN = "[data-test='continue']"
    CANCEL_BTN   = "[data-test='cancel']"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Wait for Checkout Info page to load")
    def wait_for_page(self):
        self.page.wait_for_selector(self.FIRST_NAME, timeout=10000)

    @allure.step("Fill checkout info: {first} {last}, {postal}")
    def fill_info(self, first: str, last: str, postal: str):
        self.page.fill(self.FIRST_NAME, first)
        self.page.fill(self.LAST_NAME, last)
        self.page.fill(self.POSTAL_CODE, postal)

    @allure.step("Click Continue to Order Summary")
    def continue_to_overview(self):
        self.page.click(self.CONTINUE_BTN)
        self.page.wait_for_selector("#checkout_summary_container", timeout=10000)


class CheckoutOverviewPage:
    """Checkout Step Two: Order summary / overview."""

    CART_ITEMS     = ".cart_item"
    ITEM_NAME      = ".inventory_item_name"
    ITEM_PRICE     = ".inventory_item_price"
    SUBTOTAL_LABEL = ".summary_subtotal_label"
    TAX_LABEL      = ".summary_tax_label"
    TOTAL_LABEL    = ".summary_total_label"
    FINISH_BTN     = "[data-test='finish']"
    CANCEL_BTN     = "[data-test='cancel']"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Wait for Checkout Overview page to load")
    def wait_for_page(self):
        self.page.wait_for_selector("#checkout_summary_container", timeout=10000)

    def get_product_names(self) -> list:
        """Return list of all product names on the overview page."""
        return [el.text_content().strip()
                for el in self.page.query_selector_all(self.ITEM_NAME)]

    def get_product_prices(self) -> list:
        """Return list of all product prices (as floats) on the overview page."""
        prices = []
        for el in self.page.query_selector_all(self.ITEM_PRICE):
            price_text = el.text_content().strip().replace("$", "")
            prices.append(float(price_text))
        return prices

    def get_subtotal(self) -> float:
        """Return item subtotal (before tax) as float."""
        text = self.page.text_content(self.SUBTOTAL_LABEL)
        # Format: "Item total: $XX.XX"
        return float(text.split("$")[1].strip())

    def get_tax(self) -> float:
        """Return tax amount as float."""
        text = self.page.text_content(self.TAX_LABEL)
        return float(text.split("$")[1].strip())

    def get_total(self) -> float:
        """Return the grand total as float."""
        text = self.page.text_content(self.TOTAL_LABEL)
        # Format: "Total: $XX.XX"
        return float(text.split("$")[1].strip())

    def get_expected_total(self) -> float:
        """Return subtotal + tax as cross-check."""
        return round(self.get_subtotal() + self.get_tax(), 2)

    @allure.step("Click Finish to complete purchase")
    def finish_purchase(self):
        self.page.click(self.FINISH_BTN)
        self.page.wait_for_selector("#checkout_complete_container", timeout=10000)


class CheckoutCompletePage:
    """Order confirmation page."""

    COMPLETE_HEADER  = ".complete-header"
    COMPLETE_TEXT    = ".complete-text"
    PONY_EXPRESS_IMG = ".pony_express"
    BACK_HOME_BTN    = "[data-test='back-to-products']"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Wait for Order Confirmation page to load")
    def wait_for_page(self):
        self.page.wait_for_selector("#checkout_complete_container", timeout=10000)

    def get_success_header(self) -> str:
        return self.page.text_content(self.COMPLETE_HEADER).strip()

    def get_success_text(self) -> str:
        return self.page.text_content(self.COMPLETE_TEXT).strip()

    def is_success_displayed(self) -> bool:
        return self.page.is_visible(self.COMPLETE_HEADER)

    @allure.step("Go back to Products page")
    def back_to_products(self):
        self.page.click(self.BACK_HOME_BTN)
        self.page.wait_for_selector("#inventory_container")
