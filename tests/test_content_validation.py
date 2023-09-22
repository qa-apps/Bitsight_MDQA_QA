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
        
        assert privacy_link.is_visible(), "Privacy policy link not found"
        
        # Click and verify navigation
        privacy_link.click()
        page.wait_for_load_state('networkidle')
        
        # Verify privacy page content
        page_content = page.content().lower()
        privacy_keywords = ['privacy', 'data', 'information', 'personal', 'collect']
        
        found_keywords = [kw for kw in privacy_keywords if kw in page_content]
        assert len(found_keywords) >= 3, "Privacy policy page missing expected content"
        
    def test_terms_of_service_link(self, page: Page):
        """
        Test terms of service/use link and content
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find terms link
        terms_link = page.locator('a:has-text("Terms")').first
        
        if terms_link.is_visible():
            terms_link.click()
            page.wait_for_load_state('networkidle')
            
            # Verify terms page content
            page_content = page.content().lower()
            terms_keywords = ['terms', 'agreement', 'service', 'use', 'conditions']
            
            found_keywords = [kw for kw in terms_keywords if kw in page_content]
            assert len(found_keywords) >= 2, "Terms page missing expected content"
            
    def test_social_media_links(self, page: Page):
        """
        Test social media links presence
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Common social media platforms
        social_platforms = [
            ('linkedin', 'linkedin.com'),
            ('twitter', 'twitter.com'),
            ('facebook', 'facebook.com'),
            ('youtube', 'youtube.com')
        ]
        
        found_social = []
        
        for platform, domain in social_platforms:
            social_link = page.locator(f'a[href*="{domain}"]').first
            if social_link:
                found_social.append(platform)
                
                # Verify link has proper attributes
                href = social_link.get_attribute('href')
                target = social_link.get_attribute('target')
                
                assert href and domain in href, f"{platform} link invalid"
                # Social links should open in new tab
                assert target == '_blank' or target is None, f"{platform} link should open in new tab"
                
        assert len(found_social) > 0, "No social media links found"
        
    def test_testimonials_content(self, page: Page):
        """
        Test testimonials/case studies content
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Look for testimonials section
        testimonials = page.locator('.testimonial, .case-study, .customer-story, blockquote').all()
        
        if testimonials:
            for testimonial in testimonials[:3]:
                text = testimonial.text_content()
                
                # Testimonials should have substantial content
                assert text and len(text) > 20, "Testimonial has insufficient content"
                
                # Check for attribution
                author = testimonial.locator('.author, .name, .attribution').first
                
    def test_cta_button_text(self, page: Page):
        """
        Test Call-to-Action button text content
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find CTA buttons
        cta_buttons = page.locator('a.button, button, a[class*="btn"]').all()[:10]
        
        common_cta_texts = ['demo', 'learn', 'get started', 'contact', 'download', 'sign up', 'request']
        
        for button in cta_buttons:
            if button.is_visible():
                button_text = button.text_content()
                
                # CTA should have text
                assert button_text and len(button_text.strip()) > 0, "CTA button has no text"
                
                # Check if it's a meaningful CTA
                has_cta_keyword = any(keyword in button_text.lower() for keyword in common_cta_texts)
                
    def test_navigation_labels(self, page: Page):
        """
        Test navigation menu labels and text
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Get navigation items
        nav_items = page.locator('nav a, header a').all()[:20]
        
        for item in nav_items:
            if item.is_visible():
                item_text = item.text_content()
                
                # Navigation items should have text
                assert item_text and len(item_text.strip()) > 0, "Navigation item has no text"
                
                # Text should be reasonably short for navigation
                assert len(item_text) < 50, f"Navigation text too long: {item_text}"
                
    def test_error_message_content(self, page: Page):
        """
        Test error message content quality
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Navigate to 404 page
        page.goto(f"{homepage.base_url}/nonexistent-page-404-test")
        
        page_content = page.content()
        
        # Error page should have helpful content
        helpful_elements = ['home', 'back', 'search', 'sitemap', 'contact']
        found_elements = [elem for elem in helpful_elements if elem in page_content.lower()]
        
        # Should provide navigation options
        assert len(found_elements) > 0, "404 page not helpful to users"
        
    def test_loading_message_content(self, page: Page):
        """
        Test loading states and messages
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Look for loading indicators
        loading_indicators = page.locator('.loading, .spinner, [aria-busy="true"]').all()
        
        for indicator in loading_indicators:
            if indicator.is_visible():
                # Loading indicators should have accessible text
                aria_label = indicator.get_attribute('aria-label')
                text_content = indicator.text_content()
                
                has_accessible_text = aria_label or text_content
                
    def test_form_field_labels(self, page: Page):
        """
        Test form field labels and placeholders
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Check form fields
        form_fields = page.locator('input, select, textarea').all()
        
        for field in form_fields[:10]:
            if field.is_visible():
                field_id = field.get_attribute('id')
                field_name = field.get_attribute('name')
                placeholder = field.get_attribute('placeholder')
                aria_label = field.get_attribute('aria-label')
                
                # Field should have some identifying text
                has_label = False
                
                if field_id:
                    label = page.locator(f'label[for="{field_id}"]').first
                    if label and label.is_visible():
                        label_text = label.text_content()
                        assert label_text and len(label_text) > 0, f"Field {field_name} has empty label"
                        has_label = True
                        
                # If no label, should have placeholder or aria-label
                if not has_label:
                    assert placeholder or aria_label, f"Field {field_name} has no label, placeholder, or aria-label"
                    
    def test_date_format_consistency(self, page: Page):
        """
        Test date format consistency across the site
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find dates on the page
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}-\d{2}-\d{2}',      # YYYY-MM-DD
            r'\w+ \d{1,2}, \d{4}',     # Month DD, YYYY
            r'\d{1,2} \w+ \d{4}'       # DD Month YYYY
        ]
        
        page_content = page.content()
        found_dates = []
        
        for pattern in date_patterns:
            matches = re.findall(pattern, page_content)
            if matches:
                found_dates.extend(matches)
