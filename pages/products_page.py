from pages.base_page import BasePage
from playwright.sync_api import Page, Locator
from typing import List, Dict, Any, Optional

class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Product page locators
        self.page_title = 'h1'
        self.product_cards = '.product-card'
        self.features_section = '[data-testid="features"]'
        self.benefits_section = '[data-testid="benefits"]'
        self.pricing_link = 'a:has-text("Pricing")'
        self.documentation_link = 'a:has-text("Documentation")'
        
        # TPRM specific elements
        self.tprm_title = 'h1:has-text("Third-Party Risk Management")'
        self.vendor_profiles = 'text=vendor profiles'
        self.ai_assessment = 'text=AI to accelerate assessments'
        self.framework_mapping = 'text=security frameworks'
        
        # Exposure Management elements
        self.exposure_title = 'h1:has-text("Exposure Management")'
        self.digital_assets = 'text=digital assets'
        self.shadow_it = 'text=shadow IT'
        self.risk_visualization = 'text=visualize areas'
        
        # Threat Intelligence elements
        self.threat_title = 'h1:has-text("Cyber Threat Intelligence")'
        self.underground_forums = 'text=underground forums'
        self.real_time_monitoring = 'text=real-time'
        self.ransomware_insights = 'text=ransomware groups'
        
    def navigate_to_tprm(self) -> None:
        """
        Navigate to Third-Party Risk Management product page
        """
        self.navigate_to('/products/third-party-risk-management')
        self.wait_for_page_load()
        
    def navigate_to_exposure_management(self) -> None:
        """
        Navigate to Exposure Management product page
        """
        self.navigate_to('/solutions/exposure-management')
        self.wait_for_page_load()
        
    def navigate_to_threat_intelligence(self) -> None:
        """
        Navigate to Cyber Threat Intelligence product page
        """
        self.navigate_to('/products/cyber-threat-intelligence')
        self.wait_for_page_load()
        
    def verify_tprm_page_elements(self) -> Dict[str, bool]:
        """
        Verify all TPRM page elements are present
        """
        elements = {
            'title': self.is_visible(self.tprm_title),
            'vendor_profiles': self.is_visible(self.vendor_profiles),
            'ai_assessment': self.is_visible(self.ai_assessment),
            'framework_mapping': self.is_visible(self.framework_mapping)
        }
        return elements
        
    def verify_exposure_page_elements(self) -> Dict[str, bool]:
        """
        Verify all Exposure Management page elements
        """
        elements = {
            'title': self.is_visible(self.exposure_title),
            'digital_assets': self.is_visible(self.digital_assets),
            'shadow_it': self.is_visible(self.shadow_it),
            'risk_visualization': self.is_visible(self.risk_visualization)
        }
        return elements
        
    def verify_threat_intelligence_elements(self) -> Dict[str, bool]:
        """
        Verify all Threat Intelligence page elements
        """
        elements = {
            'title': self.is_visible(self.threat_title),
            'underground_forums': self.is_visible(self.underground_forums),
            'real_time': self.is_visible(self.real_time_monitoring),
            'ransomware': self.is_visible(self.ransomware_insights)
        }
        return elements
        
    def get_product_features(self) -> List[str]:
        """
        Extract all product features from the page
        """
        features = []
        feature_elements = self.page.locator('li').all()
        for element in feature_elements:
            text = element.text_content()
            if text and len(text) > 10:
                features.append(text)
        return features
        
    def click_request_demo_button(self) -> None:
        """
        Click on the Request Demo button on product page
        """
        demo_button = self.page.locator('a:has-text("Request") >> visible=true').first
        if demo_button:
            demo_button.click()
            
    def click_learn_more_button(self) -> None:
        """
        Click on Learn More button
        """
        learn_more = self.page.locator('a:has-text("Learn more") >> visible=true').first
        if learn_more:
            learn_more.click()
            
    def verify_product_navigation(self) -> bool:
        """
        Verify product navigation works correctly
        """
        current_url = self.get_page_url()
        return '/products' in current_url or '/solutions' in current_url
        
    def check_product_images(self) -> bool:
        """
        Check if all product images are loaded
        """
        images = self.page.locator('img').all()
        for img in images:
            if img.is_visible():
                natural_width = img.evaluate('el => el.naturalWidth')
                if natural_width == 0:
                    return False
        return True
        
    def get_related_products(self) -> List[str]:
        """
        Get list of related products if displayed
        """
        related_section = self.page.locator('text=Related Products')
        if related_section.is_visible():
            related_items = self.page.locator('.related-product').all()
            return [item.text_content() or '' for item in related_items]
        return []
        
    def verify_cta_buttons(self) -> Dict[str, bool]:
        """
        Verify all CTA buttons are present and clickable
        """
        ctas = {
            'demo': self.page.locator('a:has-text("Demo")').is_visible(),
            'contact': self.page.locator('a:has-text("Contact")').is_visible(),
            'learn': self.page.locator('a:has-text("Learn")').is_visible()
        }
        return ctas
        
    def check_video_content(self) -> bool:
        """
        Check if video content is present and playable
        """
        videos = self.page.locator('video, iframe[src*="youtube"], iframe[src*="vimeo"]')
        return videos.count() > 0
        
    def get_testimonials(self) -> List[Dict[str, str]]:
        """
        Extract customer testimonials if present
        """
        testimonials = []
        testimonial_elements = self.page.locator('.testimonial, [data-testid="testimonial"]').all()
        
        for element in testimonial_elements:
            quote = element.locator('.quote, blockquote').text_content()
            author = element.locator('.author, .name').text_content()
            if quote and author:
                testimonials.append({'quote': quote, 'author': author})
                
        return testimonials
        
    def verify_breadcrumbs(self) -> bool:
        """
        Verify breadcrumb navigation is present
        """
        breadcrumbs = self.page.locator('nav[aria-label="breadcrumb"], .breadcrumb')
        return breadcrumbs.is_visible()
        
    def check_social_sharing(self) -> Dict[str, bool]:
        """
        Check for social sharing buttons
        """
        social_buttons = {
            'twitter': self.page.locator('a[href*="twitter.com"]').is_visible(),
            'linkedin': self.page.locator('a[href*="linkedin.com"]').is_visible(),
            'facebook': self.page.locator('a[href*="facebook.com"]').is_visible()
        }
        return social_buttons
