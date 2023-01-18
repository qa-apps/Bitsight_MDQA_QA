import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
import re

@pytest.mark.regression
class TestRegressionFull:
    """
    Full regression test suite for BitSight website functionality
    """
    
    def test_complete_homepage_functionality(self, page: Page):
        """
        Test all homepage functionality comprehensively
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Verify page title and meta tags
        assert page.title(), "Page title is missing"
        
        meta_description = page.locator('meta[name="description"]').get_attribute('content')
        assert meta_description, "Meta description is missing"
        
        meta_keywords = page.locator('meta[name="keywords"]').get_attribute('content')
        # Keywords might be optional
        
        # Verify all sections load
        assert homepage.is_homepage_loaded(), "Homepage not fully loaded"
        
        # Check all navigation elements
