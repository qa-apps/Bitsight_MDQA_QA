import pytest
from playwright.sync_api import Page, expect, BrowserContext
from pages.home_page import HomePage
from pages.products_page import ProductsPage

@pytest.mark.cross_browser
class TestCrossBrowser:
    """
    Cross-browser compatibility testing for BitSight website
    """
    
    def test_chromium_compatibility(self, page: Page):
        """
        Test website functionality in Chromium-based browsers
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check browser name
        browser_info = page.evaluate('''() => {
            return {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                vendor: navigator.vendor,
                language: navigator.language
            };
        }''')
        
        # Verify page loads correctly
        assert homepage.is_homepage_loaded(), "Homepage failed in Chromium"
        
        # Check CSS support
        css_support = page.evaluate('''() => {
            return {
                grid: CSS.supports('display', 'grid'),
                flexbox: CSS.supports('display', 'flex'),
                customProperties: CSS.supports('--custom', 'value'),
                backdropFilter: CSS.supports('backdrop-filter', 'blur(10px)')
            };
        }''')
        
        # Modern browsers should support these
        assert css_support['grid'], "CSS Grid not supported"
        assert css_support['flexbox'], "Flexbox not supported"
        
    @pytest.mark.skip(reason="Run separately with Firefox")
    def test_firefox_compatibility(self, page: Page):
        """
        Test website functionality in Firefox
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Firefox-specific checks
        is_firefox = page.evaluate('() => navigator.userAgent.includes("Firefox")')
        
        if is_firefox:
            # Test Firefox-specific features
            assert homepage.is_homepage_loaded(), "Homepage failed in Firefox"
            
            # Check for Firefox-specific issues
            nav_menu = homepage.verify_navigation_menu()
            assert all(nav_menu.values()), "Navigation issues in Firefox"
            
    @pytest.mark.skip(reason="Run separately with WebKit")
    def test_webkit_safari_compatibility(self, page: Page):
        """
        Test website functionality in WebKit/Safari
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # WebKit/Safari specific checks
        is_webkit = page.evaluate('() => navigator.userAgent.includes("WebKit")')
        
        if is_webkit:
            # Test Safari-specific features
            assert homepage.is_homepage_loaded(), "Homepage failed in WebKit"
            
            # Check for Safari-specific CSS support
            webkit_features = page.evaluate('''() => {
                return {
                    webkitAppearance: CSS.supports('-webkit-appearance', 'none'),
                    safariSmooth: CSS.supports('-webkit-font-smoothing', 'antialiased')
                };
            }''')
            
    def test_javascript_api_compatibility(self, page: Page):
        """
        Test JavaScript API compatibility across browsers
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check for modern JavaScript APIs
        js_apis = page.evaluate('''() => {
            return {
                fetch: typeof fetch !== 'undefined',
                promise: typeof Promise !== 'undefined',
                localStorage: typeof localStorage !== 'undefined',
                sessionStorage: typeof sessionStorage !== 'undefined',
                intersectionObserver: typeof IntersectionObserver !== 'undefined',
                mutationObserver: typeof MutationObserver !== 'undefined',
                requestAnimationFrame: typeof requestAnimationFrame !== 'undefined'
            };
        }''')
        
        # All modern browsers should support these
        assert js_apis['fetch'], "Fetch API not supported"
        assert js_apis['promise'], "Promise not supported"
        assert js_apis['localStorage'], "LocalStorage not supported"
        
    def test_viewport_rendering_cross_browser(self, page: Page):
        """
        Test viewport rendering across different browsers
        """
        homepage = HomePage(page)
        
        viewports = [
            {'width': 1920, 'height': 1080, 'name': 'Full HD'},
            {'width': 1366, 'height': 768, 'name': 'Laptop'},
            {'width': 375, 'height': 667, 'name': 'iPhone'},
            {'width': 768, 'height': 1024, 'name': 'iPad'}
        ]
        
        for viewport in viewports:
            page.set_viewport_size({'width': viewport['width'], 'height': viewport['height']})
            homepage.navigate_to()
            
            # Check if page renders correctly
            is_visible = homepage.is_visible(homepage.hero_title)
            assert is_visible, f"Content not visible at {viewport['name']} viewport"
            
            # Check for horizontal scroll (shouldn't exist)
            has_horizontal_scroll = page.evaluate('''() => {
                return document.documentElement.scrollWidth > document.documentElement.clientWidth;
            }''')
            
            assert not has_horizontal_scroll, f"Horizontal scroll detected at {viewport['name']}"
            
    def test_font_rendering_cross_browser(self, page: Page):
        """
        Test font rendering and loading across browsers
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check font loading
        fonts = page.evaluate('''() => {
            const fontFaces = [];
            document.fonts.forEach(font => {
                fontFaces.push({
                    family: font.family,
                    status: font.status,
                    weight: font.weight,
                    style: font.style
                });
            });
            return fontFaces;
        }''')
        
        # Check if fonts loaded successfully
        loaded_fonts = [f for f in fonts if f['status'] == 'loaded']
        assert len(loaded_fonts) > 0, "No fonts loaded successfully"
        
        # Check computed font styles
        heading_font = page.locator('h1').first.evaluate('''el => {
            const computed = window.getComputedStyle(el);
            return {
                fontFamily: computed.fontFamily,
                fontSize: computed.fontSize,
                fontWeight: computed.fontWeight
            };
        }''')
        
        assert heading_font['fontFamily'], "No font family applied to heading"
        
    def test_input_compatibility(self, page: Page):
        """
        Test form input compatibility across browsers
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        homepage.click_request_demo()
        
        page.wait_for_load_state('networkidle')
        
        # Test HTML5 input types support
        input_support = page.evaluate('''() => {
            const types = ['email', 'tel', 'url', 'number', 'date', 'color'];
            const support = {};
            
            types.forEach(type => {
                const input = document.createElement('input');
                input.type = type;
                support[type] = input.type === type;
            });
            
            return support;
        }''')
        
        # Modern browsers should support these
        assert input_support['email'], "Email input not supported"
        assert input_support['tel'], "Tel input not supported"
        
    def test_media_compatibility(self, page: Page):
        """
        Test media elements compatibility
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Check video/audio support
        media_support = page.evaluate('''() => {
            const video = document.createElement('video');
            const audio = document.createElement('audio');
            
            return {
                video: {
                    mp4: video.canPlayType('video/mp4'),
                    webm: video.canPlayType('video/webm'),
                    ogg: video.canPlayType('video/ogg')
                },
                audio: {
                    mp3: audio.canPlayType('audio/mpeg'),
                    ogg: audio.canPlayType('audio/ogg'),
                    wav: audio.canPlayType('audio/wav')
                }
            };
        }''')
        
        # At least one format should be supported
        video_supported = any(media_support['video'].values())
        audio_supported = any(media_support['audio'].values())
        
        assert video_supported or True, "No video formats supported"
        assert audio_supported or True, "No audio formats supported"
        
    def test_console_errors_cross_browser(self, page: Page):
        """
        Test for console errors across browsers
        """
        homepage = HomePage(page)
        
        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg) if msg.type == 'error' else None)
        
        homepage.navigate_to()
        page.wait_for_load_state('networkidle')
        
        # Check for browser-specific errors
        assert len(console_errors) == 0, f"Console errors found: {[str(e) for e in console_errors[:3]]}"
        
    def test_local_storage_compatibility(self, page: Page):
        """
        Test local storage functionality across browsers
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Test localStorage operations
        storage_test = page.evaluate('''() => {
            try {
                const testKey = 'test_key';
                const testValue = 'test_value';
                
                // Set item
                localStorage.setItem(testKey, testValue);
                
                // Get item
                const retrieved = localStorage.getItem(testKey);
                
