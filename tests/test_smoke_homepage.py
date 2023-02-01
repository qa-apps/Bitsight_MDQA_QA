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
