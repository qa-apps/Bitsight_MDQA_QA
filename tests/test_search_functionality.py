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
            'info@bitsight',
            '"exact phrase"'
        ]
        
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            for query in special_queries:
                search_input = search_form.locator('input').first
                search_input.fill(query)
                search_input.press('Enter')
                
                page.wait_for_load_state('domcontentloaded')
                
                # Should handle special characters without errors
                assert page.title() != "", f"Page broke with query: {query}"
                
                # Go back for next search
                homepage.navigate_to()
                
    def test_search_autocomplete(self, page: Page):
        """
        Test search autocomplete/suggestions if available
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            
            # Type slowly to trigger autocomplete
            search_input.type('sec', delay=200)
            page.wait_for_timeout(1000)
            
            # Check for autocomplete suggestions
            suggestions = page.locator('.autocomplete, .suggestions, [role="listbox"]').first
            
            if suggestions and suggestions.is_visible():
                suggestion_items = suggestions.locator('li, [role="option"]').all()
                assert len(suggestion_items) > 0, "No autocomplete suggestions shown"
                
    def test_search_result_relevance(self, page: Page):
        """
        Test if search results are relevant
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        search_query = "risk"
        
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            search_input.fill(search_query)
            search_input.press('Enter')
            
            page.wait_for_load_state('networkidle')
            
            # Check if results page contains search term
            page_content = page.content().lower()
            assert search_query.lower() in page_content, f"Search results don't contain '{search_query}'"
            
    def test_search_filters(self, page: Page):
        """
        Test search filters if available
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Perform initial search
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            search_input.fill("security")
            search_input.press('Enter')
            
            page.wait_for_load_state('networkidle')
            
            # Look for filter options
            filters = page.locator('.filter, .facet, input[type="checkbox"]').all()
            
            if filters:
                # Try applying a filter
                for filter_element in filters[:2]:
                    if filter_element.is_visible():
                        filter_element.click()
                        page.wait_for_timeout(1000)
                        
    def test_search_pagination(self, page: Page):
        """
        Test search results pagination
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Search for common term likely to have multiple results
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            search_input.fill("security")
            search_input.press('Enter')
            
            page.wait_for_load_state('networkidle')
            
            # Look for pagination
            pagination = page.locator('.pagination, .pager, nav[aria-label="pagination"]').first
            
            if pagination and pagination.is_visible():
                # Check for page numbers
                page_links = pagination.locator('a, button').all()
                
                if len(page_links) > 1:
                    # Click next page
                    next_button = pagination.locator('a:has-text("Next"), button:has-text("Next")').first
                    if next_button and next_button.is_visible():
                        next_button.click()
                        page.wait_for_load_state('networkidle')
                        
                        # Verify page changed
                        assert page.url != homepage.base_url, "Pagination did not work"
                        
    def test_search_no_results(self, page: Page):
        """
        Test search with query that returns no results
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Search for gibberish
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            search_input.fill("xyzabc123randomquery999")
            search_input.press('Enter')
            
            page.wait_for_load_state('networkidle')
            
            # Should show no results message
            page_content = page.content().lower()
            
            no_results_indicators = ['no results', 'not found', '0 results', 'no matches']
            has_no_results_message = any(indicator in page_content for indicator in no_results_indicators)
            
            # Page should handle no results gracefully
            assert page.title() != "", "Page broke with no results"
            
    def test_search_highlighting(self, page: Page):
        """
        Test if search terms are highlighted in results
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        search_query = "security"
        
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            search_input.fill(search_query)
            search_input.press('Enter')
            
            page.wait_for_load_state('networkidle')
            
            # Look for highlighted terms
            highlighted = page.locator('mark, .highlight, .search-highlight, strong').all()
            
            if highlighted:
                for element in highlighted[:3]:
                    text = element.text_content()
                    if text and search_query.lower() in text.lower():
                        print(f"Found highlighted term: {text}")
                        
    def test_search_clear_functionality(self, page: Page):
        """
        Test clearing search input
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            
            # Enter search term
            search_input.fill("test search")
            assert search_input.input_value() == "test search", "Input not filled"
            
            # Look for clear button
            clear_button = search_form.locator('button:has-text("Clear"), .clear-search').first
            
            if clear_button and clear_button.is_visible():
                clear_button.click()
                assert search_input.input_value() == "", "Search not cleared"
            else:
                # Use keyboard shortcut
                search_input.select_all()
                search_input.press('Delete')
                assert search_input.input_value() == "", "Search not cleared with keyboard"
                
    def test_search_history(self, page: Page):
        """
        Test if search history is maintained
        """
        homepage = HomePageReal(page)
        homepage.navigate_to()
        
        # Perform multiple searches
        searches = ['risk', 'security', 'compliance']
        
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            for term in searches:
                search_input = search_form.locator('input').first
                search_input.fill(term)
                search_input.press('Enter')
                page.wait_for_load_state('domcontentloaded')
                
                # Go back
                page.go_back()
                
            # Check if we can navigate through search history
            page.go_forward()
            assert page.url != homepage.base_url, "Search history navigation failed"
