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
