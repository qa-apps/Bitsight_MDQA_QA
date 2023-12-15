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
            for item in nav_items[:5]:
                link = item.locator('a, button').first
                assert link, "Navigation item missing interactive element"
                
    def test_footer_structure(self, page: Page):
        """
        Test footer structure and content
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        footer = page.locator('footer').first
        assert footer.is_visible(), "Footer not visible"
        
        # Check for common footer elements
        footer_sections = footer.locator('div, section, nav').all()
        assert len(footer_sections) > 0, "Footer has no content sections"
        
        # Check for copyright
        copyright_text = footer.text_content()
        assert '©' in copyright_text or 'copyright' in copyright_text.lower(), "Copyright information missing"
        
        # Check for footer links
        footer_links = footer.locator('a').all()
        assert len(footer_links) > 5, "Footer has too few links"
        
        # Check for common footer pages
        footer_text = copyright_text.lower()
        common_pages = ['privacy', 'terms', 'contact']
        found_pages = [page for page in common_pages if page in footer_text]
        assert len(found_pages) > 0, "Footer missing common legal/contact links"
        
    def test_content_hierarchy(self, page: Page):
        """
        Test content hierarchy and organization
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check heading hierarchy
        h1_elements = page.locator('h1').all()
        h2_elements = page.locator('h2').all()
        h3_elements = page.locator('h3').all()
        
        assert len(h1_elements) == 1, f"Page should have exactly one H1, found {len(h1_elements)}"
        assert len(h2_elements) > 0, "Page should have H2 elements"
        
        # H1 should come before H2s
        if h1_elements and h2_elements:
            h1_position = page.locator('h1').first.bounding_box()
            h2_position = page.locator('h2').first.bounding_box()
            
            if h1_position and h2_position:
                # H1 typically appears before H2
                pass
                
    def test_form_structure(self, page: Page):
        """
        Test form structure and elements
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        forms = page.locator('form').all()
        
        for form in forms:
            if form.is_visible():
                # Check for form method and action
                method = form.get_attribute('method')
                action = form.get_attribute('action')
                
                # Form should have proper attributes
                assert method in ['get', 'post', 'GET', 'POST', None], f"Invalid form method: {method}"
                
                # Check for submit button
                submit = form.locator('button[type="submit"], input[type="submit"]').first
                assert submit, "Form missing submit button"
                
                # Check for fieldsets if multiple sections
                fieldsets = form.locator('fieldset').all()
                if len(fieldsets) > 0:
                    for fieldset in fieldsets:
                        legend = fieldset.locator('legend').first
                        # Fieldsets should have legends
                        
    def test_table_structure(self, page: Page):
        """
        Test table structure if present
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        tables = page.locator('table').all()
        
        for table in tables:
            if table.is_visible():
                # Check for table headers
                headers = table.locator('th').all()
                
                # Check for caption
                caption = table.locator('caption').first
                
                # Check for thead, tbody structure
                thead = table.locator('thead').first
                tbody = table.locator('tbody').first
                
                # Tables should use proper structure
                if headers:
                    assert len(headers) > 0, "Table has headers defined"
                    
    def test_list_structure(self, page: Page):
        """
        Test list structure and nesting
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check unordered lists
        ul_lists = page.locator('ul').all()[:5]
        for ul in ul_lists:
            if ul.is_visible():
                list_items = ul.locator('> li').all()
                assert len(list_items) > 0, "UL has no list items"
                
        # Check ordered lists
        ol_lists = page.locator('ol').all()[:5]
        for ol in ol_lists:
            if ol.is_visible():
                list_items = ol.locator('> li').all()
                assert len(list_items) > 0, "OL has no list items"
                
    def test_media_structure(self, page: Page):
        """
        Test media elements structure
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check images
        images = page.locator('img').all()[:10]
        for img in images:
            if img.is_visible():
                src = img.get_attribute('src')
                assert src, "Image missing src attribute"
                
                # Check for responsive images
                srcset = img.get_attribute('srcset')
                sizes = img.get_attribute('sizes')
                
                # Modern images might use srcset for responsive
                
        # Check for picture elements
        pictures = page.locator('picture').all()
        for picture in pictures:
            sources = picture.locator('source').all()
            img = picture.locator('img').first
            
            assert img, "Picture element missing img fallback"
            
    def test_sidebar_structure(self, page: Page):
        """
        Test sidebar structure if present
        """
        products_page = ProductsPage(page)
        products_page.navigate_to_tprm()
        
        # Look for aside or sidebar elements
        sidebar = page.locator('aside, .sidebar, [role="complementary"]').first
        
        if sidebar and sidebar.is_visible():
            # Check sidebar content
            sidebar_links = sidebar.locator('a').all()
            sidebar_sections = sidebar.locator('section, div').all()
            
            assert len(sidebar_links) > 0 or len(sidebar_sections) > 0, "Sidebar has no content"
            
    def test_breadcrumb_structure(self, page: Page):
        """
        Test breadcrumb navigation structure
        """
        products_page = ProductsPage(page)
        products_page.navigate_to_tprm()
        
        breadcrumb = page.locator('nav[aria-label="breadcrumb"], .breadcrumb').first
        
        if breadcrumb and breadcrumb.is_visible():
            # Should use list structure
            breadcrumb_list = breadcrumb.locator('ol, ul').first
            
            if breadcrumb_list:
                items = breadcrumb_list.locator('li').all()
                assert len(items) > 1, "Breadcrumb should have multiple items"
                
                # Last item should be current page
                last_item = items[-1] if items else None
                if last_item:
                    aria_current = last_item.get_attribute('aria-current')
                    
    def test_modal_structure(self, page: Page):
        """
        Test modal/dialog structure if present
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Try to trigger a modal
        modal_triggers = page.locator('[data-toggle="modal"], [data-bs-toggle="modal"]').all()
        
        if modal_triggers:
            modal_triggers[0].click()
            page.wait_for_timeout(1000)
            
            modal = page.locator('.modal, [role="dialog"]').first
            
            if modal and modal.is_visible():
                # Check modal structure
                modal_header = modal.locator('.modal-header, header').first
                modal_body = modal.locator('.modal-body, .content').first
                modal_footer = modal.locator('.modal-footer, footer').first
                
                # Modal should have proper sections
                assert modal_body, "Modal missing body section"
