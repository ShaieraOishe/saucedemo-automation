"""
conftest.py - Shared fixtures for SauceDemo automation tests
"""
import os
import pytest
from playwright.sync_api import sync_playwright
import allure

# ── Shared constants ──────────────────────────────────────────────────────────
BASE_URL = "https://www.saucedemo.com"
PASSWORD = "secret_sauce"


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the SauceDemo base URL."""
    return BASE_URL


@pytest.fixture(scope="session")
def password() -> str:
    """Return the shared password for all SauceDemo users."""
    return PASSWORD


@pytest.fixture(scope="function")
def browser_context():
    """Provide a fresh browser context (with video recording) for each test."""
    # Ensure the video output directory exists before Playwright tries to use it
    video_dir = os.path.join("allure-results", "videos")
    os.makedirs(video_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=200)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=video_dir,
        )
        page = context.new_page()

        yield page

        # Attach a full-page screenshot to the Allure report on every test
        try:
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name="Final Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass

        # Close context first so the video file is flushed to disk
        context.close()

        # Attach the recorded video to the Allure report
        try:
            video_path = page.video.path()
            if video_path and os.path.exists(video_path):
                with open(video_path, "rb") as vf:
                    allure.attach(
                        vf.read(),
                        name="Test Video",
                        attachment_type=allure.attachment_type.WEBM,
                    )
        except Exception:
            pass

        browser.close()
