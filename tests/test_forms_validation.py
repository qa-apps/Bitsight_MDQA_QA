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
