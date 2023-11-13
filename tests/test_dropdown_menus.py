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
            
        # Test clicking first item
        if dropdown_items:
            first_item = dropdown_items[0]
            first_text = first_item.text_content()
            first_item.click()
            page.wait_for_load_state('networkidle')
            
            # Verify navigation or action occurred
            assert page.url != homepage.base_url or page.locator(f'text="{first_text}"').is_visible(), "Dropdown item click had no effect"
            
        # Return to homepage for next test
        homepage.navigate_to()
        
        # Test dropdown closes when clicking outside
        solutions_button.click()
        page.wait_for_timeout(500)
        assert dropdown.is_visible(), "Dropdown should be open"
        
        # Click outside
        page.click('body', position={'x': 0, 'y': 0})
        page.wait_for_timeout(500)
        assert not dropdown.is_visible(), "Dropdown did not close when clicking outside"
        
    def test_products_dropdown_complete(self, page: Page):
        """
        Complete test of Products dropdown menu functionality
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find and click Products menu
        products_button = page.locator('button:has-text("Products"), a:has-text("Products")').first
        assert products_button.is_visible(), "Products menu button not found"
        
        products_button.click()
        page.wait_for_timeout(500)
        
        # Find dropdown
        dropdown = page.locator('[role="menu"], .dropdown-menu').nth(1) if page.locator('[role="menu"]').count() > 1 else page.locator('[role="menu"], .dropdown-menu').first
        
        if dropdown.is_visible():
            # Count product items
            product_items = dropdown.locator('a').all()
            assert len(product_items) > 0, "Products dropdown is empty"
            
            # Test each product link
            for i, item in enumerate(product_items[:3]):  # Test first 3 to avoid timeout
                homepage.navigate_to()
                products_button.click()
                page.wait_for_timeout(500)
                
                # Re-query items as DOM might change
                current_items = dropdown.locator('a').all()
                if i < len(current_items):
                    item_text = current_items[i].text_content()
                    item_href = current_items[i].get_attribute('href')
                    
                    # Verify link properties
                    assert item_text, f"Product item {i} has no text"
                    assert item_href, f"Product item {i} has no href"
                    
                    # Click and verify navigation
                    current_items[i].click()
                    page.wait_for_load_state('networkidle')
                    
                    # Should navigate to product page
                    assert page.url != homepage.base_url, f"Product link '{item_text}' did not navigate"
                    
    def test_resources_dropdown_complete(self, page: Page):
        """
        Complete test of Resources dropdown menu functionality  
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find Resources menu
        resources_button = page.locator('button:has-text("Resources"), a:has-text("Resources")').first
        assert resources_button.is_visible(), "Resources menu not found"
        
        # Open dropdown
        resources_button.click()
        page.wait_for_timeout(500)
        
        # Find dropdown content
        dropdown = page.locator('[role="menu"], .dropdown-menu').nth(2) if page.locator('[role="menu"]').count() > 2 else page.locator('[role="menu"], .dropdown-menu').first
        
        if dropdown.is_visible():
            # Get resource categories
            categories = dropdown.locator('.category, .section, h3, h4').all()
            
            # Get resource links
            resource_links = dropdown.locator('a').all()
            assert len(resource_links) > 0, "No links in Resources dropdown"
            
            # Verify link diversity (different types of resources)
            link_texts = [link.text_content() for link in resource_links[:10]]
            
            # Common resource types to check for
            resource_types = ['blog', 'guide', 'whitepaper', 'case', 'webinar', 'report', 'research']
            found_types = []
            
            for link_text in link_texts:
                if link_text:
                    text_lower = link_text.lower()
                    for resource_type in resource_types:
                        if resource_type in text_lower:
                            found_types.append(resource_type)
                            break
                            
            # Resources should have variety
            assert len(set(found_types)) > 0 or len(resource_links) > 5, "Resources dropdown lacks variety"
            
    def test_company_dropdown_complete(self, page: Page):
        """
        Complete test of Company dropdown menu functionality
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find Company menu
        company_button = page.locator('button:has-text("Company"), a:has-text("Company")').first
        assert company_button.is_visible(), "Company menu not found"
        
        company_button.click()
        page.wait_for_timeout(500)
        
        # Find dropdown
        dropdown = page.locator('[role="menu"], .dropdown-menu').nth(3) if page.locator('[role="menu"]').count() > 3 else page.locator('[role="menu"], .dropdown-menu').first
        
        if dropdown.is_visible():
            # Check for common company pages
            expected_pages = ['about', 'team', 'careers', 'contact', 'news', 'partners']
            dropdown_text = dropdown.text_content().lower()
            
            found_pages = [page_type for page_type in expected_pages if page_type in dropdown_text]
            assert len(found_pages) > 2, f"Company dropdown missing common pages. Found: {found_pages}"
            
            # Get all links
            company_links = dropdown.locator('a').all()
            assert len(company_links) > 0, "No links in Company dropdown"
            
    def test_dropdown_keyboard_navigation(self, page: Page):
        """
        Test keyboard navigation through dropdown menus
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Focus on Solutions menu
        solutions_button = page.locator('button:has-text("Solutions")').first
        solutions_button.focus()
        
        # Open with Enter key
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)
        
        dropdown = page.locator('[role="menu"], .dropdown-menu').first
        
        if dropdown.is_visible():
            # Navigate with arrow keys
            page.keyboard.press('ArrowDown')
            page.wait_for_timeout(100)
            page.keyboard.press('ArrowDown')
            page.wait_for_timeout(100)
            
            # Check if item is focused
            focused = page.locator(':focus').first
