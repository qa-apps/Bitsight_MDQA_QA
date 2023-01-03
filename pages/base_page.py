from playwright.sync_api import Page, Locator, expect
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = 'https://www.bitsight.com'
        
    def navigate_to(self, path: str = '') -> None:
        """
        Navigate to a specific path on the website
        """
        url = f'{self.base_url}{path}' if path else self.base_url
        logger.info(f'Navigating to: {url}')
        self.page.goto(url, wait_until='networkidle')
        
    def wait_for_page_load(self) -> None:
        """
        Wait for the page to fully load
        """
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_load_state('domcontentloaded')
        
    def click_element(self, locator: str, force: bool = False) -> None:
        """
        Click on an element with retry logic
        """
        element = self.page.locator(locator)
        element.wait_for(state='visible', timeout=30000)
        element.click(force=force)
        
    def fill_input(self, locator: str, text: str) -> None:
        """
        Fill an input field with text
        """
        element = self.page.locator(locator)
        element.wait_for(state='visible')
        element.fill(text)
        
    def get_text(self, locator: str) -> str:
        """
        Get text content of an element
        """
        element = self.page.locator(locator)
        element.wait_for(state='visible')
        return element.text_content() or ''
        
    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        """
        Check if an element is visible
        """
        try:
            element = self.page.locator(locator)
            element.wait_for(state='visible', timeout=timeout)
            return True
        except:
            return False
            
    def get_all_links(self) -> List[str]:
        """
        Get all links on the current page
        """
        links = self.page.locator('a[href]').all()
        return [link.get_attribute('href') or '' for link in links]
        
    def check_page_title(self, expected_title: str) -> bool:
        """
        Verify page title contains expected text
        """
        actual_title = self.page.title()
        return expected_title.lower() in actual_title.lower()
        
    def scroll_to_element(self, locator: str) -> None:
        """
        Scroll to make element visible
        """
        element = self.page.locator(locator)
        element.scroll_into_view_if_needed()
        
