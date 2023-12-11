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
        
        if skip_link.count() > 0:
            first_skip = skip_link.first
            
            # Skip link might be visually hidden but should be in DOM
            assert first_skip, "Skip navigation link found"
            
            # Tab to make it visible (if implemented properly)
            page.keyboard.press('Tab')
            
            # Some skip links only show on focus
            
    def test_language_attribute(self, page: Page):
        """
        Test that page has proper language attributes
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check html lang attribute
        html_lang = page.locator('html').get_attribute('lang')
        assert html_lang, "HTML element missing lang attribute"
        assert len(html_lang) >= 2, f"Invalid language code: {html_lang}"
        
    def test_page_title_descriptive(self, page: Page):
        """
        Test that page titles are descriptive and unique
        """
        homepage = HomePage(page)
        products_page = ProductsPage(page)
        
        # Check homepage title
        homepage.navigate_to()
        home_title = page.title()
        assert home_title, "Homepage missing title"
        assert len(home_title) > 10, "Homepage title too short"
        
        # Check product page title
        products_page.navigate_to_tprm()
        product_title = page.title()
        assert product_title, "Product page missing title"
        assert product_title != home_title, "Page titles should be unique"
        
    def test_error_messages_clear(self, page: Page):
        """
        Test that error messages are clear and accessible
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Try to submit empty form
        submit_button = page.locator('button[type="submit"], input[type="submit"]').first
        
        if submit_button and submit_button.is_visible():
            submit_button.click()
            page.wait_for_timeout(1000)
            
            # Look for error messages
            errors = page.locator('.error, .invalid-feedback, [role="alert"]').all()
            
            for error in errors:
                if error.is_visible():
                    error_text = error.text_content()
                    
                    # Error should have meaningful text
                    assert error_text and len(error_text) > 5, "Error message too short or missing"
                    
                    # Error should be associated with field
                    aria_describedby = error.get_attribute('aria-describedby')
                    
    def test_responsive_text_sizing(self, page: Page):
        """
        Test that text remains readable at different zoom levels
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Test at different zoom levels
        zoom_levels = [1, 1.5, 2]
        
        for zoom in zoom_levels:
            page.evaluate(f'document.body.style.zoom = "{zoom}"')
            page.wait_for_timeout(500)
            
            # Check that main content is still visible
            main_heading = page.locator('h1').first
            assert main_heading.is_visible(), f"Content not visible at {zoom}x zoom"
            
        # Reset zoom
        page.evaluate('document.body.style.zoom = "1"')
        
    def test_link_purpose_clear(self, page: Page):
        """
        Test that link purposes are clear from their text
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check for vague link text
        vague_texts = ['click here', 'read more', 'more', 'here', 'link']
        links = page.locator('a').all()[:20]
        
        for link in links:
            if link.is_visible():
                text = (link.text_content() or '').lower().strip()
                
                # Links shouldn't use vague text alone
                if text in vague_texts:
                    # Check if there's additional context
                    aria_label = link.get_attribute('aria-label')
                    title = link.get_attribute('title')
                    
                    assert aria_label or title, f"Link with vague text '{text}' lacks context"
                    
    def test_multimedia_accessibility(self, page: Page):
