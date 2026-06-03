"""
tests/test_q2_standard_user.py
Q2 [50 Marks] - standard_user full purchase journey with cart verification.

Steps:
  1. Login with standard_user
  2. Reset App State from hamburger menu
  3. Add any 3 items to cart
  4. Navigate to final checkout overview page
  5. Verify product names and total price
  6. Finish purchase and verify success message
  7. Reset App State again
  8. Logout
"""
import allure
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage

USER = "standard_user"

PRODUCTS_TO_ADD = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
]

SUCCESS_HEADER = "Thank you for your order!"


@allure.epic("SauceDemo Automation")
@allure.feature("Q2 - Standard User Full Purchase Journey")
@allure.story("standard_user completes a full end-to-end purchase with cart and price verification")
@allure.severity(allure.severity_level.BLOCKER)
class TestStandardUserPurchase:

    @allure.title("Q2: standard_user - Add 3 items, verify checkout details, complete purchase, logout")
    @allure.description(
        "Login as standard_user, reset app state, add 3 products, verify names and "
        "total price on the overview page, complete the purchase, verify the success "
        "message, then reset state and logout."
    )
    def test_standard_user_full_journey(self, browser_context, password):
        page = browser_context

        login_page        = LoginPage(page)
        inventory_page    = InventoryPage(page)
        cart_page         = CartPage(page)
        checkout_info     = CheckoutInfoPage(page)
        checkout_overview = CheckoutOverviewPage(page)
        complete_page     = CheckoutCompletePage(page)

        # Step 1: Login
        with allure.step(f"Login as '{USER}'"):
            login_page.login(USER, password)
            inventory_page.wait_for_page()

        # Step 2: Reset App State
        with allure.step("Reset App State via hamburger menu"):
            inventory_page.reset_app_state()
            cart_count = inventory_page.get_cart_count()
            assert cart_count == 0, \
                f"Cart should be empty after reset, but badge shows {cart_count}"

        # Step 3: Add 3 products to cart
        expected_names  = []
        expected_prices = []

        for product_name in PRODUCTS_TO_ADD:
            with allure.step(f"Add '{product_name}' to cart"):
                all_names  = inventory_page.get_all_item_names()
                all_prices = inventory_page.get_all_item_prices()
                idx = all_names.index(product_name)
                expected_prices.append(all_prices[idx])
                expected_names.append(product_name)
                inventory_page.add_to_cart_by_name(product_name)

        with allure.step("Verify cart badge shows 3 items"):
            count = inventory_page.get_cart_count()
            assert count == 3, f"Expected 3 items in cart, got {count}"

        # Step 4: Navigate to Cart
        with allure.step("Navigate to Cart page"):
            inventory_page.go_to_cart()
            cart_page.wait_for_page()

        # Step 5: Proceed through Checkout Info
        with allure.step("Click Checkout button"):
            cart_page.proceed_to_checkout()

        with allure.step("Fill in checkout information"):
            checkout_info.wait_for_page()
            checkout_info.fill_info("John", "Doe", "12345")
            checkout_info.continue_to_overview()

        # Step 6: Verify on Overview Page
        with allure.step("Verify product names on Checkout Overview"):
            checkout_overview.wait_for_page()
            actual_names = checkout_overview.get_product_names()

            allure.attach(
                "\n".join(expected_names),
                name="Expected Product Names",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                "\n".join(actual_names),
                name="Actual Product Names",
                attachment_type=allure.attachment_type.TEXT,
            )

            assert sorted(actual_names) == sorted(expected_names), (
                f"Product name mismatch!\n"
                f"Expected: {sorted(expected_names)}\n"
                f"Actual  : {sorted(actual_names)}"
            )

        with allure.step("Verify total price on Checkout Overview"):
            actual_total      = checkout_overview.get_total()
            actual_subtotal   = checkout_overview.get_subtotal()
            actual_tax        = checkout_overview.get_tax()
            expected_subtotal = round(sum(expected_prices), 2)
            expected_total    = round(expected_subtotal + actual_tax, 2)

            allure.attach(
                (
                    f"Products      : {PRODUCTS_TO_ADD}\n"
                    f"Expected Sub  : ${expected_subtotal}\n"
                    f"Actual Sub    : ${actual_subtotal}\n"
                    f"Tax           : ${actual_tax}\n"
                    f"Expected Total: ${expected_total}\n"
                    f"Actual Total  : ${actual_total}"
                ),
                name="Price Breakdown",
                attachment_type=allure.attachment_type.TEXT,
            )

            assert actual_subtotal == expected_subtotal, (
                f"Subtotal mismatch! Expected ${expected_subtotal}, got ${actual_subtotal}"
            )
            assert actual_total == expected_total, (
                f"Total price mismatch! Expected ${expected_total}, got ${actual_total}"
            )

        # Step 7: Finish Purchase
        with allure.step("Click Finish to complete the order"):
            checkout_overview.finish_purchase()

        # Step 8: Verify Success Message
        with allure.step("Verify order success message"):
            complete_page.wait_for_page()
            assert complete_page.is_success_displayed(), \
                "Success header was NOT displayed on confirmation page."

            success_header = complete_page.get_success_header()
            success_text   = complete_page.get_success_text()

            allure.attach(
                f"Header: {success_header}\nText: {success_text}",
                name="Success Confirmation",
                attachment_type=allure.attachment_type.TEXT,
            )

            assert success_header == SUCCESS_HEADER, (
                f"Success header mismatch!\n"
                f"Expected: '{SUCCESS_HEADER}'\n"
                f"Actual  : '{success_header}'"
            )

        # Step 9: Back to products, Reset State, Logout
        with allure.step("Navigate back to products page"):
            complete_page.back_to_products()
            inventory_page.wait_for_page()

        with allure.step("Reset App State (second time)"):
            inventory_page.reset_app_state()

        with allure.step("Logout"):
            inventory_page.logout()
            assert page.is_visible("#login-button"), \
                "Logout failed — login button not visible."