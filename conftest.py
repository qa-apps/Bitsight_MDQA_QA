"""
Pytest configuration and fixtures for BitSight automation tests
"""

import pytest
from playwright.sync_api import Page, BrowserContext
from typing import Generator
import os
from datetime import datetime

@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for BitSight website"""
    return "https://www.bitsight.com"

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

@pytest.fixture(scope="function")
def context(browser) -> Generator[BrowserContext, None, None]:
    """Create a new browser context for each test"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True
    )
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context) -> Generator[Page, None, None]:
    """Create a new page for each test"""
    page = context.new_page()
    yield page
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{screenshot_dir}/{item.name}_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved: {screenshot_path}")
