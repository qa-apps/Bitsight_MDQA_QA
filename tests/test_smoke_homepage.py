import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.base_page import BasePage

@pytest.mark.smoke
class TestSmokeHomepage:
    """
    Smoke tests for BitSight homepage critical functionality
    """
    
    def test_homepage_loads_successfully(self, page: Page):
        """
        Test that homepage loads without errors
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        assert homepage.is_homepage_loaded(), "Homepage failed to load properly"
        assert page.title() != "", "Page title is empty"
        assert "BitSight" in page.title() or "Bitsight" in page.title(), "Page title doesn't contain BitSight"
        
        # Verify no console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)
        page.reload()
        assert len(console_errors) == 0, f"Console errors found: {console_errors}"
        
    def test_main_navigation_elements_present(self, page: Page):
        """
        Test that all main navigation elements are visible
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        nav_status = homepage.verify_navigation_menu()
        
        assert nav_status['solutions'], "Solutions menu not found"
        assert nav_status['products'], "Products menu not found"
        assert nav_status['resources'], "Resources menu not found"
        assert nav_status['company'], "Company menu not found"
        assert nav_status['demo'], "Request Demo button not found"
        assert nav_status['login'], "Login button not found"
        
    def test_hero_section_elements(self, page: Page):
        """
        Test hero section contains all required elements
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        hero_status = homepage.verify_hero_section()
        
        assert hero_status['hero_title'], "Hero title not visible"
        assert hero_status['hero_subtitle'], "Hero subtitle not visible"
        assert hero_status['learn_more'], "Learn More button not visible"
        assert hero_status['customer_stories'], "Customer stories link not visible"
        
    def test_product_sections_visible(self, page: Page):
        """
        Test that all product sections are visible on homepage
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        product_status = homepage.verify_product_sections()
        
        assert product_status['tprm'], "TPRM section not visible"
        assert product_status['exposure'], "Exposure Management section not visible"
        assert product_status['threat_intel'], "Threat Intelligence section not visible"
        assert product_status['governance'], "Governance section not visible"
        
    def test_request_demo_button_clickable(self, page: Page):
        """
        Test Request Demo button is clickable and navigates correctly
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        initial_url = page.url
        homepage.click_request_demo()
        page.wait_for_load_state('networkidle')
        
        assert page.url != initial_url, "URL did not change after clicking Request Demo"
        assert 'demo' in page.url.lower() or 'contact' in page.url.lower(), "Did not navigate to demo/contact page"
        
    def test_page_has_footer(self, page: Page):
        """
        Test that footer is present with links
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        footer = page.locator('footer')
        assert footer.is_visible(), "Footer is not visible"
        
        footer_links = homepage.get_footer_links()
        assert len(footer_links) > 0, "No footer links found"
        
    def test_page_loads_within_timeout(self, page: Page):
        """
        Test page loads within acceptable time
        """
        homepage = HomePage(page)
        
        import time
        start_time = time.time()
        homepage.navigate_to()
        load_time = time.time() - start_time
        
        assert load_time < 10, f"Page took too long to load: {load_time} seconds"
        
    def test_critical_images_load(self, page: Page):
        """
        Test that critical images on homepage are loaded
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        images = page.locator('img').all()[:5]  # Check first 5 images
