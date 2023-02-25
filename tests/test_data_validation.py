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
        ]
        
        meta_data = {}
        
        for path, name in pages_to_test:
            page.goto(f"https://www.bitsight.com{path}", wait_until='domcontentloaded')
            
            # Collect meta data
            title = page.title()
            description = page.locator('meta[name="description"]').get_attribute('content')
            og_title = page.locator('meta[property="og:title"]').get_attribute('content')
            og_description = page.locator('meta[property="og:description"]').get_attribute('content')
            
            meta_data[name] = {
                'title': title,
                'description': description,
                'og_title': og_title,
                'og_description': og_description
            }
            
            # Validate individual page meta
            assert title and len(title) > 10, f"{name} missing or short title"
            assert description and len(description) > 50, f"{name} missing or short description"
            
        # Check for uniqueness
        titles = [data['title'] for data in meta_data.values() if data['title']]
        assert len(titles) == len(set(titles)), "Duplicate page titles found"
        
        descriptions = [data['description'] for data in meta_data.values() if data['description']]
        assert len(descriptions) == len(set(descriptions)), "Duplicate meta descriptions found"
        
    def test_link_data_integrity(self, page: Page):
        """
        Test link data integrity and validity
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Get all links
        links = page.locator('a[href]').all()[:30]
        
        link_data = []
        
        for link in links:
            if link.is_visible():
                href = link.get_attribute('href')
                text = link.text_content()
                title = link.get_attribute('title')
                target = link.get_attribute('target')
                
                link_data.append({
                    'href': href,
                    'text': text,
                    'title': title,
                    'target': target
                })
                
                # Validate link data
                assert href, "Link missing href attribute"
                
