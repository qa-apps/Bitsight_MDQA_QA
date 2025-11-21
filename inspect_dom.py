from playwright.sync_api import sync_playwright
import json

def inspect_bitsight_dom():
    """
    Inspect the actual DOM of BitSight website and extract real selectors
    """
    with sync_playwright() as p:
        # Launch browser in headed mode for debugging
        browser = p.chromium.launch(
            headless=False,  # Show browser for inspection
            slow_mo=500  # Slow down actions to see what's happening
        )
        
        page = browser.new_page()
        
        print("\n" + "="*80)
        print("INSPECTING BITSIGHT.COM DOM STRUCTURE")
        print("="*80)
        
        # Navigate to homepage
        page.goto('https://www.bitsight.com')
        page.wait_for_load_state('networkidle')
        
        # Extract actual navigation menu structure
        print("\n[1] NAVIGATION MENU STRUCTURE:")
        print("-" * 40)
        
        # Find actual nav elements
        nav_elements = page.evaluate('''() => {
            const navItems = [];
            
            // Try different possible nav selectors
            const selectors = [
                'nav a', 
                'header a',
                '[role="navigation"] a',
                '.nav-link',
                '.menu-item a'
            ];
            
            for (const selector of selectors) {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    if (el.textContent.trim()) {
                        navItems.push({
                            text: el.textContent.trim(),
                            href: el.href,
                            class: el.className,
                            id: el.id,
                            selector: selector
                        });
                    }
                });
            }
            
            return navItems.slice(0, 20);  // First 20 items
        }''')
        
        for item in nav_elements:
            print(f"  Text: {item['text'][:30]}")
            print(f"  Selector: {item['selector']}")
            print(f"  Class: {item['class']}")
            print()
            
        # Check for dropdown menus
        print("\n[2] DROPDOWN/MENU BUTTONS:")
        print("-" * 40)
        
        dropdown_info = page.evaluate('''() => {
            const dropdowns = [];
            
            // Common dropdown patterns
            const patterns = [
                'button[aria-expanded]',
                'button[aria-haspopup]',
                '[data-toggle="dropdown"]',
                '.dropdown-toggle',
                'button.menu-toggle'
            ];
            
            patterns.forEach(pattern => {
                document.querySelectorAll(pattern).forEach(el => {
                    dropdowns.push({
                        text: el.textContent.trim(),
                        selector: pattern,
                        classes: el.className,
                        ariaExpanded: el.getAttribute('aria-expanded'),
                        ariaHaspopup: el.getAttribute('aria-haspopup')
                    });
                });
            });
            
            return dropdowns;
        }''')
        
        for dropdown in dropdown_info:
            print(f"  Text: {dropdown['text']}")
            print(f"  Selector: {dropdown['selector']}")
            print()
            
        # Look for hero section
        print("\n[3] HERO SECTION ELEMENTS:")
        print("-" * 40)
        
        hero_info = page.evaluate('''() => {
            const hero = {};
            
            // Find main heading
            const h1 = document.querySelector('h1');
            if (h1) {
                hero.h1 = {
                    text: h1.textContent.trim(),
                    class: h1.className,
                    parent: h1.parentElement.className
                };
            }
            
            // Find CTA buttons
            const ctaButtons = [];
            ['Request', 'Demo', 'Learn', 'Get Started'].forEach(text => {
                const button = document.querySelector(`a:contains("${text}"), button:contains("${text}")`);
                if (button) {
                    ctaButtons.push({
                        text: button.textContent.trim(),
                        href: button.href,
                        class: button.className
                    });
                }
            });
            hero.buttons = ctaButtons;
            
            return hero;
        }''')
        
        print(f"  H1: {hero_info.get('h1', {}).get('text', 'Not found')}")
        
        # Check for forms
        print("\n[4] FORMS ON PAGE:")
        print("-" * 40)
        
        forms = page.locator('form').all()
        print(f"  Forms found: {len(forms)}")
        
        # Inspect with Playwright Inspector (debugging tool)
        print("\n[5] OPENING PLAYWRIGHT INSPECTOR...")
        print("-" * 40)
        print("Use the Inspector to:")
        print("  - Hover over elements to see selectors")
        print("  - Click 'Pick Locator' to select elements")  
        print("  - Copy the generated selectors")
        print("\nWaiting 60 seconds for inspection...")
        
        # Open Playwright Inspector
        page.pause()  # This opens the Playwright Inspector tool!
        
        browser.close()

if __name__ == "__main__":
    inspect_bitsight_dom()
