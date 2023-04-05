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
        
        if fcp:
            assert fcp < 3000, f"First Contentful Paint too slow: {fcp}ms"
            
    def test_largest_contentful_paint(self, page: Page):
        """
        Test Largest Contentful Paint (LCP) metric
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        page.wait_for_timeout(3000)  # Wait for LCP to stabilize
        
        # Get LCP metric
        lcp = page.evaluate('''() => {
            return new Promise((resolve) => {
                const observer = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    resolve(lastEntry.startTime);
                });
                observer.observe({ entryTypes: ['largest-contentful-paint'] });
                
                // Fallback if no LCP
                setTimeout(() => resolve(null), 1000);
            });
        }''')
        
        if lcp:
            assert lcp < 4000, f"Largest Contentful Paint too slow: {lcp}ms"
            
    def test_cumulative_layout_shift(self, page: Page):
        """
        Test Cumulative Layout Shift (CLS) metric
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        page.wait_for_timeout(3000)
        
        # Measure CLS
        cls = page.evaluate('''() => {
            let clsScore = 0;
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsScore += entry.value;
                    }
                }
            });
            observer.observe({ entryTypes: ['layout-shift'] });
            
            return new Promise(resolve => {
                setTimeout(() => {
                    observer.disconnect();
                    resolve(clsScore);
                }, 2000);
            });
        }''')
        
        # CLS should be less than 0.1 for good user experience
        if cls:
            assert cls < 0.25, f"Cumulative Layout Shift too high: {cls}"
            
    def test_time_to_interactive(self, page: Page):
        """
        Test Time to Interactive (TTI) metric
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Measure when page becomes interactive
        tti = page.evaluate('''() => {
            return new Promise((resolve) => {
                if (document.readyState === 'complete') {
                    resolve(performance.now());
                } else {
                    window.addEventListener('load', () => {
                        resolve(performance.now());
                    });
                }
            });
        }''')
        
        assert tti < 5000, f"Time to Interactive too long: {tti}ms"
        
    def test_resource_loading_performance(self, page: Page):
        """
        Test resource loading performance
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        page.wait_for_load_state('networkidle')
        
        # Get resource timing data
        resources = page.evaluate('''() => {
            const resources = performance.getEntriesByType('resource');
            return resources.map(r => ({
                name: r.name,
                type: r.initiatorType,
                duration: r.duration,
                size: r.transferSize || 0
            }));
        }''')
        
        # Analyze resource loading
        slow_resources = [r for r in resources if r['duration'] > 3000]
        assert len(slow_resources) == 0, f"Found {len(slow_resources)} slow resources (>3s)"
        
        # Check for large resources
        large_resources = [r for r in resources if r['size'] > 1000000]  # 1MB
        for resource in large_resources[:3]:
            print(f"Large resource: {resource['name'][-50:]} - {resource['size']/1024/1024:.2f}MB")
            
    def test_javascript_execution_time(self, page: Page):
        """
        Test JavaScript execution performance
        """
        homepage = HomePage(page)
        homepage.navigate_to()
        
        # Measure JS execution time
        js_perf = page.evaluate('''() => {
