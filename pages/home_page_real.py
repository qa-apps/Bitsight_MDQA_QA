from pages.base_page import BasePage
from playwright.sync_api import Page, Locator
from typing import List, Dict, Any

class HomePageReal(BasePage):
    """
    HomePage with ACTUAL selectors from BitSight's real DOM structure
    Based on DOM inspection performed on Nov 20, 2024
    """
    def __init__(self, page: Page):
        super().__init__(page)
        
        # REAL Navigation selectors from DOM
        self.header = 'header.site-header'
        self.main_nav = 'header.site-header nav'
        
        # REAL Menu items - these are the actual class names found
        self.menu_link_class = '.main-menu-block__item-link'
        self.resources_link = 'a.main-menu-block__item-link:has-text("Resources")'
        
        # REAL Demo buttons - actual URLs and classes found
        self.demo_button = 'a[href*="/demo/security-rating"]'
        self.demo_button_alt = 'a:has-text("Request Demo")'
        self.supply_chain_demo = 'a[href="/demo/security-rating"]:has-text("supply chain")'
        self.exposure_demo = 'a[href="/demo/bitsight-demo"]'
        self.threat_intel_demo = 'a[href="/demo/bitsight-threat-intelligence-demo"]'
        
        # REAL Login button
        self.login_button = 'a[href="https://service.bitsighttech.com/"]'
        
        # REAL Hero section - actual classes from DOM
        self.hero_container = '.hero-homepage__title'
        self.hero_h1 = 'h1:has-text("AI-powered intelligence")'
        
        # REAL Footer selector
        self.footer = 'footer.site-footer.footer'
        
        # REAL Form IDs found
        self.search_form = '#views-exposed-form-search-search-page'
        
        # REAL Button classes
        self.button_filled_white = '.button--filled-white'
        self.contact_button = 'a.button--filled-white[href="/contact-us"]'
        
    def verify_real_header_structure(self) -> Dict[str, bool]:
        """
        Verify the actual header structure exists
        """
        return {
            'header_exists': self.is_visible(self.header),
            'has_transparent_class': 'site-header--transparent' in (self.page.locator(self.header).get_attribute('class') or ''),
            'nav_exists': self.page.locator(f'{self.header} nav').count() > 0
        }
        
    def get_real_menu_links(self) -> List[Dict[str, str]]:
        """
        Get all actual menu links with the real class name
        """
        links = self.page.locator(self.menu_link_class).all()
        menu_items = []
        
        for link in links:
            menu_items.append({
                'text': link.text_content() or '',
                'href': link.get_attribute('href') or '',
                'class': link.get_attribute('class') or ''
            })
            
        return menu_items
        
    def click_real_demo_button(self, demo_type: str = 'main') -> None:
        """
        Click on actual demo buttons based on real href values
        """
        demo_map = {
            'main': self.demo_button,
            'supply_chain': self.supply_chain_demo,
            'exposure': self.exposure_demo,
            'threat_intel': self.threat_intel_demo
        }
        
        selector = demo_map.get(demo_type, self.demo_button)
        self.click_element(selector)
        
    def verify_real_hero_section(self) -> Dict[str, Any]:
        """
        Verify the actual hero section with real selectors
        """
        h1_element = self.page.locator('h1').first
        
        return {
            'h1_exists': h1_element.is_visible() if h1_element else False,
            'h1_text': h1_element.text_content() if h1_element else '',
            'hero_container_exists': self.is_visible(self.hero_container),
            'hero_contains_ai_text': 'AI-powered' in (h1_element.text_content() or '') if h1_element else False
        }
        
    def get_real_footer_info(self) -> Dict[str, Any]:
        """
        Get actual footer information
        """
        footer = self.page.locator(self.footer).first
        
        if footer and footer.is_visible():
            return {
                'exists': True,
                'class': footer.get_attribute('class'),
                'link_count': footer.locator('a').count(),
                'has_copyright': '©' in (footer.text_content() or '')
            }
        return {'exists': False}
        
    def search_using_real_form(self, query: str) -> None:
        """
        Use the actual search form found in DOM
        """
        search_form = self.page.locator(self.search_form).first
        
        if search_form and search_form.is_visible():
            search_input = search_form.locator('input[type="text"], input[type="search"]').first
            if search_input:
                search_input.fill(query)
                search_input.press('Enter')
                
    def get_all_real_images(self) -> List[Dict[str, str]]:
        """
        Get all images with their actual src and alt attributes
        """
        images = self.page.locator('img').all()[:10]  # First 10 images
        image_info = []
        
        for img in images:
            image_info.append({
                'src': img.get_attribute('src') or '',
                'alt': img.get_attribute('alt') or '',
                'class': img.get_attribute('class') or ''
            })
            
        return image_info
