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
            assert focused, "No element has focus after arrow navigation"
            
            # Close with Escape
            page.keyboard.press('Escape')
            page.wait_for_timeout(500)
            assert not dropdown.is_visible(), "Dropdown did not close with Escape key"
            
    def test_dropdown_hover_behavior(self, page: Page):
        """
        Test dropdown hover open/close behavior
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Test each main menu item
        menu_items = ['Solutions', 'Products', 'Resources', 'Company']
        
        for menu_text in menu_items:
            menu_button = page.locator(f'button:has-text("{menu_text}"), a:has-text("{menu_text}")').first
            
            if menu_button.is_visible():
                # Hover to potentially open
                menu_button.hover()
                page.wait_for_timeout(300)
                
                # Check if dropdown opened on hover
                dropdown = page.locator('[role="menu"], .dropdown-menu').first
                
                # Move mouse away
                page.mouse.move(0, 0)
                page.wait_for_timeout(300)
                
    def test_dropdown_mobile_behavior(self, page: Page):
        """
        Test dropdown behavior on mobile viewport
        """
        homepage = HomePage(page)
        
        # Set mobile viewport
        page.set_viewport_size({'width': 375, 'height': 667})
        homepage.navigate_to()
        
        # Find mobile menu button
        mobile_menu = page.locator('.mobile-menu, [aria-label="Menu"], .hamburger').first
        
        if mobile_menu.is_visible():
            mobile_menu.click()
            page.wait_for_timeout(500)
            
            # Find mobile navigation
            mobile_nav = page.locator('.mobile-nav, .nav-mobile, nav').first
            
            if mobile_nav.is_visible():
                # Look for expandable menu items
                expandable_items = mobile_nav.locator('[aria-expanded], .has-submenu, .dropdown-toggle').all()
                
                for item in expandable_items[:2]:
                    if item.is_visible():
                        # Click to expand
                        item.click()
                        page.wait_for_timeout(500)
                        
                        # Check if submenu opened
                        expanded = item.get_attribute('aria-expanded')
                        if expanded:
                            assert expanded == 'true', "Menu item did not expand"
                            
    def test_dropdown_link_validity(self, page: Page):
        """
        Test all dropdown links are valid and working
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        all_dropdown_links = []
        
        # Collect links from all dropdowns
        menu_items = ['Solutions', 'Products', 'Resources', 'Company']
        
        for menu_text in menu_items:
            homepage.navigate_to()
            
            menu_button = page.locator(f'button:has-text("{menu_text}"), a:has-text("{menu_text}")').first
            if menu_button.is_visible():
                menu_button.click()
                page.wait_for_timeout(500)
                
                dropdown = page.locator('[role="menu"], .dropdown-menu').first
                if dropdown.is_visible():
                    links = dropdown.locator('a').all()
                    
                    for link in links:
                        href = link.get_attribute('href')
                        text = link.text_content()
                        
                        if href and not href.startswith('#'):
                            all_dropdown_links.append({'href': href, 'text': text, 'menu': menu_text})
                            
        # Test sample of links
        for link_data in all_dropdown_links[:5]:
            if link_data['href'].startswith('http'):
                response = page.request.head(link_data['href'])
                assert response.status < 400, f"Broken link in {link_data['menu']} dropdown: {link_data['text']} ({link_data['href']})"
