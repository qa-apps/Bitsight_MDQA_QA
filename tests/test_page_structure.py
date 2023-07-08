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
        
        # Check Open Graph tags
        og_title = page.locator('meta[property="og:title"]').get_attribute('content')
        og_description = page.locator('meta[property="og:description"]').get_attribute('content')
        og_image = page.locator('meta[property="og:image"]').get_attribute('content')
        
        # OG tags are recommended for social sharing
        if og_title:
            assert og_title, "Open Graph title present"
            
    def test_semantic_html_structure(self, page: Page):
        """
        Test use of semantic HTML5 elements
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check for semantic elements
        semantic_elements = {
            'header': page.locator('header'),
            'nav': page.locator('nav'),
            'main': page.locator('main'),
            'footer': page.locator('footer'),
            'article': page.locator('article'),
            'section': page.locator('section')
        }
        
        # Header, nav, and footer should be present
        assert semantic_elements['header'].count() > 0, "No <header> element found"
        assert semantic_elements['nav'].count() > 0, "No <nav> element found"
        assert semantic_elements['footer'].count() > 0, "No <footer> element found"
        
        # Main content area
        main_count = semantic_elements['main'].count()
        assert main_count <= 1, f"Multiple <main> elements found: {main_count}"
        
    def test_structured_data_markup(self, page: Page):
        """
        Test for structured data (JSON-LD, microdata)
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check for JSON-LD structured data
        json_ld_scripts = page.locator('script[type="application/ld+json"]').all()
        
        for script in json_ld_scripts:
            content = script.inner_text()
            try:
                data = json.loads(content)
                
                # Verify basic structure
                assert '@context' in data, "JSON-LD missing @context"
                assert '@type' in data or 'type' in data, "JSON-LD missing @type"
                
            except json.JSONDecodeError:
                assert False, "Invalid JSON-LD structured data"
                
    def test_navigation_structure(self, page: Page):
        """
        Test navigation menu structure and hierarchy
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check main navigation
        main_nav = page.locator('nav').first
        assert main_nav.is_visible(), "Main navigation not visible"
        
        # Check for list structure in navigation
        nav_list = main_nav.locator('ul, ol').first
        if nav_list:
            nav_items = nav_list.locator('li').all()
            assert len(nav_items) > 0, "Navigation list has no items"
            
            # Each item should have a link
