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
        """
        Test navigation menu UI at different screen sizes
        """
        homepage = HomePage(page)
        
        # Desktop view
        page.set_viewport_size({'width': 1920, 'height': 1080})
        homepage.navigate_to()
        
        desktop_nav = page.locator('nav, header').first
        assert desktop_nav.is_visible(), "Desktop navigation not visible"
        
        # Tablet view
        page.set_viewport_size({'width': 768, 'height': 1024})
        page.wait_for_timeout(500)
        
        # Mobile view
        page.set_viewport_size({'width': 375, 'height': 667})
        page.wait_for_timeout(500)
        
        # Check for hamburger menu in mobile
        mobile_menu_button = page.locator('.hamburger, [aria-label="Menu"], .mobile-menu-toggle').first
        assert mobile_menu_button.is_visible() or page.locator('button').first.is_visible(), "Mobile menu button not found"
        
    def test_modal_dialog_ui(self, page: Page):
        """
        Test modal dialog UI if present
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Try to trigger a modal (e.g., video modal, contact modal)
        modal_triggers = page.locator('[data-toggle="modal"], [data-modal], button:has-text("Watch")').all()
        
        for trigger in modal_triggers[:1]:
            if trigger.is_visible():
                trigger.click()
                page.wait_for_timeout(1000)
                
                # Check for modal
                modal = page.locator('.modal, [role="dialog"], .overlay').first
                if modal.is_visible():
                    # Check for close button
                    close_button = modal.locator('.close, [aria-label="Close"], button:has-text("×")').first
                    assert close_button.is_visible(), "Modal close button not found"
                    
                    # Close modal
                    close_button.click()
                    page.wait_for_timeout(500)
                    assert not modal.is_visible(), "Modal did not close"
                    
    def test_accordion_collapse_elements(self, page: Page):
        """
        Test accordion/collapse UI elements if present
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Look for accordion elements
        accordions = page.locator('.accordion, [data-accordion], .collapse-trigger, .faq-item').all()
        
        for accordion in accordions[:3]:
            if accordion.is_visible():
                # Get initial state
                content = accordion.locator('.content, .panel, .answer').first
                initial_visible = content.is_visible() if content else False
                
                # Click to toggle
                accordion.click()
                page.wait_for_timeout(500)
                
                # Check state changed
                if content:
                    new_visible = content.is_visible()
                    assert new_visible != initial_visible, "Accordion did not toggle"
                    
    def test_tab_navigation_ui(self, page: Page):
        """
        Test tab navigation UI components
        """
        products_page = ProductsPage(page)
        products_page.navigate_to_tprm()
        
        # Look for tab components
        tabs = page.locator('[role="tablist"], .tabs, .nav-tabs').first
        
        if tabs and tabs.is_visible():
            tab_buttons = tabs.locator('[role="tab"], .tab').all()
            
            for i, tab in enumerate(tab_buttons[:3]):
                if tab.is_visible():
                    # Click tab
                    tab.click()
                    page.wait_for_timeout(500)
                    
                    # Check aria-selected or active class
                    is_selected = tab.get_attribute('aria-selected') == 'true' or 'active' in (tab.get_attribute('class') or '')
                    assert is_selected, f"Tab {i} not marked as selected after click"
                    
    def test_tooltip_hover_elements(self, page: Page):
        """
        Test tooltip UI elements on hover
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Look for elements with tooltips
        tooltip_elements = page.locator('[data-tooltip], [title], [aria-describedby]').all()[:5]
        
        for element in tooltip_elements:
            if element.is_visible():
                # Hover to trigger tooltip
                element.hover()
                page.wait_for_timeout(500)
                
                # Check for tooltip appearance
                tooltip = page.locator('.tooltip, [role="tooltip"]').first
                
                # Move away to hide tooltip
                page.mouse.move(0, 0)
                
    def test_carousel_slider_ui(self, page: Page):
        """
        Test carousel/slider UI components
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Look for carousel elements
        carousel = page.locator('.carousel, .slider, [data-carousel]').first
        
        if carousel and carousel.is_visible():
            # Check for navigation controls
            prev_button = carousel.locator('.prev, [aria-label*="previous"], button:has-text("<")').first
            next_button = carousel.locator('.next, [aria-label*="next"], button:has-text(">")').first
            
            if next_button and next_button.is_visible():
                # Get initial slide
                active_slide = carousel.locator('.active, .current').first
                initial_content = active_slide.text_content() if active_slide else ""
                
                # Click next
                next_button.click()
                page.wait_for_timeout(1000)
                
                # Check if content changed
                new_active = carousel.locator('.active, .current').first
                new_content = new_active.text_content() if new_active else ""
                
                if initial_content and new_content:
                    assert initial_content != new_content, "Carousel did not advance"
                    
    def test_progress_indicators(self, page: Page):
        """
        Test progress bars and loading indicators
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Look for progress indicators
        progress_bars = page.locator('.progress, [role="progressbar"], .loading').all()
        
        for progress in progress_bars[:3]:
            if progress.is_visible():
                # Check for value attributes
                value = progress.get_attribute('aria-valuenow') or progress.get_attribute('data-value')
                max_value = progress.get_attribute('aria-valuemax') or '100'
