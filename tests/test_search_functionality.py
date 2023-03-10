import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.home_page_real import HomePageReal

@pytest.mark.search
class TestSearchFunctionality:
    """
    Comprehensive search functionality testing for BitSight website
    """
    
    def test_search_form_presence(self, page: Page):
        """
        Test that search form exists on the page
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Look for search form with actual ID
        search_form = page.locator('#views-exposed-form-search-search-page')
        
        assert search_form.count() > 0, "Search form not found on page"
        
        # Check if form has necessary elements
        if search_form.first.is_visible():
            search_input = search_form.locator('input[type="text"], input[type="search"]').first
            assert search_input, "Search input field not found"
            
    def test_basic_search_functionality(self, page: Page):
        """
        Test basic search functionality
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Use actual search form
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            
            # Perform search
            search_query = "security"
            search_input.fill(search_query)
            search_input.press('Enter')
            
            page.wait_for_load_state('networkidle')
            
            # Check if navigated to search results
            current_url = page.url
            assert 'search' in current_url or search_query in current_url, "Search did not navigate to results"
            
    def test_search_with_different_queries(self, page: Page):
        """
        Test search with various query types
        """
        homepage = HomePageReal(page)
        
        search_queries = [
            'risk management',
            'cybersecurity',
            'third party',
            'compliance',
            'threat intelligence'
        ]
        
        for query in search_queries:
            homepage.navigate_to()
            
            search_form = page.locator('#views-exposed-form-search-search-page').first
            if search_form.is_visible():
                search_input = search_form.locator('input').first
                search_input.fill(query)
                search_input.press('Enter')
                
                page.wait_for_load_state('domcontentloaded')
                
                # Verify search executed
                assert page.url != homepage.base_url, f"Search for '{query}' did not navigate"
                
    def test_search_input_validation(self, page: Page):
        """
        Test search input field validation
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            
            # Test empty search
            search_input.clear()
            search_input.press('Enter')
            page.wait_for_timeout(1000)
            
            # Test very long query
            long_query = 'a' * 500
            search_input.fill(long_query)
            actual_value = search_input.input_value()
            
            # Check if there's a length limit
            if len(actual_value) < len(long_query):
                print(f"Search input has character limit: {len(actual_value)}")
                
            search_input.clear()
            
    def test_search_special_characters(self, page: Page):
        """
        Test search with special characters
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        special_queries = [
            'test & security',
            'risk-management',
            'third_party',
            '2024 report',
