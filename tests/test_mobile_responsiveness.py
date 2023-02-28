import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage

@pytest.mark.mobile
class TestMobileResponsiveness:
    """
    Mobile responsiveness and touch interaction testing
    """
    
    def test_mobile_viewport_rendering(self, page: Page):
        """
        Test rendering on various mobile viewports
        """
        homepage = HomePage(page)
        
        mobile_viewports = [
            {'name': 'iPhone SE', 'width': 375, 'height': 667},
            {'name': 'iPhone XR', 'width': 414, 'height': 896},
            {'name': 'iPhone 12 Pro', 'width': 390, 'height': 844},
            {'name': 'Pixel 5', 'width': 393, 'height': 851},
            {'name': 'Samsung Galaxy S8+', 'width': 360, 'height': 740},
            {'name': 'Samsung Galaxy S20', 'width': 412, 'height': 915}
        ]
        
        for device in mobile_viewports:
            page.set_viewport_size({'width': device['width'], 'height': device['height']})
            homepage.navigate_to()
            
            # Check if page loads properly
            assert homepage.is_visible(homepage.hero_title), f"Hero not visible on {device['name']}"
