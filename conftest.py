import pytest
import os
import json
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page, BrowserContext, Playwright
from typing import Generator, Dict, Any
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL', 'https://www.bitsight.com')
HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
SLOW_MO = int(os.getenv('SLOW_MO', '0'))
TIMEOUT = int(os.getenv('TIMEOUT', '30000'))

@pytest.fixture(scope='session')
def base_url() -> str:
    return BASE_URL

@pytest.fixture(scope='function')
def browser_context_args(browser_context_args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **browser_context_args,
        'viewport': {'width': 1920, 'height': 1080},
        'ignore_https_errors': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

@pytest.fixture(scope='function')
def context(browser, browser_context_args: Dict[str, Any]) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(**browser_context_args)
    context.set_default_timeout(TIMEOUT)
    context.set_default_navigation_timeout(TIMEOUT)
    yield context
    context.close()

@pytest.fixture(scope='function')
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    page.set_default_timeout(TIMEOUT)
    page.set_default_navigation_timeout(TIMEOUT)
    yield page
    page.close()

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    yield
    if request.node.rep_call.failed:
        screenshot_dir = Path('screenshots')
        screenshot_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_name = request.node.name.replace('/', '_')
        screenshot_path = screenshot_dir / f'{test_name}_{timestamp}.png'
        page.screenshot(path=str(screenshot_path))

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)
