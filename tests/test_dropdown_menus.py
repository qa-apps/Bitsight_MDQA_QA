import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from typing import List

@pytest.mark.navigation
@pytest.mark.dropdown
class TestDropdownMenus:
    """
    Comprehensive dropdown menu testing for BitSight website
    """
    
    def test_solutions_dropdown_complete(self, page: Page):
        """
        Complete test of Solutions dropdown menu functionality
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Hover and click Solutions menu
        solutions_button = page.locator('button:has-text("Solutions"), a:has-text("Solutions")').first
        assert solutions_button.is_visible(), "Solutions menu button not found"
        
        # Test hover behavior
        solutions_button.hover()
        page.wait_for_timeout(500)
        
        # Click to open dropdown
        solutions_button.click()
        page.wait_for_timeout(500)
        
        # Find dropdown menu
        dropdown = page.locator('[role="menu"], .dropdown-menu, .submenu').first
        assert dropdown.is_visible(), "Solutions dropdown did not open"
        
        # Get all dropdown items
        dropdown_items = dropdown.locator('a, [role="menuitem"]').all()
        assert len(dropdown_items) > 0, "No items in Solutions dropdown"
        
        # Store items for testing
        item_texts = []
        item_hrefs = []
        
        for item in dropdown_items:
            text = item.text_content()
            href = item.get_attribute('href')
            
            item_texts.append(text)
            item_hrefs.append(href)
            
            # Verify item properties
            assert text, "Dropdown item has no text"
            assert href or item.get_attribute('role') == 'menuitem', "Dropdown item has no action"
            
