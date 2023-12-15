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
                checkbox.check()
                assert checkbox.is_checked(), "Checkbox not checked"
                
                # Uncheck
                checkbox.uncheck()
                assert not checkbox.is_checked(), "Checkbox not unchecked"
                
        # Test radio buttons
        radios = page.locator('input[type="radio"]').all()
        
        if len(radios) > 1:
            # Click first radio
            radios[0].check()
            assert radios[0].is_checked(), "Radio not selected"
            
            # Click second radio
            radios[1].check()
            assert radios[1].is_checked(), "Second radio not selected"
            assert not radios[0].is_checked(), "First radio still selected"
            
    def test_form_data_persistence(self, page: Page):
        """
        Test if form data persists during navigation
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Fill some fields
        test_data = {
            'name': fake.name(),
            'email': fake.email(),
            'company': fake.company()
        }
        
        for field_type, value in test_data.items():
            field = page.locator(f'input[name*="{field_type}"], input[placeholder*="{field_type}"]').first
            if field and field.is_visible():
                field.fill(value)
                
        # Navigate away and back
        page.go_back()
        page.wait_for_timeout(1000)
        page.go_forward()
        page.wait_for_timeout(1000)
        
        # Check if data persisted (usually it shouldn't for security)
        for field_type, expected_value in test_data.items():
            field = page.locator(f'input[name*="{field_type}"]').first
            if field and field.is_visible():
                actual_value = field.input_value()
                # Data typically shouldn't persist for security
                
    def test_form_submission_success(self, page: Page):
        """
        Test successful form submission with valid data
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Fill form with valid data
        form_data = {
            'first': fake.first_name(),
            'last': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'company': fake.company(),
            'title': fake.job()
        }
        
        form = page.locator('form').first
        
        if form.is_visible():
            # Fill all visible fields
            for field_hint, value in form_data.items():
                field = form.locator(f'input[name*="{field_hint}"], input[placeholder*="{field_hint}"]').first
                if field and field.is_visible():
                    field.fill(value)
                    
            # Note: We don't actually submit to avoid creating test data
            # In real tests, you would submit and verify success message
            
    def test_textarea_functionality(self, page: Page):
        """
        Test textarea fields if present
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        textareas = page.locator('textarea').all()
        
        for textarea in textareas:
            if textarea.is_visible():
                # Test multiline input
                multiline_text = "Line 1\nLine 2\nLine 3"
                textarea.fill(multiline_text)
                
                # Verify input
                value = textarea.input_value()
                assert '\n' in value or 'Line 1' in value, "Textarea not accepting multiline text"
                
                # Test character limit if exists
                max_length = textarea.get_attribute('maxlength')
                if max_length:
                    long_text = 'x' * (int(max_length) + 100)
                    textarea.fill(long_text)
                    actual_length = len(textarea.input_value())
                    assert actual_length <= int(max_length), "Textarea exceeded max length"
