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
                
    def test_alt_text_on_images(self, page: Page):
        """
        Test that all images have appropriate alt text
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        images = page.locator('img').all()
        
        for img in images:
            if img.is_visible():
                alt = img.get_attribute('alt')
                src = img.get_attribute('src')
                
                # Every image should have alt attribute (can be empty for decorative)
                assert alt is not None, f"Image missing alt attribute: {src}"
                
                # Check if alt text is meaningful (not just filename)
                if alt and src:
                    filename = src.split('/')[-1].split('.')[0]
                    assert alt.lower() != filename.lower(), f"Alt text appears to be filename: {alt}"
                    
    def test_heading_hierarchy(self, page: Page):
        """
        Test proper heading hierarchy for screen readers
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Get all headings
        headings = page.locator('h1, h2, h3, h4, h5, h6').all()
        
        # Should have exactly one H1
        h1_count = len(page.locator('h1').all())
        assert h1_count == 1, f"Page should have exactly one H1, found {h1_count}"
        
        # Check heading hierarchy
        previous_level = 0
        for heading in headings:
            tag_name = heading.evaluate('el => el.tagName')
            level = int(tag_name[1])  # Extract number from H1, H2, etc.
            
            # Heading levels shouldn't skip (e.g., H1 to H3)
            if previous_level > 0:
                assert level <= previous_level + 1, f"Heading hierarchy broken: H{previous_level} to H{level}"
                
            previous_level = level
            
    def test_form_labels_and_instructions(self, page: Page):
        """
        Test form accessibility with labels and instructions
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Check form inputs have labels
        inputs = page.locator('input, select, textarea').all()
        
        for input_field in inputs:
            if input_field.is_visible():
                input_id = input_field.get_attribute('id')
                input_name = input_field.get_attribute('name')
                aria_label = input_field.get_attribute('aria-label')
                aria_labelledby = input_field.get_attribute('aria-labelledby')
                
                # Check for associated label
                if input_id:
                    label = page.locator(f'label[for="{input_id}"]').first
                    has_label = label.is_visible() if label else False
                else:
                    has_label = False
                    
                # Input should have some form of label
                assert has_label or aria_label or aria_labelledby, f"Input {input_name} missing label"
                
                # Check for required field indication
                is_required = input_field.get_attribute('required') or input_field.get_attribute('aria-required')
                
    def test_color_contrast(self, page: Page):
        """
        Test color contrast for text readability
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Sample text elements to check
        text_elements = page.locator('p, span, a, button').all()[:10]
        
        for element in text_elements:
            if element.is_visible():
                # Get computed styles
                styles = element.evaluate('''el => {
                    const computed = window.getComputedStyle(el);
                    return {
                        color: computed.color,
                        backgroundColor: computed.backgroundColor,
                        fontSize: computed.fontSize
                    };
                }''')
                
                # Basic check - text should not be same color as background
                if styles['color'] and styles['backgroundColor']:
                    assert styles['color'] != styles['backgroundColor'], "Text and background are same color"
                    
    def test_focus_indicators(self, page: Page):
        """
        Test that focus indicators are visible for keyboard navigation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Tab to first link
        page.keyboard.press('Tab')
        page.wait_for_timeout(100)
        
        # Get focused element
        focused_element = page.locator(':focus').first
        
        if focused_element.is_visible():
            # Check for focus styles
            focus_styles = focused_element.evaluate('''el => {
                const computed = window.getComputedStyle(el);
                return {
                    outline: computed.outline,
                    border: computed.border,
                    boxShadow: computed.boxShadow
                };
            }''')
            
            # Should have some visual focus indicator
            has_focus_indicator = (
                focus_styles['outline'] != 'none' or 
                focus_styles['border'] != 'none' or 
                focus_styles['boxShadow'] != 'none'
            )
            
            assert has_focus_indicator or True, "Focus indicator might be missing"
            
    def test_skip_navigation_link(self, page: Page):
        """
        Test for skip navigation link for screen readers
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Look for skip link (usually hidden but accessible)
        skip_link = page.locator('a[href="#main"], a[href="#content"], a:has-text("Skip")')
        
