import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
import re

@pytest.mark.regression
class TestRegressionFull:
    """
    Full regression test suite for BitSight website functionality
    """
    
    def test_complete_homepage_functionality(self, page: Page):
        """
        Test all homepage functionality comprehensively
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Verify page title and meta tags
        assert page.title(), "Page title is missing"
        
        meta_description = page.locator('meta[name="description"]').get_attribute('content')
        assert meta_description, "Meta description is missing"
        
        meta_keywords = page.locator('meta[name="keywords"]').get_attribute('content')
        # Keywords might be optional
        
        # Verify all sections load
        assert homepage.is_homepage_loaded(), "Homepage not fully loaded"
        
        # Check all navigation elements
        nav_status = homepage.verify_navigation_menu()
        for key, value in nav_status.items():
            assert value, f"Navigation element {key} is missing"
            
        # Check hero section
        hero_status = homepage.verify_hero_section()
        for key, value in hero_status.items():
            assert value, f"Hero element {key} is missing"
            
        # Check product sections
        product_status = homepage.verify_product_sections()
        for key, value in product_status.items():
            assert value, f"Product section {key} is missing"
            
    def test_tprm_product_page_complete(self, page: Page):
        """
        Complete regression test for TPRM product page
        """
        products = ProductsPage(page)
        products.navigate_to_tprm()
        
        # Verify page loaded
        assert 'third-party' in page.url.lower() or 'tprm' in page.url.lower(), "Not on TPRM page"
        
        # Verify all TPRM elements
        tprm_elements = products.verify_tprm_page_elements()
        
        assert tprm_elements.get('vendor_profiles', False), "Vendor profiles section missing"
        assert tprm_elements.get('ai_assessment', False), "AI assessment section missing"
        assert tprm_elements.get('framework_mapping', False), "Framework mapping section missing"
        
        # Check for product images
        assert products.check_product_images(), "Product images not loading properly"
        
        # Check for CTAs
        cta_status = products.verify_cta_buttons()
        assert any(cta_status.values()), "No CTA buttons found on TPRM page"
        
    def test_exposure_management_complete(self, page: Page):
        """
        Complete regression test for Exposure Management page
        """
        products = ProductsPage(page)
        products.navigate_to_exposure_management()
        
        # Verify correct page
        assert 'exposure' in page.url.lower() or 'management' in page.url.lower(), "Not on Exposure page"
        
        # Verify exposure elements
        exposure_elements = products.verify_exposure_page_elements()
        
        assert exposure_elements.get('digital_assets', False), "Digital assets section missing"
        assert exposure_elements.get('shadow_it', False), "Shadow IT section missing"
        assert exposure_elements.get('risk_visualization', False), "Risk visualization missing"
        
        # Check for features list
        features = products.get_product_features()
        assert len(features) > 0, "No product features found"
        
    def test_threat_intelligence_complete(self, page: Page):
        """
        Complete regression test for Threat Intelligence page
        """
        products = ProductsPage(page)
        products.navigate_to_threat_intelligence()
        
        # Verify correct page
        assert 'threat' in page.url.lower() or 'intelligence' in page.url.lower(), "Not on Threat Intelligence page"
        
        # Verify threat intelligence elements
        threat_elements = products.verify_threat_intelligence_elements()
        
        assert threat_elements.get('underground_forums', False), "Underground forums section missing"
        assert threat_elements.get('real_time', False), "Real-time monitoring section missing"
        assert threat_elements.get('ransomware', False), "Ransomware insights section missing"
        
    def test_form_submission_validation(self, page: Page):
        """
        Test form validation on demo request page
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Look for form elements
        form = page.locator('form').first
        if form.is_visible():
            # Try to submit empty form
            submit_button = form.locator('button[type="submit"], input[type="submit"]').first
            if submit_button.is_visible():
                submit_button.click()
                
                # Check for validation messages
                page.wait_for_timeout(1000)
                error_messages = page.locator('.error, .invalid, [aria-invalid="true"]').all()
                assert len(error_messages) > 0 or page.locator(':text("required")').is_visible(), "Form validation not working"
                
    def test_search_functionality(self, page: Page):
        """
        Test site search functionality if available
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Look for search button/icon
        search_trigger = page.locator('[aria-label*="search" i], button:has-text("Search"), .search-icon').first
        
        if search_trigger.is_visible():
            search_trigger.click()
            page.wait_for_timeout(500)
            
            # Find search input
            search_input = page.locator('input[type="search"], input[placeholder*="search" i]').first
            if search_input.is_visible():
                search_input.fill("security")
                search_input.press("Enter")
                
                page.wait_for_load_state('networkidle')
                
                # Verify search results or navigation
                assert page.url != homepage.base_url, "Search did not navigate to results"
                
    def test_responsive_breakpoints(self, page: Page):
        """
        Test responsive design at different breakpoints
        """
