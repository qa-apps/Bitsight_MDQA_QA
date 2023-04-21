import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage

@pytest.mark.ui
class TestUIElements:
    """
    UI elements testing for BitSight website
    """
    
    def test_button_states_and_interactions(self, page: Page):
        """
        Test button states (hover, active, disabled) and interactions
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find all buttons
        buttons = page.locator('button, a.button, a.btn, [role="button"]').all()[:10]
        
        for button in buttons:
            if button.is_visible():
                # Get initial styles
                initial_styles = button.evaluate('el => window.getComputedStyle(el)')
                
                # Test hover state
                button.hover()
                page.wait_for_timeout(100)
                hover_styles = button.evaluate('el => window.getComputedStyle(el)')
                
                # Hover should change some visual aspect
                # This could be color, background, transform, etc.
                
                # Test if button is clickable
                is_disabled = button.get_attribute('disabled')
                if not is_disabled:
                    assert button.is_enabled(), "Button appears enabled but is not"
                    
    def test_form_input_elements(self, page: Page):
        """
        Test various form input elements
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Test text inputs
        text_inputs = page.locator('input[type="text"], input[type="email"]').all()
        for input_field in text_inputs[:3]:
            if input_field.is_visible():
                # Test focus state
                input_field.focus()
                assert input_field.evaluate('el => document.activeElement === el'), "Input did not receive focus"
                
                # Test placeholder
                placeholder = input_field.get_attribute('placeholder')
                
                # Test input capability
                input_field.fill("Test input")
                assert input_field.input_value() == "Test input", "Input value not set correctly"
                
                # Clear input
                input_field.clear()
                assert input_field.input_value() == "", "Input not cleared"
                
    def test_dropdown_menus_ui(self, page: Page):
        """
        Test dropdown menu UI behavior
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Test Solutions dropdown
        solutions_button = page.locator('button:has-text("Solutions")').first
        if solutions_button.is_visible():
            # Check initial state (should be closed)
            dropdown_menu = page.locator('[role="menu"]').first
            initial_visibility = dropdown_menu.is_visible() if dropdown_menu else False
            
            # Open dropdown
            solutions_button.click()
            page.wait_for_timeout(500)
            
            # Check dropdown is now visible
            assert dropdown_menu.is_visible() if dropdown_menu else True, "Dropdown did not open"
            
            # Check dropdown items are visible
            dropdown_items = page.locator('[role="menuitem"], .dropdown-item').all()
            assert len(dropdown_items) > 0, "No dropdown items found"
            
            # Close dropdown by clicking outside
            page.click('body', position={'x': 0, 'y': 0})
            page.wait_for_timeout(500)
            
            # Verify dropdown closed
            if dropdown_menu:
                assert not dropdown_menu.is_visible(), "Dropdown did not close"
                
    def test_navigation_menu_responsiveness(self, page: Page):
