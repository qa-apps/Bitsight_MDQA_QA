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
        
    def take_screenshot(self, name: str) -> None:
        """
        Take a screenshot of the current page
        """
        self.page.screenshot(path=f'screenshots/{name}.png', full_page=True)
        
    def get_page_url(self) -> str:
        """
        Get current page URL
        """
        return self.page.url
        
    def go_back(self) -> None:
        """
        Navigate back in browser history
        """
        self.page.go_back()
        
    def refresh_page(self) -> None:
        """
        Refresh the current page
        """
        self.page.reload()
        
    def wait_for_element(self, locator: str, state: str = 'visible') -> None:
        """
        Wait for element to be in specified state
        """
        element = self.page.locator(locator)
        element.wait_for(state=state)
        
    def get_attribute(self, locator: str, attribute: str) -> Optional[str]:
        """
        Get attribute value of an element
        """
        element = self.page.locator(locator)
        return element.get_attribute(attribute)
        
    def hover_over_element(self, locator: str) -> None:
        """
        Hover over an element
        """
        element = self.page.locator(locator)
        element.hover()
        
    def select_dropdown_option(self, locator: str, value: str) -> None:
        """
        Select an option from dropdown
        """
        element = self.page.locator(locator)
        element.select_option(value)
        
    def get_dropdown_options(self, locator: str) -> List[str]:
        """
        Get all options from a dropdown
        """
        element = self.page.locator(locator)
        options = element.locator('option').all()
        return [opt.text_content() or '' for opt in options]
        
    def check_broken_links(self) -> List[Dict[str, Any]]:
        """
        Check for broken links on the page
        """
        broken_links = []
        links = self.get_all_links()
        
        for link in links:
            if link and not link.startswith('#'):
                try:
                    response = self.page.request.get(link)
                    if response.status >= 400:
                        broken_links.append({'url': link, 'status': response.status})
                except Exception as e:
                    broken_links.append({'url': link, 'error': str(e)})
                    
        return broken_links
        
    def check_images_loaded(self) -> bool:
        """
        Check if all images are properly loaded
        """
        images = self.page.locator('img').all()
        for img in images:
            if not img.is_visible() or img.get_attribute('naturalWidth') == '0':
                return False
        return True
