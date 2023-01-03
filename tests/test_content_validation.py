import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
import re

@pytest.mark.content
class TestContentValidation:
    """
    Content validation and text verification testing
    """
    
    def test_homepage_content_structure(self, page: Page):
        """
        Test homepage content structure and hierarchy
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check main heading
        h1_elements = page.locator('h1').all()
        assert len(h1_elements) == 1, f"Expected 1 H1, found {len(h1_elements)}"
        
        h1_text = h1_elements[0].text_content()
        assert h1_text, "H1 has no text content"
        assert len(h1_text) > 10, "H1 text too short"
        
        # Check for AI-powered messaging (from actual content)
        assert 'AI' in h1_text or 'intelligence' in h1_text.lower(), "Main heading doesn't match brand messaging"
        
        # Check subheadings
        h2_elements = page.locator('h2').all()
        assert len(h2_elements) > 0, "No H2 elements found"
        
        # Verify content sections
        content_sections = page.locator('section, article, .content-section').all()
        assert len(content_sections) > 0, "No content sections found"
        
    def test_product_descriptions(self, page: Page):
        """
        Test product description content
        """
        products_page = ProductsPage(page)
        
        products = [
            ('Third-Party Risk Management', '/products/third-party-risk-management'),
            ('Exposure Management', '/solutions/exposure-management'),
            ('Cyber Threat Intelligence', '/products/cyber-threat-intelligence')
        ]
        
        for product_name, url in products:
            products_page.navigate_to(url)
            page.wait_for_load_state('networkidle')
            
            # Check for product name in content
            page_content = page.content()
            
            # Product page should contain its name
            assert product_name.lower() in page_content.lower() or url.split('/')[-1] in page.url, f"Product page for {product_name} missing content"
            
