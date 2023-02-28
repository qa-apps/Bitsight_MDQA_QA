import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
import json

@pytest.mark.structure
class TestPageStructure:
    """
    Page structure and validation tests for BitSight website
    """
    
    def test_html_structure_validity(self, page: Page):
        """
        Test HTML structure and DOCTYPE
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check for DOCTYPE
        has_doctype = page.evaluate('() => document.doctype !== null')
        assert has_doctype, "Page missing DOCTYPE declaration"
        
        # Check HTML5 structure
        html = page.locator('html').first
        assert html, "HTML element not found"
        
        # Check for head and body
        head = page.locator('head').first
        body = page.locator('body').first
        
        assert head, "HEAD element not found"
        assert body, "BODY element not found"
        
    def test_meta_tags_present(self, page: Page):
        """
        Test presence of important meta tags
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check viewport meta tag
        viewport = page.locator('meta[name="viewport"]').get_attribute('content')
        assert viewport, "Viewport meta tag missing"
        assert 'width' in viewport, "Viewport missing width setting"
        
        # Check charset
        charset = page.locator('meta[charset]').get_attribute('charset')
        if not charset:
            charset = page.locator('meta[http-equiv="Content-Type"]').get_attribute('content')
        assert charset, "Character encoding not specified"
        
        # Check description
        description = page.locator('meta[name="description"]').get_attribute('content')
        assert description, "Meta description missing"
        assert len(description) > 50, "Meta description too short"
        assert len(description) < 160, "Meta description too long"
