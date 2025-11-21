#!/usr/bin/env python3
"""
Restore all project files
"""

import os

# Create all directories
dirs = ['pages', 'tests']
for d in dirs:
    os.makedirs(d, exist_ok=True)

# All file contents stored here
FILES = {
    'requirements.txt': '''playwright==1.40.0
pytest==7.4.3
pytest-playwright==0.4.3
pytest-xdist==3.5.0
pytest-html==4.1.1
python-dotenv==1.0.0
faker==20.1.0
allure-pytest==2.13.2
requests==2.31.0
Pillow==10.1.0''',

    'pages/home_page.py': '''"""
Home Page Object for BitSight website
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Navigation menu locators
        self.navigation_menu = 'nav'
        self.solutions_menu = 'button:has-text("Solutions")'
        self.products_menu = 'button:has-text("Products")'
        self.resources_menu = 'button:has-text("Resources")'
        self.company_menu = 'button:has-text("Company")'
        
        # Call to action buttons
        self.request_demo_button = 'a:has-text("Request a demo")'
        self.demo_button = 'a:has-text("Get a Demo"), a:has-text("Request Demo")'
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
        Click on Login button
        """
        self.click_element(self.login_button)
        
    def verify_navigation_menu(self) -> Dict[str, bool]:
        """
        Verify all navigation menu items are present
        """
        return {
            'solutions': self.is_visible(self.solutions_menu),
            'products': self.is_visible(self.products_menu),
            'resources': self.is_visible(self.resources_menu),
            'company': self.is_visible(self.company_menu)
        }
        
    def scroll_to_product_section(self, product: str) -> None:
        """
        Scroll to specific product section
        """
        product_locators = {
            'tprm': self.tprm_section,
            'exposure': self.exposure_section,
            'threat_intel': self.threat_intel_section,
            'governance': self.governance_section
        }
        
        if product.lower() in product_locators:
            self.scroll_to_element(product_locators[product.lower()])
''',

    'pages/products_page.py': '''"""
Products Page Object for BitSight website
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List, Dict

class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Product navigation paths
        self.tprm_path = '/products/third-party-risk-management'
        self.exposure_path = '/solutions/exposure-management'
        self.threat_intel_path = '/products/cyber-threat-intelligence'
        
        # Product page elements
        self.product_title = 'h1'
        self.product_description = '.product-description, .hero-subtitle'
        self.features_section = '.features, .benefits'
        self.pricing_link = 'a:has-text("Pricing")'
        self.demo_cta = 'a:has-text("Get a Demo"), a:has-text("Request Demo")'
        
        # TPRM specific elements
        self.vendor_risk = 'text=Vendor Risk'
        self.continuous_monitoring = 'text=Continuous Monitoring'
        self.risk_assessment = 'text=Risk Assessment'
        
        # Exposure Management specific elements
        self.attack_surface = 'text=Attack Surface'
        self.vulnerability_management = 'text=Vulnerability'
        self.security_posture = 'text=Security Posture'
        
        # Threat Intelligence specific elements
        self.threat_detection = 'text=Threat Detection'
        self.incident_response = 'text=Incident Response'
        self.threat_analytics = 'text=Analytics'
        
    def navigate_to_tprm(self) -> None:
        """Navigate to Third-Party Risk Management page"""
        self.navigate_to(self.tprm_path)
        self.wait_for_page_load()
        
    def navigate_to_exposure(self) -> None:
        """Navigate to Exposure Management page"""
        self.navigate_to(self.exposure_path)
        self.wait_for_page_load()
        
    def navigate_to_threat_intel(self) -> None:
        """Navigate to Cyber Threat Intelligence page"""
        self.navigate_to(self.threat_intel_path)
        self.wait_for_page_load()
        
    def get_product_title(self) -> str:
        """Get the product page title"""
        return self.get_text_content(self.product_title)
        
    def get_product_features(self) -> List[str]:
        """Get list of product features"""
        features = []
        feature_elements = self.page.locator('.feature-item, .benefit-item, li').all()
        
        for element in feature_elements[:10]:  # Limit to first 10
            text = element.text_content()
            if text:
                features.append(text.strip())
                
        return features
        
    def is_demo_cta_visible(self) -> bool:
        """Check if demo CTA is visible"""
        return self.is_visible(self.demo_cta)
        
    def click_demo_cta(self) -> None:
        """Click on demo CTA button"""
        self.click_element(self.demo_cta)
        
    def verify_tprm_elements(self) -> Dict[str, bool]:
        """Verify TPRM page specific elements"""
        return {
            'vendor_risk': self.is_visible(self.vendor_risk),
            'continuous_monitoring': self.is_visible(self.continuous_monitoring),
            'risk_assessment': self.is_visible(self.risk_assessment)
        }
        
    def verify_exposure_elements(self) -> Dict[str, bool]:
        """Verify Exposure Management page specific elements"""
        return {
            'attack_surface': self.is_visible(self.attack_surface),
            'vulnerability_management': self.is_visible(self.vulnerability_management),
            'security_posture': self.is_visible(self.security_posture)
        }
        
    def verify_threat_intel_elements(self) -> Dict[str, bool]:
        """Verify Threat Intelligence page specific elements"""
        return {
            'threat_detection': self.is_visible(self.threat_detection),
            'incident_response': self.is_visible(self.incident_response),
            'threat_analytics': self.is_visible(self.threat_analytics)
        }
        
    def get_pricing_info(self) -> bool:
        """Check if pricing information is available"""
        if self.is_visible(self.pricing_link):
            self.click_element(self.pricing_link)
            self.wait_for_page_load()
            return True
        return False
        
    def scroll_to_features(self) -> None:
        """Scroll to features section"""
        if self.is_visible(self.features_section):
            self.scroll_to_element(self.features_section)
            
    def get_testimonials(self) -> List[str]:
        """Get customer testimonials if available"""
        testimonials = []
        testimonial_elements = self.page.locator('.testimonial, .quote, blockquote').all()
        
        for element in testimonial_elements[:5]:  # Limit to first 5
            text = element.text_content()
            if text:
                testimonials.append(text.strip())
                
        return testimonials
''',
}

# Write all files
for filepath, content in FILES.items():
    print(f"Restoring {filepath}")
    with open(filepath, 'w') as f:
        f.write(content)

print("\nAll files restored successfully!")
