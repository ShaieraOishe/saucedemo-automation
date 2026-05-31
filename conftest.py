"""
conftest.py - Shared fixtures for SauceDemo automation tests
"""
import pytest
from playwright.sync_api import sync_playwright
import allure


@pytest.fixture(scope="function")
def browser_context():
    """Provide a fresh browser context for each test."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=200)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir="allure-results/videos/"
        )
        page = context.new_page()
        yield page
        # Attach screenshot on completion
        try:
            screenshot = page.screenshot(full_page=True)
            allure.attach(screenshot, name="Final Screenshot",
                          attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
        context.close()
        browser.close()
