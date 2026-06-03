"""
tests/test_q3_performance_glitch_user.py
Q3 [30 Marks] - performance_glitch_user purchase journey with Z to A sort.

Steps:
  1. Login with performance_glitch_user
  2. Reset App State
  3. Filter by Name (Z to A)
  4. Add the first product (after sorting) to cart
  5. Navigate to final checkout overview page
  6. Verify all product names and total price
  7. Finish the purchase
  8. Verify successful order message
  9. Reset App State again
  10. Logout
"""
import allure
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage

USER           = "performance_glitch_user"
SUCCESS_HEADER = "Thank you for your order!"


@allure.epic("SauceDemo Automation")
@allure.feature("Q3 - Performance Glitch User Purchase Journey")
@allure.story("performance_glitch_user sorts Z to A, adds first product, verifies checkout and completes order")
@allure.severity(allure.severity_level.CRITICAL)
class TestPerformanceGlitchUserPurchase:

    @allure.title(
        "Q3: performance_glitch_user - Sort Z to A, add first item, verify checkout, complete purchase, logout"
    )
    @allure.description(
        "Login as performance_glitch_user, reset state, sort products Z to A, add the "
        "first displayed product to cart, proceed through full checkout, verify product "
        "names and total price on the overview page, finish purchase, verify success, "
        "reset state and logout."
    )
    def test_performance_glitch_user_journey(self, browser_context, password):
        page = browser_context

        login_page        = LoginPage(page)
        inventory_page    = InventoryPage(page)
        cart_page         = CartPage(page)
        checkout_info     = CheckoutInfoPage(page)
        checkout_overview = CheckoutOverviewPage(page)
        complete_page     = CheckoutCompletePage(page)

        # Step 1: Login (performance_glitch_user is intentionally slow)
        with allure.step(f"Login as '{USER}' (may experience slight delay)"):
            login_page.login(USER, password)
            inventory_page.page.wait_for_selector(
                "#inventory_container", timeout=20000
            )

        # Step 2: Reset App State
        with allure.step("Reset App State via hamburger menu"):
            inventory_page.reset_app_state()
            cart_count = inventory_page.get_cart_count()
            assert cart_count == 0, \
                f"Cart should be empty after reset, but badge shows {cart_count}"

        # Step 3: Sort by Name Z to A
        with allure.step("Sort products by Name (Z to A)"):
            inventory_page.sort_by("za")
            sorted_names = inventory_page.get_all_item_names()
            allure.attach(
                "\n".join(sorted_names),
                name="Products Sorted (Z to A)",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Step 4: Add first product to cart
        with allure.step("Add first product (Z to A order) to cart"):
            first_item     = inventory_page.add_first_item_to_cart()
            expected_name  = first_item["name"]
            expected_price = first_item["price"]
            allure.attach(
                f"Name : {expected_name}\nPrice: ${expected_price}",
                name="Added Product",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Verify cart badge shows 1 item"):
            count = inventory_page.get_cart_count()
            assert count == 1, f"Expected 1 item in cart, got {count}"

        # Step 5: Navigate to Cart
        with allure.step("Navigate to Cart page"):
            inventory_page.go_to_cart()
            cart_page.wait_for_page()

        # Step 6: Proceed to Checkout Info
        with allure.step("Click Checkout"):
            cart_page.proceed_to_checkout()

        with allure.step("Fill checkout information"):
            checkout_info.wait_for_page()
            checkout_info.fill_info("Jane", "Smith", "67890")
            checkout_info.continue_to_overview()

        # Step 7: Verify Overview — Product Names & Total Price
        with allure.step("Verify product names on Checkout Overview"):
            checkout_overview.wait_for_page()
            actual_names = checkout_overview.get_product_names()

            allure.attach(
                f"Expected: {[expected_name]}\nActual  : {actual_names}",
                name="Product Name Verification",
                attachment_type=allure.attachment_type.TEXT,
            )

            assert expected_name in actual_names, (
                f"Expected product '{expected_name}' not found in overview!\n"
                f"Actual names: {actual_names}"
            )

        with allure.step("Verify total price on Checkout Overview"):
            actual_total    = checkout_overview.get_total()
            actual_subtotal = checkout_overview.get_subtotal()
            actual_tax      = checkout_overview.get_tax()
            expected_total  = round(expected_price + actual_tax, 2)

            allure.attach(
                (
                    f"Product       : {expected_name}\n"
                    f"Expected Sub  : ${expected_price}\n"
                    f"Actual Sub    : ${actual_subtotal}\n"
                    f"Tax           : ${actual_tax}\n"
                    f"Expected Total: ${expected_total}\n"
                    f"Actual Total  : ${actual_total}"
                ),
                name="Price Breakdown",
                attachment_type=allure.attachment_type.TEXT,
            )

            assert actual_subtotal == expected_price, (
                f"Subtotal mismatch! Expected ${expected_price}, got ${actual_subtotal}"
            )
            assert actual_total == expected_total, (
                f"Total mismatch! Expected ${expected_total}, got ${actual_total}"
            )

        # Step 8: Finish Purchase
        with allure.step("Click Finish to complete the order"):
            checkout_overview.finish_purchase()

        # Step 9: Verify Success Message
        with allure.step("Verify order success message"):
            complete_page.wait_for_page()
            assert complete_page.is_success_displayed(), \
                "Success header NOT displayed on confirmation page."

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

        # Step 10: Back to Products, Reset, Logout
        with allure.step("Navigate back to products page"):
            complete_page.back_to_products()
            inventory_page.wait_for_page()

        with allure.step("Reset App State (second time)"):
            inventory_page.reset_app_state()

        with allure.step("Logout"):
            inventory_page.logout()
            assert page.is_visible("#login-button"), \
                "Logout failed — login button not visible."