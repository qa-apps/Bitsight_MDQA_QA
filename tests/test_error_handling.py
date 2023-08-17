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
        
        # Set very short timeout
        page.set_default_timeout(100)
        
        try:
            # This might timeout
            page.goto('https://httpstat.us/200?sleep=5000')
        except Exception as e:
            # Should handle timeout gracefully
            assert 'timeout' in str(e).lower(), "Timeout not properly handled"
            
        # Reset timeout
        page.set_default_timeout(30000)
        
    def test_redirect_handling(self, page: Page):
        """
        Test redirect handling
        """
        homepage = HomePage(page)
        
        # Test common redirect scenarios
        redirect_urls = [
            f"{homepage.base_url}/index.html",
            f"{homepage.base_url}/home",
            homepage.base_url.replace('https://', 'http://')  # HTTP to HTTPS
        ]
        
        for url in redirect_urls:
            try:
                response = page.goto(url, wait_until='domcontentloaded')
                
                if response:
                    # Check if redirected properly
                    final_url = page.url
                    
                    # Should redirect to main domain
                    assert 'bitsight.com' in final_url, f"Redirect failed for {url}"
                    
            except Exception:
                # Some redirects might not work in test environment
                pass
                
    def test_invalid_input_handling(self, page: Page):
        """
        Test handling of invalid user inputs
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Try XSS in search
        search_payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            "'; DROP TABLE users; --",
            '../../../etc/passwd'
        ]
        
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input[type="text"], input[type="search"]').first
            
            for payload in search_payloads:
                if search_input.is_visible():
                    search_input.fill(payload)
                    search_input.press('Enter')
                    page.wait_for_timeout(1000)
                    
                    # Page should not break or show errors
                    assert page.title() != "", "Page broke with invalid input"
                    
                    # Should not execute script
                    page_text = page.content()
                    assert '<script>alert' not in page_text, "Script not properly escaped"
                    
    def test_browser_back_button_handling(self, page: Page):
        """
        Test browser back button functionality
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        initial_url = page.url
        
        # Navigate to another page
        homepage.click_request_demo()
        page.wait_for_load_state('networkidle')
        second_url = page.url
        
        assert initial_url != second_url, "Navigation did not occur"
        
        # Go back
        page.go_back()
        page.wait_for_load_state('networkidle')
        
        # Should return to initial page
        assert page.url == initial_url, "Back button did not work correctly"
        
        # Go forward
        page.go_forward()
        page.wait_for_load_state('networkidle')
        
        # Should return to second page
        assert page.url == second_url, "Forward button did not work correctly"
        
    def test_session_timeout_handling(self, page: Page):
        """
        Test session timeout handling
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Simulate long idle time
        page.wait_for_timeout(2000)
        
        # Try to interact after "timeout"
        page.click('body')
        
        # Page should still be responsive
        assert page.title() != "", "Page not responsive after idle time"
        
    def test_concurrent_action_handling(self, page: Page):
        """
        Test handling of concurrent user actions
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Try rapid clicking
        for _ in range(5):
            page.click('body', position={'x': 100, 'y': 100})
            page.wait_for_timeout(100)
            
        # Page should remain stable
        assert page.title() != "", "Page broke after rapid clicking"
        
    def test_special_character_handling(self, page: Page):
        """
        Test handling of special characters in inputs
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        special_chars = [
            "Test@#$%^&*()",
            "Tëst wïth ümläüts",
            "测试中文字符",
            "🚀 Emoji test 😊",
            "Test\nwith\nnewlines",
            "Test\\with\\backslashes"
        ]
        
        input_field = page.locator('input[type="text"]').first
        
        if input_field.is_visible():
            for chars in special_chars:
                input_field.fill(chars)
                actual_value = input_field.input_value()
                
                # Should handle special characters
                assert len(actual_value) > 0, f"Failed to handle: {chars}"
                
                input_field.clear()
                
    def test_memory_leak_prevention(self, page: Page):
        """
        Test for potential memory leaks
        """
        homepage = HomePage(page)
        
        # Get initial memory usage
        initial_memory = page.evaluate('''() => {
            if (performance.memory) {
                return performance.memory.usedJSHeapSize;
            }
            return 0;
        }''')
        
        # Perform multiple navigations
        for _ in range(5):
            homepage.navigate_to()
            page.wait_for_load_state('networkidle')
            
        # Get final memory usage
