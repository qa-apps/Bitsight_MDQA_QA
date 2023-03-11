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
