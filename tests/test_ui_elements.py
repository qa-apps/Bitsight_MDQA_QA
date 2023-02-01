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
