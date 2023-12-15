from pages.base_page import BasePage
from playwright.sync_api import Page, Locator
from typing import List, Dict, Any

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Navigation menu locators
        self.solutions_menu = 'button:has-text("Solutions")'
        self.products_menu = 'button:has-text("Products")'
        self.resources_menu = 'button:has-text("Resources")'
        self.company_menu = 'button:has-text("Company")'
        self.demo_button = 'a:has-text("Request Demo")'
        self.login_button = 'a:has-text("Log In")'
        
        # Hero section locators
        self.hero_title = 'h1'
        self.hero_subtitle = 'h2'
        self.learn_more_button = 'a:has-text("Learn more")'
        self.customer_stories_link = 'a:has-text("See customer stories")'
        
        # Product sections
        self.tprm_section = 'text=Third-Party Risk Management'
        self.exposure_section = 'text=Exposure Management'
        self.threat_intel_section = 'text=Cyber Threat Intelligence'
        self.governance_section = 'text=Governance & Reporting'
        
    def is_homepage_loaded(self) -> bool:
        """
        Verify homepage is properly loaded
        """
        self.wait_for_page_load()
        return self.is_visible(self.hero_title) and 'bitsight' in self.page.url.lower()
        
    def click_solutions_menu(self) -> None:
        """
        Click on Solutions menu to open dropdown
        """
        self.hover_over_element(self.solutions_menu)
        self.click_element(self.solutions_menu)
        
    def click_products_menu(self) -> None:
        """
        Click on Products menu to open dropdown
        """
        self.hover_over_element(self.products_menu)
        self.click_element(self.products_menu)
        
    def click_resources_menu(self) -> None:
        """
        Click on Resources menu to open dropdown
        """
        self.hover_over_element(self.resources_menu)
        self.click_element(self.resources_menu)
        
    def click_company_menu(self) -> None:
        """
        Click on Company menu to open dropdown
        """
        self.hover_over_element(self.company_menu)
        self.click_element(self.company_menu)
        
    def get_solutions_dropdown_items(self) -> List[str]:
        """
        Get all items from Solutions dropdown menu
        """
        self.click_solutions_menu()
        self.page.wait_for_timeout(1000)
        items = self.page.locator('[role="menu"] a').all()
        return [item.text_content() or '' for item in items]
        
    def get_products_dropdown_items(self) -> List[str]:
        """
        Get all items from Products dropdown menu
        """
        self.click_products_menu()
        self.page.wait_for_timeout(1000)
        items = self.page.locator('[role="menu"] a').all()
        return [item.text_content() or '' for item in items]
        
    def get_resources_dropdown_items(self) -> List[str]:
        """
        Get all items from Resources dropdown menu
        """
        self.click_resources_menu()
        self.page.wait_for_timeout(1000)
        items = self.page.locator('[role="menu"] a').all()
        return [item.text_content() or '' for item in items]
        
    def click_request_demo(self) -> None:
        """
        Click on Request Demo button
        """
        self.click_element(self.demo_button)
        
    def click_login(self) -> None:
        """
        Click on Log In button
        """
        self.click_element(self.login_button)
        
    def verify_hero_section(self) -> Dict[str, bool]:
        """
        Verify all elements in hero section are present
        """
        results = {
            'hero_title': self.is_visible(self.hero_title),
            'hero_subtitle': self.is_visible(self.hero_subtitle),
            'learn_more': self.is_visible(self.learn_more_button),
            'customer_stories': self.is_visible(self.customer_stories_link)
        }
        return results
        
    def verify_product_sections(self) -> Dict[str, bool]:
        """
        Verify all product sections are visible
        """
        results = {
            'tprm': self.is_visible(self.tprm_section),
            'exposure': self.is_visible(self.exposure_section),
            'threat_intel': self.is_visible(self.threat_intel_section),
            'governance': self.is_visible(self.governance_section)
        }
        return results
        
    def navigate_to_product_section(self, section: str) -> None:
        """
        Navigate to specific product section
        """
        section_map = {
            'tprm': self.tprm_section,
            'exposure': self.exposure_section,
            'threat_intel': self.threat_intel_section,
            'governance': self.governance_section
        }
        
        if section.lower() in section_map:
            self.scroll_to_element(section_map[section.lower()])
            self.click_element(section_map[section.lower()])
            
    def get_footer_links(self) -> List[str]:
        """
        Get all links from the footer section
        """
        footer = self.page.locator('footer')
        links = footer.locator('a[href]').all()
        return [link.get_attribute('href') or '' for link in links]
        
    def verify_navigation_menu(self) -> Dict[str, bool]:
        """
        Verify all navigation menu items are present
        """
        results = {
            'solutions': self.is_visible(self.solutions_menu),
            'products': self.is_visible(self.products_menu),
            'resources': self.is_visible(self.resources_menu),
            'company': self.is_visible(self.company_menu),
            'demo': self.is_visible(self.demo_button),
            'login': self.is_visible(self.login_button)
        }
        return results
        
    def search_site(self, query: str) -> None:
        """
        Perform site search if search functionality exists
        """
        search_button = self.page.locator('[aria-label="Search"]')
        if search_button.is_visible():
            search_button.click()
            search_input = self.page.locator('input[type="search"]')
            search_input.fill(query)
            search_input.press('Enter')
            
    def check_responsive_design(self) -> Dict[str, bool]:
        """
        Check if page is responsive at different viewports
        """
        viewports = {
            'desktop': {'width': 1920, 'height': 1080},
            'tablet': {'width': 768, 'height': 1024},
            'mobile': {'width': 375, 'height': 667}
        }
        
        results = {}
        for device, viewport in viewports.items():
            self.page.set_viewport_size(viewport)
            self.page.wait_for_timeout(1000)
            results[device] = self.is_visible(self.hero_title)
            
        return results
