import pytest
from playwright.sync_api import Page, expect, BrowserContext
from pages.home_page import HomePage
from pages.products_page import ProductsPage

@pytest.mark.cross_browser
class TestCrossBrowser:
    """
    Cross-browser compatibility testing for BitSight website
    """
    
    def test_chromium_compatibility(self, page: Page):
        """
        Test website functionality in Chromium-based browsers
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check browser name
        browser_info = page.evaluate('''() => {
            return {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                vendor: navigator.vendor,
                language: navigator.language
            };
        }''')
        
        # Verify page loads correctly
        assert homepage.is_homepage_loaded(), "Homepage failed in Chromium"
        
        # Check CSS support
        css_support = page.evaluate('''() => {
