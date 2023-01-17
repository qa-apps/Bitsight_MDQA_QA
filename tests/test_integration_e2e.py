import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from faker import Faker

fake = Faker()

@pytest.mark.e2e
@pytest.mark.slow
class TestIntegrationE2E:
    """
    End-to-end integration testing for complete user journeys
    """
    
    def test_complete_demo_request_journey(self, page: Page):
        """
        Test complete journey from homepage to demo request
        """
        homepage = HomePage(page)
        
        # Step 1: Land on homepage
        homepage.navigate_to()
        assert homepage.is_homepage_loaded(), "Homepage failed to load"
        
        # Step 2: Explore product information
        products_page = ProductsPage(page)
        products_page.navigate_to_tprm()
        page.wait_for_load_state('networkidle')
        
        assert 'third-party' in page.url.lower() or 'tprm' in page.url.lower(), "Did not navigate to TPRM page"
        
        # Step 3: Click Request Demo
        demo_button = page.locator('a:has-text("Request"), a:has-text("Demo")').first
        if demo_button.is_visible():
            demo_button.click()
            page.wait_for_load_state('networkidle')
            
            # Step 4: Fill demo form
            form = page.locator('form').first
            
            if form.is_visible():
                # Fill form fields
                form_data = {
                    'first': fake.first_name(),
                    'last': fake.last_name(),
                    'email': fake.email(),
                    'company': fake.company(),
                    'phone': fake.phone_number()
                }
                
                for field_hint, value in form_data.items():
                    field = form.locator(f'input[name*="{field_hint}"], input[placeholder*="{field_hint}"]').first
                    if field and field.is_visible():
                        field.fill(value)
                        
                # Note: Not submitting to avoid creating test data
                
        # Step 5: Navigate back to homepage
        homepage.navigate_to()
