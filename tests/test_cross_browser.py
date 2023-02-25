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
            return {
                grid: CSS.supports('display', 'grid'),
                flexbox: CSS.supports('display', 'flex'),
                customProperties: CSS.supports('--custom', 'value'),
                backdropFilter: CSS.supports('backdrop-filter', 'blur(10px)')
            };
        }''')
        
        # Modern browsers should support these
        assert css_support['grid'], "CSS Grid not supported"
        assert css_support['flexbox'], "Flexbox not supported"
        
    @pytest.mark.skip(reason="Run separately with Firefox")
    def test_firefox_compatibility(self, page: Page):
        """
        Test website functionality in Firefox
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Firefox-specific checks
        is_firefox = page.evaluate('() => navigator.userAgent.includes("Firefox")')
        
        if is_firefox:
            # Test Firefox-specific features
