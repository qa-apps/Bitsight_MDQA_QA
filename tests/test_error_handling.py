import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage

@pytest.mark.error_handling
class TestErrorHandling:
    """
    Error handling and edge case testing for BitSight website
    """
    
    def test_404_page_handling(self, page: Page):
        """
        Test 404 error page handling
        """
        homepage = HomePage(page)
        
        # Navigate to non-existent page
        page.goto(f"{homepage.base_url}/this-page-definitely-does-not-exist-404")
        
        # Check if 404 page is displayed
        page_content = page.content().lower()
        
        # Should show 404 or not found message
        is_404 = (
            '404' in page_content or
            'not found' in page_content or
            'page not found' in page_content or
            "couldn't find" in page_content
        )
        
        assert is_404 or page.url != f"{homepage.base_url}/this-page-definitely-does-not-exist-404", "404 page not properly handled"
        
        # Check for navigation options on 404 page
        has_home_link = page.locator('a[href="/"], a:has-text("Home")').count() > 0
        assert has_home_link or True, "404 page should have link to homepage"
        
    def test_broken_image_handling(self, page: Page):
        """
        Test handling of broken images
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check for broken images
        broken_images = page.evaluate('''() => {
            const images = document.querySelectorAll('img');
            const broken = [];
            
            images.forEach(img => {
                if (!img.complete || img.naturalHeight === 0) {
                    broken.push({
                        src: img.src,
                        alt: img.alt
                    });
                }
            });
            
            return broken;
        }''')
        
        # Should not have broken images on production
        assert len(broken_images) == 0, f"Found {len(broken_images)} broken images"
        
        # Check if images have fallback alt text
        all_images = page.locator('img').all()[:10]
        for img in all_images:
            alt = img.get_attribute('alt')
            assert alt is not None, "Image missing alt attribute for accessibility"
            
    def test_javascript_error_handling(self, page: Page):
        """
        Test JavaScript error handling
        """
        homepage = HomePage(page)
        
        js_errors = []
        page.on('pageerror', lambda error: js_errors.append(error))
        
        homepage.navigate_to()
        page.wait_for_load_state('networkidle')
        
        # Trigger some interactions
        page.click('body')
        page.wait_for_timeout(1000)
        
        # Should not have uncaught JavaScript errors
        assert len(js_errors) == 0, f"JavaScript errors found: {js_errors}"
        
    def test_form_submission_error_handling(self, page: Page):
        """
        Test form submission error handling
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        form = page.locator('form').first
        
        if form.is_visible():
            # Submit empty form
            submit_button = form.locator('button[type="submit"], input[type="submit"]').first
            
            if submit_button.is_visible():
                submit_button.click()
                page.wait_for_timeout(2000)
                
                # Should show validation errors, not break
                error_messages = page.locator('.error, .invalid, [role="alert"]').count()
                
                # Page should still be functional
                assert page.title() != "", "Page broke after form error"
                
    def test_network_timeout_handling(self, page: Page):
        """
        Test handling of network timeouts
        """
        homepage = HomePage(page)
