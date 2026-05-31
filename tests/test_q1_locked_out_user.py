"""
tests/test_q1_locked_out_user.py
Q1 [20 Marks] - Verify locked_out_user error message on login.
"""
import allure
import pytest
from pages.login_page import LoginPage

BASE_URL = "https://www.saucedemo.com"
PASSWORD = "secret_sauce"
LOCKED_USER = "locked_out_user"
EXPECTED_ERROR = "Epic sadface: Sorry, this user has been locked out."


@allure.epic("SauceDemo Automation")
@allure.feature("Q1 - Locked Out User")
@allure.story("Locked-out user should see an error message on login attempt")
@allure.severity(allure.severity_level.CRITICAL)
class TestLockedOutUser:

    @allure.title("Q1: Verify error message for locked_out_user")
    @allure.description(
        "Attempt to login with 'locked_out_user' and verify that the correct "
        "error message is displayed on the login page."
    )
    def test_locked_out_user_error_message(self, browser_context):
        page = browser_context
        login_page = LoginPage(page)

        with allure.step("Navigate to SauceDemo login page"):
            login_page.navigate()

        with allure.step(f"Attempt login with username='{LOCKED_USER}'"):
            login_page.enter_username(LOCKED_USER)
            login_page.enter_password(PASSWORD)
            login_page.click_login()

        with allure.step("Verify error banner is visible"):
            assert login_page.is_error_displayed(), \
                "Error message banner was NOT displayed after login attempt."

        with allure.step("Capture and verify error message text"):
            actual_error = login_page.get_error_message()
            allure.attach(
                actual_error,
                name="Actual Error Message",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                EXPECTED_ERROR,
                name="Expected Error Message",
                attachment_type=allure.attachment_type.TEXT
            )
            assert actual_error == EXPECTED_ERROR, (
                f"Error message mismatch!\n"
                f"Expected: '{EXPECTED_ERROR}'\n"
                f"Actual  : '{actual_error}'"
            )

        with allure.step("Verify user is still on login page (not redirected)"):
            assert "saucedemo.com" in page.url, "User was unexpectedly redirected."
            assert page.is_visible("#login-button"), \
                "Login button not visible — user may have been logged in."
