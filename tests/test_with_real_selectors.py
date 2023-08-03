import pytest
from playwright.sync_api import Page, expect
from pages.home_page_real import HomePageReal

@pytest.mark.real
class TestWithRealSelectors:
    """
    Tests using ACTUAL DOM selectors from BitSight website
    This demonstrates the difference between guessed and real selectors
    """
    
    def test_actual_header_structure(self, page: Page):
        """
        Test with real header selectors from DOM inspection
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Using REAL selectors discovered from DOM
        header_info = homepage.verify_real_header_structure()
        
        assert header_info['header_exists'], "Header with class 'site-header' not found"
        assert header_info['has_transparent_class'], "Header missing 'site-header--transparent' class"
        assert header_info['nav_exists'], "Navigation element not found in header"
        
        # The actual header uses these classes:
        # - site-header
        # - site-header--transparent
        
    def test_actual_menu_links(self, page: Page):
        """
        Test actual menu links with real class names
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Get menu items using REAL class: main-menu-block__item-link
        menu_links = homepage.get_real_menu_links()
        
        assert len(menu_links) > 0, "No menu links found with actual class 'main-menu-block__item-link'"
        
        # Print what we actually found
        for link in menu_links[:5]:
            print(f"Found menu item: {link['text']} -> {link['href']}")
            
    def test_actual_demo_buttons(self, page: Page):
        """
        Test the actual demo button URLs found in DOM
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # These are the ACTUAL demo URLs found:
        # - /demo/security-rating
        # - /demo/bitsight-demo  
        # - /demo/bitsight-threat-intelligence-demo
        
        demo_buttons = [
            ('a[href*="/demo/security-rating"]', 'Security Rating Demo'),
            ('a[href*="/demo/bitsight-demo"]', 'BitSight Demo'),
            ('a[href*="/demo/bitsight-threat-intelligence-demo"]', 'Threat Intel Demo')
        ]
        
        for selector, name in demo_buttons:
            elements = page.locator(selector).all()
            if elements:
                print(f"✓ Found {name}: {len(elements)} instances")
            else:
                print(f"✗ {name} not found")
                
    def test_actual_hero_section(self, page: Page):
        """
        Test hero section with actual text and classes
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        hero_info = homepage.verify_real_hero_section()
        
        # The ACTUAL h1 text is: "AI-powered intelligence that outsmarts cyber risk"
        assert hero_info['h1_exists'], "H1 element not found"
        assert hero_info['hero_contains_ai_text'], "H1 doesn't contain expected 'AI-powered' text"
        
        # The actual hero container class is: hero-homepage__title
        assert hero_info['hero_container_exists'], "Hero container with class 'hero-homepage__title' not found"
        
        print(f"Actual H1 text: {hero_info['h1_text']}")
        
    def test_actual_footer_structure(self, page: Page):
        """
        Test footer with actual classes found
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        footer_info = homepage.get_real_footer_info()
        
        assert footer_info['exists'], "Footer not found"
        
        # The ACTUAL footer classes are: "site-footer footer"
        assert 'site-footer' in (footer_info.get('class') or ''), "Footer missing 'site-footer' class"
        assert 'footer' in (footer_info.get('class') or ''), "Footer missing 'footer' class"
        
        # Actual footer has 27 links as discovered
        assert footer_info.get('link_count', 0) > 20, f"Footer has only {footer_info.get('link_count', 0)} links, expected > 20"
        
    def test_actual_login_button(self, page: Page):
        """
        Test the actual login button URL
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # The ACTUAL login URL is: https://service.bitsighttech.com/
        login_button = page.locator('a[href="https://service.bitsighttech.com/"]').first
        
        assert login_button.is_visible(), "Login button with actual URL not found"
        
        # Verify the URL
        href = login_button.get_attribute('href')
        assert href == 'https://service.bitsighttech.com/', f"Login URL is {href}, not the expected service.bitsighttech.com"
        
    def test_actual_images(self, page: Page):
        """
        Test actual images found on the page
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        images = homepage.get_all_real_images()
        
        # The page actually has 114 images as discovered
        all_images_count = page.locator('img').count()
        print(f"Total images on page: {all_images_count}")
        
        # Check first few images
        for i, img in enumerate(images[:3]):
            print(f"Image {i+1}: {img['alt'] or 'No alt text'}")
            print(f"  Source: {img['src']}")
            
        # Actual first image is: HP hero wave background
        if images:
            first_img = images[0]
            assert 'Hero' in first_img.get('src', '') or 'hero' in first_img.get('alt', '').lower(), "First image is not the hero background"
            
    def test_comparison_generic_vs_real(self, page: Page):
        """
        Demonstrate the difference between generic and real selectors
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        print("\n" + "="*60)
        print("COMPARISON: Generic vs Real Selectors")
        print("="*60)
        
        # What I guessed vs what's actually there
        comparisons = [
            {
                'element': 'Solutions Menu',
                'generic': 'button:has-text("Solutions")',
                'reality': 'Not a button - menu structure is different',
                'found_generic': page.locator('button:has-text("Solutions")').count(),
                'found_real': page.locator('a:has-text("Solutions")').count()
            },
            {
                'element': 'Demo Button',
                'generic': 'a:has-text("Request Demo")',
                'reality': 'a[href*="/demo/security-rating"]',
