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
            
            # Check for horizontal scrolling (should not exist)
            has_horizontal_scroll = page.evaluate('''() => {
                return document.documentElement.scrollWidth > document.documentElement.clientWidth;
            }''')
            
            assert not has_horizontal_scroll, f"Horizontal scroll detected on {device['name']}"
            
            # Check if navigation is accessible
            mobile_menu = page.locator('.mobile-menu, .hamburger, [aria-label="Menu"]').first
            assert mobile_menu.is_visible() or page.locator('nav').is_visible(), f"Navigation not accessible on {device['name']}"
            
    def test_touch_interactions(self, page: Page):
        """
        Test touch interactions on mobile
        """
        # Set mobile viewport
        page.set_viewport_size({'width': 375, 'height': 667})
        
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Test tap on mobile menu
        mobile_menu = page.locator('.mobile-menu, .hamburger, button[aria-label="Menu"]').first
        
        if mobile_menu.is_visible():
            # Simulate tap
            mobile_menu.tap()
            page.wait_for_timeout(500)
            
            # Menu should open
            mobile_nav = page.locator('.mobile-nav, .nav-mobile, nav').first
            assert mobile_nav.is_visible() or page.locator('[role="menu"]').is_visible(), "Mobile menu did not open on tap"
            
            # Test swipe gesture (if carousel exists)
            carousel = page.locator('.carousel, .slider').first
            if carousel and carousel.is_visible():
                # Get initial state
                initial_state = carousel.inner_html()
                
                # Simulate swipe
                box = carousel.bounding_box()
                if box:
                    page.mouse.move(box['x'] + box['width'] - 50, box['y'] + box['height'] / 2)
                    page.mouse.down()
                    page.mouse.move(box['x'] + 50, box['y'] + box['height'] / 2)
                    page.mouse.up()
                    
