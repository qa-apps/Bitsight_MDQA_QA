import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
import time
import json

@pytest.mark.performance
class TestPerformanceMetrics:
    """
    Performance testing for BitSight website
    """
    
    def test_page_load_time(self, page: Page):
        """
        Test page load time is within acceptable limits
        """
        homepage = HomePage(page)
        
        # Measure load time
        start_time = time.time()
        homepage.navigate_to()
        page.wait_for_load_state('networkidle')
        load_time = time.time() - start_time
        
        assert load_time < 10, f"Page load time too long: {load_time:.2f} seconds"
        
        # Get detailed timing metrics
        timing = page.evaluate('''() => {
            const perf = performance.timing;
            return {
                dns: perf.domainLookupEnd - perf.domainLookupStart,
                tcp: perf.connectEnd - perf.connectStart,
                request: perf.responseStart - perf.requestStart,
                response: perf.responseEnd - perf.responseStart,
                dom: perf.domComplete - perf.domLoading,
                load: perf.loadEventEnd - perf.loadEventStart,
                total: perf.loadEventEnd - perf.navigationStart
            };
        }''')
        
        # Check individual metrics
        assert timing['dns'] < 1000, f"DNS lookup too slow: {timing['dns']}ms"
        assert timing['dom'] < 3000, f"DOM processing too slow: {timing['dom']}ms"
        assert timing['total'] < 10000, f"Total load time too slow: {timing['total']}ms"
        
    def test_first_contentful_paint(self, page: Page):
        """
        Test First Contentful Paint (FCP) metric
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Get FCP metric
        fcp = page.evaluate('''() => {
            const entries = performance.getEntriesByType('paint');
            const fcp = entries.find(entry => entry.name === 'first-contentful-paint');
            return fcp ? fcp.startTime : null;
        }''')
        
