import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage

@pytest.mark.usability
class TestUsabilityAccessibility:
    """
    Usability and accessibility testing for BitSight website
    """
    
    def test_keyboard_navigation(self, page: Page):
        """
        Test keyboard navigation through the website
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Tab through first 10 interactive elements
        for i in range(10):
            page.keyboard.press('Tab')
            page.wait_for_timeout(100)
            
            # Check if an element has focus
            focused_element = page.evaluate('() => document.activeElement')
            assert focused_element, f"No element focused after {i+1} Tab presses"
            
        # Test Enter key on focused link
        page.keyboard.press('Enter')
        page.wait_for_timeout(1000)
        
        # Should navigate or perform action
        
    def test_aria_labels_present(self, page: Page):
        """
        Test that interactive elements have appropriate ARIA labels
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check buttons
        buttons = page.locator('button').all()[:10]
        for button in buttons:
            if button.is_visible():
                text = button.text_content()
                aria_label = button.get_attribute('aria-label')
                aria_labelledby = button.get_attribute('aria-labelledby')
                
                # Button should have accessible name
                assert text or aria_label or aria_labelledby, "Button missing accessible label"
                
        # Check links
        links = page.locator('a').all()[:10]
        for link in links:
            if link.is_visible():
                text = link.text_content()
                aria_label = link.get_attribute('aria-label')
                
                # Links should have meaningful text
                assert text or aria_label, "Link missing accessible text"
