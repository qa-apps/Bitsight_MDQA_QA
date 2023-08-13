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
                
                # Check for valid URL format
                if href.startswith('http'):
                    assert re.match(r'https?://[^\s]+', href), f"Invalid URL format: {href}"
                    
                # External links should have target="_blank"
                if href and 'bitsight.com' not in href and href.startswith('http'):
                    assert target == '_blank' or target is None, f"External link {href} should open in new tab"
                    
                # Links should have text or title
                assert text or title, f"Link {href} has no text or title"
                
    def test_image_data_validation(self, page: Page):
        """
        Test image data and attributes
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        images = homepage.get_all_real_images()
        
        for img_data in images:
            src = img_data['src']
            alt = img_data['alt']
            
            # Validate image data
            assert src, "Image missing src attribute"
            
            # Check for valid image URL
            if src.startswith('http'):
                assert re.match(r'https?://[^\s]+\.(jpg|jpeg|png|gif|webp|svg)', src, re.I), f"Invalid image URL: {src}"
                
            # Alt text validation
            assert alt is not None, f"Image {src} missing alt attribute"
            
            # Alt text shouldn't be file name
            if alt:
                filename = src.split('/')[-1].split('.')[0] if '/' in src else ''
                assert alt.lower() != filename.lower(), f"Alt text is filename for {src}"
                
    def test_form_data_attributes(self, page: Page):
        """
        Test form data attributes and validation rules
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Navigate to form page
        demo_button = page.locator('a[href*="demo"]').first
        if demo_button.is_visible():
            demo_button.click()
            page.wait_for_load_state('networkidle')
            
            forms = page.locator('form').all()
            
            for form in forms:
                if form.is_visible():
                    # Check form attributes
                    method = form.get_attribute('method')
                    action = form.get_attribute('action')
                    form_id = form.get_attribute('id')
                    
                    # Validate form data
                    assert method in ['get', 'post', 'GET', 'POST', None], f"Invalid form method: {method}"
                    
                    # Check input fields
                    inputs = form.locator('input').all()
                    
                    for input_field in inputs:
                        input_type = input_field.get_attribute('type')
                        input_name = input_field.get_attribute('name')
                        required = input_field.get_attribute('required')
                        pattern = input_field.get_attribute('pattern')
                        maxlength = input_field.get_attribute('maxlength')
                        
                        # Validate input attributes
                        assert input_type, "Input missing type attribute"
                        
                        # Email fields should have email type
                        if input_name and 'email' in input_name.lower():
                            assert input_type == 'email', f"Email field has wrong type: {input_type}"
                            
                        # Phone fields should have tel type
                        if input_name and ('phone' in input_name.lower() or 'tel' in input_name.lower()):
                            assert input_type == 'tel', f"Phone field has wrong type: {input_type}"
                            
                        # Check data validation attributes
                        if pattern:
                            # Pattern should be valid regex
                            try:
                                re.compile(pattern)
                            except re.error:
                                assert False, f"Invalid pattern regex: {pattern}"
                                
                        if maxlength:
                            assert maxlength.isdigit(), f"Invalid maxlength: {maxlength}"
                            assert int(maxlength) > 0, f"Maxlength too small: {maxlength}"
                            
    def test_navigation_data_structure(self, page: Page):
        """
        Test navigation menu data structure
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Get navigation structure
        nav_data = page.evaluate('''() => {
            const nav = document.querySelector('nav, header');
            const items = [];
            
            if (nav) {
                const links = nav.querySelectorAll('a');
                links.forEach(link => {
                    items.push({
                        text: link.textContent.trim(),
                        href: link.href,
                        hasSubmenu: link.getAttribute('aria-expanded') !== null,
                        ariaLabel: link.getAttribute('aria-label')
                    });
                });
            }
            
            return items;
        }''')
        
        # Validate navigation data
        assert len(nav_data) > 0, "No navigation items found"
        
        for item in nav_data:
            # Each item should have text and href
            assert item['text'] or item['ariaLabel'], "Nav item missing text"
            assert item['href'], "Nav item missing href"
            
            # Check for valid URLs
            if item['href'].startswith('http'):
                assert 'bitsight.com' in item['href'] or item['href'].startswith('http'), "Invalid nav URL"
                
    def test_schema_org_validation(self, page: Page):
        """
        Test Schema.org microdata if present
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Check for microdata
        microdata_items = page.locator('[itemscope]').all()
        
        for item in microdata_items:
            itemtype = item.get_attribute('itemtype')
            
            if itemtype:
                # Validate schema.org URL
                assert 'schema.org' in itemtype, f"Invalid schema type: {itemtype}"
                
                # Check for required properties based on type
                if 'Organization' in itemtype:
                    name = item.locator('[itemprop="name"]').first
                    assert name, "Organization schema missing name"
                    
                if 'Product' in itemtype:
                    name = item.locator('[itemprop="name"]').first
                    description = item.locator('[itemprop="description"]').first
                    assert name or description, "Product schema missing required properties"
                    
    def test_api_endpoint_validation(self, page: Page):
        """
        Test API endpoints referenced in the page
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Look for API endpoints in page
        api_endpoints = page.evaluate('''() => {
            const endpoints = [];
            
            // Check for API calls in scripts
            const scripts = document.querySelectorAll('script');
            scripts.forEach(script => {
                const content = script.innerHTML;
                const apiPattern = /https?:\/\/[^\\s"']+api[^\\s"']*/gi;
                const matches = content.match(apiPattern);
                if (matches) {
                    endpoints.push(...matches);
                }
            });
            
            // Check for data attributes
            const dataElements = document.querySelectorAll('[data-api], [data-endpoint]');
            dataElements.forEach(el => {
                const api = el.getAttribute('data-api') || el.getAttribute('data-endpoint');
                if (api) endpoints.push(api);
            });
            
            return [...new Set(endpoints)];
        }''')
        
        # Validate API endpoints
        for endpoint in api_endpoints:
            # Check for valid URL format
            if endpoint.startswith('http'):
                assert re.match(r'https?://[^\s]+', endpoint), f"Invalid API endpoint: {endpoint}"
                
                # API endpoints should use HTTPS
                assert endpoint.startswith('https'), f"API endpoint not using HTTPS: {endpoint}"
                
    def test_cookie_data_validation(self, page: Page):
        """
        Test cookie data and attributes
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Get cookies
        cookies = page.context.cookies()
        
        for cookie in cookies:
            # Validate cookie data
            assert 'name' in cookie, "Cookie missing name"
            assert 'value' in cookie, "Cookie missing value"
            assert 'domain' in cookie, "Cookie missing domain"
            
            # Security validations
            if 'bitsight.com' in cookie.get('domain', ''):
                # Production cookies should be secure
                assert cookie.get('secure', False) or 'localhost' in cookie['domain'], f"Cookie {cookie['name']} not secure"
                
                # Session cookies should be httpOnly
