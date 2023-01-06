import pytest
from playwright.sync_api import Page, expect
from pages.home_page_real import HomePageReal
from pages.products_page import ProductsPage
import json
import re

@pytest.mark.data
class TestDataValidation:
    """
    Data validation and integrity testing for BitSight website
    """
    
    def test_json_ld_structured_data(self, page: Page):
        """
        Test JSON-LD structured data validity
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Extract JSON-LD data
        json_ld_scripts = page.locator('script[type="application/ld+json"]').all()
        
        for script in json_ld_scripts:
            content = script.inner_text()
            
            try:
                # Parse JSON
                data = json.loads(content)
                
                # Validate required fields
                assert '@context' in data, "JSON-LD missing @context"
                assert '@type' in data or 'type' in data, "JSON-LD missing @type"
                
                # Check for organization data
                if data.get('@type') == 'Organization' or data.get('type') == 'Organization':
                    assert 'name' in data, "Organization missing name"
                    assert data.get('name', '').lower() == 'bitsight' or 'bitsight' in data.get('name', '').lower(), "Organization name incorrect"
                    
                    # Check for contact info
                    if 'contactPoint' in data:
                        contact = data['contactPoint']
                        assert 'contactType' in contact or '@type' in contact, "Contact point missing type"
                        
                # Check for website data
                if data.get('@type') == 'WebSite' or data.get('type') == 'WebSite':
                    assert 'url' in data, "Website missing URL"
                    assert 'bitsight.com' in data.get('url', ''), "Website URL incorrect"
                    
            except json.JSONDecodeError as e:
                assert False, f"Invalid JSON-LD data: {e}"
                
    def test_meta_data_consistency(self, page: Page):
        """
        Test meta data consistency across pages
        """
        pages_to_test = [
            ('/', 'Homepage'),
            ('/products/third-party-risk-management', 'TPRM'),
            ('/resources', 'Resources')
