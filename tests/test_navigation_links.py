import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from typing import List, Dict

@pytest.mark.navigation
class TestNavigationLinks:
    """
    Comprehensive navigation and link testing for BitSight website
    """
    
    def test_main_menu_solutions_dropdown(self, page: Page):
        """
        Test Solutions dropdown menu items and navigation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Open Solutions dropdown
        homepage.click_solutions_menu()
        page.wait_for_timeout(1000)
        
        # Get all dropdown items
        dropdown_items = page.locator('[role="menu"] a, .dropdown-menu a').all()
        assert len(dropdown_items) > 0, "No items found in Solutions dropdown"
        
        # Test first few items to avoid timeout
        for item in dropdown_items[:3]:
            item_text = item.text_content()
            item_href = item.get_attribute('href')
            
            assert item_text, "Dropdown item has no text"
            assert item_href, f"Dropdown item '{item_text}' has no href"
            
            # Click and verify navigation
            item.click()
            page.wait_for_load_state('networkidle')
            assert page.url != homepage.base_url, f"Failed to navigate from Solutions item: {item_text}"
            
            # Go back for next item
            homepage.navigate_to()
            homepage.click_solutions_menu()
            page.wait_for_timeout(500)
            
    def test_main_menu_products_dropdown(self, page: Page):
        """
        Test Products dropdown menu items and navigation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Open Products dropdown
        homepage.click_products_menu()
        page.wait_for_timeout(1000)
        
        # Get all dropdown items
        dropdown_items = page.locator('[role="menu"] a, .dropdown-menu a').all()
        assert len(dropdown_items) > 0, "No items found in Products dropdown"
        
        # Verify each item has proper attributes
        for item in dropdown_items:
            assert item.get_attribute('href'), "Product dropdown item missing href"
            assert item.text_content(), "Product dropdown item missing text"
            
    def test_main_menu_resources_dropdown(self, page: Page):
        """
        Test Resources dropdown menu items and navigation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Open Resources dropdown
        homepage.click_resources_menu()
        page.wait_for_timeout(1000)
        
        # Get all dropdown items
        dropdown_items = page.locator('[role="menu"] a, .dropdown-menu a').all()
        assert len(dropdown_items) > 0, "No items found in Resources dropdown"
        
        # Test navigation for first few items
        for item in dropdown_items[:3]:
            item_text = item.text_content()
            item.click()
            page.wait_for_load_state('networkidle')
            
            # Verify navigation occurred
            assert page.url != homepage.base_url, f"Failed to navigate from Resources: {item_text}"
            
            # Navigate back
            homepage.navigate_to()
            homepage.click_resources_menu()
            page.wait_for_timeout(500)
            
    def test_main_menu_company_dropdown(self, page: Page):
        """
        Test Company dropdown menu items and navigation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Open Company dropdown
        homepage.click_company_menu()
        page.wait_for_timeout(1000)
        
        # Get all dropdown items
        dropdown_items = page.locator('[role="menu"] a, .dropdown-menu a').all()
        assert len(dropdown_items) > 0, "No items found in Company dropdown"
        
        # Verify structure of dropdown items
        for item in dropdown_items:
            href = item.get_attribute('href')
            text = item.text_content()
            
            assert text, "Company dropdown item has no text"
            if href and not href.startswith('#'):
                assert href.startswith('http') or href.startswith('/'), f"Invalid href format: {href}"
                
    def test_footer_navigation_links(self, page: Page):
        """
