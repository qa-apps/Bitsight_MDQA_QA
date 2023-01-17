import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
import json

@pytest.mark.structure
class TestPageStructure:
    """
    Page structure and validation tests for BitSight website
    """
    
    def test_html_structure_validity(self, page: Page):
        """
        Test HTML structure and DOCTYPE
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
