import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from faker import Faker
import re

fake = Faker()

@pytest.mark.forms
class TestFormsValidation:
    """
    Comprehensive form validation and submission testing
    """
    
    def test_demo_form_field_validation(self, page: Page):
        """
        Test demo request form field validation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Find form
        form = page.locator('form').first
        
        if form.is_visible():
            # Test required field validation
            submit_button = form.locator('button[type="submit"], input[type="submit"]').first
            
            if submit_button.is_visible():
                # Click submit without filling fields
                submit_button.click()
                page.wait_for_timeout(1000)
                
                # Check for validation messages
                error_messages = page.locator('.error, .invalid, [aria-invalid="true"], .error-message').all()
                required_indicators = page.locator('[required], [aria-required="true"]').all()
                
                assert len(error_messages) > 0 or len(required_indicators) > 0, "No validation on empty form submission"
                
    def test_email_field_validation(self, page: Page):
        """
        Test email field format validation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        email_field = page.locator('input[type="email"], input[name*="email"]').first
        
        if email_field and email_field.is_visible():
            # Test invalid email formats
            invalid_emails = [
                'notanemail',
                '@nodomain.com',
                'missing@',
                'spaces in@email.com',
                'double@@email.com'
            ]
            
            for invalid_email in invalid_emails:
                email_field.fill(invalid_email)
                email_field.blur()  # Trigger validation
                page.wait_for_timeout(500)
                
                # Check for validation state
                is_invalid = email_field.get_attribute('aria-invalid') == 'true'
                has_error_class = 'error' in (email_field.get_attribute('class') or '')
                
                # Clear for next test
                email_field.clear()
                
    def test_phone_field_validation(self, page: Page):
        """
        Test phone number field validation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        phone_field = page.locator('input[type="tel"], input[name*="phone"]').first
        
        if phone_field and phone_field.is_visible():
            # Test various phone formats
            phone_numbers = [
                '123-456-7890',
                '(123) 456-7890',
                '+1 123 456 7890',
                '1234567890',
                'invalid phone'
            ]
            
            for phone in phone_numbers:
                phone_field.fill(phone)
                phone_field.blur()
                page.wait_for_timeout(200)
                
                # Validation depends on implementation
                phone_field.clear()
                
    def test_form_field_character_limits(self, page: Page):
        """
        Test character limits on form fields
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Test text input limits
        text_fields = page.locator('input[type="text"], input[type="email"]').all()
        
        for field in text_fields[:3]:
            if field.is_visible():
                # Try to input very long string
                long_text = 'a' * 500
                field.fill(long_text)
                
                # Get actual value
                actual_value = field.input_value()
                
                # Check if there's a max length
                max_length = field.get_attribute('maxlength')
                if max_length:
                    assert len(actual_value) <= int(max_length), f"Field exceeded maxlength of {max_length}"
                    
                field.clear()
                
    def test_dropdown_selection(self, page: Page):
        """
        Test dropdown/select field functionality
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Find select elements
        selects = page.locator('select').all()
        
        for select in selects:
            if select.is_visible():
                # Get options
                options = select.locator('option').all()
                
                if len(options) > 1:
                    # Select second option
                    select.select_option(index=1)
                    
                    # Verify selection
                    selected_value = select.input_value()
                    assert selected_value, "No value selected from dropdown"
                    
    def test_checkbox_and_radio_buttons(self, page: Page):
        """
        Test checkbox and radio button functionality
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Test checkboxes
        checkboxes = page.locator('input[type="checkbox"]').all()
        
        for checkbox in checkboxes[:3]:
            if checkbox.is_visible():
                # Check the checkbox
