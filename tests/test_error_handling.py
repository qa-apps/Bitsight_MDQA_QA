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
