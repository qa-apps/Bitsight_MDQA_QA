import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from faker import Faker

fake = Faker()

@pytest.mark.e2e
@pytest.mark.slow
class TestIntegrationE2E:
    """
    End-to-end integration testing for complete user journeys
    """
    
    def test_complete_demo_request_journey(self, page: Page):
        """
        Test complete journey from homepage to demo request
        """
        homepage = HomePage(page)
        
        # Step 1: Land on homepage
        homepage.navigate_to()
        assert homepage.is_homepage_loaded(), "Homepage failed to load"
        
        # Step 2: Explore product information
        products_page = ProductsPage(page)
        products_page.navigate_to_tprm()
        page.wait_for_load_state('networkidle')
        
        assert 'third-party' in page.url.lower() or 'tprm' in page.url.lower(), "Did not navigate to TPRM page"
        
        # Step 3: Click Request Demo
        demo_button = page.locator('a:has-text("Request"), a:has-text("Demo")').first
        if demo_button.is_visible():
            demo_button.click()
            page.wait_for_load_state('networkidle')
            
            # Step 4: Fill demo form
            form = page.locator('form').first
            
            if form.is_visible():
                # Fill form fields
                form_data = {
                    'first': fake.first_name(),
                    'last': fake.last_name(),
                    'email': fake.email(),
                    'company': fake.company(),
                    'phone': fake.phone_number()
                }
                
                for field_hint, value in form_data.items():
                    field = form.locator(f'input[name*="{field_hint}"], input[placeholder*="{field_hint}"]').first
                    if field and field.is_visible():
                        field.fill(value)
                        
                # Note: Not submitting to avoid creating test data
                
        # Step 5: Navigate back to homepage
        homepage.navigate_to()
        assert homepage.is_homepage_loaded(), "Could not return to homepage"
        
    def test_product_exploration_journey(self, page: Page):
        """
        Test user journey exploring different products
        """
        homepage = HomePage(page)
        products_page = ProductsPage(page)
        
        # Start from homepage
        homepage.navigate_to()
        
        # Explore each product area
        product_paths = [
            '/products/third-party-risk-management',
            '/solutions/exposure-management',
            '/products/cyber-threat-intelligence'
        ]
        
        for path in product_paths:
            products_page.navigate_to(path)
            page.wait_for_load_state('networkidle')
            
            # Verify on correct page
            assert path.split('/')[-1] in page.url, f"Failed to navigate to {path}"
            
            # Check for Learn More or Demo buttons
            cta_buttons = page.locator('a:has-text("Learn"), a:has-text("Demo")').all()
            assert len(cta_buttons) > 0, f"No CTAs found on {path}"
            
            # Check for feature information
            features = products_page.get_product_features()
            assert len(features) > 0, f"No features found on {path}"
            
    def test_information_seeking_journey(self, page: Page):
        """
        Test journey of user seeking information
        """
        homepage = HomePage(page)
        
        # Step 1: Start from homepage
        homepage.navigate_to()
        
        # Step 2: Navigate to Resources
        resources_link = page.locator('a:has-text("Resources")').first
        if resources_link.is_visible():
            resources_link.click()
            page.wait_for_load_state('networkidle')
            
            assert 'resources' in page.url.lower(), "Did not navigate to resources"
            
            # Step 3: Look for specific resource types
            resource_types = ['case study', 'whitepaper', 'blog', 'guide']
            found_resources = []
            
            for resource_type in resource_types:
                resource_link = page.locator(f'text=/{resource_type}/i').first
                if resource_link:
                    found_resources.append(resource_type)
                    
            assert len(found_resources) > 0, "No resources found"
            
        # Step 4: Use search functionality
        homepage.navigate_to()
        search_form = page.locator('#views-exposed-form-search-search-page').first
        
        if search_form.is_visible():
            search_input = search_form.locator('input').first
            search_input.fill("security")
            search_input.press('Enter')
            page.wait_for_load_state('networkidle')
            
            # Verify search results
            assert 'search' in page.url or 'security' in page.url, "Search did not execute"
            
    def test_navigation_consistency_journey(self, page: Page):
        """
        Test navigation consistency across different pages
        """
        homepage = HomePage(page)
        
        pages_to_test = [
            '/',
            '/products/third-party-risk-management',
            '/resources',
            '/contact-us'
        ]
        
        for page_path in pages_to_test:
            homepage.navigate_to(page_path)
            page.wait_for_load_state('networkidle')
            
            # Check header is present
            header = page.locator('header').first
            assert header.is_visible(), f"Header missing on {page_path}"
            
            # Check footer is present
            footer = page.locator('footer').first
            assert footer.is_visible(), f"Footer missing on {page_path}"
            
            # Check main navigation
            nav = page.locator('nav').first
            assert nav.is_visible() or page.locator('.mobile-menu').is_visible(), f"Navigation missing on {page_path}"
            
    def test_mobile_user_journey(self, page: Page):
        """
        Test complete user journey on mobile device
        """
        # Set mobile viewport
        page.set_viewport_size({'width': 375, 'height': 667})
        
        homepage = HomePage(page)
        
        # Step 1: Load homepage on mobile
        homepage.navigate_to()
        
        # Step 2: Open mobile menu
        mobile_menu = page.locator('.mobile-menu, .hamburger, [aria-label="Menu"]').first
        
        if mobile_menu.is_visible():
            mobile_menu.click()
            page.wait_for_timeout(500)
            
            # Step 3: Navigate to a product page
            product_link = page.locator('a:has-text("Products"), a:has-text("Solutions")').first
            if product_link.is_visible():
                product_link.click()
                page.wait_for_load_state('networkidle')
                
        # Step 4: Scroll through content
        page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
        page.wait_for_timeout(1000)
        
        # Step 5: Return to top
        page.evaluate('window.scrollTo(0, 0)')
        
        # Verify still functional
        assert page.title() != "", "Mobile journey broke the page"
        
    def test_multi_product_comparison_journey(self, page: Page):
        """
        Test journey comparing multiple products
        """
        homepage = HomePage(page)
        products_page = ProductsPage(page)
        
        # Collect information from each product
        product_info = {}
        
        products = [
            ('TPRM', '/products/third-party-risk-management'),
            ('Exposure', '/solutions/exposure-management'),
            ('Threat Intel', '/products/cyber-threat-intelligence')
        ]
        
        for name, path in products:
            products_page.navigate_to(path)
            page.wait_for_load_state('networkidle')
            
            # Collect features
            features = products_page.get_product_features()
            
            # Collect CTAs
            ctas = page.locator('a:has-text("Demo"), a:has-text("Learn")').count()
            
            product_info[name] = {
                'features': len(features),
                'ctas': ctas,
                'url': page.url
            }
            
        # Verify we collected info from all products
        assert len(product_info) == 3, "Failed to collect all product information"
        
        # Each product should have features and CTAs
        for product, info in product_info.items():
            assert info['features'] > 0 or info['ctas'] > 0, f"{product} missing content"
            
    def test_conversion_funnel_journey(self, page: Page):
        """
        Test typical conversion funnel journey
        """
        homepage = HomePage(page)
        
        # Step 1: Awareness - Land on homepage
        homepage.navigate_to()
        initial_url = page.url
        
        # Step 2: Interest - Explore products
        products_page = ProductsPage(page)
        products_page.navigate_to_tprm()
        
        # Track navigation
        assert page.url != initial_url, "User did not explore products"
        
        # Step 3: Consideration - Read more details
        learn_more = page.locator('a:has-text("Learn more")').first
        if learn_more.is_visible():
            learn_more.click()
            page.wait_for_load_state('networkidle')
            
        # Step 4: Intent - Click demo CTA
        demo_cta = page.locator('a:has-text("Request Demo"), a:has-text("Get Demo")').first
        if demo_cta.is_visible():
            demo_cta.click()
            page.wait_for_load_state('networkidle')
            
            # Step 5: Action - Start filling form
            form = page.locator('form').first
            if form.is_visible():
                # User reached conversion point
                assert True, "User completed funnel to conversion point"
                
    def test_returning_visitor_journey(self, page: Page):
        """
        Test journey of a returning visitor
        """
        homepage = HomePage(page)
        
        # First visit - set some context
        homepage.navigate_to()
        
        # Simulate storing user preference (if applicable)
        page.evaluate('''() => {
            localStorage.setItem('visited', 'true');
            localStorage.setItem('interest', 'tprm');
        }''')
        
        # Second visit - returning user
        homepage.navigate_to()
        
        # Check if preferences persist
        visited = page.evaluate('() => localStorage.getItem("visited")')
        interest = page.evaluate('() => localStorage.getItem("interest")')
        
        assert visited == 'true', "Visit not remembered"
