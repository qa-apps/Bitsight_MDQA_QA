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
