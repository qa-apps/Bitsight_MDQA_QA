import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from typing import List

@pytest.mark.navigation
@pytest.mark.dropdown
class TestDropdownMenus:
    """
    Comprehensive dropdown menu testing for BitSight website
    """
    
    def test_solutions_dropdown_complete(self, page: Page):
