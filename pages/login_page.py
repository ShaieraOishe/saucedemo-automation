"""
pages/login_page.py - Login Page Object
"""
import allure
from playwright.sync_api import Page


class LoginPage:
    URL = "https://www.saucedemo.com"

    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON   = "#login-button"
    ERROR_MESSAGE  = "[data-test='error']"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Navigate to Login Page")
    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_selector(self.LOGIN_BUTTON)

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str):
        self.page.fill(self.USERNAME_INPUT, username)

    @allure.step("Enter password")
    def enter_password(self, password: str):
        self.page.fill(self.PASSWORD_INPUT, password)

    @allure.step("Click Login button")
    def click_login(self):
        self.page.click(self.LOGIN_BUTTON)

    @allure.step("Login as {username}")
    def login(self, username: str, password: str):
        self.navigate()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    @allure.step("Get error message text")
    def get_error_message(self) -> str:
        self.page.wait_for_selector(self.ERROR_MESSAGE)
        return self.page.text_content(self.ERROR_MESSAGE).strip()

    def is_error_displayed(self) -> bool:
        return self.page.is_visible(self.ERROR_MESSAGE)
