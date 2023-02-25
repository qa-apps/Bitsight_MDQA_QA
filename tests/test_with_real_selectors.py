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
