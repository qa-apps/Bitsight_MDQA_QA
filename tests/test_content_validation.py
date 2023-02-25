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
            
            # Check for key product features
            features_keywords = ['features', 'benefits', 'capabilities', 'solutions']
            found_keywords = [kw for kw in features_keywords if kw in page_content.lower()]
            
            assert len(found_keywords) > 0, f"Product page {product_name} missing feature descriptions"
            
    def test_contact_information_presence(self, page: Page):
        """
        Test presence of contact information
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check footer for contact info
        footer = page.locator('footer').first
        footer_text = footer.text_content() if footer else ''
        
        # Look for contact indicators
        contact_indicators = ['contact', 'email', 'phone', 'address', 'support']
        found_indicators = [ind for ind in contact_indicators if ind in footer_text.lower()]
        
        assert len(found_indicators) > 0, "No contact information found in footer"
        
        # Check for contact page link
        contact_link = page.locator('a:has-text("Contact")').first
        assert contact_link.is_visible() or 'contact' in footer_text.lower(), "No contact link found"
        
    def test_copyright_information(self, page: Page):
        """
        Test copyright and legal information
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        footer = page.locator('footer').first
        footer_text = footer.text_content() if footer else ''
        
        # Check for copyright symbol
        assert '©' in footer_text or 'copyright' in footer_text.lower(), "Copyright information missing"
        
        # Check for current or recent year
        import datetime
        current_year = datetime.datetime.now().year
        years_to_check = [str(current_year), str(current_year - 1)]
        
        year_found = any(year in footer_text for year in years_to_check)
        assert year_found, f"Copyright year not current (expected {current_year})"
        
        # Check for company name
        assert 'bitsight' in footer_text.lower(), "Company name not in copyright"
        
    def test_privacy_policy_link(self, page: Page):
        """
        Test privacy policy link and content
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find privacy policy link
        privacy_link = page.locator('a:has-text("Privacy")').first
