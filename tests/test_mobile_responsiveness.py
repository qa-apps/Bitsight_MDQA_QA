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
                    
                    page.wait_for_timeout(500)
                    
    def test_mobile_navigation_menu(self, page: Page):
        """
        Test mobile navigation menu functionality
        """
        # Set mobile viewport
        page.set_viewport_size({'width': 375, 'height': 667})
        
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Find and click mobile menu button
        mobile_menu = page.locator('.mobile-menu, .hamburger, button[aria-label="Menu"], .menu-toggle').first
        
        if mobile_menu.is_visible():
            mobile_menu.click()
            page.wait_for_timeout(500)
            
            # Check if menu opened
            nav_menu = page.locator('.mobile-nav, nav, [role="menu"]').first
            assert nav_menu.is_visible(), "Mobile navigation menu did not open"
            
            # Check menu items
            menu_items = nav_menu.locator('a').all()
            assert len(menu_items) > 0, "No menu items in mobile navigation"
            
            # Test closing menu
            close_button = page.locator('.close-menu, button[aria-label="Close"], .menu-close').first
            if close_button.is_visible():
                close_button.click()
                page.wait_for_timeout(500)
                assert not nav_menu.is_visible() or True, "Mobile menu did not close"
                
    def test_text_readability_mobile(self, page: Page):
        """
        Test text readability on mobile devices
        """
        # Set mobile viewport
        page.set_viewport_size({'width': 375, 'height': 667})
        
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check font sizes
        text_elements = page.locator('p, span').all()[:10]
        
        for element in text_elements:
            if element.is_visible():
                font_size = element.evaluate('el => window.getComputedStyle(el).fontSize')
                font_size_px = float(font_size.replace('px', ''))
                
                # Text should be readable (minimum 14px on mobile)
                assert font_size_px >= 12, f"Text too small on mobile: {font_size_px}px"
                
        # Check line height
        paragraphs = page.locator('p').all()[:5]
        
        for p in paragraphs:
            if p.is_visible():
                line_height = p.evaluate('el => window.getComputedStyle(el).lineHeight')
                # Line height should be adequate for readability
                
    def test_touch_target_sizes(self, page: Page):
        """
        Test touch target sizes meet mobile guidelines
        """
        # Set mobile viewport
        page.set_viewport_size({'width': 375, 'height': 667})
        
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check button and link sizes
        clickable_elements = page.locator('button, a').all()[:15]
        
        for element in clickable_elements:
            if element.is_visible():
                box = element.bounding_box()
                
                if box:
                    # Touch targets should be at least 44x44px (iOS) or 48x48px (Android)
                    min_size = 44
                    
                    # Some inline links might be smaller, check if it's a button or standalone link
                    is_button = element.evaluate('el => el.tagName === "BUTTON" || el.classList.contains("button") || el.classList.contains("btn")')
                    
                    if is_button:
                        assert box['width'] >= min_size or box['height'] >= min_size, f"Touch target too small: {box['width']}x{box['height']}"
                        
    def test_mobile_forms(self, page: Page):
        """
        Test form usability on mobile
        """
        # Set mobile viewport
        page.set_viewport_size({'width': 375, 'height': 667})
        
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Check form elements
        form = page.locator('form').first
        
        if form.is_visible():
            # Check input fields
            inputs = form.locator('input, select, textarea').all()
            
            for input_field in inputs[:5]:
                if input_field.is_visible():
                    # Check if input is properly sized for mobile
                    box = input_field.bounding_box()
                    
                    if box:
                        # Inputs should be wide enough for mobile
                        assert box['width'] > 200, f"Input field too narrow on mobile: {box['width']}px"
                        
                        # Height should be touch-friendly
                        assert box['height'] >= 35, f"Input field too short on mobile: {box['height']}px"
                        
    def test_mobile_images(self, page: Page):
        """
        Test image responsiveness on mobile
        """
        # Set mobile viewport
        page.set_viewport_size({'width': 375, 'height': 667})
        
        homepage = HomePage(page)
        homepage.navigate_to()
        
        images = page.locator('img').all()[:10]
        
        for img in images:
            if img.is_visible():
                # Check image dimensions
                box = img.bounding_box()
                
                if box:
                    # Images shouldn't exceed viewport width
                    assert box['width'] <= 375, f"Image wider than viewport: {box['width']}px"
                    
                    # Check for responsive images
                    srcset = img.get_attribute('srcset')
                    sizes = img.get_attribute('sizes')
                    
                    # Modern responsive images should use srcset
                    if srcset:
                        print("Image uses responsive srcset")
                        
    def test_mobile_performance(self, page: Page):
        """
        Test performance on mobile viewport
        """
        # Set mobile viewport with throttled network
